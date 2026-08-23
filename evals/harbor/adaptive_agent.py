import asyncio
import importlib
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, override

from harbor.agents.base import BaseAgent
from harbor.agents.installed.claude_code import ClaudeCode
from harbor.agents.installed.codex import Codex
from harbor.models.agent.context import AgentContext

from evals.harbor.controller import drive_conversation
from evals.harbor.engineering_benchmark import authority_violation, tree_digest, tree_inventory
from evals.harbor.port_verifier import verify_extension, verify_initial


CONTROLLER_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["message", "complete", "stop"]},
        "category": {
            "type": ["string", "null"],
            "enum": ["material_answer", "progress", None],
        },
        "basis_ids": {"type": "array", "items": {"type": "string"}},
        "message": {"type": ["string", "null"]},
        "reason": {"type": ["string", "null"]},
    },
    "required": ["action", "category", "basis_ids", "message", "reason"],
    "additionalProperties": False,
}


def normalize_controller_decision(value: dict[str, Any]) -> dict[str, Any]:
    action = value.get("action")
    if action == "message":
        return {
            key: value[key]
            for key in ("action", "category", "basis_ids", "message")
            if value.get(key) is not None
        }
    if action in {"complete", "stop"}:
        return {
            "action": action,
            "basis_ids": [],
            **(
                {"reason": value["reason"]}
                if value.get("reason") is not None
                else ({"reason": "completed"} if action == "complete" else {})
            ),
        }
    return {key: item for key, item in value.items() if item is not None}


