import json
import os
import shlex
from pathlib import Path
from typing import Any, override

from harbor.agents.base import BaseAgent
from harbor.agents.installed.claude_code import ClaudeCode
from harbor.agents.installed.codex import Codex
from harbor.models.agent.context import AgentContext

from evals.harbor.validate_subjects import load_subject


class SubjectLifecycleAgent(BaseAgent):
    def __init__(
        self,
        logs_dir: Path,
        model_name: str | None = None,
        *,
        subject_agent: str,
        subject_path: str,
        extra_env: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            logs_dir=logs_dir,
            model_name=model_name,
            extra_env=extra_env,
            **kwargs,
        )
        self._declaration = load_subject(Path(subject_path))
        agents = {"claude-code": ClaudeCode, "codex": Codex}
        if subject_agent not in agents:
            raise ValueError(f"Unsupported subject host: {subject_agent}")
        subject_env = dict(extra_env or {})
        subject_env.update(self._declaration["configuration"].get(subject_agent, {}))

        self._subject = agents[subject_agent](
            logs_dir=logs_dir,
            model_name=model_name,
            extra_env=subject_env,
            **kwargs,
        )
        self._host = subject_agent
        self._unsupported = self._declaration["unsupported"].get(subject_agent)

    @staticmethod
    def name() -> str:
        return "devcraft-subject-lifecycle"

    def version(self) -> str | None:
        return self._subject.version()

    @override
    def to_agent_info(self):
        return self._subject.to_agent_info()

    @override
    async def setup(self, environment) -> None:
        if self._unsupported:
            return
        self._subject.session_id = self.session_id
        self._subject.context_id = self.context_id
        await self._subject.setup(environment)

    def _agent_env(self) -> dict[str, str]:
        env = dict(self._declaration["configuration"].get(self._host, {}))
        if self._host == "codex":
            env["CODEX_HOME"] = "/tmp/codex-home"
            return env
        env["CLAUDE_CONFIG_DIR"] = "/logs/agent/sessions"
        token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
        if token:
            env.update(CLAUDE_CODE_OAUTH_TOKEN=token, CLAUDE_FORCE_OAUTH="1")
        return env

    async def _exec(self, environment, argv: list[str]):
        command = (
            'export PATH="$HOME/.local/bin:$PATH"; '
            'if [ -s ~/.nvm/nvm.sh ]; then . ~/.nvm/nvm.sh; fi; '
            + shlex.join(argv)
        )
        return await self._subject.exec_as_agent(
            environment, command, env=self._agent_env(), timeout_sec=180
        )

    def _latest_response(self) -> str:
        self._subject.populate_context_post_run(AgentContext())
        trajectory = json.loads((self.logs_dir / "trajectory.json").read_text())
        for step in reversed(trajectory["steps"]):
            if step.get("source") == "agent" and isinstance(step.get("message"), str):
                return step["message"]
        raise RuntimeError("agent trajectory has no response")

    @override
    async def run(self, instruction: str, environment, context: AgentContext) -> None:
        del instruction
        checkout = "/tmp/devcraft-subject"
        state_canary = "/tmp/agentic-devcraft-subject-state"
        source = self._declaration["source"]
        report: dict[str, Any] = {
            "subject": self._declaration["id"],
            "host": self._host,
            "outcome": "pending",
            "isolation": {"status": "pending"},
            "stages": {
                "setup": {"status": "pending"},
                "discovery": {"status": "pending"},
                "use": {"status": "pending"},
            },
        }

        if self._unsupported:
            report.update(outcome="unsupported", evidence=self._unsupported)
            report["isolation"] = {"status": "not_run"}
            for stage in report["stages"].values():
                stage["status"] = "not_run"
            context.metadata = {"subject_lifecycle": report}
            (self.logs_dir / "subject-lifecycle.json").write_text(
                json.dumps(report, indent=2) + "\n"
            )
            return

        try:
            canary = await self._exec(environment, ["test", "!", "-e", state_canary])
            if canary.return_code != 0:
                raise RuntimeError("subject state leaked from an earlier trial")
            report["isolation"] = {"status": "passed"}

            setup_commands = [
                [
                    "mkdir",
                    "-p",
                    "/tmp/codex-home" if self._host == "codex" else "/logs/agent/sessions",
                ],
                ["git", "clone", "--quiet", "--no-checkout", source["repository"], checkout],
                ["git", "-C", checkout, "checkout", "--quiet", source["revision"]],
            ]
            for command in setup_commands:
                result = await self._exec(environment, command)
                if result.return_code != 0:
                    raise RuntimeError("source checkout failed")

            revision_result = await self._exec(
                environment, ["git", "-C", checkout, "rev-parse", "HEAD"]
            )
            digest_result = await self._exec(
                environment, ["git", "-C", checkout, "rev-parse", "HEAD^{tree}"]
            )
            revision = (revision_result.stdout or "").strip()
            digest = (digest_result.stdout or "").strip()
            if revision != source["revision"] or not digest:
                raise RuntimeError("source provenance mismatch")

            for command in self._declaration["install"][self._host]:
                resolved = [part.replace("{checkout}", checkout) for part in command]
                result = await self._exec(environment, resolved)
                if result.return_code != 0:
                    detail = ((result.stderr or result.stdout or "").strip())[-1000:]
                    raise RuntimeError(
                        f"subject installation failed ({shlex.join(resolved)}): {detail}"
                    )

            report["stages"]["setup"] = {
                "status": "passed",
                "repository": source["repository"],
                "revision": revision,
                "digest": {"algorithm": "git-tree-sha1", "value": digest},
            }

            discovery = self._declaration["discovery"][self._host]
            result = await self._exec(environment, discovery["command"])
            output = (result.stdout or "") + (result.stderr or "")
            if result.return_code != 0 or discovery["expect"] not in output:
                raise RuntimeError("subject discovery failed")
            report["stages"]["discovery"] = {"status": "passed"}

            probe = self._declaration["use_probe"][self._host]
            await self._subject.run(probe["prompt"], environment, context)
            response = self._latest_response()
            self._subject.populate_context_post_run(context)
            if probe["expect"].casefold() not in response.casefold():
                raise RuntimeError("subject use probe failed")
            for path in probe.get("expect_paths", []):
                result = await self._exec(environment, ["test", "-e", path])
                if result.return_code != 0:
                    raise RuntimeError(f"subject use probe did not create {path}")
            report["stages"]["use"] = {"status": "passed"}
            await self._exec(environment, ["touch", state_canary])
            report["outcome"] = "passed"
        except Exception as exc:
            report["outcome"] = "failed"
            if report["isolation"]["status"] == "pending":
                report["isolation"] = {"status": "failed", "reason": str(exc)}
            failed = False
            for stage in report["stages"].values():
                if stage["status"] == "pending":
                    if not failed:
                        stage.update(status="failed", reason=str(exc))
                        failed = True
                    else:
                        stage.update(status="not_run")
        finally:
            context.metadata = {"subject_lifecycle": report}
            (self.logs_dir / "subject-lifecycle.json").write_text(
                json.dumps(report, indent=2) + "\n"
            )

    @override
    def populate_context_post_run(self, context: AgentContext) -> None:
        if self._unsupported:
            return
        self._subject.populate_context_post_run(context)
