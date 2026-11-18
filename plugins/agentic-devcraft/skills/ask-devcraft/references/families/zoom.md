# openai/plugins family: zoom (Zoom)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `zoom` family. The catalog entry is in openai-platforms.md.

## Family: zoom
- source path: `plugins/zoom` (plugin v1.0.0, MIT, author Zoom; README names upstream `zoom/zoom-plugin-codex`, imported commit 6f30034c94b4594daaf814cd9bf4cf972b90a323). 53 skills: 3 routers, the rest product, platform and debug skills.
- manifest notes: Codex-only packaging (`.codex-plugin/plugin.json`); no Claude or Cursor manifest, hooks or rules. `.app.json` declares one Zoom app connector (id `asdk_app_69373a13116c819189d046aea1278836`), auth managed by Codex and not exposed as a token; it covers meeting-content lookup (summaries, transcripts, recordings), not developer credentials. `.mcp.json` declares an HTTP MCP server (`https://mcp.zoom.us/mcp/meeting/streamable`) with a placeholder OAuth client ID (`<ZOOM_PUBLIC_CLIENT_ID>`); whether Codex loads it is not established. No skill needs the connector or MCP to read its guidance; building needs the user's own Zoom Marketplace app credentials. Every skill sets `allow_implicit_invocation: false`, so it runs only when the user names it (`$start`). The plugin also ships 25 slash commands and 2 reviewer subagents (`zoom-integration-reviewer`, `zoom-oauth-scope-auditor`), Codex-only. `debug-zoom-auth`, `debug-zoom-webhook` and `zoom-integration-doctor` exist only as commands, not skills. Command conventions require explicit confirmation for destructive or production-impacting steps. Host-visible names differ from directories for many skills (e.g. `rest-api` is `build-zoom-rest-api-app`, `rtms` is `zoom-rtms`, `general` is `zoom-general`); skill bodies link siblings by directory path, and nested platform leaves may not appear in a host listing. Frontmatter descriptions are mostly one line ("Use when using RTMS."), so matching must use the records below. SDK version, platform and support claims (React Native up to 0.75.4, no Expo; March 2026 external-meeting OBF/ZAK rule; SDK snapshot versions) are source claims to recheck.
- router: `start` is the default entry but reaches only five skills (plan-zoom-product, setup-zoom-oauth, build-zoom-meeting-app, build-zoom-bot, debug-zoom): classify by job-to-be-done, route, load product references only after the route is clear, one recommendation, one clarifier only if ambiguous. `plan-zoom-product` (interview: one clarifier, primary surface, minimum support, rejected alternatives, next steps) and `choose-zoom-approach` (decision table: REST / webhooks or WebSockets / Meeting SDK / Video SDK / Apps SDK / RTMS plus Meeting SDK / Phone / Contact Center / Virtual Agent) cover the rest; `plan-zoom-integration` then phases the delivery. Gate: a real Zoom meeting never goes to Video SDK and a custom session never to Meeting SDK.
- development distance: core-dev (SDK, REST, webhook and bot integration code for a vendor platform; only relevant when the task involves Zoom).
- disclosure: router-delegated; three routers plus parent skills (meeting-sdk, video-sdk, contact-center, virtual-agent) own the routing, so records stay one-liners for matching.
- settled conflicts: `debug-zoom` is the broad failure entry and `debug-zoom-integration` is its fixed auth-first triage order (recommend the first; add the second for a systematic pass). `setup-zoom-oauth` is the decision-first auth pass; `zoom-oauth` is the exact-flow reference after it. Webhooks are the default for events; WebSockets only for latency or no inbound endpoint. `zoom-rtms` is an invisible backend media stream; `zoom-meeting-sdk-linux` is a visible participant; `scribe` is stored media only. `zoom-meeting-sdk-linux` (real meeting) and `zoom-video-sdk-linux` (custom session) are not interchangeable. Custom UI around a real browser meeting is `zoom-meeting-sdk-web-component-view`, not Video SDK. Product skills share the Video SDK parent `build-zoom-video-sdk-app`, whose references omit the macOS, Flutter, React Native and Unity leaves (they exist on disk).

