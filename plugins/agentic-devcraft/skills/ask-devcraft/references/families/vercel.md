# openai/plugins family: vercel (Vercel)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `vercel` family. The catalog entry is in openai-platforms.md.

## Family: vercel
- source path: `plugins/vercel`. Imports upstream `vercel/vercel-plugin` v0.21.4 (Vercel Labs, Apache-2.0). 54 skills; frontmatter name equals directory name for all.
- manifest notes: Codex-only packaging (`.codex-plugin/plugin.json`; no Claude or Cursor manifest, no hooks; skills are discovered from frontmatter metadata). Listed in the marketplace as `installation: AVAILABLE`, `authentication: ON_INSTALL`, no product restriction. One app connector, `vercel` (`.app.json`). An HTTP MCP server `https://mcp.vercel.com` (OAuth 2.1, read-oriented) is in `.mcp.json`, but `plugin.json` references only the app file, so whether a host loads the MCP is unestablished. It also ships three agent definitions (ai-architect, deployment-expert, performance-optimizer), five slash commands (`/vercel:bootstrap`, `deploy`, `env`, `status`, `marketplace`) and `vercel.md` (a product graph, not a skill); the Codex manifest does not enumerate agents or commands, so their availability per host is unestablished. Most skills need the `vercel` CLI logged in with a linked project (`.vercel/project.json`); CI needs `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`. Command conventions: MCP for reads, CLI for writes; explicit user "yes" for production deploys, env removal, cache purge and domain changes (most skill bodies do not repeat this).
- router: none for the family (`vercel.md` is a graph, not a skill). Partial entry skills with sequences: `knowledge-update` -> `marketplace` (any external service: load marketplace first, then categorize -> discover -> install -> build; storage, auth and AI route to `vercel-storage`, `auth`, `ai-sdk`); `bootstrap` (first-run setup: link -> env -> Neon -> pull -> key diff -> DB scripts -> dev; next-forge repos go to `next-forge`); `verification` / `investigation-mode` / `agent-browser-verify` (debug ladder: browser smoke check -> end-to-end walk -> stuck-app triage; two no-signal steps stop).
- development distance: core-dev
- disclosure: rich. There is no family-wide router skill, and the 54 skills cover genuinely different scenarios (setup, AI features, caching, compute, security, deploy, debugging).
- source conflicts, settled: `knowledge-update` says marketplace first for all external capabilities, while `marketplace` hands storage, auth and AI to dedicated skills: send those three to `vercel-storage`, `auth`, `ai-sdk`, everything else to `marketplace`. The `/vercel:marketplace` command (links first, user picks) differs from the skill (provisions the top result): have the user confirm the provider before install. `next-forge` says only the database is required, `bootstrap` lists Clerk keys: plan for Clerk keys until `keys.ts` shows otherwise. The graph advertises tokenless CI via OIDC, `deployments-cicd` rejects it: assume CI needs `VERCEL_TOKEN`. Local OIDC lifetime is about 24h in `ai-gateway` and 12h in `env-vars`: assume 12h, then re-run `vercel env pull`. `revalidateTag` single-argument examples in `next-cache-components` and `cms` conflict with the performance agent and `runtime-cache` (deprecated in Next.js 16): pass a second argument such as `'max'`. Prices, limits and versions quoted below are source claims.
- name collisions: `react-best-practices` (same body) and `shadcn` (entirely different text) are also skill names in `build-web-apps`; hosts list by frontmatter name, so qualify with the plugin.

### agent-browser
- id: vercel:agent-browser (source path: plugins/vercel/skills/agent-browser/SKILL.md)
- description: "Browser automation CLI for AI agents. Use when the user needs to interact with websites, verify dev server output, test web apps, navigate pages, fill forms, click buttons, take screenshots, extract data, or automate any browser task. Also triggers when a dev server starts so you can verify it visually."
- use when: I need an agent to click through a site, fill a form, log in and reuse state, extract page text, or compare screenshots.
- not for: `agent-browser-verify` (automatic dev-server smoke check), `investigation-mode` (diagnosing an unknown failure).
- needs: `agent-browser` CLI with a browser runtime and a reachable URL; credentials for authenticated sites.
- side effects: writes local screenshots/PDF/state; can submit real forms on live sites with no per-submission approval gate.
- part of: standalone; the execution primitive inside `agent-browser-verify`, `verification` and `investigation-mode`.

### agent-browser-verify
- id: vercel:agent-browser-verify (source path: plugins/vercel/skills/agent-browser-verify/SKILL.md)
- description: "Automated browser verification for dev servers. Triggers when a dev server starts to run a visual gut-check with agent-browser — verifies the page loads, checks for console errors, validates key UI elements, and reports pass/fail before continuing."
- use when: I just started a dev server and want a quick check that the page really renders, with no overlay, errors or missing controls, before continuing.
- not for: `verification` (end-to-end UI -> API -> data check), `investigation-mode` (nothing loads, cause unknown), `agent-browser` (arbitrary browsing).
- needs: running local server and URL; `agent-browser` CLI with browser; Vercel/workflow logs only for the hang branch.
- side effects: writes screenshots; may edit app code in a fix loop (max two retry cycles).
- part of: step inside `verification`; runs right after dev-server start; uses `agent-browser`.

### ai-elements
- id: vercel:ai-elements (source path: plugins/vercel/skills/ai-elements/SKILL.md)
- description: "AI Elements component library guidance — pre-built React components for AI interfaces built on shadcn/ui. Use when building chat UIs, message displays, tool call rendering, streaming responses, reasoning panels, or any AI-native interface with the AI SDK."
- use when: I'm building a React chat or AI interface and want prebuilt components for streaming markdown, tool calls, reasoning panels or voice instead of hand-writing renderers.
- not for: `json-render` (hand-written `UIMessage.parts` rendering), `chat-sdk` (Slack/Teams bots, not web widgets), `geist` (fonts only). Not for non-React, server-only or no-shadcn pipelines.
- needs: React with shadcn initialised on the Radix base; AI SDK v6 and `@ai-sdk/react`; package manager and network.
- side effects: installs dependencies and copies component source into `src/components/ai-elements/`; install only needed components, never the whole suite.
- part of: UI step after `ai-sdk`; complemented by `shadcn` and `geist`.

