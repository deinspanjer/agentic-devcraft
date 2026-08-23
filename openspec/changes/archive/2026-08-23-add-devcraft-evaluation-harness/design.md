## Context

The repository currently has no evaluation runner or behavioral corpus. The first useful milestone is not an A/B score: it is proof that Harbor can launch authenticated Claude Code and Codex agents, preserve a conversation, and install and invoke the exact subject under test. See [proposal.md](proposal.md) for motivation and [the capability spec](specs/devcraft-evaluation/spec.md) for the behavior contract.

The bootstrap suite deliberately exercises canonical installation. Most later behavioral trials evaluate instruction content rather than installation machinery, so those trials may use Harbor's direct skill injection or isolated host-native configuration after installation has been proven separately.

## Goals / Non-Goals

**Goals:**

- Establish a pinned Harbor scaffold that launches authenticated Claude Code and Codex agents from clean environments.
- Support one-shot prompts, scripted continued sessions, and adaptive testing-agent conversations.
- Install, configure, discover, invoke, and tear down each declared test subject.
- Prove the Devcraft status skill, Superpowers, GSD, Pocock, OpenSpec, and Spec Kit through a bootstrap compatibility matrix.
- Produce paired, inspectable behavioral trials after the bootstrap suite works.
- Isolate skill content from hook influence and from undeclared local configuration.
- Prefer deterministic verification and retain enough raw evidence to diagnose score differences.
- Reuse an existing evaluation framework when it supports the required agent setup and conversation lifecycle.

**Non-Goals:**

- Benchmark model vendors or choose a universally best model.
- Benchmark marketplace browsing or installation UX beyond the canonical commands needed by a declared smoke test.
- Build a general replacement for Harbor's task, isolation, result, or concurrency features.
- Generate evaluation cases with an LLM in the first implementation.
- Publish a benchmark service, dashboard, or hosted result store.
- Reduce correctness, false positives, adherence, and overhead to one score.

## Decisions

### 1. Bootstrap on Harbor

Install Harbor as a project-scoped development tool, then pin the version that passes the bootstrap suite. Use Harbor's installed Claude Code and Codex agents, disposable environments, tasks, trials, and result layout directly. The first acceptance path must prove:

- both CLIs launch in disposable environments using runtime authentication;
- undeclared user configuration is absent;
- a one-shot prompt returns machine-readable evidence;
- a fixed follow-up resumes the same logical session;
- an adaptive testing agent can choose a subsequent message through a narrow controller;
- a declared subject can be installed, discovered, and invoked; and
- results include termination, provenance, timing, final workspace state, and available usage data.

If Harbor lacks one required edge, add only that adapter. Do not create a parallel runner or duplicate Harbor's dataset, parallelism, or reporting features.

Alternatives considered:

- **Build a general-purpose harness immediately:** maximizes control but duplicates isolation, job, result, and agent integration work before the requirements are proven.
- **Gate the project on a Harbor-or-custom-runner decision:** adds a competing architecture before the requested Harbor path has been exercised.
- **Use only direct headless CLI calls:** simple, but cannot evaluate the accepted multi-turn behaviors.

### 2. Use each CLI's supported subscription-auth bridge

Authentication is a preflight concern, not a fixture concern, and the two CLIs use different bridges.

For Claude Code, generate a long-lived subscription token with `claude setup-token` and pass it to the Harbor agent only as `CLAUDE_CODE_OAUTH_TOKEN`. The local runner may resolve that variable from macOS Keychain; CI and other platforms supply it through their secret manager. Do not save the token in this repository or in a reusable test-subject definition. Clear competing Anthropic API-key variables for subscription-auth trials so credential precedence cannot silently change the tested path.

For Codex, set `CODEX_AUTH_JSON_PATH` to the user's host `auth.json` (normally `$CODEX_HOME/auth.json` or `~/.codex/auth.json`). Harbor's installed Codex agent natively uploads that file to `/tmp/codex-secrets/auth.json`, links it from its ephemeral `CODEX_HOME`, fixes container ownership, and removes both temporary locations after the run. Use that mechanism rather than adding a custom Docker mount or copy layer.