### start
- id: zoom:start (source path: plugins/zoom/skills/start/SKILL.md)
- description: "Use when starting Zoom work."
- use when: A new Zoom task where the product or surface is unknown ("I want to do something with Zoom"); the plugin's default entry. Its table routes only to plan-zoom-product, setup-zoom-oauth, build-zoom-meeting-app, build-zoom-bot and debug-zoom, then loads supporting references; for Video SDK, RTMS, Team Chat, Phone, Contact Center, Virtual Agent, Cobrowse, Scribe, Rivet or Apps SDK go via plan-zoom-product or choose-zoom-approach, or straight to the named skill.
- side effects: none; writes nothing (routing only)

### plan-zoom-product
- id: zoom:plan-zoom-product (source path: plugins/zoom/skills/plan-zoom-product/SKILL.md)
- description: "Use when choosing products."
- use when: "I know the outcome but not whether I need Zoom meetings, custom video, events, phone/support, APIs or an app inside Zoom": picks one primary surface, the minimum supporting pieces, why alternatives lose, and next steps; asks one short clarifier if ambiguous. Plans only.

### choose-zoom-approach
- id: zoom:choose-zoom-approach (source path: plugins/zoom/skills/choose-zoom-approach/SKILL.md)
- description: "Use when choosing architecture."
- use when: Wanting the surface-mapping table without the interview: REST for backend automation/reporting, webhooks or WebSockets for events, Meeting SDK to embed real meetings, Video SDK for custom video, Apps SDK inside the Zoom client, RTMS (plus Meeting SDK if needed) for live media/bots. Never Video SDK for a real meeting nor Meeting SDK for a custom session. Decides only; plan-zoom-product adds the clarifier and rejected alternatives.

### plan-zoom-integration
- id: zoom:plan-zoom-integration (source path: plugins/zoom/skills/plan-zoom-integration/SKILL.md)
- description: "Use when planning Zoom integrations."
- use when: The Zoom product is chosen and you need an implementable architecture: auth/scope checklist, phases prototype, core integration, reliability, launch, early risks (OAuth, webhook verification, SDK limits, Marketplace review) and the smallest proving deliverable. Plans only; an already-broken integration goes to debug-zoom first.

### zoom-general
- id: zoom:general (source path: plugins/zoom/skills/general/SKILL.md)
- description: "Use when comparing products."
- use when: The goal is understood and you need cross-product context, auth-model differences (user OAuth, account OAuth, SDK signatures) or Marketplace publication background before narrowing; not a first-step router (use start or plan-zoom-product).

### setup-zoom-oauth
- id: zoom:setup-zoom-oauth (source path: plugins/zoom/skills/setup-zoom-oauth/SKILL.md)
- description: "Use when setting up OAuth."
- use when: Auth is the blocker or will shape the integration: choose Zoom app type, OAuth grant, minimum scopes and token storage/refresh, in that order; also first-pass auth debugging. Decision-first; hands to zoom-oauth for the exact flow.

### zoom-oauth
- id: zoom:oauth (source path: plugins/zoom/skills/oauth/SKILL.md)
- description: "Use when implementing OAuth."
- use when: Implement or debug the exact Zoom OAuth flow after setup-zoom-oauth: grant (PKCE for public clients, auth code for confidential web), scopes, token audience, refresh rotation, redirect/account/publication checks. SDK signatures are not OAuth tokens.
- side effects: implementing the refresh flow rotates single-use refresh tokens; the replacement must be persisted before the next refresh

