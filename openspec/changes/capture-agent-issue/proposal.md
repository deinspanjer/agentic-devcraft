# Proposal

## Why

Agent failures currently arrive as informal anecdotes that are difficult to compare or turn into skill experiments. A small, explicitly invoked capture skill can produce consistent evidence packets while keeping investigation work out of the active session's context.

## What Changes

- Introduce `capture-agent-issue` for Claude Code and Codex, with one portable instruction source and host-specific explicit-only invocation controls.
- Keep the entrypoint minimal: capture directly in a confirmed tool-capable side/fork session; delegate once from an ordinary session. If identity or capability cannot be established, ask one focused question or report the limitation without recursive isolation attempts.
- The collector reads actual subject-session/rollout records, investigates relevant project material, and saves the packet. Keep original-subject identity and cutoff distinct from collector identity and inherited fork records.
- Capture the user's account, acting-agent self-assessment when supplied, separately attributed evidence-supported findings, execution constraints, and runtime/session metrics with provenance. Record inherited reviewer context without claiming formal blinding.
- Produce Markdown packets suitable for Agentic Devcraft refinement and experiment design, following the user's payload-privacy preference (de-identified by default); retain requested details where enforced policy permits.
- Save by default under the host's temporary directory, preserving recognizable project and session names and a capture-start date/hour/minute in UTC in the path. Apply only filesystem-required name handling. Do not create default capture artifacts in a worktree.
- Include expected versus actual behavior, relevant effective instructions/configuration, a decision/correction timeline, and evaluation-ready reproduction and success criteria when evidence supports them.
- Package the skill in the shared `agentic-devcraft` plugin and install it through each harness's native marketplace workflow, replacing the former standalone links. Remote GitHub publication and underlying-task remediation remain outside this request.

## Capabilities

### New Capabilities

- `agent-issue-capture`: Explicit, context-preserving collection of agent issue evidence and metrics into local experiment packets with user-selected payload privacy.

### Modified Capabilities

None. This captures inputs for subsequent evaluations; it does not change the existing evaluation runner or its contracts.

## Impact

- Shared source: `plugins/agentic-devcraft/skills/capture-agent-issue/`, including launcher, worker guidance, packet template, and invocation metadata. The earlier candidate source was reconciled and removed after verified marketplace installation.
- Native local-marketplace registrations and plugin installations for Claude Code and Codex, with instructions in `USERS.md`. Default packets live outside worktrees in private temporary directories; reconcile the earlier checkout-based output guidance and obsolete ignore rule during implementation.
- Small harness-specific retrieval/metric guidance; add a helper only if demonstrated necessary for dependable extraction. No new service, telemetry daemon, remote issue integration, or evaluation-runner integration.
- Other agents can follow the shared workflow; native discovery and invocation enforcement outside the two supported harnesses are not guaranteed.