Credential contents must not appear in task definitions, command lines captured in results, normalized transcripts, workspace diffs, or logs. A sandboxed host-side `auth status` result is not evidence for or against container authentication. The in-container smoke request is authoritative for both paths.

Alternatives considered:

- **Mount the user's complete agent homes:** convenient but leaks unrelated instructions, plugins, hooks, session data, and credentials into the test.
- **Build a custom Codex auth mount:** duplicates Harbor's native upload, ownership, linking, and cleanup behavior.
- **Treat a sandboxed host CLI status as authoritative:** tests a different filesystem and process boundary from the Harbor agent under test.

### 3. Treat the testing agent as a controller, not the subject

A conversational trial has two distinct roles:

- The **agent under test** receives the task, Devcraft configuration, repository tools, and persistent workspace.
- The **testing agent** receives the scenario policy, the prior transcript, and any hidden test facts needed to choose the next message. It does not receive the arm label or expected conclusion.

After each completed agent-under-test turn, the controller asks the testing agent for structured output containing either the next user message or a stop decision with a reason. The controller then resumes the same agent-under-test session. A deterministic scripted controller is used instead when the next turn does not require model judgment.

This keeps adaptive conversation available without making every multi-turn test expensive or nondeterministic.

Alternatives considered:

- **Let the verifier impersonate the user after the trial:** cannot influence the conversation being evaluated.
- **Give the testing agent full treatment metadata:** makes it easier for the tester to cue the expected behavior and contaminates the comparison.
- **Require an LLM testing agent for every case:** adds cost and variance where a fixed sequence is sufficient.

### 4. Separate canonical installation smoke tests from content injection

Each trial constructs an isolated agent home and project workspace. Bootstrap smoke tests run the subject's declared canonical installation or provisioning action, then verify host discovery and perform a minimal representative invocation. Setup records the canonical source, resolved revision, content digest, host, and installation method.

Later content-focused trials copy only declared skills into the selected host's native location and install only declared hooks. The control arm uses the same setup path with empty Devcraft configuration. External workflow fixtures are provisioned independently so Peters Toolkit, OpenSpec, or another workflow is a declared test factor rather than ambient machine state.

Unreleased Devcraft candidates live under `proposals/skills/`, outside the shared marketplace payload. Comparison arms reference that one source directly for both hosts. Promotion moves the source into `plugins/agentic-devcraft/skills/`; it never creates parallel Claude and Codex copies.

Canonical installation may use a marketplace when that is the subject's supported procedure, but marketplace browsing and user-interface behavior are not evaluated. This keeps installation evidence separate from behavioral scores.

Alternatives considered:

- **Install the marketplace for every behavioral treatment:** exercises more production machinery but makes content trials slower and failures harder to attribute.
- **Reuse the developer's normal agent home:** simpler authentication, but leaks unrelated skills, hooks, instructions, and plugins into both arms.

### 5. Keep test-subject declarations small

Use one declarative record per subject containing only its identifier, canonical source and pinned reference, supported hosts, install or provision command, required configuration, discovery check, and use probe. A smoke result has separate setup, discovery, and use stages. An unsupported host combination is evidence, not a pass or a silent skip.

The initial records cover `devcraft-status`, `superpowers`, `gsd`, `pocock`, `openspec`, and `spec-kit`. Resolve and cite the canonical source and supported host matrix during implementation; do not encode an inferred installer as fact.

Alternatives considered:

- **Create a plugin system for installers:** unnecessary for six bounded subjects; a small record plus the command Harbor already runs is enough.
- **Use one generic file-exists assertion:** cannot establish that an agent discovers or can use the installed behavior.

### 6. Hand-author a small behavioral corpus

The first corpus contains bounded cases with known facts and admissible outcomes:

1. Review integrity: one clean fixture and one matched fixture with seeded defects.
2. Cold factual verification: a draft decision with load-bearing claims, including a false claim and a dependent sibling case.
3. Decision evolution: a multi-turn case in which later evidence invalidates an earlier basis.
4. Workflow ownership: an explicit OpenSpec choice in a repository where another Devcraft route is available.
5. Peters coexistence: equivalent Peters-only, Devcraft-only, and combined configurations.