### ai-gateway
- id: vercel:ai-gateway (source path: plugins/vercel/skills/ai-gateway/SKILL.md)
- description: "Vercel AI Gateway expert guidance. Use when configuring model routing, provider failover, cost tracking, or managing multiple AI providers through a unified API."
- use when: My AI app needs model failover, per-user spend limits or budgets, one endpoint for many providers, or I'm debugging Gateway auth or model-ID errors.
- not for: `ai-sdk` (SDK API usage and verification), `ai-generation-persistence` (storing results and cost in the app), `env-vars` (generic env repair). Use direct provider SDKs only for provider-specific features.
- needs: `ai@^6`; linked Vercel project with Gateway enabled and `vercel env pull` (OIDC), or `AI_GATEWAY_API_KEY`.
- side effects: model calls consume Gateway credits; no deploy by itself.
- part of: step inside `ai-sdk` and the chatbot/durable-agent builds; standalone for policy questions.

### ai-generation-persistence
- id: vercel:ai-generation-persistence (source path: plugins/vercel/skills/ai-generation-persistence/SKILL.md)
- description: "AI generation persistence patterns — unique IDs, addressable URLs, database storage, and cost tracking for every LLM generation"
- use when: Generated chats or images vanish on refresh, can't be shared by URL, or I need generation history, dedup and token/cost records.
- not for: `ai-gateway` (routes and meters provider usage), `ai-elements` (renders saved or streaming content), `bootstrap` (provisions the database/Blob first).
- needs: an app database and schema (example: Neon + Drizzle), Blob storage, `nanoid`; optional Upstash Redis for dedup.
- side effects: writes prompts, results and metadata to the database; the example puts images in public Blob; generation and storage cost money.
- part of: persistence step after `ai-sdk`; pairs with `ai-gateway`.

### ai-sdk
- id: vercel:ai-sdk (source path: plugins/vercel/skills/ai-sdk/SKILL.md)
- description: "Vercel AI SDK expert guidance. Use when building AI-powered features — chat interfaces, text generation, structured output, tool calling, agents, MCP integration, streaming, embeddings, reranking, image generation, or working with any LLM provider."
- use when: I'm implementing or fixing text generation, streaming chat, structured output, tools, embeddings or agents with Vercel's TypeScript AI SDK, especially when old API examples fail.
- not for: `ai-gateway` (provider routing, auth, cost), `chat-sdk` (messaging-platform bots), `eve` (durable filesystem agents), `workflow` (DurableAgent on Workflow DevKit).
- needs: JS/TS project; `ai` package and its bundled docs; Gateway OIDC or key for model calls.
- side effects: installs packages (initially only `ai`), edits code; running it can make billed model calls.
- part of: entry point for AI features; hands off to `ai-elements`, `json-render`, `ai-gateway`.

### auth
- id: vercel:auth (source path: plugins/vercel/skills/auth/SKILL.md)
- description: "Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications. Covers middleware auth patterns, sign-in/sign-up flows, and Marketplace provisioning. Use when implementing user authentication."
- use when: I'm adding login, signup, sessions, route/API protection or enterprise SSO to a Next.js app, or fixing a Clerk Core 3 migration.
- not for: `sign-in-with-vercel` (Vercel accounts as the identity provider), `vercel-connect` (outbound third-party tokens). Provider pick: Clerk for fastest drop-in UI, Descope for passwordless/social, Auth0 for enterprise SSO.
- needs: Next.js; Clerk, Descope or Auth0 account and keys; Vercel CLI for the Marketplace path; Node 20.9+ for the Clerk upgrade CLI.
- side effects: installs packages, can provision auth resources and changes access control; Clerk needs the user to accept terms and finish the dashboard connection.
- part of: standalone; reached from `marketplace`; companion to `bootstrap` and `next-forge`.

### bootstrap
- id: vercel:bootstrap (source path: plugins/vercel/skills/bootstrap/SKILL.md)
- description: "Project bootstrapping orchestrator for repos that depend on Vercel-linked resources (databases, auth, and managed integrations). Use when setting up or repairing a repository so linking, environment provisioning, env pulls, and first-run db/dev commands happen in the correct safe order."
- use when: A fresh clone or new machine won't start because it needs linked Vercel resources, database credentials and env files set up in the right order.
- not for: `env-vars` (env sync only), `marketplace` (provider choice and provisioning), `next-forge` (template-specific setup).
- needs: authenticated Vercel CLI, team and project; an env template; package scripts; Neon via Marketplace (dashboard or Neon CLI as fallback).
- side effects: links the project, provisions resources, writes `AUTH_SECRET` to all environments, and runs DB push/seed/migrate only after env keys verify.
- part of: entry router for first-run setup: link -> env template -> Neon -> pull -> key diff -> DB scripts -> dev; hands next-forge repos to `next-forge`, then `agent-browser-verify`.

### cdn-caching
- id: vercel:cdn-caching (source path: plugins/vercel/skills/cdn-caching/SKILL.md)
- description: "Debug Vercel CDN caching — cache hit rate, stale content, revalidation behavior, ISR + PPR, per-request cache reasons (cacheReason), and costs."
- use when: Vercel cache hit rate dropped, content is stale or bypassing cache, or ISR costs rose, and I need to find which routes or tags are responsible.
- not for: `next-cache-components` (Next.js caching in code), `runtime-cache` (key-value cache), `vercel-firewall` (bot traffic), `investigation-mode` (general failures).
- needs: authenticated Vercel CLI, team/project IDs, logs and header access; `vercel metrics` needs Observability Plus.
- side effects: diagnostics are read-only; any cache purge needs explicit user approval.
- part of: standalone diagnostic entry; hands off to `next-cache-components`, `runtime-cache`, `vercel-firewall`.

### chat-sdk
- id: vercel:chat-sdk (source path: plugins/vercel/skills/chat-sdk/SKILL.md)
- description: "Vercel Chat SDK expert guidance. Use when building multi-platform chat bots — Slack, Telegram, Microsoft Teams, Discord, Google Chat, GitHub, Linear — with a single codebase. Covers the Chat class, adapters, threads, messages, cards, modals, streaming, state management, and webhook setup."
- use when: I'm building one bot that handles mentions, DMs, threads, cards or AI replies across Slack, Teams, Discord, Telegram, Google Chat, GitHub or Linear.
- not for: `ai-elements`/`json-render` (React web chat UI), `ai-sdk` (generation and tool loops), `eve` (durable agent runtime). A `useChat` website request is a negative signal.
- needs: `chat` package and `@chat-adapter/*`; platform bot credentials and webhooks; Redis/Postgres state (or memory); optional AI SDK.
- side effects: can post, edit, delete and schedule real messages and persist state.
- part of: standalone entry for cross-platform bots; integrates `ai-sdk`.