### build-zoom-rest-api-app
- id: zoom:rest-api (source path: plugins/zoom/skills/rest-api/SKILL.md)
- description: "Use when calling REST APIs."
- use when: Backend code that calls Zoom REST endpoints deterministically: meetings, webinars, recordings, users, chat, phone, admin; endpoint and scopes first, then wrappers with pagination, retry and rate-limit handling. Hand-written REST; rivet-sdk is the framework alternative.
- needs: a Zoom OAuth app (user-level for user resources, account-level for admin; server-to-server only where the API documents it)
- side effects: implemented mutating API calls change real Zoom resources; read-only calls and reading the guidance do not

### rivet-sdk
- id: zoom:rivet-sdk (source path: plugins/zoom/skills/rivet-sdk/SKILL.md)
- description: "Use when using Rivet SDK."
- use when: Server-side Zoom integration on Zoom's Rivet framework instead of hand-rolled REST and webhook plumbing, including Lambda-style receivers; only after confirming Rivet fits. Niche.

### setup-zoom-webhooks
- id: zoom:webhooks (source path: plugins/zoom/skills/webhooks/SKILL.md)
- description: "Use when building Zoom webhooks."
- use when: Receiving Zoom events over HTTP callbacks: signature and endpoint validation first, then idempotent handlers, storage of event IDs, timestamps and delivery metadata, optional queue; the default for events. Also debugging validation, signature or delivery failures.
- needs: a public HTTPS endpoint, app event subscriptions and a webhook secret token for URL validation and signature verification; Zoom supplies the validation challenge

### setup-zoom-websockets
- id: zoom:websockets (source path: plugins/zoom/skills/websockets/SKILL.md)
- description: "Use when building Zoom WebSockets."
- use when: Zoom events over a persistent connection when you need low latency or cannot expose an inbound HTTP endpoint (firewall): auth, heartbeat, reconnect/backoff. Otherwise prefer setup-zoom-webhooks; events only, not media (zoom-rtms).

### build-zoom-team-chat-app
- id: zoom:team-chat (source path: plugins/zoom/skills/team-chat/SKILL.md)
- description: "Use when building Team Chat."
- use when: Posting or receiving Zoom Team Chat messages, a chatbot, interactive message cards (buttons, forms, slash commands) or chat automation; picks Team Chat API (user-scoped) versus Chatbot API (bot identity) first. A support chatbot product is build-zoom-virtual-agent instead.
- needs: a Zoom app of the right type with scopes and role enablement; confirm whether Zoom for Developers is enabled on the account; a webhook endpoint for interactivity and lifecycle events
- side effects: sends chat messages when run live

### build-zoom-meeting-app
- id: zoom:build-zoom-meeting-app (source path: plugins/zoom/skills/build-zoom-meeting-app/SKILL.md)
- description: "Use when embedding meetings."
- use when: "Let users join a real Zoom meeting from our app", possibly with meeting creation: confirms real meeting versus custom session, then Meeting SDK, platform skill, REST only for creation/reporting, webhooks or RTMS only if needed. Workflow entry above build-zoom-meeting-sdk-app.

### build-zoom-meeting-sdk-app
- id: zoom:meeting-sdk (source path: plugins/zoom/skills/meeting-sdk/SKILL.md)
- description: "Use when using Meeting SDK."
- use when: Real Zoom meetings are settled and you need the right SDK platform: confirms fit, picks platform, validates join/start inputs (meeting number, password, signature, role, host ZAK, waiting room), smallest working join first, then custom UI, raw data, recording. Parent of the zoom-meeting-sdk-* platform skills; external meetings need OBF/ZAK from 2 March 2026 per source.

### zoom-meeting-sdk-web
- id: zoom:meeting-sdk/web (source path: plugins/zoom/skills/meeting-sdk/web/SKILL.md)
- description: "Zoom Meeting SDK for Web - Embed Zoom meeting capabilities into web applications. Two integration options: Client View (full-page, familiar Zoom UI) and Component View (embeddable, Promise-based API). Includes SharedArrayBuffer setup for HD video, gallery view, and virtual backgrounds."
- use when: Join real Zoom meetings from the browser: decides full-page Client View versus embedded Component View, signature/init/join, SharedArrayBuffer and cross-origin isolation for HD/gallery; optionally runs probe-sdk before joining.
- needs: Meeting SDK credentials, a backend signature endpoint, COOP/COEP headers for advanced features