Cases share fixtures only when the shared state is itself part of the comparison. Expected outcomes are written by humans and kept outside the agent-under-test workspace when possible.

Alternatives considered:

- **Generate probes automatically from each skill:** useful at scale, but generated expectations would be difficult to trust during bootstrap.
- **Start with broad software benchmarks:** measures general coding ability more than the specific behavioral contracts Devcraft introduces.

### 7. Separate trial evidence from comparison summaries

Every trial retains:

- resolved configuration and version provenance;
- raw machine-readable events and normalized transcript;
- termination reason;
- final workspace diff or state;
- deterministic verifier details;
- optional blinded judge details;
- elapsed time, turns, tool calls, and reported token usage.

Comparison summaries calculate per-measure arm deltas and keep repetitions visible. Raw run output is ignored by Git by default; compact fixture definitions, verifier code, and deliberately accepted summaries may be committed.

No single aggregate score is introduced. A skill that improves recall while increasing fabricated findings must expose both effects.

### 8. Fail closed on setup and authority

A setup mismatch is not a zero score; it is an invalid trial. Credentials enter only through runtime environment configuration and are redacted from persisted events. Installation trials receive network access only to declared model endpoints and canonical source hosts. Trial workspaces receive no authority to mutate other external systems unless a case explicitly requires it.

### 9. Keep Harbor evaluations in the local development cycle

Harbor evaluations run as developer-invoked local commands, not as GitHub Actions. Network-isolated runs use any local Docker backend that passes Harbor's nftables capability probe, with a compatible Linux Docker host as fallback. CI remains appropriate for deterministic compiled-code or script tests and for release automation, but it does not own authenticated Harbor evaluation runs.

## Risks / Trade-offs

- **Harbor's multi-step resume may cover scripted turns but not an adaptive tester** → Add only a narrow controller or custom Harbor agent that selects the next message and resumes the existing session.
- **The Claude setup token may expire or be shadowed by an API-key variable** → Preflight the token inside Harbor, clear competing credentials for the subscription trial, and report regeneration as a blocked prerequisite without logging the token.
- **Codex may rewrite or refresh its in-container `auth.json`** → Harbor isolates that copy in its temporary secrets directory and removes it without propagating changes to the host file.
- **Installers may execute changing remote scripts or mutate external state** → Resolve canonical sources, pin revisions where possible, isolate each run, allowlist required hosts, and retain source provenance.
- **A toolkit may not support both agents** → Record a sourced unsupported matrix entry; do not rewrite the toolkit, pretend success, or silently skip it.
- **Host-native skill discovery can change between CLI versions** → Pin and record host versions, verify setup before scoring, and keep host setup separate from behavioral fixtures.
- **A testing agent can steer toward the expected answer** → Blind it to arm identity and expected conclusions; prefer scripted turns when possible.
- **Model nondeterminism can dominate small differences** → Run paired repetitions in mixed order and report individual outcomes alongside deltas.
- **LLM judging can reproduce the same biases being tested** → Use deterministic checks for known facts and seeded defects; reserve blinded judging for irreducibly qualitative criteria.
- **Raw trajectories may contain secrets or large volumes of data** → Redact before persistence, keep raw results untracked, and retain only evidence required to diagnose the trial.
- **Peters Toolkit fixtures can accidentally become redistribution of the toolkit** → Reference or provision the locally available source for evaluation and commit only minimal test-owned context unless licensing review permits more.

## Migration Plan

1. Add project-scoped Harbor configuration and verify the local Docker prerequisite.
2. Inject a Claude setup token and supply the Codex `auth.json` through Harbor's native environment switch, then prove one authenticated in-container one-shot run for each CLI.
3. Prove scripted resume and one adaptive testing-agent conversation, adding only the missing controller edge if Harbor does not provide it directly.
4. Add the six test-subject declarations and run their install, discovery, and use smoke matrix on both hosts, recording unsupported combinations explicitly.
5. Pin the proven Harbor and subject revisions, then add one paired review-integrity comparison using direct content injection.
6. Add the remaining behavioral cases and document the repeatable local commands.

Rollback consists of removing the evaluation-only Harbor files and pinned development dependency; published marketplaces and skills are unaffected.
