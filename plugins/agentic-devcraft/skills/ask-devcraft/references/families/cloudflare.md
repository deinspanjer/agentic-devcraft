# openai/plugins family: cloudflare (Cloudflare)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `cloudflare` family. The catalog entry is in openai-platforms.md.

## Family: cloudflare
- source path: `plugins/cloudflare` (v0.1.2; upstream cloudflare/skills)
- manifest notes: bundles HTTP MCP `cloudflare-api` (https://mcp.cloudflare.com/mcp; OAuth on first connection, optional bearer token) for account administration, not for building servers. README/commands declare `/cloudflare:build-agent` and `/cloudflare:build-mcp`; the Codex manifest has no commands field, so registration is unestablished. `web-perf` needs a separately configured Chrome DevTools MCP. Not host-restricted. Source examples disagree (TOML `new_classes` vs JSONC `new_sqlite_classes`; SSE vs Streamable HTTP): follow each skill's current-docs gate.
- router: `cloudflare` is a product-selection router: eight decision trees (run code, store data, AI, networking, security, media, analytics, IaC) that load its own references/ directories, not the eight sibling skills. It requires current docs before citing limits, pricing or API signatures.
- development distance: core-dev
- disclosure: rich. The router covers product choice only; the other skills cover different scenarios (CLI operations, Durable Objects, agents, MCP servers, sandboxes, performance audit, code review).

### cloudflare
- id: cloudflare:cloudflare (source path: plugins/cloudflare/skills/cloudflare/SKILL.md)
- description: "Comprehensive Cloudflare platform skill covering Workers, Pages, storage (KV, D1, R2), AI (Workers AI, Vectorize, Agents SDK), networking (Tunnel, Spectrum), security (WAF, DDoS), and infrastructure-as-code (Terraform, Pulumi). Use for any Cloudflare development task. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: I need Cloudflare for a hosting, storage, AI, networking, security or analytics job and have not chosen the product.
- not for: wrangler (product chosen, CLI operations); workers-best-practices (Worker code correctness); agents-sdk, durable-objects, sandbox-sdk (abstraction already known); web-perf (auditing a real page).
- needs: workload, data and latency requirements; current Cloudflare docs. The optional `cloudflare-api` MCP provides account API access; its declaration does not restrict it to reads.
- side effects: product/reference selection prescribes no provisioning; type retrieval may download a package. Effects of implementation depend on the selected reference.
- part of: entry router for product selection; routes to its own references/, not to sibling skills.

### agents-sdk
- id: cloudflare:agents-sdk (source path: plugins/cloudflare/skills/agents-sdk/SKILL.md)
- description: "Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, or chat applications. Covers Agent class, state management, callable RPC, Workflows integration, and React hooks. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: Add state, callable RPC, schedules, resumable chat, workflows, email, or MCP tools to an agent built on Cloudflare's `Agent` class.
- not for: building-ai-agent-on-cloudflare (new project through deploy); durable-objects (no Agent layer); building-mcp-server-on-cloudflare (full remote server). Same host name as OpenAI's `agents-sdk`: this one is Cloudflare.
- needs: npm and the `agents` package, a Worker project with Durable Object bindings and SQLite migration, current Agents docs.
- side effects: writes local code and config; installs `agents` if missing. No deployment step is prescribed.
- part of: standalone SDK specialist.

### building-ai-agent-on-cloudflare
- id: cloudflare:building-ai-agent-on-cloudflare (source path: plugins/cloudflare/skills/building-ai-agent-on-cloudflare/SKILL.md)
- description: "Builds AI agents on Cloudflare using the Agents SDK with state management, real-time WebSockets, scheduled tasks, tool integration, and chat capabilities. Generates production-ready agent code deployed to Workers. Use when: user wants to "build an agent", "AI agent", "chat agent", "stateful agent", mentions "Agents SDK", needs "real-time AI", "WebSocket AI", or asks about agent "state management", "scheduled tasks", or "tool calling". Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: Build and host a chatbot or realtime AI assistant with persistent conversations on Cloudflare, starting from a new project.
- not for: agents-sdk (focused API work in an existing agent); building-mcp-server-on-cloudflare (deliverable is a tool endpoint); durable-objects (no AI/Agent layer).
- needs: Workers-enabled Cloudflare account, Node 18+, Wrangler, `cloudflare/agents-starter`, Workers AI binding; extra credentials per tool.
- side effects: scaffolds a project, deploys a Worker with persistent state, uses billed Workers AI inference.
- part of: entry point of `/cloudflare:build-agent`; runs scaffold, agent code, config, deploy, endpoint check.

### building-mcp-server-on-cloudflare
- id: cloudflare:building-mcp-server-on-cloudflare (source path: plugins/cloudflare/skills/building-mcp-server-on-cloudflare/SKILL.md)
- description: "Builds remote MCP (Model Context Protocol) servers on Cloudflare Workers with tools, OAuth authentication, and production deployment. Generates server code, configures auth providers, and deploys to Workers. Use when: user wants to "build MCP server", "create MCP tools", "remote MCP", "deploy MCP", add "OAuth to MCP", or mentions Model Context Protocol on Cloudflare. Also triggers on "MCP authentication" or "MCP deployment". Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: Build and deploy a remote MCP server on Workers with tools, optional OAuth, and connect MCP clients to it.
- not for: agents-sdk (MCP client or server inside an agent); building-ai-agent-on-cloudflare (builds the AI app); the bundled `cloudflare-api` MCP only administers an account.
- needs: Workers account, Node 18+, Wrangler, MCP Inspector; OAuth branch needs a registered provider app and Wrangler secrets.
- side effects: deploys a public endpoint, stores secrets, exposes tools. Source gives no rule for public vs OAuth: ask.
- part of: entry point of `/cloudflare:build-mcp`: tools, entry point, Inspector test, deploy, connect clients.

### durable-objects
- id: cloudflare:durable-objects (source path: plugins/cloudflare/skills/durable-objects/SKILL.md)
- description: "Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers Workers integration, wrangler config, and testing with Vitest. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: A chat room, game, booking or inventory system, per-tenant record, or persistent WebSocket needs one consistent coordinator, or I want existing Durable Object code reviewed.
- not for: workers-best-practices (stateless Workers); agents-sdk (AI agents on top of DOs); wrangler (CLI and config); cloudflare router branches for D1/Hyperdrive (relational storage).
- needs: Worker/DO project, Wrangler binding and migration config; Vitest with `@cloudflare/vitest-pool-workers` for tests.
- side effects: writes local code and config.
- part of: standalone; receives Durable Object hand-offs from workers-best-practices.

### sandbox-sdk
- id: cloudflare:sandbox-sdk (source path: plugins/cloudflare/skills/sandbox-sdk/SKILL.md)
- description: "Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev environments, or executing untrusted code. Covers Sandbox SDK lifecycle, commands, files, code interpreter, and preview URLs. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: My product must run user- or LLM-generated code, give an agent shell and file tools, or isolate build and validation runs.
- not for: agents-sdk (orchestrates agents; the sandbox isolates their execution); wrangler (manages resources, not the execution SDK); chunk (CircleCI-hosted sandboxes).
- needs: `@cloudflare/sandbox`, working local Docker (`docker info`), Dockerfile, Durable Object binding. Production preview URLs need a custom domain with wildcard DNS, not `.workers.dev`.
- side effects: runs commands in containers, writes sandbox files, can expose public preview URLs; destroy temporary sandboxes.
- part of: standalone.

### web-perf
- id: cloudflare:web-perf (source path: plugins/cloudflare/skills/web-perf/SKILL.md)
- description: "Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (FCP, LCP, TBT, CLS, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed. Biases towards retrieval from current documentation over pre-trained knowledge."
- use when: This page is slow: audit Core Web Vitals or Lighthouse, find render-blocking resources and layout shifts, and get ranked fixes.
- not for: workers-best-practices (server code, not browser measurements); cloudflare (choosing analytics products); circleci-config (CI runtime, not page load).
- needs: Chrome DevTools MCP configured separately (not bundled; the skill stops and asks if absent); an accessible URL; source access only for the codebase phase.
- side effects: loads the page and makes network requests; report only, no patches required.
- part of: standalone audit: trace, vitals, network, accessibility, codebase.

### workers-best-practices
- id: cloudflare:workers-best-practices (source path: plugins/cloudflare/skills/workers-best-practices/SKILL.md)
- description: "Reviews and authors Cloudflare Workers code against production best practices. Load when writing new Workers, reviewing Worker code, configuring wrangler.jsonc, or checking for common Workers anti-patterns (streaming, floating promises, global state, secrets, bindings, observability). Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: Write or review Worker code and wrangler config for production: floating promises, request-crossing global state, unbounded buffering, binding/type mismatch, secrets, observability.
- not for: durable-objects (entity coordination); wrangler (command syntax); code-review (general CodeRabbit diff review; this one is Workers-specific and reads full files).
- needs: full source files, wrangler config, latest `@cloudflare/workers-types` or generated types; `tsc --noEmit` and floating-promise lint.
- side effects: local edits only; deployment is not a step.
- part of: standalone; hands Durable Object work to durable-objects and CLI work to wrangler.

### wrangler
- id: cloudflare:wrangler (source path: plugins/cloudflare/skills/wrangler/SKILL.md)
- description: "Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets Store. Load before running wrangler commands to ensure correct syntax and best practices. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
- use when: Run Wrangler: develop locally, deploy or roll back, tail logs, manage secrets, create or delete KV/R2/D1/Queues/Vectorize, apply D1 migrations, push containers, deploy Pages.
- not for: cloudflare (product selection); workers-best-practices (code correctness).
- needs: Wrangler v4+, Node, `wrangler whoami` or login for remote work, correct resource IDs and environment.
- side effects: production deploys, resource and data deletion, secret changes, remote SQL, registry pushes; the source has no universal confirmation gate, so confirm first. Workers AI always runs remotely and is billed, even in local dev.
- part of: standalone; load before running any Wrangler command.
