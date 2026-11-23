---
name: capture-agent-issue
description: Capture a local agent issue packet for skill tuning and experiments. Only run when the user explicitly invokes capture-agent-issue.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Capture Agent Issue

Freeze capture-start UTC; preserve it through clarification.

In OpenCode, read the Launcher section of
[references/harness/opencode.md](references/harness/opencode.md) before choosing
direct capture or delegation.

In a natively confirmed tool-capable side/fork session, read [worker.md](worker.md)
and capture directly, honoring mode restrictions. Separate original subject
identity/cutoff from collector identity.

In an ordinary session, delegate **once**, without inherited history. Pass the
invocation unchanged, available subject/runtime locator, project directory,
capture-start, pre-capture event/turn boundary, and this skill's absolute
`worker.md` path. The worker reads evidence directly and saves the packet.
Do not read detailed guidance or gather excerpts in the ordinary parent.

Unknown mode/identity/capability: ask one focused question or report the specific
limitation. Never recursively fork/delegate or silently collect in an ordinary
parent. User claims alone do not confirm isolation.

Relay only compact completion, clarification, approval, or failure results.
Normal host approval applies to writes; no publishing or underlying-task changes.