### zoom-meeting-sdk-web-client-view
- id: zoom:meeting-sdk/web/client-view (source path: plugins/zoom/skills/meeting-sdk/web/client-view/SKILL.md)
- description: "Zoom Meeting SDK Web - Client View. Full-page Zoom meeting experience with the familiar Zoom interface. Uses ZoomMtg global singleton with callback-based API. Ideal for quick integration with minimal customization. Provides the same UI as Zoom Web Client."
- use when: The familiar full-page Zoom UI quickly with limited customization (ZoomMtg singleton, callbacks), or a Client View that joins but renders black or behind the SPA. Contrast zoom-meeting-sdk-web-component-view.

### zoom-meeting-sdk-web-component-view
- id: zoom:meeting-sdk/web/component-view (source path: plugins/zoom/skills/meeting-sdk/web/component-view/SKILL.md)
- description: "Zoom Meeting SDK Web - Component View. Embeddable Zoom meeting components with Promise-based API for flexible integration. Ideal for React/Vue/Angular apps and custom layouts. Uses ZoomMtgEmbedded with async/await patterns and embeddable UI containers."
- use when: A real Zoom meeting inside one area of a React/Vue/Angular page with surrounding UI, resizing or a custom toolbar (ZoomMtgEmbedded, create the client once, await init then join). The right route for custom UI around a real meeting, never Video SDK; some Client View features are absent.

### zoom-meeting-sdk-android
- id: zoom:meeting-sdk/android (source path: plugins/zoom/skills/meeting-sdk/android/SKILL.md)
- description: "Zoom Meeting SDK for Android native apps. Use when embedding Zoom meetings in Android with default/custom UI, PKCE + SDK auth, join/start flows, and Meeting SDK API integration."
- use when: Real Zoom join/start in a native Android app, default UI first then custom UI, or fixing Android SDK auth and permissions.

### zoom-meeting-sdk-ios
- id: zoom:meeting-sdk/ios (source path: plugins/zoom/skills/meeting-sdk/ios/SKILL.md)
- description: "Zoom Meeting SDK for iOS native apps. Use when embedding Zoom meetings in iOS with default/custom UI, PKCE + SDK auth, host start with ZAK, and mobile lifecycle handling."
- use when: Real Zoom meetings in a native iOS app: stable default-UI join first, then host start with ZAK, custom UI and audio/lifecycle handling.

### zoom-meeting-sdk-macos
- id: zoom:meeting-sdk/macos (source path: plugins/zoom/skills/meeting-sdk/macos/SKILL.md)
- description: "Zoom Meeting SDK for macOS native apps. Use when embedding Zoom meetings in macOS with default/custom UI, PKCE + SDK auth, host start/join flows, and desktop meeting feature controllers."
- use when: Real Zoom meetings in a native macOS desktop app: default UI first, then host flow, custom UI and desktop controllers; recheck share and annotation after SDK upgrades.

### zoom-meeting-sdk-windows
- id: zoom:meeting-sdk/windows (source path: plugins/zoom/skills/meeting-sdk/windows/SKILL.md)
- description: "Zoom Meeting SDK for Windows - Native C++ SDK for embedding Zoom meetings into Windows desktop applications. Supports custom UI architecture with raw video/audio data, headless bots, and deep integration with meeting features. Includes SDK architecture patterns and Windows message loop handling."
- use when: A native Windows Zoom desktop app or headless recorder, custom UI or raw video/audio capture, or auth that times out because callbacks never arrive (Windows message loop is mandatory).
- needs: Windows 10+, Visual Studio with C++; source says native .sln/.vcxproj projects and not CMake

