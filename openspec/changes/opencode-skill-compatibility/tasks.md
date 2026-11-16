# Tasks

## 1. OpenCode native capability gate

- [x] 1.1 Inspect the selected V2 executable and actual session/message/log/fork schemas in an isolated HOME/XDG/config/data environment; retain a non-sensitive evidence note with binary path, version, schema fields, and connection context. Verify no normal harness configuration, cache, or unrelated live session was accessed or modified.
- [x] 1.2 Demonstrate trusted current collector identity, original subject lookup, pre-invocation cutoff, suitable-fork boundary, and one-hop fresh-worker routing with disposable native sessions; record compact handoff/results and parent-versus-worker context behavior. Stop and return for a revised decision if safe routing cannot be demonstrated; a blanket unsupported-host notice does not complete this task.
- [x] 1.3 Demonstrate cutoff-safe original record retrieval across pages and a tool completing after the frozen boundary, including a finite durable-log read and sequence/message-boundary linkage; retain synthetic evidence proving the late outcome is excluded. If current projected messages cannot reconstruct the cutoff, verify the bounded-event route or leave this gate incomplete.

## 2. Shared runtime portability and status

- [x] 2.1 Add OpenCode-only on-call metadata to all four canonical skills, audit relative resources and host-specific metadata, and declare verified interpreter/capability requirements; inspect complete copied standalone directories and verify no implicit change to Claude/Codex invocation policy.
- [x] 2.2 Use the local `release.json` contract defined in the catalog change's design and make status use applicable loaded-installation evidence, unknown-version fallback, conflict reporting, and activation distinct from availability. Verify standalone-with-provenance, missing-provenance, conflicting-record, and actual package-layout cases without network or mutation; use focused tests only for nontrivial reader/selection code introduced.
- [x] 2.3 Establish the `references/harness/<harness>.md` layout: split capture's `references/harness-records.md` into `codex.md` and `claude.md` with profile text unchanged, update the worker's selection step and every reference to the old path, and record the convention in `DEVELOPERS.md`. Verify the moved text is identical, no file combines several harnesses' profiles, and the existing capture helper tests still pass.
- [x] 2.4 Update `USERS.md` for OpenCode IDs, `@` versus OpenChamber `$` selection, status semantics, on-call behavior, and prerequisites, and `DEVELOPERS.md` for the canonical-source and provenance handoff contract; verify examples against isolated native discovery/loading and inspect that no global installation is suggested as already performed.

## 3. Instruction cleanup portability

- [x] 3.1 Revise every file-selection, override, XOR, ignore, counter, and output rule in `agent-instructions-cleanup/SKILL.md` to depend on the target harnesses, moving each harness's file-selection and precedence rules into its own `references/harness/` file and leaving the main skill harness-neutral; verify OpenCode-only, Codex-only, mixed-target, and unknown-target examples produce accurate semantics without silently deleting ignored files.
- [x] 3.2 Exercise synthetic instruction trees containing both file types and conflicting guidance; inspect the verbatim preservation map, destinations, dated mirror, report/index, and clarification/in-place approval gates. Verify original fixture files remain unchanged before approval; retain compact acceptance evidence rather than prose-string tests.
- [x] 3.3 Document target-harness selection and preservation behavior in `USERS.md`, preserving existing Claude/Codex invocation guidance; review the documented mixed-host case against the accepted synthetic example.

## 4. Documentation refactoring portability

- [x] 4.1 Change audit output defaults to `<root>/.agents/artifacts/doc-pattern` and omitted planner output to the divergence input's directory; update both helpers and all examples. Exercise audit/plan from outside the target workspace and explicit legacy/custom destinations, verifying one coherent artifact location and unchanged target inputs.
- [x] 4.2 Remove nesting-alone `AGENTS.md` violations from the helper and bundled baseline, update generated cleanup advice and references for OpenCode, and preserve no-auto-edit instruction policy. Verify a scoped nested instruction file is not a violation while existing audience/classification findings still operate; add a narrow behavioral regression only if existing coverage does not protect this decision.
- [x] 4.3 Exercise audit, scaffolding, and restructuring plan generation on a small fixture; inspect classification, hidden-directory exclusion, level artifacts, root/all scope, redundancy traceability, and developer-rule propagation/approval requirements. Update `USERS.md`/`DEVELOPERS.md` with new defaults and preserved explicit paths, and verify documented commands against the fixture.

## 5. Native OpenCode capture integration

- [x] 5.1 Add the verified OpenCode launcher route and worker retrieval instructions as `references/harness/opencode.md`, using the capability evidence from group 1; verify direct suitable-fork capture, ordinary one-hop capture, named-other-subject selection, missing identity, forbidden delegation, and no recursive or bulk-parent investigation.
- [x] 5.2 Add only the narrow native-record normalization/metric code demonstrated necessary by group 1; verify stable-ID deduplication, pagination boundaries, mutable tool state at cutoff, subject/collector separation, human/peer/generated/unknown attribution, and auxiliary-versus-request usage with focused synthetic behavioral checks. Reject unresolved boundaries or partial-page failures rather than silently measuring full/empty sessions.
- [x] 5.3 Integrate normalized subject metrics and evidence into the existing packet workflow and retain existing exclusive private-save behavior; verify unavailable physical transcript size/other absent fields are explicit, export bytes are not relabeled, capture-start survives clarification, and privacy/approval results remain compact. Reuse existing save tests and inspect synthetic default/full-detail packets without exposing private reasoning.
- [x] 5.4 Update the capture profile, worker/template only where needed, `USERS.md`, and `DEVELOPERS.md` with verified OpenCode invocation, records, capability limits, metric semantics, and recovery behavior; verify every documented field/route against the recorded runtime and preserve the existing user-confirmed Claude/Codex acceptance without reopening its removed integration matrix.

## 6. Cross-host standalone integration acceptance

- [x] 6.1 Run native explicit-loading and actual workflow smoke checks for all four complete standalone skill directories in the isolated V2 runtime from an unrelated workspace, including full ordinary/fork capture and compact parent results; retain source revision, binary/version/client, provenance, findings, and gaps in a scrubbed evidence artifact. Verify no dependency on another client's home/cache or original plugin checkout.
- [x] 6.2 Validate both existing marketplace manifests and isolated Claude/Codex payload layouts, run the scoped helper checks and repository-mandated checks in `DEVELOPERS.md`, and inspect the final diff for unrelated changes. Report real execution versus packaging-only coverage and confirm no user's global installation was changed.
- [x] 6.3 Run `openspec validate opencode-skill-compatibility --strict`, review all compatibility claims against retained evidence, and update `README.md` links/capability summary only for verified support. Confirm catalog publication remains separate and no unfinished native capability gate is represented as complete.

## Workflow follow-up

- Review and apply this change only after explicit user authorization; planning does not install or implement anything.
- Coordinate the future HTTP catalog's generated release record and complete file inventory with this reader contract before publishing.
- At archive time, check whether the active `capture-agent-issue` change has archived and preserve distinct ownership of the generic capture contract and OpenCode-specific integration.
