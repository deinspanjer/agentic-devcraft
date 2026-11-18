# openai/plugins family: openai-developers (OpenAI Developers)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `openai-developers` family. The catalog entry is in openai-engineering.md.

## Family: openai-developers
- source path: `plugins/openai-developers` (v1.2.3)
- manifest notes: Codex-only marketplace entry. App connector `openai-platform`; local MCP `openai-api-key-local-confirmation` (Node, ./mcp/server.mjs); Node key helper; Apps starter scaffold. `build-chatgpt-app` metadata declares the OpenAI developer docs MCP (https://developers.openai.com/mcp). `openai-docs` is referenced but not bundled. Key creation is Codex local/app only; troubleshooting assumes Codex `sandbox_permissions`.
- router: none. Credential gate outranks implementation: for OpenAI-backed or provider-unspecified AI work, `openai-platform-api-key` inspects existing conventions, asks reuse vs new key, and stops before any design, code, scaffolding or smoke test. Exception: model or prompt migrations needing only source edits and offline validation. Then `agents-sdk` or `build-chatgpt-app`; `openai-api-troubleshooting` after a runtime failure.
- development distance: core-dev
- disclosure: rich. No router, and the five skills cover different scenarios (key gate, agent app, ChatGPT app, submission, error triage).

### openai-platform-api-key
- id: openai-developers:openai-platform-api-key (source path: plugins/openai-developers/skills/openai-platform-api-key/SKILL.md)
- description: "Use when Codex is asked to build, run, test, debug, or configure an OpenAI-backed or provider-unspecified AI app, UI, script, CLI, generator, or tool, especially requests phrased only as "using AI" or generators driven by forms/user input; also use for OPENAI_API_KEY or sk-proj setup. Do not gate model or prompt migrations that can proceed with source edits and offline validation. Otherwise treat this as the credential gate: inspect safely, ask reuse-vs-new before API work, and never expose plaintext."
- use when: Building any app or script that uses OpenAI or an unspecified AI provider, or setting up OPENAI_API_KEY: decide reuse vs a new key first.
- not for: openai-api-troubleshooting (classifies a failed request, then may hand key setup here); openai-ads-conversions-setup (Ads secrets). Exempt: other providers, offline model/prompt migrations, docs/conceptual examples, static mockups and direct one-off outputs.
- needs: Codex local/app harness; safe credential-presence checks and a reuse/new decision. New-key creation needs the Platform app connector and org/project access; destination confirmation uses the local MCP or a typed fallback.
- side effects: the creation branch creates an account credential and writes a local secret to a confirmed destination; reuse may require no write. Later API use is billable. After successful setup-picker launch, the turn must end.
- part of: mandatory first step before agents-sdk and build-chatgpt-app for OpenAI-backed work; hands to implementation after the decision.

### agents-sdk
- id: openai-developers:agents-sdk (source path: plugins/openai-developers/skills/agents-sdk/SKILL.md)
- description: "Build, run, deploy, and evaluate OpenAI Agents SDK apps from Codex. Use when the user asks to create or adapt an Agents SDK app, build from a prompt or Codex thread, prepare a runnable agent prototype, add a focused eval harness, or deploy locally through the Agents SDK Deployment Manager."
- use when: Turn an idea, repo or prior Codex thread into a runnable OpenAI Agents SDK app, add focused evals, or deploy it locally with the Deployment Manager.
- not for: build-chatgpt-app (MCP and widget in ChatGPT); Cloudflare `agents-sdk` (same host name; agents on Workers); openai-api-troubleshooting (failed call).
- needs: the openai-platform-api-key decision and current Agents docs; Python preferred (`uv`, `openai-agents`), TypeScript if requested. Local deployment defaults to Docker but supports a local-process target.
- side effects: installs dependencies, makes billable API calls, may clone the cookbook, starts services.
- part of: step after openai-platform-api-key. One agent first; evals and deploy only on request.

### build-chatgpt-app
- id: openai-developers:build-chatgpt-app (source path: plugins/openai-developers/skills/build-chatgpt-app/SKILL.md)
- description: "Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK metadata or CSP or domain settings, or produce a docs-aligned project scaffold. Prefer a docs-first workflow by invoking the openai-docs skill or OpenAI developer docs MCP tools before generating code."
- use when: Build, scaffold, refactor or debug a ChatGPT app: MCP server, widget UI, tool metadata, CSP.
- not for: chatgpt-app-submission (import file for an existing server); agents-sdk (agent runtime, not ChatGPT UI); building-mcp-server-on-cloudflare (generic remote MCP, not Apps SDK).
- needs: current Apps SDK docs (`openai-docs` or docs MCP); MCP Inspector, HTTPS tunnel, ChatGPT developer mode for full checks.
- side effects: writes a repo scaffold; hosting and publishing only when in scope.
- part of: entry to the app-building phases; chatgpt-app-submission comes afterward.

### chatgpt-app-submission
- id: openai-developers:chatgpt-app-submission (source path: plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md)
- description: "Inspect a ChatGPT Apps MCP server codebase and generate chatgpt-app-submission.json with app info suggestions, tool hint justifications, test cases, and negative test cases, then report review-check findings and outputSchema warnings for submission review."
- use when: My ChatGPT app's MCP server is built; generate the submission JSON with tool-hint justifications and test cases for review.
- not for: build-chatgpt-app (building or fixing the app); openai-api-troubleshooting (no submission semantics).
- needs: local MCP server code only.
- side effects: writes exactly one `chatgpt-app-submission.json` in the current directory. Missing or wrong tool hints block it until a minimal source fix is approved. Does not submit or publish.
- part of: step after build-chatgpt-app; standalone.

### openai-api-troubleshooting
- id: openai-developers:openai-api-troubleshooting (source path: plugins/openai-developers/skills/openai-api-troubleshooting/SKILL.md)
- description: "Use when an OpenAI API request fails and Codex needs to classify the likely cause, explain the next step, and route to the right follow-up. Covers common runtime failures such as blocked outbound network access, invalid credentials, exhausted API quota or credits, rate limits, and model, project, or organization access issues; delegate key provisioning to openai-platform-api-key and current documentation lookups to openai-docs."
- use when: An OpenAI API request already failed: blocked network, bad credentials, quota or credits, rate limit, or model/project/org access.
- not for: openai-platform-api-key (creates or configures keys); openai-docs (current facts, not error classification).
- needs: concrete request and error evidence; a network-failure retry uses Codex `sandbox_permissions=require_escalated`.
- side effects: retrying the real request can consume quota; never creates or rotates keys.
- part of: standalone diagnostic, often invoked inside agents-sdk work.
