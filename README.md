# Agentic Devcraft

Agentic Devcraft is building composable development-workflow skills for Claude
Code, Codex, and OpenCode. It also provides a reusable local evaluation framework for
testing whether agent configurations, workflows, toolkits, and skills improve
engineering outcomes rather than merely sounding useful.

## Current evidence

- A reusable Harbor harness runs isolated, subscription-authenticated Codex and
  Claude subjects with retained provenance and deterministic verification.
- A dual-host smoke matrix verifies setup, discovery, and use of Devcraft
  Status, Superpowers, GSD, Pocock Skills, OpenSpec, and Spec Kit.
- A 12-trial Codex baseline exercises a Python-to-Rust port and controlled
  extension across model, reasoning, and subagent-availability factors.

Start with the [results and findings index](evals/harbor/results/README.md) for a
short synopsis and links to the supporting evidence.

## Released

The shared Claude/Codex plugin packages `agent-instructions-cleanup`,
`documentation-pattern-refactor`, `capture-agent-issue`, and `status`. The two
refactoring skills preserve agent guidance and organize documentation by audience.
The same four skills load in OpenCode V2 as standalone, on-call skills from a local
checkout or the generated [HTTP catalog](USERS.md#opencode).
See [USERS.md](USERS.md) for marketplace installation, use, and Air integration.

## Under evaluation

Candidate skills live outside the published plugin under
[`proposals/skills/`](proposals/skills/). Their location is intentional: they
can be tested directly without becoming installable marketplace content.

## Methodology and evidence

- [Evaluation methodology and current learnings](docs/EVALUATION.md)
- [Developer setup and repository structure](DEVELOPERS.md)
- [Planned evaluation and skill work](TODO.md)
- [Human-readable results and findings](evals/harbor/results/README.md)

Harbor evaluations are part of the local development cycle, not GitHub Actions.
The only workflow publishes the OpenCode skill catalog for stable releases.