### cms
- id: vercel:cms (source path: plugins/vercel/skills/cms/SKILL.md)
- description: "Headless CMS integration guidance — Sanity (native Vercel Marketplace), Contentful, DatoCMS, Storyblok, and Builder.io. Covers studio setup, content modeling, preview mode, revalidation webhooks, and Visual Editing. Use when building content-driven sites with a headless CMS on Vercel."
- use when: A content-driven Next.js site needs editor-managed content, an embedded Sanity Studio, live preview or revalidation webhooks.
- not for: `geistdocs` (versioned MDX docs, not editor-managed), `cdn-caching` (webhook invalidation cost), `next-forge` (its own BaseHub path). Sanity and Contentful are substantive; the other vendors are only named.
- needs: Next.js; CMS account and tokens; Vercel CLI for Sanity Marketplace provisioning; revalidation and draft secrets.
- side effects: can provision resources and change published content; webhooks invalidate caches.
- part of: build step after `marketplace`; hands off to `env-vars` and the caching skills.

### cron-jobs
- id: vercel:cron-jobs (source path: plugins/vercel/skills/cron-jobs/SKILL.md)
- description: "Vercel Cron Jobs configuration and best practices. Use when adding, editing, or debugging scheduled tasks in vercel.json."
- use when: I need a scheduled task (daily digest, cleanup, sync) on Vercel, or a configured cron isn't firing.
- not for: `workflow` (durable multi-step jobs), `vercel-queues` (event delivery), `deployments-cicd` (getting the schedule to production).
- needs: a deployed API route, five-field UTC schedule, `CRON_SECRET`; Hobby limits two jobs, once daily (source claim).
- side effects: production-only; invokes real production logic on a schedule.
- part of: standalone; a background-task evidence source for `investigation-mode`.

### deployments-cicd
- id: vercel:deployments-cicd (source path: plugins/vercel/skills/deployments-cicd/SKILL.md)
- description: "Vercel deployment and CI/CD expert guidance. Use when deploying, promoting, rolling back, inspecting deployments, building with --prebuilt, or configuring CI workflow files for Vercel."
- use when: I want to ship a preview or production build, promote, roll back, troubleshoot a deployment, or write GitHub/GitLab/Bitbucket CI for Vercel.
- not for: `env-vars` (missing config), `investigation-mode` (unexplained runtime failure), `vercel-cli` (one-off CLI task).
- needs: Vercel CLI, linked project; CI needs `VERCEL_TOKEN`, org and project IDs (runtime OIDC does not replace them).
- side effects: builds, deploys and changes live production aliases; may post PR comments. `/vercel:deploy` defaults to preview and requires explicit yes for production.
- part of: standalone release specialist; follows `bootstrap` and `marketplace`.

### email
- id: vercel:email (source path: plugins/vercel/skills/email/SKILL.md)
- description: "Email sending integration guidance — Resend (native Vercel Marketplace) with React Email templates. Covers API setup, transactional emails, domain verification, and template patterns. Use when sending emails from a Vercel-deployed application."
- use when: I need transactional email from a Vercel app: Resend sending, React Email templates, sender-domain verification, broadcasts or delivery webhooks.
- not for: `chat-sdk` (chat-platform bots), `cms` (editable site content). `next-forge` uses `RESEND_TOKEN`; this skill uses `RESEND_API_KEY`.
- needs: Resend account or Marketplace install; server-only `RESEND_API_KEY`; DNS control for a custom sender domain.
- side effects: sends real email, uploads templates, creates webhooks and may schedule broadcasts; no send-approval gate in the skill.
- part of: build step after `marketplace`.

### env-vars
- id: vercel:env-vars (source path: plugins/vercel/skills/env-vars/SKILL.md)
- description: "Vercel environment variable expert guidance. Use when working with .env files, vercel env commands, OIDC tokens, or managing environment-specific configuration."
- use when: My local app misses a secret, an OIDC token expired, preview reads production config, or I need to sync, add, remove or diff Vercel env variables.
- not for: `bootstrap` (ordered first-run setup), `ai-gateway` (model auth policy), `deployments-cicd` (release).
- needs: Vercel CLI linked to the project; `.env*` files; optional dotenv-cli.
- side effects: `env pull` can replace the whole local env file; add/remove changes remote environments including production (confirm first).
- part of: standalone; step inside `bootstrap`, `marketplace` and Gateway setup.

### eve
- id: vercel:eve (source path: plugins/vercel/skills/eve/SKILL.md)
- description: "Build durable AI agents and agent-powered applications with the eve framework. Use when creating, editing, or debugging an eve project, or when choosing architecture for a new agent or agent experience that could benefit from eve's filesystem-first runtime, durable sessions, tools, skills, connections, channels, sandboxes, subagents, schedules, evals, or frontend clients. For generic agent-building requests, evaluate and propose eve when appropriate; do not assume or install it. Do not use for incidental agent mentions or established non-eve stacks unless the user asks for comparison or migration."
- use when: I'm working in an existing Eve project, weighing architecture for a durable agent with tools, channels, schedules or subagents, or inspecting deployed Eve agent-run traces.
- not for: `ai-sdk` (direct ToolLoopAgent), `workflow` (DurableAgent), `chat-sdk` (bot transport). For a generic agent request it proposes Eve but must not assume or install it.
- needs: `eve` package or approved scaffold and its installed docs; for deployed runs, authenticated Vercel CLI or MCP.
- side effects: may scaffold or install the framework after selection; runtime costs depend on its docs.
- part of: entry point for Eve work; reads installed docs before any code.