### zoom-meeting-sdk-linux
- id: zoom:meeting-sdk/linux (source path: plugins/zoom/skills/meeting-sdk/linux/SKILL.md)
- description: "Zoom Meeting SDK for Linux - C++ headless meeting bots with raw audio/video access, transcription, recording, and AI integration for server-side automation"
- use when: A visible, headless meeting participant on a Linux server that auto-joins and captures raw audio/video (PCM/YUV) or starts cloud recording. Versus zoom-rtms: this one is a participant with identity and controls; RTMS is an invisible backend stream.
- needs: Ubuntu/CentOS/Oracle Linux x86_64, C++ toolchain, PulseAudio with virtual devices, GLib main loop, Meeting SDK credentials, OBF or ZAK for external meetings

### zoom-meeting-sdk-electron
- id: zoom:meeting-sdk/electron (source path: plugins/zoom/skills/meeting-sdk/electron/SKILL.md)
- description: "Zoom Meeting SDK for Electron desktop applications. Use when embedding Zoom meetings in an Electron app with the Node addon wrapper, JWT auth, join/start flows, settings controllers, and raw data integration."
- use when: Zoom meetings in an Electron desktop app through the native Node addon wrapper and an IPC bridge, with desktop controls or raw media.
- needs: compatible Electron/Node toolchain and a native addon compiler

### zoom-meeting-sdk-react-native
- id: zoom:meeting-sdk/react-native (source path: plugins/zoom/skills/meeting-sdk/react-native/SKILL.md)
- description: "Zoom Meeting SDK for React Native. Use when embedding Zoom meetings in React Native iOS/Android apps with @zoom/meetingsdk-react-native, JWT auth, join/start flows, platform setup, and native bridge troubleshooting."
- use when: One React Native app joining or starting Zoom meetings via @zoom/meetingsdk-react-native, or diagnosing the wrapper/native bridge; check source limits first (RN up to 0.75.4, no Expo).
- needs: npm package plus native iOS/Android SDK artifacts and a backend JWT endpoint

### zoom-meeting-sdk-unreal
- id: zoom:meeting-sdk/unreal (source path: plugins/zoom/skills/meeting-sdk/unreal/SKILL.md)
- description: "Zoom Meeting SDK for Unreal Engine wrapper integrations. Use when building Unreal projects that embed Zoom meetings with C++ and Blueprint wrappers, including wrapper-to-SDK mapping concerns."
- use when: Real Zoom meetings in an Unreal Engine project through C++ or Blueprint wrappers. Niche; the Windows skill is the semantic reference.

### build-zoom-video-sdk-app
- id: zoom:video-sdk (source path: plugins/zoom/skills/video-sdk/SKILL.md)
- description: "Use when using Video SDK."
- use when: A custom video product with app-owned UX and session lifecycle on any platform, not a real Zoom meeting: confirms fit, platform, server-side session tokens, then join, publish/subscribe, share, chat; advanced media later. Parent of the zoom-video-sdk-* skills and ui-toolkit; the fork against build-zoom-meeting-sdk-app.

### ui-toolkit
- id: zoom:ui-toolkit (source path: plugins/zoom/skills/ui-toolkit/SKILL.md)
- description: "Use when using Zoom UI Toolkit."
- use when: A prebuilt web UI for a custom Video SDK session (chat, captions, recording, theming), mounted in the app shell. Not for Meeting SDK joins; deep media layout control routes to build-zoom-video-sdk-app, with zoom-video-sdk-web linked as the web reference.

### probe-sdk
- id: zoom:probe-sdk (source path: plugins/zoom/skills/probe-sdk/SKILL.md)
- description: "Use when using Probe SDK."
- use when: Pre-join readiness checks in the browser (support, camera, mic, speaker, network, CPU) with an allow/warn/block policy before a Meeting SDK or Video SDK join. Diagnoses only; never joins.

