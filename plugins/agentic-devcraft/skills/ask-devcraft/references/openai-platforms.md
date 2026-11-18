# openai/plugins: app building and vendor developer platforms
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Plugins from the OpenAI marketplace for building web, mobile, desktop and game apps, and for developing on a vendor's platform (hosting, databases, durable execution, payments, commerce, communications, design-to-code, video as code). Engineering workflow, security, review, CI, analytics and agent tooling are in openai-engineering.md.

Reading the records: a record heading is the host-visible skill name (the SKILL.md frontmatter `name`); `id` is `<plugin>:<skill directory>` followed by the SKILL.md path inside the source repository; `description` quotes the frontmatter description (whitespace collapsed), so compare it with an installed skill's description to establish that the installed copy is the one recorded here. Full records carry `use when`, `not for`, `needs`, `side effects` and `part of`; short records omit fields with nothing to state. A family marked router-delegated keeps its routing in the `router` line: when that router is installed, hand the task to it instead of re-deriving the route from the short records.

Families in order. Core-dev: `build-web-apps`, `build-ios-apps` (families/build-ios-apps.md), `build-macos-apps` (families/build-macos-apps.md), `expo` (families/expo.md), `test-android-apps`, `game-studio`, `vercel` (families/vercel.md), `cloudflare` (families/cloudflare.md), `supabase`, `temporal`, `stripe`, `shopify` (families/shopify.md), `twilio-developer-kit` (families/twilio-developer-kit.md), `zoom`. Adjacent: `figma` (families/figma.md), `product-design`, `magicpath`, `build-web-data-visualization`, `hyperframes`, `remotion`. Then pointers to the far families, the marketplace entries with no skills, and a note on openai/skills.

## Family: build-web-apps
- source path: `plugins/build-web-apps` (v0.1.2)
- manifest notes: Codex manifest only (`skills: ./skills/`); no MCP server, app connector, commands, hooks or auth policy. The two workflow skills name host tools the plugin does not supply: an installed `@imagegen` skill, `view_image`, the Browser plugin or in-app browser, Codex Plan-mode `request_user_input`, and `openai-developers:openai-platform-api-key` for AI features. Stripe and Supabase skills are advice only: no credentials, CLI or environment policy.
- router: none. Two entry points: `frontend-app-builder` (concept by Image Gen, extract spec, implement in slices, paired concept-vs-screenshot QA) and `frontend-testing-debugging` (Browser-first rendered fix loop, then `react-best-practices` after meaningful React/Next edits). The other four are consulted alone.
- development distance: core-dev
- disclosure: simple. Six skills: two workflows and four reference guides.
- name collisions (hosts list by frontmatter name, so qualify with the plugin): `stripe-best-practices` also in `stripe` (different, fuller text); `supabase-postgres-best-practices` also in `supabase` (near-identical); `react-best-practices` and `shadcn` also in `vercel` (react same body, shadcn different text). Directory names `shadcn-best-practices` and `supabase-best-practices` differ from the host-visible names.

### frontend-app-builder
- id: build-web-apps:frontend-app-builder (source path: plugins/build-web-apps/skills/frontend-app-builder/SKILL.md)
- description: "Use for new frontend applications, dashboards, games, creative websites, hero sections, and visually driven UI from scratch, or when the user explicitly asks for a redesign/restyle/modernization. Builds from clean, airy, high-taste, readable image-generated concept design with section-specific references, faithful implementation, and browser testing."
- use when: "Build a new dashboard, site, game or hero from scratch," or explicitly redesign, restyle or modernize a UI so the visual concept and the working code match.
- not for: `frontend-testing-debugging` (targeted bug or tweak on existing UI, no redesign); `react-best-practices` (performance); `swiftui-patterns` (native Mac).
- needs: Installed `@imagegen` unless the user opts out or the task is a small existing-design-system UI fix; `view_image`, Browser or in-app browser (Playwright fallback with stated reason); `request_user_input` for approval in Codex Plan mode.
- side effects: many image generations and browser runs, cost not quantified; writes assets and app code; no deploy. Overbroad for a bug fix.
- part of: entry point (concept, spec, slice implementation, paired fidelity QA); AI features route to the credential skill.

