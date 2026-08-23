# Using Agentic Devcraft

Only skills under `plugins/agentic-devcraft/skills/` are released. Candidate
skills under `proposals/` are not installed by either marketplace.

## Codex

```bash
codex plugin marketplace add deinspanjer/agentic-devcraft
codex plugin add agentic-devcraft@agentic-devcraft
```

Run `$agentic-devcraft:status` to verify the installation.

## Claude Code

```bash
claude plugin marketplace add deinspanjer/agentic-devcraft
claude plugin install agentic-devcraft@agentic-devcraft --scope user
```

Run `/agentic-devcraft:status` to verify the installation.