class AdaptiveAgent(BaseAgent):
    CONTROLLER_ENV_KEYS = (
        "PATH",
        "TMPDIR",
        "LANG",
        "LC_ALL",
        "TERM",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
    )

    def __init__(
        self,
        logs_dir: Path,
        model_name: str | None = None,
        *,
        subject_agent: str,
        controller_policy: str = "",
        controller_model: str = "haiku",
        controller_agent: str = "claude-code",
        controller_reasoning: str = "medium",
        scenario_policy_path: str | None = None,
        extension_prompt_path: str | None = None,
        verifier_contracts_path: str | None = None,
        verifier_oracle_path: str | None = None,
        verifier_reference_path: str | None = None,
        verifier_module: str = "evals.harbor.port_verifier",
        max_turns: int = 2,
        max_reported_tokens: int | None = None,
        max_repeated_questions: int = 3,
        controller_timeout_sec: float = 60.0,
        conversation_timeout_sec: float = 240.0,
        extra_env: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            logs_dir=logs_dir,
            model_name=model_name,
            extra_env=extra_env,
            **kwargs,
        )
        agents = {"claude-code": ClaudeCode, "codex": Codex}
        if subject_agent not in agents:
            raise ValueError(f"Unsupported adaptive subject: {subject_agent}")
        if max_turns < 1 or controller_timeout_sec <= 0 or conversation_timeout_sec <= 0:
            raise ValueError("controller limits must be positive")

        self._subject = agents[subject_agent](
            logs_dir=logs_dir,
            model_name=model_name,
            extra_env=extra_env,
            **kwargs,
        )
        self._subject_agent = subject_agent
        self._controller_policy = controller_policy
        self._controller_model = controller_model
        if controller_agent not in agents:
            raise ValueError(f"Unsupported controller agent: {controller_agent}")
        self._controller_agent = controller_agent
        self._controller_reasoning = controller_reasoning
        self._scenario_policy = (
            json.loads(Path(scenario_policy_path).read_text())
            if scenario_policy_path
            else None
        )
        self._extension_prompt = (
            Path(extension_prompt_path).read_text().strip()
            if extension_prompt_path
            else None
        )
        if (self._scenario_policy is None) != (self._extension_prompt is None):
            raise ValueError("scenario policy and extension prompt must be supplied together")
        if verifier_oracle_path and verifier_reference_path:
            raise ValueError("supply one verifier reference path")
        verifier_reference_path = verifier_reference_path or verifier_oracle_path
        if bool(verifier_contracts_path) != bool(verifier_reference_path):
            raise ValueError("verifier contracts and reference must be supplied together")
        if not re.fullmatch(r"evals\.harbor\.[a-z_]+_verifier", verifier_module):
            raise ValueError("verifier module must be a local Harbor verifier")
        self._verifier_contracts = Path(verifier_contracts_path) if verifier_contracts_path else None
        self._verifier_oracle = Path(verifier_reference_path) if verifier_reference_path else None
        self._verifier_module = verifier_module
        self._max_turns = max_turns
        self._max_reported_tokens = max_reported_tokens
        self._max_repeated_questions = max_repeated_questions
        self._controller_timeout_sec = controller_timeout_sec
        self._conversation_timeout_sec = conversation_timeout_sec
        self._setup_contamination: list[str] = []
        self._effective_configuration = {
            "subject_agent": subject_agent,
            "subject_model": model_name,
            "controller_agent": controller_agent,
            "controller_model": controller_model,
            "controller_reasoning": controller_reasoning,
            "max_turns": max_turns,
            "max_reported_tokens": max_reported_tokens,
            "max_repeated_questions": max_repeated_questions,
            "controller_timeout_sec": controller_timeout_sec,
            "conversation_timeout_sec": conversation_timeout_sec,
            "verifier_module": verifier_module,
            "controller_environment_keys": list(self.CONTROLLER_ENV_KEYS),
        }

    @staticmethod
    def name() -> str:
        return "devcraft-adaptive"

    def version(self) -> str | None:
        return self._subject.version()

    @override
    def to_agent_info(self):
        return self._subject.to_agent_info()

    @override
    async def setup(self, environment) -> None:
        self._subject.session_id = self.session_id
        self._subject.context_id = self.context_id
        await self._subject.setup(environment)
        if self._scenario_policy is not None:
            workspace_probe = await environment.exec(
                "find /app -maxdepth 2 -type f -o -type d",
                timeout_sec=30,
                user="node",
            )
            visible = workspace_probe.stdout or ""
            for name in ("/app/AGENTS.md", "/app/CLAUDE.md", "/app/.agents", "/app/.claude", "/app/openspec"):
                if name in visible:
                    self._setup_contamination.append(name)

    def _latest_response(self) -> str:
        trajectory = self._trajectory()
        for step in reversed(trajectory["steps"]):
            if step.get("source") == "agent" and isinstance(step.get("message"), str):
                return step["message"]
        raise RuntimeError("agent trajectory has no response")

    def _trajectory(self) -> dict[str, Any]:
        self._subject.populate_context_post_run(AgentContext())
        return json.loads((self.logs_dir / "trajectory.json").read_text())

    @staticmethod
    def _command_inputs(trajectory: dict[str, Any]) -> list[str]:
        inputs = []
        for step in trajectory.get("steps", []):
            for call in step.get("tool_calls") or []:
                value = (call.get("arguments") or {}).get("input")
                if isinstance(value, str) and "tools.exec_command(" in value:
                    inputs.append(value)
        return inputs

    async def _testing_agent(self, request: dict[str, Any]) -> Any:
        if self._controller_agent == "codex":
            return await self._codex_testing_agent(request)
        executable = shutil.which("claude")
        token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
        if executable is None or not token:
            raise RuntimeError("Claude testing-agent authentication is unavailable")

        schema = {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["message", "stop"]},
                "message": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["action"],
            "additionalProperties": False,
        }
        system_prompt = (
            "You control a behavioral test conversation. Inspect only the supplied "
            "policy and transcript. Return the next user message or a stop decision. "
            "You are not told the test arm or expected conclusion."
        )

        with tempfile.TemporaryDirectory(prefix="devcraft-controller-") as temp_dir:
            env = os.environ.copy()
            env.update(
                CLAUDE_CONFIG_DIR=temp_dir,
                CLAUDE_CODE_OAUTH_TOKEN=token,
                CLAUDE_FORCE_OAUTH="1",
            )
            env.pop("ANTHROPIC_API_KEY", None)
            env.pop("ANTHROPIC_AUTH_TOKEN", None)
            process = await asyncio.create_subprocess_exec(
                executable,
                "--safe-mode",
                "--tools",
                "",
                "--strict-mcp-config",
                "--mcp-config",
                '{"mcpServers":{}}',
                "--no-session-persistence",
                "--print",
                "--output-format",
                "json",
                "--json-schema",
                json.dumps(schema, separators=(",", ":")),
                "--model",
                self._controller_model,
                "--system-prompt",
                system_prompt,
                cwd=temp_dir,
                env=env,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(
                process.communicate(json.dumps(request).encode()),
                timeout=self._controller_timeout_sec,
            )
            if process.returncode != 0:
                raise RuntimeError("Claude testing agent failed")

        output = json.loads(stdout)
        decision = output.get("structured_output")
        if decision is None:
            raise RuntimeError("Claude testing agent returned no structured output")
        return decision

    async def _codex_testing_agent(self, request: dict[str, Any]) -> Any:
        executable = shutil.which("codex")
        auth_path = Path(
            os.environ.get(
                "CODEX_AUTH_JSON_PATH",
                Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json",
            )
        )
        if executable is None or not auth_path.is_file():
            raise RuntimeError("Codex testing-agent authentication is unavailable")
        system_prompt = (
            "You control a bounded engineering-test conversation. Use only the supplied "
            "policy, transcript, stage, and observation. Select an exact policy answer "
            "only for a direct covered question, request the exact progress message when "
            "needed, mark complete when the agent reports finished validated work, or stop "
            "with scenario_gap. Do not invent or volunteer requirements. Return JSON only."
        )
        with tempfile.TemporaryDirectory(prefix="devcraft-codex-controller-") as raw:
            temp = Path(raw)
            codex_home = temp / ".codex"
            codex_home.mkdir()
            shutil.copy2(auth_path, codex_home / "auth.json")
            schema_path = temp / "schema.json"
            output_path = temp / "decision.json"
            schema_path.write_text(json.dumps(CONTROLLER_SCHEMA))
            env = {
                key: os.environ[key]
                for key in self.CONTROLLER_ENV_KEYS
                if key in os.environ
            }
            env.update(CODEX_HOME=str(codex_home), HOME=str(temp), NO_COLOR="1")
            process = await asyncio.create_subprocess_exec(
                executable,
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--disable",
                "multi_agent",
                "--model",
                self._controller_model,
                "-c",
                f"model_reasoning_effort={self._controller_reasoning}",
                "-c",
                "web_search=disabled",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(output_path),
                "-",
                cwd=temp,
                env=env,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            payload = json.dumps({"system": system_prompt, "request": request}).encode()
            _, stderr = await asyncio.wait_for(
                process.communicate(payload), timeout=self._controller_timeout_sec
            )
            if process.returncode != 0 or not output_path.is_file():
                raise RuntimeError(
                    "Codex testing agent failed: "
                    + stderr.decode(errors="replace")[-500:]
                )
            return normalize_controller_decision(json.loads(output_path.read_text()))

    async def _observation(self, environment, stage: str) -> dict[str, Any]:
        state = await environment.exec(
            "git -C /app rev-parse --abbrev-ref HEAD 2>/dev/null; git -C /app rev-parse HEAD 2>/dev/null",
            timeout_sec=30,
            user="node",
        )
        state_lines = (state.stdout or "").splitlines()
        commits = await environment.exec(
            "git -C /app log -5 --format=%s 2>/dev/null",
            timeout_sec=30,
            user="node",
        )
        status = await environment.exec(
            "git -C /app status --porcelain=v1 2>/dev/null",
            timeout_sec=30,
            user="node",
        )
        trajectory = self._trajectory()
        latest = self._latest_response()
        final_metrics = trajectory.get("final_metrics") or {}
        tool_text = "\n".join(self._command_inputs(trajectory))
        unsafe = next(
            (
                violation
                for line in tool_text.splitlines()
                if (violation := authority_violation(line)) is not None
            ),
            None,
        )
        validations = [
            line.strip()
            for line in latest.splitlines()
            if re.search(r"\b(?:cargo|python3?)\s+(?:test|check|run)\b", line)
        ][:10]
        return {
            "stage": stage,
            "branch": state_lines[0] if state_lines else None,
            "head": state_lines[1] if len(state_lines) > 1 else None,
            "recent_commits": (commits.stdout or "").splitlines(),
            "changed_paths": [line[3:] for line in (status.stdout or "").splitlines() if len(line) > 3],
            "validation_claims": validations,
            "workflow_artifacts": [],
            "contamination": list(self._setup_contamination),
            "reported_output_tokens": final_metrics.get("total_completion_tokens"),
            "unsafe_authority": unsafe,
        }

    async def _checkpoint(
        self,
        environment,
        stage: str,
        transcript: list[dict[str, str]],
        controller_result: dict[str, Any],
        parent_digest: str | None = None,
    ) -> dict[str, Any]:
        destination = self.logs_dir / "snapshots" / stage
        destination.mkdir(parents=True)
        await environment.download_dir("/app", destination)
        observation = await self._observation(environment, stage)
        trajectory = self._trajectory()
        verifier = {"status": "not_configured"}
        if self._verifier_contracts and self._verifier_oracle:
            if self._verifier_module == "evals.harbor.port_verifier":
                initial_verifier, extension_verifier = verify_initial, verify_extension
            else:
                module = importlib.import_module(self._verifier_module)
                initial_verifier = module.verify_initial
                extension_verifier = module.verify_extension
            verifier = await asyncio.to_thread(
                initial_verifier if stage == "initial" else extension_verifier,
                destination,
                self._verifier_oracle,
                self._verifier_contracts,
            )
        record = {
            "stage": stage,
            "session_id": self._subject.session_id,
            "workspace_digest": tree_digest(destination),
            "inventory": tree_inventory(destination),
            "parent_workspace_digest": parent_digest,
            "transcript": list(transcript),
            "trajectory": trajectory,
            "git": {
                key: observation[key]
                for key in ("branch", "head", "recent_commits", "changed_paths")
            },
            "effective_configuration": self._effective_configuration,
            "controller": controller_result,
            "verifier": verifier,
        }
        (self.logs_dir / "snapshots" / f"{stage}.json").write_text(
            json.dumps(record, indent=2) + "\n"
        )
        return record

    async def _run_scenario(
        self,
        instruction: str,
        environment,
        context: AgentContext,
        started: float,
    ) -> dict[str, Any]:
        await asyncio.wait_for(
            self._subject.run(instruction, environment, context),
            timeout=self._conversation_timeout_sec,
        )
        transcript = [
            {"role": "user", "content": instruction},
            {"role": "agent", "content": self._latest_response()},
        ]

        async def send(message: str) -> str:
            await self._subject.resume(message, environment, context)
            return self._latest_response()

        async def run_stage(stage: str, transcript_start: int) -> dict[str, Any]:
            remaining = self._conversation_timeout_sec - (time.monotonic() - started)
            return await drive_conversation(
                policy=self._scenario_policy,
                transcript=transcript,
                decide=self._testing_agent,
                send=send,
                max_turns=self._max_turns,
                timeout_sec=max(remaining, 0.001),
                stage=stage,
                observe=lambda: self._observation(environment, stage),
                max_reported_tokens=self._max_reported_tokens,
                max_repeated_questions=self._max_repeated_questions,
                transcript_start=transcript_start,
            )

        initial = await run_stage("initial", 0)
        checkpoints = [await self._checkpoint(environment, "initial", transcript, initial)]
        stages = {"initial": initial}
        if initial["termination"] in {"completed", "turn_limit"}:
            extension_start = len(transcript)
            transcript.append({"role": "user", "content": self._extension_prompt})
            remaining = self._conversation_timeout_sec - (time.monotonic() - started)
            try:
                await asyncio.wait_for(
                    self._subject.resume(self._extension_prompt, environment, context),
                    timeout=max(remaining, 0.001),
                )
                transcript.append({"role": "agent", "content": self._latest_response()})
                extension = await run_stage("extension", extension_start)
            except TimeoutError:
                extension = {
                    "turns": 0,
                    "termination": "time_limit",
                    "reason": "extension agent timeout",
                    "tester_requests": [],
                    "decisions": [],
                    "observations": [],
                }
            stages["extension"] = extension
            checkpoints.append(
                await self._checkpoint(
                    environment,
                    "extension",
                    transcript,
                    extension,
                    checkpoints[0]["workspace_digest"],
                )
            )
        return {
            "session_id": self._subject.session_id,
            "turns": max(stage["turns"] for stage in stages.values()),
            "termination": list(stages.values())[-1]["termination"],
            "reason": list(stages.values())[-1]["reason"],
            "stages": stages,
            "checkpoints": checkpoints,
            "transcript": transcript,
        }

    @override
    async def run(self, instruction: str, environment, context: AgentContext) -> None:
        started = time.monotonic()
        record_path = self.logs_dir / "controller.json"
        try:
            if self._scenario_policy is not None:
                result = await self._run_scenario(
                    instruction, environment, context, started
                )
                record_path.write_text(json.dumps(result, indent=2) + "\n")
                return
            await asyncio.wait_for(
                self._subject.run(instruction, environment, context),
                timeout=self._conversation_timeout_sec,
            )
            transcript = [
                {"role": "user", "content": instruction},
                {"role": "agent", "content": self._latest_response()},
            ]

            async def send(message: str) -> str:
                await self._subject.resume(message, environment, context)
                return self._latest_response()

            remaining = self._conversation_timeout_sec - (time.monotonic() - started)
            result = await drive_conversation(
                policy=self._controller_policy,
                transcript=transcript,
                decide=self._testing_agent,
                send=send,
                max_turns=self._max_turns,
                timeout_sec=max(remaining, 0.001),
            )
        except TimeoutError:
            result = {
                "turns": 0,
                "termination": "timeout",
                "reason": "initial agent timeout",
                "tester_requests": [],
                "decisions": [],
            }
        except Exception as exc:
            result = {
                "turns": 0,
                "termination": "controller_error",
                "reason": type(exc).__name__,
                "tester_requests": [],
                "decisions": [],
            }

        record_path.write_text(json.dumps(result, indent=2) + "\n")

    @override
    def populate_context_post_run(self, context: AgentContext) -> None:
        self._subject.populate_context_post_run(context)