### zoom-video-sdk-web
- id: zoom:video-sdk/web (source path: plugins/zoom/skills/video-sdk/web/SKILL.md)
- description: "Zoom Video SDK for Web - JavaScript/TypeScript integration for browser-based video sessions, real-time communication, screen sharing, recording, and live transcription"
- use when: A browser app (JS/TS, React, Next.js, Vue) with custom video sessions, screen share, chat, recording or transcription; the most developed Video SDK platform skill. Custom UI around a real meeting is zoom-meeting-sdk-web-component-view instead.
- side effects: leave(true) ends the session for everyone (host-only)

### zoom-video-sdk-windows
- id: zoom:video-sdk/windows (source path: plugins/zoom/skills/video-sdk/windows/SKILL.md)
- description: "Zoom Video SDK for Windows - C++ integration for video sessions, raw audio/video capture, screen sharing, recording, and real-time communication"
- use when: A Windows C++ or C# (C++/CLI) app on the Video SDK: Canvas rendering or raw data capture/injection, Win32/WinForms/WPF, or a join where callbacks never fire (message pump).
- needs: Windows 10 1903+/11, Visual Studio 2019/2022 with C++ and .NET workloads

### zoom-video-sdk-linux
- id: zoom:video-sdk/linux (source path: plugins/zoom/skills/video-sdk/linux/SKILL.md)
- description: "Zoom Video SDK for Linux - C++ headless bots, raw audio/video capture/injection, Qt/GTK integration, Docker support"
- use when: C++ headless bots, raw audio/video capture or injection, Docker or Qt/GTK apps on the Video SDK for Linux (raw data only, no Canvas). A bot inside a real Zoom meeting is zoom-meeting-sdk-linux.
- needs: Ubuntu 20.04+/Debian 11+, GCC 9+, CMake 3.14+, PulseAudio, GLib main loop
- side effects: instructs the user to run apt install, write ~/.config/zoomus.conf and copy Qt libraries

### zoom-video-sdk-flutter
- id: zoom:video-sdk/flutter (source path: plugins/zoom/skills/video-sdk/flutter/SKILL.md)
- description: "Zoom Video SDK for Flutter. Use when building custom video session apps in Flutter with flutter_zoom_videosdk, event-driven architecture, session lifecycle handling, and mobile platform integration patterns."
- use when: A Flutter app on the Video SDK with flutter_zoom_videosdk; a navigation index into lifecycle, setup and events.

### zoom-video-sdk-react-native
- id: zoom:video-sdk/react-native (source path: plugins/zoom/skills/video-sdk/react-native/SKILL.md)
- description: "Zoom Video SDK for React Native. Use when building custom mobile video session experiences with @zoom/react-native-videosdk, event listeners, helper-based APIs, and backend JWT token flows."
- use when: A React Native app on the Video SDK with @zoom/react-native-videosdk; a navigation index covering provider, helper APIs and events. Not for real meetings (zoom-meeting-sdk-react-native).

### zoom-video-sdk-android
- id: zoom:video-sdk/android (source path: plugins/zoom/skills/video-sdk/android/SKILL.md)
- description: "Zoom Video SDK for Android native apps. Use when building custom Android video experiences with full UI control, session tokens, raw media options, and event-driven participant state."
- use when: A native Android app with custom Video SDK sessions; a reading-order index, no inline code.

### zoom-video-sdk-ios
- id: zoom:video-sdk/ios (source path: plugins/zoom/skills/video-sdk/ios/SKILL.md)
- description: "Zoom Video SDK for iOS native apps. Use when building custom iOS video sessions with full UI control, token-based session auth, and event-driven media/participant flows."
- use when: A native iOS app with custom Video SDK sessions; a reading-order index, no inline code.