### geist
- id: vercel:geist (source path: plugins/vercel/skills/geist/SKILL.md)
- description: "Expert guidance for Geist, Vercel's default typography system and font family for precise Next.js interfaces. Use when configuring Geist Sans, Geist Mono, or Geist Pixel, setting up font imports, or applying Vercel typography and aesthetic guidance."
- use when: I'm setting up Geist Sans, Mono or Pixel fonts in Next.js/Tailwind, fixing font imports or CSS variables, or restoring coding ligatures.
- not for: `geistdocs` (docs-site template), `shadcn` (general components), `ai-elements` (AI UI).
- needs: Next.js/React and the `geist` package; nothing else.
- side effects: changes dependency, layout and CSS files.
- part of: standalone; UI-baseline step in `bootstrap`.

### geistdocs
- id: vercel:geistdocs (source path: plugins/vercel/skills/geistdocs/SKILL.md)
- description: "Expert guidance for Geistdocs, Vercel's documentation template built with Next.js and Fumadocs — MDX authoring, configuration, AI chat, i18n, feedback, deployment. Use when creating documentation sites, configuring geistdocs, writing MDX content, or setting up docs infrastructure."
- use when: I'm creating or editing a documentation microsite with MDX pages, search, Ask AI, translations, feedback or llms.txt using the Geistdocs template.
- not for: `cms` (editor-managed content), `geist` (fonts), `next-forge` (its docs app is Mintlify). Not for API-reference generators, Storybook or Docusaurus.
- needs: Node 18+, pnpm, GitHub account; `AI_GATEWAY_API_KEY` for Ask AI; Vercel account to deploy. Beta.
- side effects: template CLI clones and installs; the deploy steps push to GitHub and import into Vercel; feedback creates GitHub issues, with no approval gate in the body.
- part of: standalone; uses `ai-gateway` for Ask AI.

### investigation-mode
- id: vercel:investigation-mode (source path: plugins/vercel/skills/investigation-mode/SKILL.md)
- description: "Orchestrated debugging coordinator. Triggers on frustration signals (stuck, hung, broken, waiting) and systematically triages: runtime logs → workflow status → browser verify → deploy/env. Reports findings at every step."
- use when: My app is stuck, hung, blank or 'nothing happened' and I need systematic evidence before another speculative edit.
- not for: `agent-browser-verify` (browser-first smoke check), `cdn-caching` (cache cause), `deployments-cicd` (acting on releases). Excludes CSS/styling complaints.
- needs: runtime logs and terminal; deployment URL and CLI credentials if deployed; `agent-browser` for visual evidence.
- side effects: may add structured logging to the code; otherwise read-only.
- part of: entry router: runtime logs -> workflow status -> browser -> deploy/env; stops at root cause or two no-signal steps; hands to `observability` and `workflow`.

### json-render
- id: vercel:json-render (source path: plugins/vercel/skills/json-render/SKILL.md)
- description: "AI chat response rendering guidance — handling UIMessage parts, tool call displays, streaming states, and structured data presentation. Use when building custom chat UIs, rendering tool results, or troubleshooting AI response display issues."
- use when: My custom React AI chat shows JSON blobs, missing text or broken streaming, and I need to render `UIMessage.parts` and tool results by hand.
- not for: `ai-elements` (prebuilt components; prefer it unless customizing), `ai-sdk` (core APIs), `chat-sdk` (platform bots). Despite the name it is not a JSON-to-UI framework.
- needs: React, AI SDK v6 and `@ai-sdk/react`; an API route using the UI-message protocol.
- side effects: edits client and server code; model calls can cost money.
- part of: custom-rendering step inside `ai-sdk`; hands off to `ai-elements`.

### knowledge-update
- id: vercel:knowledge-update (source path: plugins/vercel/skills/knowledge-update/SKILL.md)
- description: "Corrects outdated LLM knowledge about the Vercel platform and introduces new products. Injected at session start."
- use when: I'm planning on Vercel from memory (Edge-only streaming, Vercel Postgres/KV, static vercel.json) or about to build something needing an external service.
- not for: `marketplace` (does the discovery and provisioning), `eve` (agent architecture). Its 'injected at session start' claim has no hook behind it, so load it deliberately.
- needs: nothing to consult; the `vercel.ts` example needs `@vercel/config`.
- side effects: none; read-only guidance dated 2026-06-29.
- part of: entry router: for any external-service build, load `marketplace` first, before recommending a provider, asking questions or writing code.

### marketplace
- id: vercel:marketplace (source path: plugins/vercel/skills/marketplace/SKILL.md)
- description: "Vercel Marketplace expert guidance — discovering, installing, and managing third-party integrations via the `vercel integration` CLI. Use when building any app that needs an external capability without a dedicated skill — commerce (stores, storefronts, selling products), payments (checkout, subscriptions, billing), observability/monitoring, messaging/email, search, or CMS — or when discovering, installing, or managing integrations."
- use when: My app needs an external capability (store, payments, search, monitoring, messaging) and a real service must be chosen and provisioned before I build.
- not for: `vercel-storage`, `auth` and `ai-sdk` (the dedicated routes it hands off to), `bootstrap` (repairs known dependencies). The `/vercel:marketplace` command differs: it links first and lets the user pick.
- needs: Vercel CLI; no auth for `integration categories/discover`, linked project to install; vendor account or browser steps.
- side effects: provisions real services under billing and `env pull` writes local secrets; stops for account or claim steps.
- part of: entry router: categorize -> discover -> install -> build; Shopify for catalogs, Stripe for payments without a catalog; called by `knowledge-update`.

### micro
- id: vercel:micro (source path: plugins/vercel/skills/micro/SKILL.md)
- description: "Expert guidance for micro — asynchronous HTTP microservices framework by Vercel. Use when building lightweight HTTP servers, API endpoints, or microservices using the micro library."
- use when: I'm building or maintaining a tiny Node HTTP service on the `micro` library, parsing request bodies and composing small handlers.
- not for: `microfrontends` (unrelated frontend composition), `ncc` (bundles it), `nextjs` (full app routes).
- needs: Node.js and `micro`; no Vercel account.
- side effects: installs dependencies and runs a local server.
- part of: standalone.

