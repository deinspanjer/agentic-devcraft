from pathlib import Path
from typing import Any

from harbor.agents.installed.base import CliFlag
from harbor.agents.installed.codex import Codex


class EvaluationCodex(Codex):
    CLI_FLAGS = [
        *Codex.CLI_FLAGS,
        CliFlag(
            "dangerously_bypass_hook_trust",
            cli="--dangerously-bypass-hook-trust",
            type="bool",
            default=False,
        ),
    ]

    def __init__(self, *args: Any, hooks_path: str | None = None, **kwargs: Any) -> None:
        self._evaluation_hooks = Path(hooks_path) if hooks_path else None
        if self._evaluation_hooks is not None and not self._evaluation_hooks.is_file():
            raise ValueError(f"hooks file does not exist: {self._evaluation_hooks}")
        super().__init__(*args, **kwargs)

    async def _upload_effective_config(self, environment, config, remote_path) -> None:
        await super()._upload_effective_config(environment, config, remote_path)
        if self._evaluation_hooks is not None:
            await self._upload_config_text(
                environment,
                content=self._evaluation_hooks.read_text(),
                remote_path=(self._REMOTE_CODEX_HOME / "hooks.json").as_posix(),
                filename="hooks.json",
            )