### zoom-video-sdk-macos
- id: zoom:video-sdk/macos (source path: plugins/zoom/skills/video-sdk/macos/SKILL.md)
- description: "Zoom Video SDK for macOS native desktop apps. Use when building custom macOS video sessions with native UI control, tokenized join, and desktop-oriented media/device workflows."
- use when: A native macOS desktop app with Video SDK sessions; a reading-order index, no inline code. The parent does not link it.

### zoom-video-sdk-unity
- id: zoom:video-sdk/unity (source path: plugins/zoom/skills/video-sdk/unity/SKILL.md)
- description: "Zoom Video SDK for Unity wrapper integrations. Use when building custom Unity-based video session experiences and mapping Unity scene/UI state to Video SDK events."
- use when: A Unity app on the Video SDK wrapper, mapping Unity scene/UI state to SDK events; a reading-order index. The parent does not link it.

### zoom-apps-sdk
- id: zoom:zoom-apps-sdk (source path: plugins/zoom/skills/zoom-apps-sdk/SKILL.md)
- description: "Use when using Apps SDK."
- use when: An app that runs inside the Zoom client (meeting, webinar, main client, phone; collaborate, immersive, camera mode, Layers API): Marketplace config, allowed domains and in-client OAuth first, then zoomSdk gated by capability. Only embedding a meeting in an external app is Meeting SDK.

### build-zoom-bot
- id: zoom:build-zoom-bot (source path: plugins/zoom/skills/build-zoom-bot/SKILL.md)
- description: "Use when building bots."
- use when: "An assistant that joins meetings, records audio, transcribes live or acts during the meeting": clarifies join, observe, transcribe, summarize or act, then routes to Meeting SDK (visible participant) and zoom-rtms, with REST and webhooks as needed. Architecture only; live and batch transcription are different workflows.
- side effects: downstream implementations join real meetings and capture media

### zoom-rtms
- id: zoom:rtms (source path: plugins/zoom/skills/rtms/SKILL.md)
- description: "Use when using RTMS."
- use when: A backend needs live meeting media (audio, video, share, chat, live transcript) or Contact Center voice streamed to a server for AI or transcription, with no visible participant. Needs identity or controls: zoom-meeting-sdk-linux; stored files: scribe.
- needs: an RTMS-enabled Zoom app, event subscription and stream authorization

### scribe
- id: zoom:scribe (source path: plugins/zoom/skills/scribe/SKILL.md)
- description: "Use when using Scribe."
- use when: Transcribing uploaded or stored audio/video files with Zoom AI Services Scribe (fast or batch mode); live media is zoom-rtms or a Meeting SDK bot.
- needs: Build-platform credentials and JWT handling; supported file format and size

### build-zoom-phone-integration
- id: zoom:phone (source path: plugins/zoom/skills/phone/SKILL.md)
- description: "Use when building Phone."
- use when: Zoom Phone in CRM calling, call events, Smart Embed, number management or call-handling automation; confirms actor, phone license/entitlements and scopes first. Not Contact Center engagements.
- side effects: can initiate calls and manage telephony resources

### build-zoom-contact-center-app
- id: zoom:contact-center (source path: plugins/zoom/skills/contact-center/SKILL.md)
- description: "Use when using Contact Center."
- use when: Zoom Contact Center engagements, campaigns, video or chat channels, Virtual Agent handoff or scheduled callbacks: picks channel and client, then the web, Android or iOS leaf before coding.

### zoom-contact-center-web
- id: zoom:contact-center/web (source path: plugins/zoom/skills/contact-center/web/SKILL.md)
- description: "Zoom Contact Center SDK for Web. Use for web chat/video/campaign embeds, engagement event handling, app-context integrations, and Smart Embed postMessage workflows."
- use when: Contact Center chat/video/campaign on a website, engagement context inside Zoom, or Smart Embed postMessage events; separates in-client Zoom Apps APIs, external embed and iframe modes; wait for zoomCampaignSdk:ready.