### microfrontends
- id: vercel:microfrontends (source path: plugins/vercel/skills/microfrontends/SKILL.md)
- description: "Guide for building, configuring, and deploying microfrontends on Vercel. Use this skill when the user mentions microfrontends, multi-zones, splitting an app across teams, independent deployments, cross-app routing, incremental migration, composing multiple frontends under one domain, microfrontends.json, @vercel/microfrontends, the microfrontends local proxy, or path-based routing between Vercel projects. Also use when the user asks about shared layouts across projects, navigation between microfrontends, fallback environments, asset prefixes, or feature flag controlled routing."
- use when: I'm splitting a large frontend across teams or projects under one domain: path routing, multi-zone migration, independent deploys, local proxy or cross-app security.
- not for: `next-forge` (shared-package monorepo, no same-domain composition), `turborepo` (task runner), `vercel-services` (multi-runtime in one project), `micro` (unrelated).
- needs: multiple Vercel projects, CLI, `@vercel/microfrontends` in every app, config in the default app; interactive terminal for group changes.
- side effects: group changes can alter billing and routing (non-interactive creation blocked beyond free tier); delete is irreversible; config takes effect on production deploy.
- part of: entry point for composition; dispatches to six topic references.

### ncc
- id: vercel:ncc (source path: plugins/vercel/skills/ncc/SKILL.md)
- description: "Expert guidance for @vercel/ncc — a simple CLI for compiling Node.js modules into a single file with all dependencies included. Use when bundling serverless functions, CLI tools, or any Node.js project into a self-contained file."
- use when: I want to bundle a Node CLI, serverless handler or GitHub Action into one self-contained file with `@vercel/ncc`.
- not for: `turbopack` (Next.js bundler), `turborepo` (workspace builds), `micro` (the HTTP framework you might bundle).
- needs: Node project with an entry file; `@vercel/ncc`; tsconfig for TypeScript.
- side effects: writes build output (`dist/`); `--transpile-only` skips type-checking.
- part of: standalone build step before `deployments-cicd`.

### next-cache-components
- id: vercel:next-cache-components (source path: plugins/vercel/skills/next-cache-components/SKILL.md)
- description: "Next.js 16 Cache Components guidance — PPR, use cache directive, cacheLife, cacheTag, updateTag, and migration from unstable_cache. Use when implementing partial prerendering, caching strategies, or migrating from older Next.js cache patterns."
- use when: My Next.js 16 app needs a static shell with dynamic sections, `use cache` boundaries, tags and invalidation, or a migration from `unstable_cache` or experimental PPR.
- not for: `cdn-caching` (platform-wide hit-rate and ISR cost), `runtime-cache` (key-value store). Not for Edge runtime or static export.
- needs: Next.js 16+ on the Node runtime.
- side effects: edits config and code; changes freshness behaviour.
- part of: standalone; handoff target from `cdn-caching`.