### frontend-testing-debugging
- id: build-web-apps:frontend-testing-debugging (source path: plugins/build-web-apps/skills/frontend-testing-debugging/SKILL.md)
- description: "Use when testing, debugging, or making targeted improvements to rendered frontend apps through the Build Web Apps or web dev plugin: local dev servers, UI regressions, interaction bugs, console errors, responsive layout, and visual QA. Check whether the Browser plugin is available and use it first when it is; otherwise use regular Playwright with the recorded reason."
- use when: "This local web page has a broken interaction, console error or responsive regression", or a targeted rendered improvement; also "use the Build Web Apps plugin" on an existing app.
- not for: `frontend-app-builder` (new design or redesign); `test-triage` (build-macos-apps, Xcode/SwiftPM tests). Playwright fallback after a Browser invocation failure needs prior user permission or a task explicitly permitting non-Browser validation (stricter than the builder's gate).
- needs: Repo or running URL, package scripts, Browser plugin skill (else Playwright, reason recorded).
- side effects: starts a local server, edits frontend code, drives the browser, writes temp scripts and screenshots outside the repo.
- part of: entry point of the rendered bug/QA loop; hands to `frontend-app-builder` for redesign and `react-best-practices` after React/Next edits.

### react-best-practices
- id: build-web-apps:react-best-practices (source path: plugins/build-web-apps/skills/react-best-practices/SKILL.md)
- description: "React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements."
- use when: "React or Next pages load slowly, requests serialize, bundles are large or re-renders are costly", or a component or data-fetching change needs a performance review. 64 rules, priority order waterfalls to bundle size to rendering.
- not for: `frontend-testing-debugging` (browser proof); `shadcn` (component APIs); `supabase-postgres-best-practices` (database). Also exposed as `vercel:react-best-practices`: same body, description framed as a post-edit checklist.
- needs: React/Next source.
- side effects: none; read-only guide, edits only when applying rules.
- part of: standalone; follow-on step in `frontend-testing-debugging`.

### shadcn
- id: build-web-apps:shadcn-best-practices (source path: plugins/build-web-apps/skills/shadcn-best-practices/SKILL.md)
- description: "Manages shadcn components and projects — adding, searching, fixing, debugging, styling, and composing UI. Provides project context, component docs, and usage examples. Applies when working with shadcn/ui, component registries, presets, --preset codes, or any project with a components.json file. Also triggers for "shadcn init", "create an app with --preset", or "switch to --preset"."
- use when: "Add or fix a shadcn dialog, form, sidebar or block," search a registry, init or switch a preset, or work in any project with `components.json`. Host-visible name is `shadcn`.
- not for: `react-best-practices` (React performance); `vercel:shadcn` (same name, entirely different text; the gates here come from this copy only).
- needs: Package runner (`npx`, `pnpm dlx`, `bunx`) with `shadcn@latest`; registry choice; network; a harness that runs its inline `!` shell block.
- side effects: writes component, config and CSS source; installs dependencies. Preset reinstall overwrites files; `--overwrite` needs explicit approval; registry must be chosen first.
- part of: standalone; optional specialist within frontend work.

### stripe-best-practices
- id: build-web-apps:stripe-best-practices (source path: plugins/build-web-apps/skills/stripe-best-practices/SKILL.md)
- description: "Guides Stripe integration decisions — API selection (Checkout Sessions vs PaymentIntents), Connect platform setup (Accounts v2, controller properties), billing/subscriptions, Treasury financial accounts, integration surfaces (Checkout, Payment Element), and migrating from deprecated Stripe APIs. Use when building, modifying, or reviewing any Stripe integration — including accepting payments, building marketplaces, integrating Stripe, processing payments, setting up subscriptions, or creating connected accounts."
- use when: "How should I take one-time payments, save a card, build a marketplace, bill subscriptions or migrate old Stripe APIs?" Reads the matching reference first (Checkout Sessions, Setup Intents, Accounts v2, Billing, Financial Accounts).
- not for: `stripe:stripe-best-practices` (same name; the `stripe` copy is longer, newer-labelled and adds Stripe CLI and restricted-key guidance; prefer it when both are exposed); `frontend-app-builder` (builds the purchase UI).
- needs: Nothing to read it; running an integration needs the user's Stripe account (no credential flow defined).
- side effects: none; advice and code only. No live-charge approval gate is defined.
- part of: standalone; routes to its own reference documents, not to sibling skills.

### supabase-postgres-best-practices
- id: build-web-apps:supabase-best-practices (source path: plugins/build-web-apps/skills/supabase-best-practices/SKILL.md)
- description: "Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations."
- use when: "A Postgres query is slow, indexes or schema need design, serverless connections overwhelm the database, RLS is costly or locking needs review." Applies to any Postgres, not only hosted Supabase.
- not for: `supabase:supabase-postgres-best-practices` (near-identical copy; this one cites a nonexistent `schema-partial-indexes.md`, the real file is `query-partial-indexes.md`); not Supabase project setup or auth.
- needs: SQL, schema or query plans.
- side effects: none; advice only. No environment or production-write policy: apply the user's own.
- part of: standalone database-performance reference.

## Family: build-ios-apps
- router: none. `ios-debugger-agent` is the build, launch and drive foundation that `ios-ettrace-performance` and `ios-memgraph-leaks` pair with; no fixed sequence.
- covers: iOS apps with Xcode and Simulator: SwiftUI authoring and refactoring, App Intents for system surfaces, building, running and driving the app on Simulator (bundled `xcodebuildmcp` MCP server), and three kinds of performance or leak evidence. Needs macOS, Xcode and Node/npx.
- development distance: core-dev
- skills (9): `ios-app-intents`, `ios-debugger-agent`, `ios-ettrace-performance`, `ios-memgraph-leaks`, `ios-simulator-browser`, `swiftui-liquid-glass`, `swiftui-performance-audit`, `swiftui-ui-patterns`, `swiftui-view-refactor`
- Full records: families/build-ios-apps.md

## Family: build-macos-apps
- router: none. Two entry points: `swiftui-patterns` (new scaffold) and `build-run-debug` (stop, build, launch fresh); `telemetry`, `window-management` and `liquid-glass` call back into `build-run-debug`.
- covers: Native macOS apps, shell-first (`xcodebuild`, `swift`, `codesign`): scaffold, launch, signing, shipping (packaging and notarization), tests, windows, glass, AppKit bridge. Out of scope: mobile simulator control, desktop UI automation, App Store Connect release management.
- development distance: core-dev
- skills (11): `appkit-interop`, `build-run-debug`, `liquid-glass`, `packaging-notarization`, `signing-entitlements`, `swiftpm-macos`, `swiftui-patterns`, `telemetry`, `test-triage`, `view-refactor`, `window-management`
- Full records: families/build-macos-apps.md

## Family: expo
- router: none. Skills are independent, with informal hints only (try Expo Go first; `expo-module` leads to `expo-dev-client`).
- covers: Expo and React Native apps: UI, networking, server routes, native modules, builds, release, upgrades; styling default is inline styles (`building-native-ui`); `expo-tailwind-setup` only when the user asks for Tailwind. Deployment, dev-client and API-route skills assume `eas-cli` and `eas login`.
- development distance: core-dev
- skills (13): `building-native-ui`, `expo-tailwind-setup`, `expo-ui-swift-ui`, `expo-ui-jetpack-compose`, `use-dom`, `native-data-fetching`, `expo-api-routes`, `expo-module`, `expo-dev-client`, `upgrading-expo`, `expo-deployment`, `expo-cicd-workflows`, `codex-expo-run-actions`
- Full records: families/expo.md

## Family: test-android-apps
- source path: `plugins/test-android-apps`
- manifest notes: v0.1.2, author OpenAI, capabilities Interactive and Read. Marketplace policy: products CODEX only, authentication ON_INSTALL. No MCP or connectors; bundled helper scripts (`ui_pick.py`, `ui_tree_summarize.py`, `simpleperf_hotspots.sh`, `heapprofd_reports.sh`). `android-emulator-qa` is vendored from `openai/skills-internal` (plugin.lock.json).
- router: none. `android-performance` composes with `android-emulator-qa` for device selection, build/install/launch, UI driving, screenshots, UI trees and logcat; it is not a router.
- development distance: core-dev
- disclosure: simple. Two skills, one functional QA and one profiling, with no router.

### android-emulator-qa
- id: test-android-apps:android-emulator-qa (source path: plugins/test-android-apps/skills/android-emulator-qa/SKILL.md)
- description: "Use when validating Android feature flows in an emulator with adb-driven launch, input, UI-tree inspection, screenshots, and logcat capture."
- use when: QA a feature flow or reproduce a UI bug in an Android emulator: launch the app, tap, swipe and type, inspect the UI tree, take screenshots and capture logcat.
- not for: `android-performance` (profiling and measurement, not functional QA).
- needs: `adb`, a booted emulator, an Android Gradle project to build and install, `python3` for the helper scripts.
- side effects: Builds and installs the app on the device, sends input events, clears logcat, and writes /tmp files.
- part of: standalone; also the driving step reused by `android-performance`. Tap coordinates come from the UI tree, not screenshots.

### android-performance
- id: test-android-apps:android-performance (source path: plugins/test-android-apps/skills/android-performance/SKILL.md)
- description: "Gather and interpret Android performance evidence on an adb target using Simpleperf CPU profiles, Perfetto or Compose traces, gfxinfo frame data, dumpsys meminfo snapshots, Java heap dumps, and native allocation traces. Use when asked to profile an Android app flow, find CPU-heavy functions, diagnose jank, capture startup or frame timing evidence, compare before/after performance, explain what code is taking time, or gather memory/leak profiling artifacts."
- use when: Profile an Android app flow: CPU-heavy functions, jank, startup or frame timing, memory or leaks, before/after comparison.
- not for: `android-emulator-qa` (functional repro and driving the flow).
- needs: An `adb` target (emulator or device); tools depend on the chosen capture (host Simpleperf, `trace_processor_shell`, optional `shark-cli`). CPU sampling usually needs a debuggable or profileable build; Perfetto or `gfxinfo` can be used when sampling is unavailable.
- side effects: Installs and drives the app on the device; writes trace and heap artifacts to a run-specific directory outside the skill folder.
- part of: composes with `android-emulator-qa` to drive the flow; not a router. Returns a report with caveats and the next smallest trace.

## Family: game-studio
- source path: `plugins/game-studio`
- manifest notes: Codex plugin manifest only (.codex-plugin, v0.1.2, OpenAI, MIT, category Developer Tools; marketplace products [CODEX]). No MCP, connector or auth. Ships architecture and starter references and three Python sprite utilities (not executed during curation). Asset generation depends on a separately installed `imagegen` skill.
- router: `game-studio`. Classifies first (2D default, plain TS/Vite 3D, React 3D, 3D asset pipeline, other engine, shared architecture/UI/QA), then routes immediately and does not stay in the loop. Default order: lock fantasy and player verbs, define loop and progression, choose track, define UI, choose asset workflow, playtest before calling anything production-ready. `web-game-foundations` is the short-lived pre-code architecture step.
- development distance: core-dev
- disclosure: router-delegated. `game-studio` covers all nine skills with explicit exits; records stay one-liners and the distinctions that decide routing (2D vs plain 3D vs React 3D) are in the use-when lines.

### game-studio
- id: game-studio:game-studio (source path: plugins/game-studio/skills/game-studio/SKILL.md)
- description: "Route early browser-game work. Use when the user needs stack selection and workflow planning across design, implementation, assets, and playtesting before moving to a specialist skill."
- use when: Entry router for 'help me build a browser game' with no chosen stack, or a request spanning runtime, HUD, assets and QA. Classifies, then routes to the specialist. Phaser is the 2D default; 2D is stronger than 3D here.

### web-game-foundations
- id: game-studio:web-game-foundations (source path: plugins/game-studio/skills/web-game-foundations/SKILL.md)
- description: "Set browser-game architecture before implementation. Use when the user needs engine choice, simulation and render boundaries, input model, asset organization, or save/debug/performance strategy."
- use when: A game has no agreed engine, simulation owner, input map, save boundary or asset policy; produces a pre-code architecture checklist, then hands off.

### phaser-2d-game
- id: game-studio:phaser-2d-game (source path: plugins/game-studio/skills/phaser-2d-game/SKILL.md)
- description: "Implement 2D browser games with Phaser. Use when the user wants a Phaser, TypeScript, and Vite stack for scenes, gameplay systems, cameras, sprite animation, and DOM-overlay HUD patterns."
- use when: Build a sprite or tile-based 2D game (tactics, top-down, platformer, 2D combat) in Phaser + TypeScript + Vite. Default for common browser-game requests.

### three-webgl-game
- id: game-studio:three-webgl-game (source path: plugins/game-studio/skills/three-webgl-game/SKILL.md)
- description: "Implement browser-game runtimes with plain Three.js. Use when the user wants imperative scene control in TypeScript or Vite with GLB assets, loaders, physics, and low-level WebGL debugging."
- use when: 3D game in plain TypeScript/Vite with direct control of Three.js camera, render loop and Rapier physics. Not for React apps (use react-three-fiber-game) or explicit Babylon.js/PlayCanvas requests.

### react-three-fiber-game
- id: game-studio:react-three-fiber-game (source path: plugins/game-studio/skills/react-three-fiber-game/SKILL.md)
- description: "Build React-hosted 3D browser games with React Three Fiber. Use when the user wants pmndrs-based scene composition, shared React state, and 3D HUD integration inside a React app."
- use when: Embed a 3D game, configurator or editor in a React product with shared UI state. Not for non-React projects; React presence alone does not justify it.

### game-ui-frontend
- id: game-studio:game-ui-frontend (source path: plugins/game-studio/skills/game-ui-frontend/SKILL.md)
- description: "Design UI surfaces for browser games. Use when the user asks for HUDs, menus, overlays, responsive layouts, or visual direction that must protect the playfield."
- use when: HUDs, menus or overlays that obscure play or fight camera controls; DOM UI with visual direction first. Needs an existing game and viewpoint.

### sprite-pipeline
- id: game-studio:sprite-pipeline (source path: plugins/game-studio/skills/sprite-pipeline/SKILL.md)
- description: "Generate and normalize 2D sprite animations. Use when the user asks for full-strip generation from approved source frames, consistent anchor and scale normalization, or preview assets for browser-game animation."
- use when: Animation frames for an already approved 2D character without silhouette, size or palette drift.
- needs: An approved seed frame, a separately installed imagegen skill, Python 3.
- side effects: writes local image files; image generation goes through imagegen

### web-3d-asset-pipeline
- id: game-studio:web-3d-asset-pipeline (source path: plugins/game-studio/skills/web-3d-asset-pipeline/SKILL.md)
- description: "Prepare and optimize browser-game 3D assets. Use when the user asks for GLB or glTF shipping work, including Blender cleanup and export, collision or LOD setup, compression, texture packaging, and runtime validation."
- use when: 3D models load slowly or arrive with wrong scale, pivots or materials; produces shipping-ready GLB/glTF, LODs, collision proxies. Engine-agnostic.
- needs: Source models, a DCC tool such as Blender, glTF Transform.
- side effects: writes local asset files

### game-playtest
- id: game-studio:game-playtest (source path: plugins/game-studio/skills/game-playtest/SKILL.md)
- description: "Run browser-game playtests and frontend QA. Use when the user asks for smoke tests, screenshot-based verification, browser automation, HUD or overlay review, or structured issue-finding in a browser game."
- use when: Does my browser game boot, respond to controls, survive scene changes and stay readable on phones; also HUD regressions and unexplained 3D frame cost. Reports findings; does not implement.
- needs: A runnable game and browser access; screenshots are mandatory for canvas/WebGL games.

## Family: vercel
- router: none for the family. Partial entry skills with sequences: `knowledge-update` -> `marketplace` (any external service), `bootstrap` (first-run setup), and the debug ladder `verification` / `investigation-mode` / `agent-browser-verify` (browser smoke check -> end-to-end walk -> stuck-app triage).
- covers: Vercel and Next.js development: setup, AI features, caching, compute, security, deploy, debugging. Most skills need the `vercel` CLI logged in with a linked project. `react-best-practices` and `shadcn` share their names with `build-web-apps` skills.
- development distance: core-dev
- skills (54): `agent-browser`, `agent-browser-verify`, `ai-elements`, `ai-gateway`, `ai-generation-persistence`, `ai-sdk`, `auth`, `bootstrap`, `cdn-caching`, `chat-sdk`, `cms`, `cron-jobs`, `deployments-cicd`, `email`, `env-vars`, `eve`, `geist`, `geistdocs`, `investigation-mode`, `json-render`, `knowledge-update`, `marketplace`, `micro`, `microfrontends`, `ncc`, `next-cache-components`, `next-forge`, `next-upgrade`, `nextjs`, `observability`, `payments`, `react-best-practices`, `routing-middleware`, `runtime-cache`, `satori`, `shadcn`, `sign-in-with-vercel`, `swr`, `turbopack`, `turborepo`, `v0-dev`, `vercel-agent`, `vercel-api`, `vercel-cli`, `vercel-connect`, `vercel-firewall`, `vercel-flags`, `vercel-functions`, `vercel-queues`, `vercel-sandbox`, `vercel-services`, `vercel-storage`, `verification`, `workflow`
- Full records: families/vercel.md

## Family: cloudflare
- router: `cloudflare` is a product-selection router only: eight decision trees that load its own references, not the eight sibling skills.
- covers: Cloudflare developer platform: product choice, CLI operations (`wrangler`), Durable Objects, agents, MCP servers, sandboxes, performance audit, Workers code review. Bundles the `cloudflare-api` MCP server for account administration. `agents-sdk` shares its host-visible name with OpenAI's `agents-sdk`.
- development distance: core-dev
- skills (9): `cloudflare`, `agents-sdk`, `building-ai-agent-on-cloudflare`, `building-mcp-server-on-cloudflare`, `durable-objects`, `sandbox-sdk`, `web-perf`, `workers-best-practices`, `wrangler`
- Full records: families/cloudflare.md

## Family: supabase
- source path: `plugins/supabase`
- manifest notes: v1.0.0 (changelog says 0.1.4). Marketplace policy: no product restriction, authentication ON_INSTALL. Remote HTTP MCP server `supabase` (`https://mcp.supabase.com/mcp`) plus a `supabase` app connector. The `supabase` skill says the MCP server uses OAuth 2.1: the user completes browser auth, then reloads the session. The plugin description advertises edge-function deploys, development branches and realtime logs; those come from the MCP server, no skill covers them.
- router: none. `supabase` claims every Supabase task; `supabase-postgres-best-practices` is a separate Postgres performance rule index.
- development distance: core-dev
- disclosure: simple. Two skills, one broad entry and one advisory index.
- name collisions: `supabase-postgres-best-practices` is also a skill name in `build-web-apps` (near-identical copy); hosts list by frontmatter name, so qualify with the plugin.

### supabase
- id: supabase:supabase (source path: plugins/supabase/skills/supabase/SKILL.md)
- description: "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector)."
- use when: Any Supabase task: supabase-js or @supabase/ssr in a framework, login/session/JWT problems, RLS or Data API exposure, schema changes and migrations, security audits, CLI or MCP trouble, extensions.
- not for: `supabase-postgres-best-practices` (Postgres query, index and schema performance, on any Postgres).
- needs: Tools depend on the task: Supabase CLI (`db query` needs v2.79.0+, `db advisors` v2.81.3+), MCP with OAuth 2.1, or supported fallbacks; CLI and MCP are not both mandatory. Network access to the Supabase docs and changelog.
- side effects: Runs SQL against the project database; creates migration files with `supabase migration new` or captures schema changes with `supabase db pull`; verifies each fix with a test query. May create `.mcp.json` during setup; package installation guidance requires pinned versions and committed lockfiles.
- part of: standalone entry for all Supabase work; no hand-off.

### supabase-postgres-best-practices
- id: supabase:supabase-postgres-best-practices (source path: plugins/supabase/skills/supabase-postgres-best-practices/SKILL.md)
- description: "Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations."
- use when: Write, review or optimize Postgres queries, schemas, indexes, connection pooling, locking or RLS performance.
- not for: `supabase` (platform correctness: auth, RLS correctness, CLI and MCP workflow).
- needs: nothing beyond the repo.
- side effects: none; advisory index of eight rule categories whose detail lives in reference files.
- part of: standalone; combines with `supabase` for an RLS review.

## Family: temporal
- source path: `plugins/temporal`
- manifest notes: v0.4.0, author Temporal, capabilities empty. Marketplace policy: no product restriction, authentication ON_INSTALL. No MCP or connectors; skills bundle scripts (`temporal-cloud-setup/scripts/provision.sh`) and large reference trees. `temporal-cloud-setup`, `temporal-ops` and `temporal-serverless` set `disable-model-invocation: true` (and `allow_implicit_invocation: false`), so they run only when the user invokes them explicitly; `temporal-developer` has no such flag. Hand-offs name `skill-temporal-workertuning`, `skill-temporal-cli` and `temporal-getting-started`, none of which are in this plugin.
- router: none. Skills are siblings: `temporal-developer` (SDK code), `temporal-ops` (running environments), `temporal-serverless` (Lambda workers), `temporal-cloud-setup` (first-time Cloud onboarding).
- development distance: core-dev
- disclosure: simple. Four skills with clearly separated scenarios and heavy detail already in the skills' own reference trees.

### temporal-developer
- id: temporal:temporal-developer (source path: plugins/temporal/skills/temporal-developer/SKILL.md)
- description: "Develop, debug, and manage Temporal applications across Python, TypeScript, Go, Java, .NET, Ruby, and Rust. Use when the user is building workflows, activities, or workers with a Temporal SDK, debugging issues like non-determinism errors, stuck workflows, or activity retries, using Temporal CLI, Temporal Server, or Temporal Cloud, or working with durable execution concepts like signals, queries, heartbeats, versioning, continue-as-new, child workflows, or saga patterns. Also use when the user mentions "run a Temporal workflow from the CLI", "start a dev server", "run temporal server start-dev", "temporal workflow start", "temporal workflow execute", "temporal workflow signal", "temporal workflow query", "temporal workflow update"."
- use when: I am building or debugging Temporal workflows, activities and workers with an SDK: non-determinism errors, stuck workflows, retries, signals, queries, versioning, saga, or running the local dev server.
- not for: `temporal-ops` (administering or diagnosing a running Cloud or self-hosted environment through the CLI); `temporal-serverless` (Lambda-hosted workers).
- needs: The `temporal` CLI and an SDK (Python, TypeScript, Go, Java, .NET, Ruby; Rust in public preview).
- side effects: Can install the Temporal CLI if missing and guide application-code changes and dev-server/Workflow CLI operations through references; it declares no read-only boundary.
- part of: standalone entry for SDK work; reads the language getting-started reference first.

### temporal-ops
- id: temporal:temporal-ops (source path: plugins/temporal/skills/temporal-ops/SKILL.md)
- description: "Administer and diagnose running Temporal Cloud or self-hosted Temporal Server environments via CLI (temporal, tcld) — not SDK code. Operations: namespace CRUD, Cloud capacity/APS, API-key rotation, mTLS cert rotation, workflow health, batch cancel/terminate/reset, export, search attributes, Ops API, billing, audit logs, Terraform, SAML/SCIM, migration. Diagnosis: bottom-up triage of stuck workflows, non-determinism, worker-health, task-queue problems, HA failover, payload size limits, performance bottlenecks, missed schedules. Do NOT trigger for generic TLS/gRPC errors unrelated to Temporal, writing application code (temporal-developer), or worker tuning/sizing (temporal-workertuning)."
- use when: Administer or diagnose a running Temporal Cloud or self-hosted environment through the CLI: namespaces, API keys, certs, batch operations, stuck workflows, connectivity, no pollers, failover.
- not for: `temporal-developer` (SDK code); `temporal-serverless` (Lambda workers); `temporal-cloud-setup` (greenfield onboarding).
- needs: `temporal` CLI; `tcld` after `tcld login` for Cloud; real credentials and a target environment. Explicit invocation only (`disable-model-invocation`).
- side effects: Can be production-impacting: namespace delete, failover, API-key delete, batch terminate. It proposes these with evidence and runs each only after per-command, per-target approval. Its auth triage greps the environment for `TEMPORAL_API_KEY`, which can print the secret.
- part of: standalone; hands off to `temporal-developer` for code. Diagnosis ends with a confidence score.

### temporal-cloud-setup
- id: temporal:temporal-cloud-setup (source path: plugins/temporal/skills/temporal-cloud-setup/SKILL.md)
- description: "Set up Temporal Cloud and run a sample Workflow on it for the user, doing the work end to end. Use when the user wants to set up Temporal Cloud, get started on Temporal Cloud, install the unified Temporal CLI (prerelease cloud-cli), create a Cloud namespace or API key, clone a money-transfer sample app, write the client config TOML, or connect a local Worker to Temporal Cloud and run a sample Workflow. This is the Cloud setup path, not the local learning path (see temporal-getting-started). Covers Python, TypeScript, Go, Java, .NET, and Ruby SDKs."
- use when: Get me started on Temporal Cloud: install the CLI, create a namespace and API key, run a sample Workflow and see durable execution.
- not for: `temporal-developer` (SDK code or local dev server); `temporal-ops` (existing namespaces, keys and certs).
- needs: A local shell with outbound network (Codex default sandbox does not qualify); a Temporal Cloud account with browser login; `git`, an SDK toolchain; Homebrew for the automatic CLI install. Explicit invocation only.
- side effects: Creates a BILLABLE Cloud namespace and an API key (expires in about 25 hours); installs or updates the prerelease CLI; writes `temporal.toml`; clones a sample repo; runs a Worker. Discloses each step; login, run and failure injection need a go-ahead.
- part of: standalone four-phase wizard; offers no teardown.

### temporal-serverless
- id: temporal:temporal-serverless (source path: plugins/temporal/skills/temporal-serverless/SKILL.md)
- description: "Deploy and operate Temporal Workers on serverless compute (AWS Lambda) driven by the Worker Controller Instance (WCI). Use when the user mentions: "serverless worker", "Temporal serverless", "Worker Controller Instance", "WCI", "deploy Temporal worker on Lambda", "Lambda packaging", "Lambda timeout", "WCI inspection", "CloudFormation Temporal"."
- use when: Deploy or operate Temporal Workers on AWS Lambda through the Worker Controller Instance, or troubleshoot a serverless Worker that is not picking up Tasks.
- not for: `temporal-developer` (general SDK code); `temporal-ops` (Cloud admin).
- needs: AWS credentials (never collected in chat); a Temporal Cloud namespace on AWS or self-hosted; `tcld` and the `temporal` CLI; a Go, Python or TypeScript SDK. Explicit invocation only; Public Preview; AWS Lambda only.
- side effects: Creates billable AWS resources (Lambda, IAM roles, CloudFormation stacks, log groups) and Worker Deployment Versions after the user approves the exact resource list.
- part of: standalone eight-step deployment sequence; offers teardown only on request.

## Family: stripe
- source path: `plugins/stripe` (Codex plugin v7.0.0, author Stripe, category Finance). 7 skills.
- manifest notes: Codex manifest only (no Claude/Cursor manifest, hooks, commands or subagents). HTTP MCP server `stripe` at https://mcp.stripe.com and an app connector, with no auth fields declared; the connector (create payment links, refunds, customers) is separate from the skills, and the CLI authenticates separately. Several skills use Claude-style tool names (`Bash`, `Read`, `Write`, `WebFetch`, `AskUserQuestion`, `Skill`); stripe-projects needs a dynamically installed skill at `.claude/skills/stripe-projects-cli`. Install/auth gates: stripe-best-practices defaults to restricted keys and `stripe whoami --format json` (never `stripe config --list`); stripe-projects accepts terms with `--accept-tos --yes`; stripe-directory asks before any payment. Source conflicts, settled: stripe-apps mandates WebFetch of its canonical docs while stripe-docs says use `stripe docs` for any docs.stripe.com page: read them with `stripe docs`, WebFetch only if the CLI lacks `docs`. stripe-apps publishing text uses `stripe config --list`, which stripe-best-practices forbids: use `stripe whoami --format json`. API default `2026-07-29.dahlia` is a source snapshot.
- router: none for the family. stripe-best-practices is a domain router for integrations only (one-time payments -> Checkout Sessions; custom form -> Checkout Sessions + Payment Element; save method -> SetupIntents; marketplace -> Accounts v2; new usage billing -> Metronome; recurring -> Billing + Checkout; tax -> Stripe Tax + Registrations; financial accounts -> v2); read the matching reference first. connect-recommend runs business discovery, fee economics and a compatibility check before presenting a Connect plan.
- development distance: core-dev (payment integration, Dashboard apps, API upgrades); stripe-directory and stripe-projects are adjacent (vendor discovery and provisioning infrastructure).
- disclosure: simple; seven skills from one vendor with clear one-line distinctions.
- name collisions: `stripe-best-practices` is also a skill name in `build-web-apps` (shorter text without the Stripe CLI and restricted-key guidance); hosts list by frontmatter name, so qualify with the plugin and prefer this plugin's copy when both are exposed.

### connect-recommend
- id: stripe:connect-recommend (source path: plugins/stripe/skills/connect-recommend/SKILL.md)
- description: "Use this skill when the user asks about Stripe Connect configuration, charge patterns, Dashboard access, or how to get started with Connect, is building a marketplace, platform, multi-vendor store, gig platform, or subscription platform, needs to pay out sellers, vendors, or providers, mentions split payments, revenue sharing, multi-party payments, or similar payment distribution concepts, provides a company URL or business description for a recommendation, builds SaaS that routes money between parties (for example, POS, booking, invoicing — not operational SaaS without payment routing), asks about onboarding or KYC for merchants, sellers, and vendors, mentions connected account Dashboard or responsibility configurations, or asks about payment flows, white-label payments, or embedded payments."
- use when: A marketplace, platform or multi-vendor/gig/SaaS-with-payouts needs a decision on who charges buyers, pays sellers, owns disputes and fees, handles KYC and what Dashboard access sellers get; a company URL or description suffices.
- not for: stripe-best-practices (implementing a configuration already decided); stripe-apps (Dashboard extension, not funds flow). SaaS with no money routed between parties is out of scope.
- needs: business info or answers; web search/fetch, repo read, interactive question tool; no credentials.
- side effects: none; recommends only (optional `connect-recommend-plan.md` on request).
- part of: entry for the Connect recommendation sequence; final option hands the plan to a coding agent; names `connect-build`, which is not bundled.

### stripe-apps
- id: stripe:stripe-apps (source path: plugins/stripe/skills/stripe-apps/SKILL.md)
- description: "Use when building, modifying, or reviewing a Stripe App — or when the user describes something that implies one (e.g. "add a panel to the customer page", "customize my Stripe Dashboard", "react to Stripe events from my app", "connect my service to Stripe without sharing API keys"). Covers the full app development workflow (scaffold, preview, upload, versioning), UI extension architecture (sandboxed iframe, Stripe UI toolkit, viewports), extension types (UI extensions, backend-only, extension interfaces, embedded apps), authentication (platform keys, OAuth, restricted API keys), stripe-app.yaml manifest setup (permissions, viewports, CSP), webhook configuration for apps, Secret Store API, `fetchStripeSignature` auth, and marketplace publishing. Use when the user mentions Stripe Apps, UI extensions, @stripe/ui-extension-sdk, stripe-app.yaml, Dashboard extensions, or customizing the Stripe Dashboard."
- use when: Build or review a Stripe App: a panel on the customer or payment page, reacting to Stripe events, or letting merchants connect without sharing API keys (`stripe-app.yaml`).
- not for: stripe-best-practices (payments in your own product); connect-recommend (marketplace funds flow).
- needs: Stripe CLI 1.25.0+ (apps, generate plugins), pnpm, Stripe login, browser (not Safari); self-hosted backend if the app has one.
- side effects: installs CLI plugins, uploads app versions, installs into test and live accounts, optional marketplace submission; generated backend may mutate Stripe.
- part of: entry for the full app-building sequence (discovery, scaffold, build, test, upload, install).

### stripe-best-practices
- id: stripe:stripe-best-practices (source path: plugins/stripe/skills/stripe-best-practices/SKILL.md)
- description: "Guides Stripe integration decisions across API selection (Checkout Sessions vs PaymentIntents), Connect platform setup (Accounts v2, controller properties), billing/subscriptions, tax and registrations (Stripe Tax, automatic_tax, product tax codes), Treasury financial accounts, integration options (Checkout, Payment Element), migrating from deprecated Stripe APIs, and security best practices (API key management, restricted keys, webhooks, OAuth). Use when building, modifying, or reviewing any Stripe integration, including accepting payments, building marketplaces, integrating Stripe, processing payments, setting up subscriptions, collecting sales tax, VAT, or GST, creating connected accounts, or implementing secure key handling."
- use when: Build, change or review a Stripe integration: one-time payments, subscriptions or metered billing, Connect setup, sales tax/VAT, financial accounts, deprecated-API migration, key and webhook security.
- not for: connect-recommend (open marketplace configuration decisions); upgrade-stripe (version bump); stripe-docs (lookup only); stripe-projects (generic infrastructure).
- needs: Stripe credentials at runtime (restricted key preferred); optional CLI sandbox: after `stripe sandbox create`, no MCP until `stripe sandbox claim`.
- side effects: optional CLI installation and sandbox/key provisioning; implementation may take payments, change tax collection or rotate keys. Never auto-creates tax registrations.
- part of: entry domain router (reference per domain); standalone guardrail.

### stripe-directory
- id: stripe:stripe-directory (source path: plugins/stripe/skills/stripe-directory/SKILL.md)
- description: "Use when the user wants to find businesses, software, service providers, or partners for a specific industry, workflow, pain point, capability, or job to be done. Also use when the agent needs to programmatically purchase or consume a service. Use Stripe Directory to build a short relevant shortlist, even if the user does not mention Stripe Directory explicitly."
- use when: Find vendors, software or partners for an industry or job, or buy a callable API service (HTTP 402) directly.
- not for: stripe-projects (provisions catalog infrastructure and credentials); ucp (merchant products and carts).
- needs: Stripe CLI with `directory`. Buying: a payer tool (Link CLI, Tempo, Privy Agent Wallet CLI, debug-only mppx) and its account.
- side effects: search is read-only; missing payer installation requires confirmation; the buy branch moves money only after the payer choice and a shown price get explicit approval.
- part of: standalone; internal purchase sequence.

### stripe-docs
- id: stripe:stripe-docs (source path: plugins/stripe/skills/stripe-docs/SKILL.md)
- description: "Use when the user or agent needs to read, search, or look up Stripe documentation or API reference. Prefer this over curl or WebFetch for any docs.stripe.com content."
- use when: Look up a Stripe docs page, search "payment intents", or inspect an API resource, method or event type.
- not for: stripe-best-practices (what to build); upgrade-stripe (migration). stripe-apps mandates WebFetch for the same pages: use `stripe docs` when the CLI has it, WebFetch otherwise; the docs get read before code either way.
- needs: Stripe CLI exposing `docs` (`Bash(stripe docs *)`).
- side effects: none; read-only.
- part of: standalone utility.

### stripe-projects
- id: stripe:stripe-projects (source path: plugins/stripe/skills/stripe-projects/SKILL.md)
- description: "Use when the user wants to provision infrastructure or third-party services using Stripe Projects. Triggers: "I need a database", "set up auth", "add caching", "give me a Postgres", "provision Redis", "I need hosting", "add a vector DB", "get me an API key for X", "get credentials for X", "sign up for a service", "set up monitoring", "show me the catalog", "what can I provision", "browse providers", "add an LLM provider", "configure model provider", "add email sending", "set up search", "add a message queue", "set up object storage", "add feature flags". Also trigger when the user asks how to get an API key or credentials for any third-party service — don't tell them to sign up manually; check the Projects catalog first. Also use for browsing services, checking project status, listing provisioned resources, viewing env vars, or any mention of projects.dev or adding/provisioning/connecting a cloud service."
- use when: "Give me a Postgres/Redis/hosting/auth", "get an API key for provider X", add LLM/email/storage/search infrastructure, or inspect project resources and env bindings.
- not for: stripe-directory (compare and buy services); stripe-best-practices (Stripe payment integration, not cloud signup).
- needs: Stripe CLI 1.40.0+, Projects plugin, eligible account, possible browser/provider OAuth. Host needs a `Skill`-style tool and `.claude/skills/stripe-projects-cli`, not bundled.
- side effects: init runs `--accept-tos --yes`; installs CLI/plugins and the local skill; writes `.projects/` and `.env`; sets/deletes project variables and changes env bindings; can provision paid cloud resources via the downstream skill.
- part of: entry; hands off to the stripe-projects-cli skill that init installs.

### upgrade-stripe
- id: stripe:upgrade-stripe (source path: plugins/stripe/skills/upgrade-stripe/SKILL.md)
- description: "Guide for upgrading Stripe API versions and SDKs"
- use when: Move an existing integration to a newer Stripe API version, server SDK, Stripe.js or mobile SDK, or understand migration risks.
- not for: stripe-best-practices (choosing APIs); stripe-docs (lookup only).
- needs: current and target versions, package manifests, changelog access; test credentials for per-request version testing.
- side effects: edits dependencies and source; makes test API calls; no Dashboard cutover step.
- part of: standalone migration workflow.

## Family: shopify
- router: none for the family. Entries: `shopify-onboarding-dev` (developer setup), `shopify-onboarding-merchant` (store owners), `shopify-dev` (docs fallback only when no API-specific skill applies); precedence rules pick the API and UI-surface skill.
- covers: Shopify apps, themes, storefronts, Functions and extensions: API authoring, UI surfaces, backend Functions, CLI execution. Outliers `shopify-onboarding-merchant` and `ucp` are merchant and shopper operations that can write to live stores or place orders.
- development distance: core-dev
- skills (20): `shopify-admin`, `shopify-app-store-review`, `shopify-custom-data`, `shopify-customer`, `shopify-dev`, `shopify-functions`, `shopify-hydrogen`, `shopify-liquid`, `shopify-onboarding-dev`, `shopify-onboarding-merchant`, `shopify-partner`, `shopify-payments-apps`, `shopify-polaris-admin-extensions`, `shopify-polaris-app-home`, `shopify-polaris-checkout-extensions`, `shopify-polaris-customer-account-extensions`, `shopify-pos-ui`, `shopify-storefront-graphql`, `shopify-use-shopify-cli`, `ucp`
- Full records: families/shopify.md

## Family: twilio-developer-kit
- router: none formal. Eight planner skills act as sub-entry points by outcome (they qualify, then name product skills); a specific request goes straight to the product skill.
- covers: Adds messaging, voice, verification, email and AI-agent integrations to application code with Twilio and SendGrid, plus compliance and security setup. Email splits by credential (Twilio Email versus SendGrid); ask when unclear.
- development distance: core-dev
- skills (55): `twilio-messaging-overview`, `twilio-messaging-channel-advisor`, `twilio-marketing-promotions-advisor`, `twilio-notifications-alerts-advisor`, `twilio-identity-verification-advisor`, `twilio-customer-support-architect`, `twilio-ai-agent-architect`, `twilio-agent-augmentation-architect`, `twilio-account-setup`, `twilio-numbers-senders`, `twilio-regulatory-compliance-bundles`, `twilio-compliance-onboarding`, `twilio-isv-sms-best-practices`, `twilio-compliance-traffic`, `twilio-iam-auth-setup`, `twilio-security-api-auth`, `twilio-organizations-setup`, `twilio-security-hardening`, `twilio-security-compliance-hipaa`, `twilio-send-message`, `twilio-sms-send-message`, `twilio-whatsapp-send-message`, `twilio-whatsapp-manage-senders`, `twilio-rcs-messaging`, `twilio-content-template-builder`, `twilio-messaging-services`, `twilio-messaging-webhooks`, `twilio-conversations-classic-api`, `twilio-email-send`, `twilio-email-deliverability-advisor`, `twilio-sendgrid-account-setup`, `twilio-sendgrid-email-send`, `twilio-sendgrid-deliverability-advisor`, `twilio-sendgrid-email-settings`, `twilio-sendgrid-engagement-quality`, `twilio-sendgrid-inbound-parse`, `twilio-sendgrid-suppressions`, `twilio-sendgrid-webhooks`, `twilio-verify-send-otp`, `twilio-lookup-phone-intelligence`, `twilio-voice-twiml`, `twilio-voice-outbound-calls`, `twilio-voice-conversation-relay`, `twilio-call-recordings`, `twilio-conference-calls`, `twilio-taskrouter-routing`, `twilio-agent-connect`, `twilio-customer-memory`, `twilio-conversation-orchestrator`, `conversation-intelligence`, `twilio-enterprise-knowledge`, `twilio-debugging-observability`, `twilio-webhook-architecture`, `twilio-reliability-patterns`, `twilio-cli-reference`
- Full records: families/twilio-developer-kit.md

## Family: zoom
- router: `start` is the default entry but reaches only five skills (plan-zoom-product, setup-zoom-oauth, build-zoom-meeting-app, build-zoom-bot, debug-zoom); `plan-zoom-product` (interview) and `choose-zoom-approach` (decision table) cover the rest, and `plan-zoom-integration` phases the delivery. Router-delegated: three routers plus parent skills own the routing, so the records stay one-liners.
- covers: Zoom platform development: REST, webhooks and WebSockets, Meeting SDK, Video SDK, Apps SDK, RTMS, Team Chat, Phone, Contact Center, Virtual Agent, OAuth setup and debugging. Codex-only packaging; every skill runs only when the user names it. Gate: a real Zoom meeting never goes to Video SDK and a custom session never to Meeting SDK.
- development distance: core-dev (only relevant when the task involves Zoom)
- skills (53): `start`, `plan-zoom-product`, `choose-zoom-approach`, `plan-zoom-integration`, `zoom-general`, `setup-zoom-oauth`, `zoom-oauth`, `build-zoom-rest-api-app`, `rivet-sdk`, `setup-zoom-webhooks`, `setup-zoom-websockets`, `build-zoom-team-chat-app`, `build-zoom-meeting-app`, `build-zoom-meeting-sdk-app`, `zoom-meeting-sdk-web`, `zoom-meeting-sdk-web-client-view`, `zoom-meeting-sdk-web-component-view`, `zoom-meeting-sdk-android`, `zoom-meeting-sdk-ios`, `zoom-meeting-sdk-macos`, `zoom-meeting-sdk-windows`, `zoom-meeting-sdk-linux`, `zoom-meeting-sdk-electron`, `zoom-meeting-sdk-react-native`, `zoom-meeting-sdk-unreal`, `build-zoom-video-sdk-app`, `ui-toolkit`, `probe-sdk`, `zoom-video-sdk-web`, `zoom-video-sdk-windows`, `zoom-video-sdk-linux`, `zoom-video-sdk-flutter`, `zoom-video-sdk-react-native`, `zoom-video-sdk-android`, `zoom-video-sdk-ios`, `zoom-video-sdk-macos`, `zoom-video-sdk-unity`, `zoom-apps-sdk`, `build-zoom-bot`, `zoom-rtms`, `scribe`, `build-zoom-phone-integration`, `build-zoom-contact-center-app`, `zoom-contact-center-web`, `zoom-contact-center-android`, `zoom-contact-center-ios`, `build-zoom-virtual-agent`, `zoom-virtual-agent-web`, `zoom-virtual-agent-android`, `zoom-virtual-agent-ios`, `zoom-cobrowse-sdk`, `debug-zoom`, `debug-zoom-integration`
- Full records: families/zoom.md

## Family: figma
- router: none single router. Mandatory-prerequisite skills each gate one Figma MCP tool (`figma-use` before every `use_figma` call, `figma-design-to-code` before `get_design_context`); `figma-swiftui` routes by direction.
- covers: Design-to-code and code-to-design through the Figma MCP server (OAuth): Figma to code, motion, SwiftUI in both directions, Code Connect, and editing Design, FigJam and Slides files. Most skills edit a Figma file rather than the repo.
- development distance: adjacent
- skills (12): `figma-design-to-code`, `figma-implement-motion`, `figma-swiftui`, `figma-code-connect`, `figma-use`, `figma-generate-design`, `figma-generate-library`, `figma-create-new-file`, `figma-generate-diagram`, `figma-use-figjam`, `figma-use-slides`, `figma-use-motion`
- Full records: families/figma.md

## Family: product-design
- source path: `plugins/product-design` (v0.1.52)
- manifest notes: Codex-only manifest (`.codex-plugin/plugin.json`); no MCP server, app connector, hooks or commands. Written for Codex Desktop (in-app browser) and ChatGPT Work Mode (cloud browser); standard ChatGPT chat is refused. Proprietary license; category Creativity. Bundles Sites-ready `templates/prototype` (Vite/React) and `templates/mobile-app` (protected phone-frame runtime). Uses but does not bundle Browser, Figma, Image Gen and Sites/Vercel tools. Persistent state goes to `$CODEX_HOME/state/plugins/product-design/`. No auth policy declared.
- router: `index` (routes only, does no focused work). Always loads `user-context` and runs its preflight first when local shell access is available. Audit/critique requests go straight to `audit`, skipping `get-context`. A new UI with no visual target goes `get-context` -> `ideate` (exactly three Image Gen options, then waits for a pick; "No Visual Target, No Build"). A selected target goes `image-to-code` -> `design-qa` (blocking) -> handoff -> one `share` nudge. "Like <URL>" means redesign: `get-context` -> screenshot the site -> `ideate`. `design-qa` is internal only. Setup-only requests may save supplied context but do not inspect the workspace, install, scaffold, generate images, audit or implement.
- settled order: assume `get-context` plays back the brief before `url-to-code` executes (index L139 and get-context L38; index L42 says load `url-to-code` directly and url-to-code never mentions `get-context`). The playback writes nothing and does not wait when target and outcome are clear.
- development distance: adjacent (design-to-code prototypes; not ordinary implementation, which the router says it does not take unless asked)
- disclosure: router-delegated. `index` owns the sequence and every gate, so records stay one-liners for matching.

### index
- id: product-design:index (source path: plugins/product-design/skills/index/SKILL.md)
- description: "Use when Product Design is explicitly invoked, or when the user's main goal is to explore a design, research UX, audit or critique a flow, faithfully clone a visual source, check a built design, or share a prototype. Do not use Product Design for ordinary implementation unless the user explicitly asks for it."
- use when: I want to design, prototype, audit, clone or share a UI and Product Design is named or is clearly the main goal; it only routes (see family note).
- needs: Codex Desktop or ChatGPT Work Mode; refuses standard ChatGPT chat; runs the `user-context` python3 preflight first when local shell access is available.

### user-context
- id: product-design:user-context (source path: plugins/product-design/skills/user-context/SKILL.md)
- description: "Load or manage Product Design's saved user context. Use when the user asks to set up Product Design, get started, onboard, save product or design sources, see what Product Design remembers, update saved context, or remember Product Design preferences. Examples include product URLs, Figma files, screenshots, reference images, codebase paths, Storybook, tokens, design systems, brand assets, and general product/design notes."
- use when: Set up or onboard Product Design, or save product URLs, Figma files, screenshots, codebase paths and brand assets for reuse across sessions.
- needs: local shell, resolvable `$CODEX_HOME`, python3.
- side effects: writes local state (`user-context.md`, `assets/`) under `$CODEX_HOME/state/plugins/product-design/`; never saves secrets.

### get-context
- id: product-design:get-context (source path: plugins/product-design/skills/get-context/SKILL.md)
- description: "Mandatory design-brief gate for clarifying the product and outcome. Use before ideation, image-to-code builds, redesigns, or product UI work to clarify missing product information and play back the brief before proceeding."
- use when: Before building, redesigning or generating UI, play back the minimum design brief (one question only if the target or outcome is missing); writes nothing. Assume it also runs before `url-to-code` (family note).

### research
- id: product-design:research (source path: plugins/product-design/skills/research/SKILL.md)
- description: "Run fast, source-grounded UX research on the highest-signal problems users are experiencing with a user-specified digital product. Use when the user asks to research user pain, UX friction, onboarding issues, docs/help problems, developer experience friction, support pain, product workflow issues, or current user complaints for a named product."
- use when: Find what users complain about for a named product: UX friction, onboarding, docs or developer-experience pain, support pain.
- needs: web access; internal connectors (Slack, Notion, Linear and similar) only if present. Read-only.

### audit
- id: product-design:audit (source path: plugins/product-design/skills/audit/SKILL.md)
- description: "Audit or critique a product flow, journey, workflow, funnel, onboarding path, checkout path, settings path, screen, or multi-step product experience by capturing screenshots first, then reporting UX, design, and accessibility findings inline from that evidence. Use Figma only when the user explicitly asks for a board. Use when the user asks to audit, review, critique, inspect, assess, analyze, evaluate, or give feedback on a product experience."
- use when: Audit or critique an existing flow or screen from screenshots captured in this run; goes straight here, skipping `get-context`.
- needs: a browser that can drive the flow; Figma tools only if a board is requested.
- side effects: writes screenshots locally; no deploy.

### ideate
- id: product-design:ideate (source path: plugins/product-design/skills/ideate/SKILL.md)
- description: "Generate image-based alternatives, remixes, or new design directions from a Product Design brief. Use when the user asks for design variants, visual exploration, remixes, or image-generated approaches from provided context."
- use when: Turn an idea, redesign request or variant ask with no visual target into exactly three Image Gen mockups, then wait for the user's pick.
- needs: `get-context` brief first; built-in Image Gen.

### image-to-code
- id: product-design:image-to-code (source path: plugins/product-design/skills/image-to-code/SKILL.md)
- description: "Implement a selected image, screenshot, mockup, or Image Gen reference as a faithful, responsive frontend."
- use when: Build a faithful, interactive frontend from a selected Image Gen option, screenshot, mockup or Figma frame; ends with a blocking `design-qa` pass.
- needs: Node/npm, Image Gen, a browser.
- side effects: writes files and starts a local dev server; does not deploy.

### url-to-code
- id: product-design:url-to-code (source path: plugins/product-design/skills/url-to-code/SKILL.md)
- description: "Clone a live URL as a runnable frontend-only local app."
- use when: Clone a live URL I own or may recreate into an editable local frontend; "like <URL>" means redesign (`get-context` then `ideate`), not this. Expect the `get-context` brief playback first (family note).
- needs: a browser that can open and capture the live URL (not a login or error page); Node/npm; no browser fallback.
- side effects: writes files and starts a local server; leaves production code untouched.

### design-qa
- id: product-design:design-qa (source path: plugins/product-design/skills/design-qa/SKILL.md)
- description: "Internal prototype QA helper. Use only after a Product Design prototype, URL-to-code build, or image-to-code build has a source visual target and a rendered implementation to compare before handoff. Do not use for broad UX critique, design critique, product audits, or flow reviews; route those user-facing requests to audit."
- use when: Internal blocking compare of a built prototype against its source visual before handoff; never for a user-facing critique (use `audit`).
- side effects: writes `design-qa.md` in the project root.

### share
- id: product-design:share (source path: plugins/product-design/skills/share/SKILL.md)
- description: "Share a runnable prototype using the user's preferred deployment tool."
- use when: Deploy or publish a finished prototype to get a shareable link.
- needs: a deployment tool (`@Sites` via `sites-hosting`, `@Vercel` or other).
- side effects: publishes to an external host; asks which target only if the user has not already selected one.

## Family: magicpath
- source path: `plugins/magicpath` (v0.1.2)
- manifest notes: Codex-only manifest; no MCP server, app connector, hooks or agents. License "UNLICENSED"; category Developer Tools. The skill shells out to the `magicpath-ai` npm CLI via `npx -y`; auth is `npx -y magicpath-ai login` (no policy in the manifest). `allowed-tools` in the skill is limited to `Bash(npx -y magicpath-ai *)`.
- router: none (single skill)
- development distance: adjacent (design-to-code: installs and authors UI components)
- disclosure: simple. One skill, and it is relevant only when the user names MagicPath.

### magicpath
- id: magicpath:magicpath (source path: plugins/magicpath/skills/magicpath/SKILL.md)
- description: "Use when the user mentions MagicPath, designs, UI components, themes, canvas selections, or repo-to-canvas UI work; run magicpath-ai to search, inspect, install, or author components."
- use when: I want to pull a component from my MagicPath canvas into my React app, apply my MagicPath theme, or put this repo's UI on a MagicPath canvas.
- not for: `image-to-code` (screenshot or mockup source) and Figma design-to-code skills (other families): choose this only when MagicPath is the named source or destination, since its description also matches generic words like "designs" and "themes".
- needs: Node and `npx` (runs `npx -y magicpath-ai ... -o json`), network, a MagicPath account (`magicpath-ai login`); a React/TS target app for `add`.
- side effects: `npx -y` may install the CLI; `add` writes `src/components/magicpath/<name>/`; `code start` creates pending canvas work and local editable files; `code submit --wait` publishes to the user's MagicPath canvas; `view` opens the OS browser; asks before installing or editing unless given an exact `generatedName`, selected canvas item, or component/project id.
- part of: standalone

## Family: build-web-data-visualization
- source path: `plugins/build-web-data-visualization`
- manifest notes: Codex plugin manifest only (.codex-plugin, v0.1.21, category Developer Tools). No MCP server, app connector, hooks or commands; ships shared references and templates (chart brief, design contracts, Playwright starters). Marketplace: authentication ON_USE, products [CODEX]. Concept-first design relies on Codex image generation.
- router: `data-visualization`. Only skill with allow_implicit_invocation; specialists stay explicit-only unless it hands off. Sequence: classify the analytical job and data shape, lock delivery constraints, define the reading path before the renderer, plan state (URL-backed filters, persistence), route to the narrowest specialist, write a technical design before implementation. Gate: for advanced visual design, generate and show large-screen and mobile concepts and wait for user approval before any project change.
- development distance: adjacent (data viz produces code but sits outside typical development)
- disclosure: router-delegated. The router covers all 18 skills, so records stay one-liners for matching and the router's routing matrix does the rest.

### data-visualization
- id: build-web-data-visualization:data-visualization (source path: plugins/build-web-data-visualization/skills/data-visualization/SKILL.md)
- description: "Route web data visualization work. Use when the user needs chart choice, visual critique, dashboards, maps or geospatial views, Gantt timelines, UML/software diagrams, scrollytelling, reports or exports, testing, accessibility, browser implementation, or concept-first visual design."
- use when: Entry router when a web chart, dashboard, map, diagram, scrolly story or report is wanted and the right specialist is not obvious; classifies the job and routes to the narrowest specialist, writes a technical design before implementation, and pauses for concept approval on advanced visual design.
- needs: Codex image generation for the concept-first path.

### visualization-strategy-and-critique
- id: build-web-data-visualization:visualization-strategy-and-critique (source path: plugins/build-web-data-visualization/skills/visualization-strategy-and-critique/SKILL.md)
- description: "Choose, lay out, critique, and explain data visualizations. Use when the user asks what visualization fits a dataset or goal, how a chart, dashboard, operational workspace, UML-like diagram, or software architecture diagram should be composed or interacted with, asks for visual page design, a layout mockup, generated large-screen and mobile concept images, or to be shown what a visualization could look like, when domain-native contextual surfaces or graphical backgrounds may help, when scrollytelling or parallax might be appropriate, wants a critique of an existing visualization, or needs guidance grounded in trusted visualization theory and practice. For advanced visual design or page-layout prompts where composition affects understanding, Codex must generate and show both large-screen and mobile portrait image concepts before implementation or text-only design handoff, plus mobile landscape when needed."
- use when: Choosing which chart or layout fits the data, critiquing an existing chart/dashboard, or designing a page or infographic with large-screen and mobile concept images. It reasons about design; the router only classifies.
- needs: Codex image generation for concept images.
- side effects: No project changes or code until the user approves the concepts.

### grammar-of-graphics-and-declarative-visualization
- id: build-web-data-visualization:grammar-of-graphics-and-declarative-visualization (source path: plugins/build-web-data-visualization/skills/grammar-of-graphics-and-declarative-visualization/SKILL.md)
- description: "Build data visualizations with declarative grammars. Use when the user needs Vega-Lite, Vega, Observable Plot, or grammar-of-graphics reasoning, especially for tabular charts that do not require bespoke rendering."
- use when: A standard tabular chart in Vega-Lite, Vega or Observable Plot; the default first implementation path before D3. Hands off when the grammar runs out.

### d3-data-visualization
- id: build-web-data-visualization:d3-data-visualization (source path: plugins/build-web-data-visualization/skills/d3-data-visualization/SKILL.md)
- description: "Build custom data visualizations with D3. Use when the user needs SVG or DOM-based charts, rich annotation, domain-native contextual backgrounds, data joins, custom scales or interactions, scroll-driven SVG scene states, or precise control over browser visualization behavior."
- use when: Bespoke SVG/DOM charts in D3: direct labels, annotation, brushing, zoom, domain backgrounds. Use when declarative grammars do not fit; move to canvas2d when DOM node count limits it.

### canvas2d-data-visualization
- id: build-web-data-visualization:canvas2d-data-visualization (source path: plugins/build-web-data-visualization/skills/canvas2d-data-visualization/SKILL.md)
- description: "Render data visualizations with Canvas2D. Use when the visualization needs high mark counts, fast redraws, immediate-mode rendering, custom hit testing, or a hybrid Canvas plus SVG or HTML architecture."
- use when: Dense charts (tens of thousands to millions of flat marks), fast redraw, custom hit testing, or blurry canvas on high-DPI. Keep axes and text in SVG/HTML; go to threejs-data-visualization for GPU picking or shaders.

### threejs-data-visualization
- id: build-web-data-visualization:threejs-data-visualization (source path: plugins/build-web-data-visualization/skills/threejs-data-visualization/SKILL.md)
- description: "Render WebGL-accelerated data visualizations with Three.js, raw WebGL, deck.gl, luma.gl, PixiJS, Sigma.js, Plotly WebGL traces, ECharts GL, CesiumJS, Babylon.js, or related GPU libraries. Use when the visualization needs true spatial structure, dense 2D or 3D GPU rendering, particle or flow animation, volumetric views, or interactive exploration that adds real analytical value."
- use when: 3D/WebGL/GPU visualization (Three.js, deck.gl, PixiJS, Cesium, particles, huge point clouds). Only when depth, GPU scale or shaders justify it over 2D.

### geospatial-and-cartographic-visualization
- id: build-web-data-visualization:geospatial-and-cartographic-visualization (source path: plugins/build-web-data-visualization/skills/geospatial-and-cartographic-visualization/SKILL.md)
- description: "Design geospatial and cartographic visualizations. Use when the user needs help deciding whether to use a map, choosing projections or basemaps, building choropleths or symbol maps, or implementing thematic maps, slippy maps, or geospatial interactions with D3 geo, Leaflet, MapLibre, Mapbox GL JS, Google Maps, OpenLayers, deck.gl, ArcGIS Maps SDK, Azure Maps, HERE Maps, CesiumJS, or related tools."
- use when: Deciding whether something should be a map and how: basemap, projection, choropleth vs symbol map, Leaflet/MapLibre/deck.gl stack, mobile map behavior. Scientific, live or disaster maps need a source-and-method ledger first.

### dashboards-and-real-time-visualization
- id: build-web-data-visualization:dashboards-and-real-time-visualization (source path: plugins/build-web-data-visualization/skills/dashboards-and-real-time-visualization/SKILL.md)
- description: "Design dashboards and live visualization systems. Use when the user needs monitoring views, streaming charts, coordinated interactions, downsampling, or performance-aware operational visualization."
- use when: Designing monitoring dashboards, streaming/WebSocket charts and coordinated views, including stale, offline and reconnect states. System-level behavior of live views, not one chart's renderer.

### statistical-and-uncertainty-visualization
- id: build-web-data-visualization:statistical-and-uncertainty-visualization (source path: plugins/build-web-data-visualization/skills/statistical-and-uncertainty-visualization/SKILL.md)
- description: "Design statistically honest and uncertainty-aware visualizations. Use when the user needs help showing distributions, intervals, confidence, missingness, sampling effects, or analytical rigor in charts and dashboards."
- use when: Showing distributions, confidence intervals, missing data or sample size honestly (histogram vs box vs violin). Thin skill body; substance is in its references.

### gantt-chart-visualization
- id: build-web-data-visualization:gantt-chart-visualization (source path: plugins/build-web-data-visualization/skills/gantt-chart-visualization/SKILL.md)
- description: "Design, critique, route, and implement Gantt charts and schedule visualizations. Use when the user mentions Gantt charts, project schedules, roadmaps with task spans, milestones, dependencies, predecessors, critical path, baselines, WBS, resource plans, capacity timelines, MS Project, Primavera P6, Jira Advanced Roadmaps, GitHub Projects, Smartsheet, monday.com, Asana, ClickUp, Azure DevOps iterations, or importing/exporting project-management data for a timeline chart."
- use when: A project schedule or roadmap with dependencies, critical path and baselines, including importing from Jira, MS Project, GitHub Projects or CSV. Advisory design; calls no PM-tool API.

### uml-and-software-architecture-visualization
- id: build-web-data-visualization:uml-and-software-architecture-visualization (source path: plugins/build-web-data-visualization/skills/uml-and-software-architecture-visualization/SKILL.md)
- description: "Design, critique, read, write, render, and implement UML and UML-like software diagrams. Use when the user mentions UML, sequence diagrams, class diagrams, activity diagrams, state machines, use case diagrams, component diagrams, deployment diagrams, object diagrams, package diagrams, profile diagrams, timing diagrams, communication diagrams, interaction overview diagrams, composite structure diagrams, ERDs, database schema diagrams, C4, BPMN, swimlanes, flowcharts, network diagrams, application architecture diagrams, software architecture diagrams, diagram-as-code, model-as-code, XMI, UMLDI, PlantUML, Mermaid, Graphviz DOT, D2, Structurizr, DBML, diagrams.net/draw.io, Kroki, or interactive diagram editors and explorers."
- use when: Choosing notation, source format and renderer for UML, C4, ERD, BPMN, sequence or state diagrams (PlantUML, Mermaid, DOT, D2, Structurizr) and interactive diagram explorers. Layout questions go to node-link-and-diagram-layout.

### node-link-and-diagram-layout
- id: build-web-data-visualization:node-link-and-diagram-layout (source path: plugins/build-web-data-visualization/skills/node-link-and-diagram-layout/SKILL.md)
- description: "Choose and apply automatic layout strategies for node-link diagrams and connected-node visuals. Use when the user asks how to auto-arrange nodes, reduce line crossings, route edges, avoid overlaps, stabilize layout, or choose graph-layout algorithms for network diagrams, dependency graphs, database schema diagrams, ERDs, state machines, decision trees, flow diagrams, box-and-line editors, or other line-connected nodes."
- use when: Auto-arranging nodes, reducing edge crossings, routing edges or choosing a layout algorithm (ELK, Dagre, Graphviz, force) for ERDs, state machines, dependency graphs. Placement, not notation; notation goes to uml-and-software-architecture-visualization.

### scrollytelling-and-parallax-data-visualization
- id: build-web-data-visualization:scrollytelling-and-parallax-data-visualization (source path: plugins/build-web-data-visualization/skills/scrollytelling-and-parallax-data-visualization/SKILL.md)
- description: "Design and implement parallax scrolling and scrollytelling data visualizations. Use when the user asks for parallax scrolling, scrollytelling, scroll-driven timelines, sticky graphics, Scrollama, ScrollTrigger, ScrollTimeline, view timelines, rich-media timelines, moviescrollers, scroll-scrubbed charts, staged narrative reveals, or interactive visual stories where scrolling changes a data visualization or media scene."
- use when: Scroll-driven data stories: Scrollama, ScrollTrigger, sticky graphics, parallax. Comes after visualization-strategy-and-critique decides scrollytelling over a stepper.

### react-and-nextjs-data-visualization
- id: build-web-data-visualization:react-and-nextjs-data-visualization (source path: plugins/build-web-data-visualization/skills/react-and-nextjs-data-visualization/SKILL.md)
- description: "Integrate data visualizations into React and Next.js applications. Use when the user needs chart components, UML-like or architecture diagram components, React integration patterns, Next.js client or server boundaries, hydration-safe rendering, lazy loading, framework-aware performance, scroll-driven visual stories, or export guidance."
- use when: Chart or diagram components inside a React or Next.js app: hydration/SSR, client-server boundaries, dynamic imports, URL-backed state, WebGL lifecycle.
- needs: A React or Next.js project.

### typescript-data-visualization-engineering
- id: build-web-data-visualization:typescript-data-visualization-engineering (source path: plugins/build-web-data-visualization/skills/typescript-data-visualization-engineering/SKILL.md)
- description: "Build typed data visualizations in TypeScript. Use when the user wants TypeScript visualization code, typed data models, browser visualization components, UML-like diagram models, interactive graph or architecture diagram contracts, scroll-driven scene contracts, library selection guidance, or a maintainable visualization architecture beyond React- or Next-specific concerns."
- use when: Typed visualization architecture in a TypeScript app: data schemas, URL view-state codecs, library selection, typed scene/diagram contracts. Framework-independent; React specifics go to react-and-nextjs-data-visualization.
- needs: A TypeScript codebase.

### testing-data-visualizations
- id: build-web-data-visualization:testing-data-visualizations (source path: plugins/build-web-data-visualization/skills/testing-data-visualizations/SKILL.md)
- description: "Test data visualizations and dashboards. Use when the user needs chart or diagram test strategy, screenshot or image diff testing, visual regression, mocked or synthetic chart data, component or unit tests, E2E dashboard QA, interactive UML-like diagram verification, scroll-driven story verification, export verification, or guidance on avoiding brittle over-testing."
- use when: How to test charts and dashboards: unit/component/E2E mix, visual regression, deterministic rendering, canvas/WebGL readiness. Dashboard and React questions about testing route here first.
- needs: Test tooling already in the project (Playwright templates are bundled, nothing is installed).

### accessibility-and-inclusive-visualization
- id: build-web-data-visualization:accessibility-and-inclusive-visualization (source path: plugins/build-web-data-visualization/skills/accessibility-and-inclusive-visualization/SKILL.md)
- description: "Make data visualizations accessible and inclusive. Use when the user needs chart or diagram accessibility guidance, text alternatives for complex visuals, color and contrast review, keyboard support, reduced-motion behavior for animation or parallax, or an accessibility QA workflow for exported figures, UML-like diagrams, and dashboards."
- use when: Making a chart, dashboard or diagram accessible: alt text, color/contrast, keyboard and screen-reader paths, reduced motion. Defines what accessible means; testing-data-visualizations verifies it.

### reports-pdfs-and-slide-automation
- id: build-web-data-visualization:reports-pdfs-and-slide-automation (source path: plugins/build-web-data-visualization/skills/reports-pdfs-and-slide-automation/SKILL.md)
- description: "Lay out and export data-rich reports and documents. Use when the user needs report structure, figure packaging, PDFs, PowerPoint or Google Slides automation, or programmatic insertion of visualizations, UML-like diagrams, or architecture diagrams into documents."
- use when: Packaging visualizations into reports, PDFs, PowerPoint or Google Slides, with figure export and a regeneration path. Document-level composition; each figure still goes through its specialist.
- needs: A Google Slides API path would need the user's own Google credentials, which the skill does not cover.
- side effects: Pending concept approval also blocks finalized assets, not just code.

## Family: hyperframes
- source path: `plugins/hyperframes`
- manifest notes: Codex plugin manifest only (.codex-plugin, v0.1.2, HeyGen, Apache-2.0, category Creativity; marketplace products [CODEX], authentication ON_INSTALL). No MCP or app connector; local `npx hyperframes` with Node 22+ and FFmpeg on PATH, Chrome for rendering, optional Docker/GPU. Skills mirror upstream heygen-com/hyperframes. Optional keys: GEMINI_API_KEY or GOOGLE_API_KEY (image descriptions), OpenAI or Groq (transcription), ElevenLabs or HeyGen MCP (TTS); local Kokoro TTS needs no key but downloads about 340 MB and Python (assume 3.10+: the TTS reference says 3.8+, the website voiceover reference says 3.10+ and that 3.9 fails). Website workflow expects harness subagents.
- router: none formal. `hyperframes` is the composition-authoring entry and `website-to-hyperframes` is the URL-to-promo orchestrator; `hyperframes-cli`, `hyperframes-registry` and `gsap` are helpers. Authoring gates: visual identity (DESIGN.md, then visual-style.md, then named style, else ask) before any HTML; static hero-frame layout before motion; lint, validate and inspect at the end. Website sequence ends at preview; MP4 render only on explicit request.
- development distance: adjacent (video as code: HTML/CSS/GSAP compositions rendered to MP4)
- disclosure: simple. Five skills with two clear entry points and helper roles; the family needs no router of its own.

### hyperframes
- id: hyperframes:hyperframes (source path: plugins/hyperframes/skills/hyperframes/SKILL.md)
- description: "Create video compositions, animations, title cards, overlays, captions, voiceovers, audio-reactive visuals, and scene transitions in HyperFrames HTML. Use when asked to build any HTML-based video content, add captions or subtitles synced to audio, generate text-to-speech narration, create audio-reactive animation (beat sync, glow, pulse driven by music), add animated text highlighting (marker sweeps, hand-drawn circles, burst lines, scribble, sketchout), or add transitions between scenes (crossfades, wipes, reveals, shader transitions). Covers composition authoring, timing, media, and the full video production workflow. For CLI commands (init, lint, preview, render, transcribe, tts) see the hyperframes-cli skill."
- use when: Create or edit an HTML video composition: animated titles, overlays, transitions, synced captions, voiceover, audio-reactive visuals that must render deterministically.
- not for: game-studio skills (interactive gameplay, not captured video); website-to-hyperframes (starts from a URL).
- needs: Node 22+, FFmpeg, Chrome; brand identity from DESIGN.md or the user; optional TTS/transcription dependencies.
- side effects: writes local project files
- part of: composition authoring entry; step 6 of website-to-hyperframes; hands commands to hyperframes-cli, tweens to gsap. Identity before any HTML; static layout before motion.

### website-to-hyperframes
- id: hyperframes:website-to-hyperframes (source path: plugins/hyperframes/skills/website-to-hyperframes/SKILL.md)
- description: "Capture a website and create a HyperFrames video from it. Use when: (1) a user provides a URL and wants a video, (2) someone says "capture this site", "turn this into a video", "make a promo from my site", (3) the user wants a social ad, product tour, or any video based on an existing website, (4) the user shares a link and asks for any kind of video content. Even if the user just pastes a URL — this is the skill to use."
- use when: Turn this website into a product promo, social ad or tour using the site's real brand and assets. The source also explicitly triggers on a bare pasted URL.
- not for: hyperframes (non-website composition); faceless-channel (illustrated scenes; refuses product ads).
- needs: Reachable URL; Node 22+, FFmpeg, Chrome; harness subagents (one per beat); optional Gemini key or ElevenLabs/HeyGen MCP.
- side effects: downloads site assets; may call paid image or TTS services; stops at local Studio preview unless an MP4 render is asked for
- part of: entry router for a seven-step sequence (capture through validate); calls hyperframes and hyperframes-cli.

### hyperframes-cli
- id: hyperframes:hyperframes-cli (source path: plugins/hyperframes/skills/hyperframes-cli/SKILL.md)
- description: "HyperFrames CLI tool — hyperframes init, lint, inspect, preview, render, transcribe, tts, doctor, browser, info, upgrade, compositions, docs, benchmark. Use when scaffolding a project, linting, validating, inspecting visual layout in compositions, previewing in the studio, rendering to video, transcribing audio, generating TTS, or troubleshooting the HyperFrames environment."
- use when: Scaffold a video project, diagnose the render environment, lint or inspect, preview, render MP4/WebM, transcribe or synthesize narration with the hyperframes CLI.
- not for: hyperframes (authoring HTML); hyperframes-registry (installing blocks).
- needs: Node 22+, npx, FFmpeg, Chrome; optional Docker/GPU; Kokoro TTS downloads about 340 MB on first use.
- side effects: init creates a project and installs coding skills; render uses up to 8 Chrome workers
- part of: operational step of hyperframes and website-to-hyperframes; standalone for troubleshooting or export. Run doctor first when rendering fails.

### hyperframes-registry
- id: hyperframes:hyperframes-registry (source path: plugins/hyperframes/skills/hyperframes-registry/SKILL.md)
- description: "Install and wire registry blocks and components into HyperFrames compositions. Use when running hyperframes add, installing a block or component, wiring an installed item into index.html, or working with hyperframes.json. Covers the add command, install locations, block sub-composition wiring, component snippet merging, and registry discovery."
- use when: Install an existing chart, overlay, shader or effect block with hyperframes add and wire it into a host composition.
- not for: hyperframes-cli init (full examples; add installs blocks and components only); gsap (writing the effect yourself).
- needs: HyperFrames project; network to the registry.
- side effects: downloads and writes compositions/*.html; may use the clipboard (--no-clipboard for headless)
- part of: reuse step inside authoring. Its claim that data-track-index orders layers conflicts with the hyperframes skill: tell the user to set CSS z-index for layering and not rely on track index.

### gsap
- id: hyperframes:gsap (source path: plugins/hyperframes/skills/gsap/SKILL.md)
- description: "GSAP animation reference for HyperFrames. Covers gsap.to(), from(), fromTo(), easing, stagger, defaults, timelines (gsap.timeline(), position parameter, labels, nesting, playback), and performance (transforms, will-change, quickTo). Use when writing GSAP animations in HyperFrames compositions."
- use when: While authoring a HyperFrames composition: tween and timeline positions, labels, easing, stagger, SVG transforms, cleanup.
- not for: hyperframes (capture-specific rules win over generic GSAP examples: no infinite repeats, no visibility animation).
- needs: GSAP and an existing composition.
- side effects: writes local animation code
- part of: reference step inside hyperframes authoring, not a production route.

## Family: remotion
- source path: `plugins/remotion` (v1.0.7, author Remotion)
- manifest notes: Codex-only marketplace entry; no MCP, app, hooks or commands; local `npx remotion` tooling (Node.js, Git). The router bundles `REFERENCE.md` copies of the other skills. Codex Studio launch: `npx remotion studio --no-open`; on an `EMFILE ... watch` error only, retry with `--webpack-poll 1000`; otherwise ask the user to start it from macOS Terminal.
- router: `remotion-best-practices` is a pure "if X, load Y" list with no workflow of its own. Any request to make or build a new video loads `remotion-create` first, project or not. Then: markup -> remotion-markup, maps, multimedia, interactivity, advanced render, studio flags, captions, SaaS/Player/Lambda, docs lookup, upgrade. Create sequence: scaffold (skip if project exists) -> markup and interactivity rules -> Studio preview -> render only if asked.
- development distance: adjacent (video as code)
- disclosure: router-delegated. The router covers all twelve skills, so records stay one-liners.

### remotion-best-practices
- id: remotion:remotion-best-practices (source path: plugins/remotion/skills/remotion-best-practices/SKILL.md)
- description: "Router for all Remotion skills"
- use when: Any Remotion (React video) request where the right sub-skill is unclear, or a follow-up edit after a video was created.

### remotion-captions
- id: remotion:remotion-captions (source path: plugins/remotion/skills/remotion-captions/SKILL.md)
- description: "Transcribing, displaying and animating captions"
- use when: Add subtitles to a Remotion video: transcribe audio, import an .srt, or display and animate captions.
- side effects: transcription installs `@remotion/install-whisper-cpp` and downloads a Whisper model.

### remotion-create
- id: remotion:remotion-create (source path: plugins/remotion/skills/remotion-create/SKILL.md)
- description: "Create a new Remotion video"
- use when: Make a new Remotion video from scratch: scaffold, design, and preview in Studio; no render unless asked.
- side effects: writes files, runs `npm i`, starts a long-running dev server.

### remotion-docs
- id: remotion:remotion-docs (source path: plugins/remotion/skills/remotion-docs/SKILL.md)
- description: "Search Remotion documentation"
- use when: Look up current Remotion API docs instead of relying on memory.
- needs: network access to algolia.net and remotion.dev; no project required.

### remotion-interactivity
- id: remotion:remotion-interactivity (source path: plugins/remotion/skills/remotion-interactivity/SKILL.md)
- description: "Structure Remotion markup for interactivity"
- use when: Make Remotion markup editable in Studio (click-select, drag, keyframes, props writing back to code); strict inline-style and inline-`interpolate()` rules.

### remotion-maps
- id: remotion:remotion-maps (source path: plugins/remotion/skills/remotion-maps/SKILL.md)
- description: "Remotion Map animation knowledge"
- use when: Put a map in a Remotion video: static map, animated route, globe, or terrain flythrough; pick one technique.
- needs: Mapbox needs an API key; MapLibre needs none; MapTiler and Cesium may need accounts (unverified).

### remotion-markup
- id: remotion:remotion-markup (source path: plugins/remotion/skills/remotion-markup/SKILL.md)
- description: "Content, animation and effects best practices"
- use when: Write or edit Remotion composition code: animation, timing, media, fonts, transitions, 3D, audio; index of about 30 topic files.
- needs: some topics need FFmpeg or an ElevenLabs API key (voiceover).

### remotion-multimedia
- id: remotion:remotion-multimedia (source path: plugins/remotion/skills/remotion-multimedia/SKILL.md)
- description: "Interacting with Mediabunny"
- use when: Read audio or video duration or video dimensions with Mediabunny, e.g. match a composition to its footage. Trimming and cropping are not documented here despite the router's wording; see remotion-markup.

### remotion-render
- id: remotion:remotion-render (source path: plugins/remotion/skills/remotion-render/SKILL.md)
- description: "Export a Remotion video"
- use when: Export a Remotion video or still from the CLI, including transparent video; for app-triggered renders use remotion-saas.
- side effects: CPU-heavy; writes output files.

### remotion-saas
- id: remotion:remotion-saas (source path: plugins/remotion/skills/remotion-saas/SKILL.md)
- description: "Build an app with Remotion"
- use when: Build an app around Remotion: embed the Player, user-triggered renders on Lambda, Vercel, Cloudflare, Node or the client, starter templates.
- side effects: cloud setup can create billable AWS/Vercel/Cloudflare resources; the skill offers guided setup instead of silent provisioning.

### remotion-studio
- id: remotion:remotion-studio (source path: plugins/remotion/skills/remotion-studio/SKILL.md)
- description: "Preview a Remotion video"
- use when: Open the Remotion Studio preview or set its CLI flags (--port, --log, --force-new).
- side effects: starts a long-running process.

### remotion-upgrade
- id: remotion:remotion-upgrade (source path: plugins/remotion/skills/remotion-upgrade/SKILL.md)
- description: "Upgrade Remotion, and related packages"
- use when: Upgrade Remotion, aligned Mediabunny, and the installed Remotion skills to one version.
- side effects: edits manifests, lockfile and installed skills.

## Far families (pointers only)
Families of openai/plugins that are far from software development. Open the named file only when the user's task is in that area.

- `life-science-research` (50 skills; router `research-router-skill`): lookups against public life-science databases across genetics, expression, pathways, structure, chemistry, clinical and literature sources. Records: far/science.md
- `ngs-analysis` (18 skills; router `ngs-analysis-router`): sequencing pipelines from BCL, FASTQ, BAM/CRAM, count matrices and VCF (variant calling, RNA-seq, scRNA-seq, epigenomics, metagenomics). Records: far/science.md
- `boltz-api-cli` (8 skills; no router): paid Boltz API jobs for protein and small-molecule design, screening, ADME, structure and binding. Records: far/science.md
- `zotero` (1 skill; no router): Zotero Desktop library search, BibTeX export and citation keys in LaTeX or Markdown drafts. Records: far/science.md
- `public-equity-investing` (23 skills; router `public-equity-investing`): listed-equity investment research, financial models and memos. Records: far/finance.md
- `adobe` (6 skills; no router): photo batch edits, mockups, social variations, template designs, quick video cuts and portrait retouching through the Adobe connector. Records: far/media.md
- `canva` (8 skills; no router): editing, critiquing, brand-checking, translating, resizing and bulk-creating Canva designs. Records: far/media.md
- `chatcut` (1 skill; no router): installing or repairing ChatCut Desktop (video editing app); contains no editing capability. Records: far/media.md
- `higgsfield` (3 skills; router `faceless-channel`): generated narrator-led faceless-channel videos, narration and burned-in subtitles. Records: far/media.md
- `creative-production` (2 skills; no router): campaign, ad, social and product imagery on a Codex desktop board. Records: far/media.md
- `google-drive` (5 skills; router `google-drive`): Drive file lifecycle, Docs, Sheets, Slides and comments. Records: far/workspace.md
- `notion` (4 skills; no router): Notion knowledge capture, meeting prep, research documentation and spec-to-task planning (writes no code). Records: far/workspace.md
- `dropbox` (6 skills; no router): finding, inspecting, sharing, organizing and cleaning up Dropbox content, and file requests. Records: far/workspace.md
- `airtable` (3 skills; no router): Airtable records, tables and filters through the `airtable-mcp` CLI. Records: far/workspace.md
- `nvidia` (12 skills; router `nvidia-skill-finder`): AI-Q blueprint, cuOpt, Dynamo, NemoClaw, Omniverse/USD and physical-AI pipelines on NVIDIA GPUs. Records: far/gpu-simulation.md

## Marketplace entries with no skills
These sixteen openai/plugins entries ship no SKILL.md: each provides only the connector or MCP server named, so there is no skill to recommend or invoke. All are listed as installation AVAILABLE, authentication ON_INSTALL.

- `linear` (Productivity): MCP server https://mcp.linear.app/mcp and app connector.
- `atlassian-rovo` (Productivity): MCP server https://mcp.atlassian.com/v1/mcp/authv2 and app connector.
- `google-calendar` (Productivity): MCP server https://calendarmcp.googleapis.com/mcp/v1 and app connector.
- `gmail` (Communication): MCP server https://gmailmcp.googleapis.com/mcp/v1 and app connector.
- `slack` (Communication): MCP server https://mcp.slack.com/mcp and app connector.
- `teams` (Communication): app connector.
- `sharepoint` (Productivity): app connector.
- `outlook-email` (Communication): app connector.
- `outlook-calendar` (Productivity): app connector.
- `github` (Developer Tools): MCP server https://api.githubcopilot.com/mcp/ and app connector.
- `granola` (Productivity): MCP server https://mcp.granola.ai/mcp and app connector.
- `monday-com` (Productivity): MCP server https://mcp.monday.com/mcp and app connector.
- `datadog` (Developer Tools): MCP server https://mcp.datadoghq.com/v1/mcp and app connector.
- `lovable` (Developer Tools): app connector.
- `clickup` (Productivity): MCP server https://mcp.clickup.com/mcp and app connector.
- `consensus` (Education & Research): MCP server https://mcp.consensus.app/mcp and app connector.

## Deprecated source: openai/skills
https://github.com/openai/skills is deprecated in favor of openai/plugins. Its README states "This repository is deprecated" and points to https://github.com/openai/plugins for current Codex skill and plugin examples, and to the Build plugins guide (https://developers.openai.com/codex/plugins/build) for adding skills. Do not treat openai/skills as a source of current skills.