### zoom-contact-center-android
- id: zoom:contact-center/android (source path: plugins/zoom/skills/contact-center/android/SKILL.md)
- description: "Zoom Contact Center SDK for Android. Use for native Android chat/video/ZVA/scheduled callback integrations, campaign mode, service lifecycle, and rejoin handling."
- use when: Contact Center chat, video, ZVA, scheduled callback or campaign entry in a native Android app, including reliable rejoin (initialize in Application.onCreate; entryId versus apiKey by channel).

### zoom-contact-center-ios
- id: zoom:contact-center/ios (source path: plugins/zoom/skills/contact-center/ios/SKILL.md)
- description: "Zoom Contact Center SDK for iOS. Use for native iOS chat/video/ZVA/scheduled callback integrations, app lifecycle bridging, rejoin flow, and callback handling."
- use when: Contact Center chat, video, ZVA or callback in a native iOS app that loses state on backgrounding or cannot resume the video engagement (set context first, forward app lifecycle, wire rejoin URL).

### build-zoom-virtual-agent
- id: zoom:virtual-agent (source path: plugins/zoom/skills/virtual-agent/SKILL.md)
- description: "Use when using Virtual Agent."
- use when: Embedding or wrapping Zoom Virtual Agent (the support chatbot product): identifies the client, then routes to the web, Android or iOS leaf; needs a campaign or entry ID and allowed origins. Not build-zoom-team-chat-app.

### zoom-virtual-agent-web
- id: zoom:virtual-agent/web (source path: plugins/zoom/skills/virtual-agent/web/SKILL.md)
- description: "Zoom Virtual Agent SDK for web embeds. Use for campaign or entry ID chat launch, event-driven controls, user context updates, and CSP-safe deployment."
- use when: Virtual Agent on a website by campaign or entry ID: show/hide/open/close, user context updates and CSP; gate calls behind readiness.

### zoom-virtual-agent-android
- id: zoom:virtual-agent/android (source path: plugins/zoom/skills/virtual-agent/android/SKILL.md)
- description: "Zoom Virtual Agent Android integration via WebView. Use for Java/Kotlin bridge callbacks, native URL handling, support_handoff relay, and lifecycle-safe embedding."
- use when: Virtual Agent in an Android WebView: inject window.zoomCampaignSdkConfig, JS bridge for exit/common/support_handoff, URL policy.

### zoom-virtual-agent-ios
- id: zoom:virtual-agent/ios (source path: plugins/zoom/skills/virtual-agent/ios/SKILL.md)
- description: "Zoom Virtual Agent iOS integration via WKWebView. Use for Swift/Objective-C script injection, message handlers, support_handoff relay, and URL routing policies."
- use when: Virtual Agent in an iOS WKWebView: WKUserScript config injection, message handlers for exit/common/handoff, navigation URL routing.

### zoom-cobrowse-sdk
- id: zoom:cobrowse-sdk (source path: plugins/zoom/skills/cobrowse-sdk/SKILL.md)
- description: "Use when using Cobrowse."
- use when: A support agent co-browsing the customer's website via session PIN/link, with masked fields and controlled remote assistance; only once co-browse is the settled choice. Auth and origins before UI, privacy masking early.
- side effects: shares the customer's page and may allow remote assistance

### debug-zoom
- id: zoom:debug-zoom (source path: plugins/zoom/skills/debug-zoom/SKILL.md)
- description: "Use when debugging issues."
- use when: "Zoom login, an API call, event delivery or meeting join is broken": the broad failure entry; names the failing layer, asks only for missing evidence, ranks 2-4 causes, short verification plan. Recommend this first.

### debug-zoom-integration
- id: zoom:debug-zoom-integration (source path: plugins/zoom/skills/debug-zoom-integration/SKILL.md)
- description: "Use when isolating failures."
- use when: The same broken integration when you want the fixed triage order: auth/app configuration, request or event verification, SDK init/platform mismatch, media/session behavior, client capability assumptions. Overlaps debug-zoom heavily; token/scope failures continue to zoom-oauth.
