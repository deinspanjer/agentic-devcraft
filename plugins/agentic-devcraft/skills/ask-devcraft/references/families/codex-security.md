# openai/plugins family: codex-security (Codex Security)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `codex-security` family. The catalog entry is in openai-engineering.md.

## Family: codex-security
- source path: `plugins/codex-security`
- manifest notes: v0.1.32, OpenAI, proprietary licence, Codex-format manifest only. Marketplace policy: products CODEX only, authentication ON_USE. Bundled MCP server `codex-security` (Node with native binaries; tools such as `start_codex_security_standard_scan`, `complete_codex_security_scan`) that inherits model credentials from the environment (`OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `FIREWORKS_API_KEY`, AWS chain for Bedrock). App connectors: `github`, `linear`, `atlassian` (read and write), used by triage-finding and track-findings. No OAuth section declared. Skills assume Codex; other hosts fall back to a terminal workflow with Python helpers.
- router: none. Three entry skills start scans: `security-scan` (whole repo, one pass, self-contained, does not call phase skills), `deep-security-scan` (one coordinator call, then one completion call), `security-diff-scan` (diff; runs preflight, then `threat-model` -> `finding-discovery` -> `validation` -> `attack-path-analysis`, then one completion call on the durable path; terminal scans use a finalizer). The four phase skills support their scan phase or explicit standalone requests, but are not primary triggers for full scans. After a scan, on request: `vulnerability-writeup`, `propose-security-hardening`, `track-findings`, `triage-finding`, `fix-finding`, `verify-fix`.
- development distance: core-dev
- disclosure: rich. No router, and the skills cover different scenarios (whole-repo scan, diff scan, triage of imported findings, fix, verify, tracker filing, disclosure writeups, hardening, SECURITY.md policy, merge risk).

### security-scan
- id: codex-security:security-scan (source path: plugins/codex-security/skills/security-scan/SKILL.md)
- description: "Use for a standard, single-pass security audit of an entire repository or a scoped path, package, folder, or submodule with no diff to review. This is the default repository scan. Do not use for PR, commit, branch, or working-tree diffs, or for deep, multi-pass scans."
- use when: Audit a whole repository, folder, package or submodule for security issues in one standard pass, with no diff.
- not for: `deep-security-scan` (exhaustive, multi-pass, variance-reducing); `security-diff-scan` (a PR, commit, branch or working-tree diff).
- needs: The `codex-security` MCP (host-backed scans) or Python for headless prompt-only scans; model credentials from the environment. The preflight must return `ready` before any source review.
- side effects: Writes scan artifacts (`scan-manifest.json`, `findings.json`, `coverage.json`, generated `report.md`) under a platform temp or scan directory; does not modify the repo. An SDK-owned run stops with unsealed JSON.
- part of: entry point (the family has no router); runs the threat model, discovery, validation and attack paths inline and does not call the phase skills. Optional follow-ups on request: `vulnerability-writeup`, `propose-security-hardening`.

### deep-security-scan
- id: codex-security:deep-security-scan (source path: plugins/codex-security/skills/deep-security-scan/SKILL.md)
- description: "Use when the user asks for a deep, exhaustive, multi-pass, or variance-reducing repository-wide or scoped-path Codex Security scan. Run repeated complete independent Standard scans with the Codex Security deep-scan tool, which aggregates their validated findings and prepares the canonical artifacts; then complete the same scan once. Do not use for PRs, commits, branch diffs, or working-tree diffs."
- use when: Run a deep, exhaustive, multi-pass or variance-reducing security scan of a repository or path.
- not for: `security-scan` (one pass); `security-diff-scan` (never for PRs or diffs).
- needs: The MCP tool `start_codex_security_deep_scan`; if absent it stops. Heavy tokens, CPU and memory; coordinator duration defaults to and is capped at 96 hours. Interactive session for the concurrent-scan prompt.
- side effects: Writes the same scan artifacts as `security-scan`; asks Cancel (Recommended) / Continue if another deep scan is running; does not modify the repo.
- part of: entry point; one coordinator call, then one `complete_codex_security_scan`; no phase skills.

### security-diff-scan
- id: codex-security:security-diff-scan (source path: plugins/codex-security/skills/security-diff-scan/SKILL.md)
- description: "Review a pull request, commit, branch diff, or working-tree patch for security vulnerabilities."
- use when: Security-review a pull request, commit, branch diff or my working-tree patch.
- not for: `assess-patch-risk` (regression and merge risk, not vulnerabilities); `security-scan` (no diff).
- needs: A Git range or local patch; the `codex-security` MCP for the durable path (other hosts use the terminal workflow with Python helpers); the `security_diff_scan` preflight; a prompt-only scan starts in the desktop app only.
- side effects: Writes scan artifacts (`report.md`, SARIF, Codex review comments for confirmed findings); validation builds and runs PoCs in a disposable copy; does not modify the repo.
- part of: entry point and orchestrator of `threat-model` -> `finding-discovery` -> `validation` -> `attack-path-analysis`; finishes only when every changed file and candidate is accounted for.

### threat-model
- id: codex-security:threat-model (source path: plugins/codex-security/skills/threat-model/SKILL.md)
- description: "Use when Codex is already in the threat-modeling phase of a security scan, the user explicitly invokes $threat-model, or the user explicitly asks to create, update, or persist a repository threat model. Do not use as the primary trigger for full PR, commit, branch, patch, or repository scans."
- use when: Create, update or save a threat model for this repository, or build the threat-model step of a scan.
- not for: `define-security-policy` (writes SECURITY.md policy, not a model).
- needs: The repo; the plugin references for artifact storage and security guidance. Delegation optional.
- side effects: Standalone, saves `threatmodel.md` via the artifact-storage tool; inside a scan it is returned to the caller.
- part of: step 1 of `security-diff-scan` (a supplied model is preserved unchanged); standard and deep scans build their own and do not call it.

### finding-discovery
- id: codex-security:finding-discovery (source path: plugins/codex-security/skills/finding-discovery/SKILL.md)
- description: "Use when Codex is already in the finding-discovery phase of a security scan or the user explicitly asks to discover candidate security findings in a repository or code change. Do not use as the primary trigger for full PR, commit, branch, patch, or repository scans."
- use when: Find candidate security findings in a code change, or in a repository when explicitly asked to do a standalone discovery pass.
- not for: `validation` (decides whether candidates are real); not the primary trigger for full scans.
- needs: The `codex-security` MCP in compact diff mode, or helper scripts in legacy diff mode; standalone repository discovery applies the checklist directly to authorized source. SECURITY.md guidance read before each file.
- side effects: Records candidates only (location, source, sink, impact, CWE); no validation or severity; does not edit code.
- part of: step 3 of `security-diff-scan` (after `threat-model`); hands off to `validation`. Diff-anchoring applies in diff mode only.

### validation
- id: codex-security:validation (source path: plugins/codex-security/skills/validation/SKILL.md)
- description: "Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid. Do not use as the primary trigger for full PR, commit, branch, patch, or repository scans."
- use when: Decide whether candidate security findings are actually valid, as a scan phase or on explicit request.
- not for: `triage-finding` (static triage of imported findings, no running code); `verify-fix` (checks a claimed fix).
- needs: The candidate list from discovery; a build environment for proof-of-concept runs (dynamic proof preferred, static tracing is a supported fallback).
- side effects: Builds and runs target code and PoCs in a disposable copy, avoiding the network unless essential; records a disposition per candidate (`reportable`, `suppressed`, `not_applicable`, `deferred`).
- part of: step 4 of `security-diff-scan` (after `finding-discovery`); hands off to `attack-path-analysis`.

### attack-path-analysis
- id: codex-security:attack-path-analysis (source path: plugins/codex-security/skills/attack-path-analysis/SKILL.md)
- description: "Use when Codex is already in the attack-path-analysis phase of a security scan or the user explicitly asks to trace a security finding from source to sink and calibrate severity. Do not use as the primary trigger for full PR, commit, branch, patch, or repository scans."
- use when: Trace a security finding from source to sink and calibrate severity and reportability.
- not for: `validation` (does it work?) vs this (does it matter and how severe?).
- needs: The per-scan threat model and validated candidates; repo evidence only, no network unless authorized.
- side effects: Records attack-path facts, severity and a final policy decision (`ignore` is recorded explicitly); does not edit code.
- part of: step 4 of `security-diff-scan` (after `validation`, for `reportable` or `deferred` candidates); standard and deep scans do this inline.

### define-security-policy
- id: codex-security:define-security-policy (source path: plugins/codex-security/skills/define-security-policy/SKILL.md)
- description: "Define, review, or update SECURITY.md guidance for a repository or component. Use when the user wants to clarify what Codex Security should review, what is out of scope, which security properties must hold, or whether existing guidance still matches the code."
- use when: Write, review or update SECURITY.md so scans know what to review, what is out of scope and which security properties must hold.
- not for: `threat-model` (generates a model, not policy).
- needs: The repo (source, tests, docs); the plugin launcher helper `resolve-security-md`; owner confirmation of scope, exclusions and accepted risk.
- side effects: Edits `<repo>/SECURITY.md` or a component SECURITY.md only after the user approves the exact diff; no staging, commits or PRs; leaves `.github/SECURITY.md` and `docs/SECURITY.md` alone.
- part of: standalone; its output feeds every scan.

### triage-finding
- id: codex-security:triage-finding (source path: plugins/codex-security/skills/triage-finding/SKILL.md)
- description: "Triage supplied or imported security findings against a repository using its security policy and static code evidence. Accepts scanner reports, advisories, GitHub findings, and Jira or Linear tickets. Do not use for discovery, duplicate triage, runtime validation, or fixes."
- use when: I have scanner results, SARIF, CVE or code-scanning or Dependabot alerts, a bug-bounty report or a Jira/Linear ticket: which are real and which should I fix first?
- not for: `validation` (runs candidates in a scan or on explicit request); `track-findings` (writes to trackers); `fix-finding`.
- needs: Supplied or imported findings; GitHub (REST or connector, asks which sources) and Linear or Atlassian connectors for tickets; the local repo and SECURITY.md.
- side effects: none; read-only and static: no tests, builds, PoCs or edits. Writeback to source systems is reviewed separately.
- part of: standalone; offers `fix-finding` for confirmed findings, run only if asked.

### fix-finding
- id: codex-security:fix-finding (source path: plugins/codex-security/skills/fix-finding/SKILL.md)
- description: "Use only when the user explicitly asks to fix and verify a validated or plausible security vulnerability. Do not use for ordinary bug fixes, correctness or design review findings, general validation, or full PR, commit, branch, patch, or repository scans."
- use when: Fix this security vulnerability and prove it is fixed.
- not for: Ordinary non-security bug fixes; `verify-fix` (read-only check); `propose-security-hardening` (systemic redesign).
- needs: The repo and a runnable test environment; explicit user request only.
- side effects: Edits source (Generate stage uses an isolated worktree or copy); outcome `fixed`, `no_change` or `blocked`; `fixed` only after all ordered verification gates pass.
- part of: reached from `triage-finding` or a direct ask; one review cycle by a fresh reviewer.

### verify-fix
- id: codex-security:verify-fix (source path: plugins/codex-security/skills/verify-fix/SKILL.md)
- description: "Use only when the user explicitly requests verification that a security fix remediates a reported vulnerability. Do not invoke automatically while implementing fixes, reviewing ordinary code changes, or running tests. Do not use for non-security fixes, candidate finding validation, or full repository scans."
- use when: Check whether this security fix really closes the reported vulnerability in the current checkout.
- not for: `fix-finding` (changes code); `validation` (fresh candidates); `assess-patch-risk` (regression and merge risk).
- needs: The current checkout and the original finding(s); explicit request only.
- side effects: none; read-only, returns JSON status `fixed`, `still_vulnerable` or `inconclusive` per finding.
- part of: standalone; follows `fix-finding` or a hand-made fix.

### assess-patch-risk
- id: codex-security:assess-patch-risk (source path: plugins/codex-security/skills/assess-patch-risk/SKILL.md)
- description: "Assess an immutable patch artifact's program impact, regression risk, and auto-merge eligibility. Use for generated patch files, provider pull-request diffs, or commit ranges when reviewers need evidence about affected runtime paths, contracts, tests, and recoverability. This skill is read-only and does not generate, edit, apply, push, or merge the patch."
- use when: Should this patch, PR or commit range be merged? What could it break? Is it auto-merge safe?
- not for: `security-diff-scan` (security vulnerabilities in a diff); `verify-fix` (security fix closure).
- needs: An immutable patch file, provider final-comparison PR diff, or a commit range with base and head (a mutable working tree is refused); Node-based validator helper from the plugin.
- side effects: Preserves the selected checkout and canonical patch; may apply the exact patch and run subject code in a disposable checkout without credentials or network. Writes a report artifact only on request, outside the subject checkout and Git directories; never pushes or merges. Recommends `merge`, `revise`, `no_op`, `block` or `hold_for_evidence`.
- part of: standalone.

### track-findings
- id: codex-security:track-findings (source path: plugins/codex-security/skills/track-findings/SKILL.md)
- description: "Track validated Codex Security findings in Linear, Jira, GitHub issues, or draft GitHub security advisories. Supports issue batches, duplicate checks, and reviewed writes. Do not use for scans or fixes."
- use when: File these validated findings from a sealed scan in Linear, Jira, GitHub issues or a draft GitHub security advisory.
- not for: `triage-finding` (read-only triage); `vulnerability-writeup` (a report, not tickets).
- needs: A sealed scan directory (manifest plus findings) and the Python validator; the Linear, Atlassian or GitHub connector, or the `gh` CLI (required for advisories).
- side effects: Writes to external trackers after the exact payload is previewed and approved; one provider and destination per run, serial; sensitive findings default to private destinations.
- part of: step after a scan; consumes sealed scan output.

### vulnerability-writeup
- id: codex-security:vulnerability-writeup (source path: plugins/codex-security/skills/vulnerability-writeup/SKILL.md)
- description: "Turn vulnerability notes, disclosure reports, PoCs, source code, or Codex Security findings into self-contained, sceptically validated, natural-sounding vulnerability reports. Use for one vulnerability or a disclosure campaign; a Codex Security scan is optional."
- use when: Write a disclosure report for this vulnerability, or a set of them, from my notes, a PoC, the source or a Codex Security finding.
- not for: `propose-security-hardening` (design proposals); `track-findings` (tickets).
- needs: The exact vulnerable source revision, or user acceptance of a report-only assessment; delegation for one subagent per vulnerability.
- side effects: Writes report files (and a sibling `poc/` only for real artifacts); no contact with external or production targets without permission.
- part of: step after a scan or standalone.

### propose-security-hardening
- id: codex-security:propose-security-hardening (source path: plugins/codex-security/skills/propose-security-hardening/SKILL.md)
- description: "Develop evidence-backed structural and architectural security hardening proposals from vulnerability disclosures, supplied findings, incident or assessment documents, source code, or a completed Codex Security scan. Use when a user asks for systemic improvements, alternatives beyond per-finding patches, before-and-after security architecture views, engineering tradeoff analysis, or an implementation-ready plan for a selected hardening option. Also use automatically after a Codex Security scan with reportable findings when the top-level scan workflow requests final-report hardening guidance."
- use when: We keep getting the same class of vulnerabilities; what systemic or architectural changes would prevent them, with options, tradeoffs and before/after diagrams?
- not for: `fix-finding` (per-finding patch); `vulnerability-writeup` (disclosure document).
- needs: Any evidence: disclosures, findings, a scan directory or ID, or source.
- side effects: Writes a `hardening/` bundle in the requested destination or beside the inputs; no source changes until the user selects an option and asks.
- part of: step after a scan (also run automatically at final-report time when a scan requests hardening guidance) or standalone.