### next-forge
- id: vercel:next-forge (source path: plugins/vercel/skills/next-forge/SKILL.md)
- description: "next-forge expert guidance — production-grade Turborepo monorepo SaaS starter by Vercel. Use when working in a next-forge project, scaffolding with `npx next-forge init`, or editing @repo/* workspace packages."
- use when: I'm starting or editing a next-forge SaaS monorepo (`apps/app`, `apps/web`, `apps/api`, `@repo/*` packages).
- not for: `bootstrap` (generic setup; it hands next-forge repos here), `microfrontends` (same-domain composition), `geistdocs` (Fumadocs vs this template's Mintlify docs). Setup docs say only the database is required; bootstrap says Clerk keys; check `keys.ts`.
- needs: Node >=18, a package manager, PostgreSQL `DATABASE_URL`; optional vendor keys; Vercel accounts only to deploy.
- side effects: installs and copies env templates; `migrate` formats schema, generates client and runs db push on the configured database.
- part of: template-specific entry; companion to `auth`, `email`, `deployments-cicd`.

### next-upgrade
- id: vercel:next-upgrade (source path: plugins/vercel/skills/next-upgrade/SKILL.md)
- description: "Upgrade Next.js to the latest version following official migration guides and codemods. Use when upgrading Next.js versions, running codemods, or migrating between major releases."
- use when: I need to upgrade Next.js to a newer major version and run the official codemods.
- not for: `nextjs` (everyday App Router work), `turbopack` (bundler config after upgrade).
- needs: Next.js project, network access to fetch the upgrade guides, a package manager.
- side effects: edits `package.json`, the lockfile and code; upgrade one major at a time, codemods first.
- part of: standalone.

### nextjs
- id: vercel:nextjs (source path: plugins/vercel/skills/nextjs/SKILL.md)
- description: "Next.js App Router expert guidance. Use when building, debugging, or architecting Next.js applications — routing, Server Components, Server Actions, Cache Components, layouts, middleware/proxy, data fetching, rendering strategies, and deployment on Vercel."
- use when: I'm writing, reviewing or debugging a Next.js App Router app: routing, Server Components, async params, metadata, images, hydration errors or self-hosting.
- not for: `next-upgrade` (version migration), `next-cache-components` (caching), `turbopack` (bundler), `routing-middleware` (middleware vs `proxy.ts`), `react-best-practices` (performance review).
- needs: a Next.js project.
- side effects: none; an index into its own reference files.
- part of: standalone default Next.js entry.

### observability
- id: vercel:observability (source path: plugins/vercel/skills/observability/SKILL.md)
- description: "Vercel Observability expert guidance — Drains (logs, traces, speed insights, web analytics), Web Analytics, Speed Insights, runtime logs, custom events, OpenTelemetry integration, and monitoring dashboards. Use when instrumenting, debugging, or optimizing application performance and user experience on Vercel."
- use when: I want logging, monitoring or analytics on Vercel: runtime logs, Web Analytics, Speed Insights, drains, OpenTelemetry, or Sentry/Datadog setup.
- not for: `vercel-api` (drain and log API details), `investigation-mode` (stuck-app debugging), `verification` (end-to-end check), `vercel-agent` (paid AI review).
- needs: Vercel project; `VERCEL_TOKEN` for REST; Pro/Enterprise for drains and custom events (source claim).
- side effects: creating or deleting drains and installing vendor integrations are writes with billing consequences.
- part of: standalone; referenced by `verification` and `investigation-mode`.

### payments
- id: vercel:payments (source path: plugins/vercel/skills/payments/SKILL.md)
- description: "Stripe payments integration guidance — native Vercel Marketplace setup, checkout sessions, webhook handling, subscription billing, and the Stripe SDK. Use when implementing payments, subscriptions, or processing transactions."
- use when: I'm adding Stripe checkout, subscriptions, webhooks or a customer portal to a Vercel app.
- not for: `marketplace` (catalog stores route to Shopify commerce), `auth`, `env-vars`. Stripe only.
- needs: Stripe account or sandbox and API keys; webhook signing secret for webhooks; Vercel CLI for the Marketplace install; `stripe` packages.
- side effects: provisions a Stripe integration and env vars; examples create Checkout/portal sessions and confirm payments (real charges with live credentials); webhook signatures must be verified against the raw body.
- part of: standalone; reached from `marketplace`.

### react-best-practices
- id: vercel:react-best-practices (source path: plugins/vercel/skills/react-best-practices/SKILL.md)
- description: "React best-practices reviewer for TSX files. Triggers after editing multiple TSX components to run a condensed quality checklist covering component structure, hooks usage, accessibility, performance, and TypeScript patterns."
- use when: I'm writing, reviewing or refactoring React/Next components, pages or data fetching for performance: waterfalls, bundle size, re-renders. Describe by body: a 64-rule performance index in eight categories, not the general accessibility/TypeScript quality checklist promised in the description.
- not for: `nextjs` (framework conventions), `swr` (client fetching), `shadcn` (components).
- needs: React/Next source (TSX or JSX); individual rule files for detailed examples.
- side effects: review alone is read-only; applying the guidance can generate or refactor code.
- part of: standalone.

### routing-middleware
- id: vercel:routing-middleware (source path: plugins/vercel/skills/routing-middleware/SKILL.md)
- description: "Vercel Routing Middleware guidance — request interception before cache, rewrites, redirects, personalization. Works with any framework. Supports Edge, Node.js, and Bun runtimes. Use when intercepting requests at the platform level."
- use when: I need to intercept requests before cache (rewrites, redirects, geo or A/B personalization, header injection), or I'm unsure whether I want middleware, Next.js 16 `proxy.ts` or Edge Functions.
- not for: `vercel-firewall` (platform security rules), `vercel-functions` (Edge Functions), `nextjs` (`proxy.ts`). Not a sole auth layer; thousands of redirects go to Bulk Redirects.
- needs: Vercel deployment; `@vercel/functions`; optional `@vercel/edge-config`.
- side effects: none beyond code edits.
- part of: standalone.

### runtime-cache
- id: vercel:runtime-cache (source path: plugins/vercel/skills/runtime-cache/SKILL.md)
- description: "Vercel Runtime Cache API guidance — ephemeral per-region key-value cache with tag-based invalidation. Shared across Functions, Routing Middleware, and Builds. Use when implementing caching strategies beyond framework-level caching."
- use when: I need a per-region key-value cache with tag invalidation across Functions and Middleware, or to purge the CDN or data cache by tag.
- not for: `next-cache-components` (framework caching), `cdn-caching` (diagnosis), `vercel-storage` (persistent data). Runtime Cache tags do not touch ISR.
- needs: Vercel deployment; `@vercel/functions`; CLI for purges.
- side effects: CLI purge and delete commands hit production caches; confirm first.
- part of: standalone.

### satori
- id: vercel:satori (source path: plugins/vercel/skills/satori/SKILL.md)
- description: "Expert guidance for Satori — Vercel's library that converts HTML and CSS to SVG, commonly used to generate dynamic OG images for Next.js and other frameworks."
- use when: I'm generating dynamic Open Graph or Twitter images (`opengraph-image.tsx`, `next/og`) or converting HTML/CSS to SVG.
- not for: `nextjs` (metadata conventions).
- needs: Next.js or another edge framework; font files.
- side effects: none; flexbox-only CSS subset, fonts loaded explicitly.
- part of: standalone.

### shadcn
- id: vercel:shadcn (source path: plugins/vercel/skills/shadcn/SKILL.md)
- description: "shadcn/ui expert guidance — CLI, component installation, composition patterns, custom registries, theming, Tailwind CSS integration, and high-quality interface design. Use when initializing shadcn, adding components, composing product UI, building custom registries, configuring themes, or troubleshooting component issues."
- use when: I'm initializing shadcn/ui, adding components, building a registry, theming with Tailwind, or composing product UI.
- not for: `v0-dev` (AI generation through a v0 account), `ai-elements` (AI components; needs `--base radix`), `geist` (fonts).
- needs: React with Tailwind; network for registry.
- side effects: writes component source into the repo; always `shadcn init -d` for non-interactive.
- part of: standalone; UI-baseline step in `bootstrap`.

### sign-in-with-vercel
- id: vercel:sign-in-with-vercel (source path: plugins/vercel/skills/sign-in-with-vercel/SKILL.md)
- description: "Sign in with Vercel guidance — OAuth 2.0/OIDC identity provider for user authentication via Vercel accounts. Use when implementing user login with Vercel as the identity provider."
- use when: I want users to log into my app with their Vercel account (OAuth 2.0/OIDC).
- not for: `auth` (Clerk/Descope/Auth0 for general users), `vercel-connect` (outbound third-party tokens). Not for machine-to-machine auth.
- needs: an integration registered in the Vercel Integrations Console (client ID and secret).
- side effects: none; conceptual guide with no code.
- part of: standalone.

### swr
- id: vercel:swr (source path: plugins/vercel/skills/swr/SKILL.md)
- description: "SWR data-fetching expert guidance. Use when building React apps with client-side data fetching, caching, revalidation, mutations, optimistic UI, pagination, or infinite loading using the SWR library."
- use when: I'm doing client-side data fetching in React with SWR: caching, revalidation, mutations, optimistic UI or infinite loading.
- not for: `nextjs` (server data patterns), `react-best-practices` (broader performance).
- needs: React app; the `swr` package.
- side effects: installs a package.
- part of: standalone.

### turbopack
- id: vercel:turbopack (source path: plugins/vercel/skills/turbopack/SKILL.md)
- description: "Turbopack expert guidance. Use when configuring the Next.js bundler, optimizing HMR, debugging build issues, or understanding the Turbopack vs Webpack differences."
- use when: I'm configuring the Next.js 16 bundler, fixing HMR or build failures, migrating webpack loaders, or analysing bundle size.
- not for: `turborepo` (monorepo task runner, often confused), `next-upgrade`, `nextjs`.
- needs: Next.js 16 project.
- side effects: none; guidance and config edits.
- part of: standalone.

### turborepo
- id: vercel:turborepo (source path: plugins/vercel/skills/turborepo/SKILL.md)
- description: "Turborepo expert guidance. Use when setting up or optimizing monorepo builds, configuring task caching, remote caching, parallel execution, or the --affected flag for incremental CI."
- use when: I'm setting up or speeding up a JS/TS monorepo build: `turbo.json`, remote cache, `--affected`, filters, CI matrix.
- not for: `turbopack` (bundler), `microfrontends`, `vercel-services` (multi-runtime in one project), `next-forge` (template). A single Next.js app doesn't need it.
- needs: a monorepo; Vercel login or token for remote cache.
- side effects: writes `turbo.json`; remote cache uploads build artifacts.
- part of: standalone.

### v0-dev
- id: vercel:v0-dev (source path: plugins/vercel/skills/v0-dev/SKILL.md)
- description: "v0 by Vercel expert guidance. Use when discussing AI code generation, generating UI components from prompts, v0 CLI usage, v0 SDK/API integration, or integrating v0 into development workflows with GitHub and Vercel deployment."
- use when: I want to use v0 itself: generate UI from prompts or screenshots, `npx v0@latest add`, or call the v0 SDK, API or MCP.
- not for: `shadcn` (local components without a v0 account), `ai-elements`.
- needs: `V0_API_KEY` and a v0 account.
- side effects: SDK `deployments.create` deploys; the GitHub integration commits and pushes to v0 branches.
- part of: standalone.

### vercel-agent
- id: vercel:vercel-agent (source path: plugins/vercel/skills/vercel-agent/SKILL.md)
- description: "Vercel Agent guidance — AI-powered code review, incident investigation, and SDK installation. Automates PR analysis and anomaly debugging. Use when configuring or understanding Vercel's AI development tools."
- use when: I want to configure or understand Vercel Agent: AI code review on PRs, incident investigation, automatic Analytics or Speed Insights install.
- not for: `observability` (instrumentation).
- needs: Vercel team and project; paid usage; investigation needs Observability Plus.
- side effects: paid per review or investigation (source claim); configured in project settings.
- part of: standalone; conceptual.

### vercel-api
- id: vercel:vercel-api (source path: plugins/vercel/skills/vercel-api/SKILL.md)
- description: "Vercel app and REST API expert guidance. Use when the agent needs live access to Vercel projects, deployments, environment variables, domains, logs, or documentation through the connected Vercel app or REST API."
- use when: I need live Vercel state (projects, deployments, env vars, domains, logs, docs) through the connected app or MCP, or via REST, `@vercel/sdk` or `vercel api`.
- not for: `vercel-cli` (deploy and other writes), `observability` (drain details), `marketplace`.
- needs: OAuth to the Vercel app or MCP (`mcp.vercel.com`), or `VERCEL_TOKEN`.
- side effects: MCP reads are read-only; the REST examples can create env vars, drains and deployments.
- part of: standalone read-path entry.

### vercel-cli
- id: vercel:vercel-cli (source path: plugins/vercel/skills/vercel-cli/SKILL.md)
- description: "Vercel CLI expert guidance. Use when deploying, managing environment variables, linking projects, viewing logs, querying metrics, managing domains, or interacting with the Vercel platform from the command line."
- use when: I need a specific Vercel CLI task: deploy, link, env vars, logs, domains, metrics, or reaching a protected preview with `vercel curl`.
- not for: `vercel-api` (MCP/REST reads), `deployments-cicd` (release and CI), `env-vars`, `bootstrap`.
- needs: `vercel` CLI, logged in and linked (`.vercel/`).
- side effects: commands can deploy to production and modify env vars and domains.
- part of: entry point of a decision tree into its own reference files.

### vercel-connect
- id: vercel:vercel-connect (source path: plugins/vercel/skills/vercel-connect/SKILL.md)
- description: "Vercel Connect expert guidance — securely obtain scoped OAuth tokens for third-party services (Slack, GitHub, MCP servers, OAuth, Snowflake) on behalf of apps or users via Vercel OIDC. Use when wiring up third-party API access, connecting to MCP servers, sending Slack messages, accessing GitHub APIs, receiving webhook events from Slack/Linear/GitHub and forwarding them to your agents and apps, or building Eve agent connections."
- use when: My app or agent needs scoped OAuth tokens for Slack, GitHub, Linear, Snowflake or MCP servers, inbound webhook auth, or Eve agent connections.
- not for: `sign-in-with-vercel` (inbound login), `auth` (end-user login), `chat-sdk`, `eve`.
- needs: Vercel CLI, team scope, OIDC token (`vc env pull`); run from the consuming project folder or pass `--cwd`.
- side effects: `vercel connect create` and `token` open a browser step the user must finish; get approval before create.
- part of: standalone four-step flow: list -> create -> token -> use.

### vercel-firewall
- id: vercel:vercel-firewall (source path: plugins/vercel/skills/vercel-firewall/SKILL.md)
- description: "Vercel Firewall expert guidance — automatic DDoS mitigation, the Vercel WAF (custom rules, IP blocking, managed rulesets, rate limiting), Attack Mode, system bypass, bot management, and the `vercel firewall` CLI. Use when configuring platform-level security, responding to attacks, or staging firewall rules."
- use when: I'm configuring WAF rules, IP blocks, rate limits or Attack Mode, or responding to abuse.
- not for: `routing-middleware` (request logic in code), `vercel-api` (firewall REST).
- needs: linked project and CLI auth; Observability Plus for CLI metrics.
- side effects: rule/IP-block changes stage drafts; ask the user to run `vercel firewall publish --yes`; attack-mode, system-bypass and mitigations apply immediately. Attack-mode enable and system-mitigations pause are blocked for agents; the user must run them.
- part of: standalone; staged rollout log -> preview deny -> prod log -> prod block.

### vercel-flags
- id: vercel:vercel-flags (source path: plugins/vercel/skills/vercel-flags/SKILL.md)
- description: "Vercel Flags guidance — feature flags platform with unified dashboard, Flags Explorer, gradual rollouts, A/B testing, and provider adapters. Use when implementing feature flags, experimentation, or staged rollouts."
- use when: I'm adding feature flags, gradual rollouts, A/B tests, Flags Explorer or flag-provider adapters.
- not for: `vercel-storage` (raw Edge Config), `routing-middleware`.
- needs: `flags` package and supported framework; Vercel provider needs a project and `FLAGS`, Flags Explorer needs `FLAGS_SECRET`; custom/other providers are supported. Public-beta pricing applies to Vercel Flags (source claim).
- side effects: edits code/config; CLI can create remote flags, and provider requests incur usage charges; fetch current docs first.
- part of: standalone.

### vercel-functions
- id: vercel:vercel-functions (source path: plugins/vercel/skills/vercel-functions/SKILL.md)
- description: "Vercel Functions expert guidance — Serverless Functions, Edge Functions, Fluid Compute, streaming, Cron Jobs, and runtime configuration. Use when configuring, debugging, or optimizing server-side code running on Vercel."
- use when: I'm configuring or debugging server-side code on Vercel: runtimes, Fluid Compute, streaming, WebSockets, `maxDuration`, or 504/500 and cold-start problems.
- not for: `routing-middleware`, `cron-jobs`, `workflow` (tasks over about 15 minutes), `vercel-queues`.
- needs: Vercel project; WebSockets require Fluid Compute.
- side effects: none; guidance and config edits.
- part of: standalone compute hub.

### vercel-queues
- id: vercel:vercel-queues (source path: plugins/vercel/skills/vercel-queues/SKILL.md)
- description: "Vercel Queues guidance (public beta) — durable event streaming with topics, consumer groups, retries, and delayed delivery. $0.60/1M ops. Powers Workflow DevKit. Use when building async processing, fan-out patterns, or event-driven architectures."
- use when: I need async processing, fan-out, delayed delivery or retries with consumer groups on Vercel Queues.
- not for: `workflow` (stateful multi-step orchestration, built on Queues), `cron-jobs` (schedules), `vercel-functions`.
- needs: Vercel project (OIDC) or `VERCEL_QUEUE_API_TOKEN`; Node 22+; public beta, fetch docs first.
- side effects: sending messages bills per operation.
- part of: standalone.

### vercel-sandbox
- id: vercel:vercel-sandbox (source path: plugins/vercel/skills/vercel-sandbox/SKILL.md)
- description: "Vercel Sandbox guidance — ephemeral Firecracker microVMs for running untrusted code safely. Supports AI agents, code generation, and experimentation. Use when executing user-generated or AI-generated code in isolation."
- use when: I want to run `agent-browser` with headless Chromium inside a Vercel Sandbox microVM for screenshots, accessibility snapshots, form automation or scheduled browser tasks. Describe by body: the description promises general untrusted-code execution, but the body teaches only browser automation.
- not for: `agent-browser` (local browser CLI); for generic code isolation this skill won't help.
- needs: `@vercel/sandbox`; OIDC or `VERCEL_TOKEN`/team/project IDs; `agent-browser`, Chromium and system dependencies installed inside the VM (or a prepared sandbox snapshot).
- side effects: creates billable sandboxes and saved VM snapshots, installs dependencies inside the VM and writes screenshots; browser form submissions can mutate live sites.
- part of: standalone; companion to `agent-browser` and `agent-browser-verify`.

### vercel-services
- id: vercel:vercel-services (source path: plugins/vercel/skills/vercel-services/SKILL.md)
- description: "Vercel Services — deploy multiple services within a single Vercel project. Use for monorepo layouts or when combining a backend (Python, Go) with a frontend (Next.js, Vite) in one deployment."
- use when: I'm deploying a Python or Go backend together with a Next.js or Vite frontend in one Vercel project.
- not for: `turborepo` (task runner), `microfrontends`, `deployments-cicd` (does the actual deploy).
- needs: Vercel project with Services framework preset; `vercel dev -L`. Beta; only Python and Go validated.
- side effects: none; writes `experimentalServices` config.
- part of: step before `deployments-cicd`, which it defers deployment to.

### vercel-storage
- id: vercel:vercel-storage (source path: plugins/vercel/skills/vercel-storage/SKILL.md)
- description: "Vercel storage expert guidance — Blob, Edge Config, and Marketplace storage (Neon Postgres, Upstash Redis). Use when choosing, configuring, or using data storage with Vercel applications."
- use when: I'm choosing or wiring storage for a Vercel app (Blob, Edge Config, Neon, Upstash, Supabase) or migrating off `@vercel/postgres` or `@vercel/kv`.
- not for: `runtime-cache` (cache), `vercel-flags` (Edge Config for flags), `marketplace`, `env-vars`.
- needs: Vercel project; Marketplace installs create vendor accounts.
- side effects: Marketplace installs provision billed resources and inject env vars; examples upload/delete Blob files, write Redis data and run database schema push/seed commands.
- part of: standalone; dedicated route from `marketplace`; `bootstrap` chains to it.

### verification
- id: vercel:verification (source path: plugins/vercel/skills/verification/SKILL.md)
- description: "Full-story verification — infers what the user is building, then verifies the complete flow end-to-end: browser → API → data → response. Triggers on dev server start and 'why isn't this working' signals."
- use when: My dev server is up and the feature partly works or I want it checked end to end (UI -> API -> data -> response).
- not for: `agent-browser-verify` (visual only), `investigation-mode` (nothing loads at all), `observability` (logging gaps).
- needs: running dev server; `agent-browser`; `vercel logs` if deployed.
- side effects: writes browser screenshots and makes page requests; no explicit app-code or database mutation step.
- part of: entry router: infer user story -> evidence baseline -> walk data flow -> report; stops at first broken boundary or two consecutive no-signal layers; hands to `agent-browser-verify`, `investigation-mode`, `observability`.

### workflow
- id: vercel:workflow (source path: plugins/vercel/skills/workflow/SKILL.md)
- description: "Vercel Workflow DevKit (WDK) expert guidance. Use when building durable workflows, long-running tasks, API routes or agents that need pause/resume, retries, step-based execution, or crash-safe orchestration with Vercel Workflow."
- use when: I need durable long-running tasks: pause/resume, retries, human approval, step pipelines, `DurableAgent`, or a stuck workflow run.
- not for: `vercel-queues` (lower-level events), `cron-jobs`, `vercel-functions`, `eve`. Not for GitHub Actions or AWS Step Functions.
- needs: `workflow` package with its docs in `node_modules`; framework integration; Vercel backend for deployed inspection.
- side effects: `npx workflow cancel` mutates runs.
- part of: standalone; built on Queues; pairs with `ai-sdk`.
