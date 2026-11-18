# openai/plugins family: build-ios-apps (Build iOS Apps)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `build-ios-apps` family. The catalog entry is in openai-platforms.md.

## Family: build-ios-apps
- source path: `plugins/build-ios-apps` (v0.1.2, author OpenAI, MIT)
- manifest notes: Codex manifest only (`.codex-plugin/plugin.json`); no Claude or Cursor manifest. One MCP server in `.mcp.json`: `xcodebuildmcp`, launched with `npx -y xcodebuildmcp@latest mcp` (unpinned), env `XCODEBUILDMCP_ENABLED_WORKFLOWS=simulator,ui-automation,debugging,logging`. No auth policy, hooks or commands. Implied requirements: macOS, Xcode and Simulator, Node/npx; Homebrew only for `ios-ettrace-performance`. Two skills name Codex-specific surfaces (in-app browser; TTY for `ettrace`).
- router: none. The README lists the nine skills. Cross-links only: `ios-ettrace-performance` and `ios-memgraph-leaks` pair with `ios-debugger-agent` for build, launch and driving the app; `ios-simulator-browser` takes its simulator UDID from the build/run workflow. No fixed sequence or plugin-level gates.
- development distance: core-dev
- disclosure: rich. No router, and the nine skills cover different scenarios (authoring, refactor, system integration, run and drive, three kinds of performance or leak evidence).

### ios-app-intents
- id: build-ios-apps:ios-app-intents (source path: plugins/build-ios-apps/skills/ios-app-intents/SKILL.md)
- description: "Design App Intents, app entities, and App Shortcuts for iOS system surfaces. Use when exposing app actions or content to Shortcuts, Siri, Spotlight, widgets, or controls."
- use when: "Make my app's actions available in Shortcuts, Siri, Spotlight, widgets or controls." Produces a small App Intents layer (1-3 intents, a few entities, shortcuts provider) and checks it builds.
- not for: `swiftui-ui-patterns` (screens inside the app, not system surfaces).
- needs: An iOS app codebase and Xcode; the skill tells the agent to check Apple docs by web search.
- side effects: writes local files (intents target and types).
- part of: standalone.

### ios-debugger-agent
- id: build-ios-apps:ios-debugger-agent (source path: plugins/build-ios-apps/skills/ios-debugger-agent/SKILL.md)
- description: "Build, run, and debug iOS apps on Simulator with XcodeBuildMCP. Use when launching an app, inspecting simulator UI or logs, or diagnosing runtime behavior."
- use when: "Build and run the app on the simulator, tap through it, read the logs." Order: pick the booted simulator, set session defaults, build and run, verify launch, then interact and capture logs.
- not for: `ios-simulator-browser` (watch the simulator in a browser or hot-reload previews); `swiftui-performance-audit` and `ios-ettrace-performance` (profiling, which this skill does not do).
- needs: The plugin's xcodebuildmcp MCP server (tools named `mcp__XcodeBuildMCP__*`), Node/npx, Xcode project and scheme, a booted simulator (asks the user to boot one; never boots unasked).
- side effects: builds and launches the app in the simulator; fetches `xcodebuildmcp@latest` via npx.
- part of: foundation skill; `ios-ettrace-performance` and `ios-memgraph-leaks` pair with it. Not a fixed-sequence entry.

### ios-ettrace-performance
- id: build-ios-apps:ios-ettrace-performance (source path: plugins/build-ios-apps/skills/ios-ettrace-performance/SKILL.md)
- description: "Capture and interpret iOS Simulator ETTrace profiles. Use when profiling launch or runtime latency, comparing traces, or finding CPU-heavy stacks."
- use when: "Profile launch or runtime latency of this app on the simulator, find the CPU-heavy stacks, compare before/after traces." Gives a flamegraph summary; refuses conclusions from an unsymbolicated trace.
- not for: `swiftui-performance-audit` (code-first diagnosis, user supplies Instruments traces); `ios-memgraph-leaks` (memory, not CPU).
- needs: macOS, Homebrew `ettrace`, a simulator-architecture ETTrace.xcframework (vendored or built from a git clone), UUID-matched dSYMs; a TTY in Codex.
- side effects: installs ETTrace with Homebrew if missing; clones/builds the framework if no compatible vendored copy exists; temporarily links it into the app target (removed afterwards unless asked to keep), builds/runs the app and writes trace artifacts.
- part of: pairs with `ios-debugger-agent` for build, launch and driving the flow.

### ios-memgraph-leaks
- id: build-ios-apps:ios-memgraph-leaks (source path: plugins/build-ios-apps/skills/ios-memgraph-leaks/SKILL.md)
- description: "Capture and inspect iOS leaks and memgraphs. Use when debugging leaked objects, retain cycles, memory growth, or before/after leak evidence."
- use when: "This screen leaks objects or memory keeps growing; find the retain cycle and prove it is fixed." Captures a memgraph from a live simulator process or reads an existing one, then proves before/after.
- not for: `ios-ettrace-performance` (CPU latency); `swiftui-performance-audit` (rendering and code-level smells, no leak proof).
- needs: Xcode command line tools (`leaks`, `xcrun simctl`), simulator UDID and bundle ID; bundled capture and summary scripts.
- side effects: writes memgraph captures to a temp folder; makes the smallest root-cause code patch. A smaller memgraph alone is not accepted as a fix.
- part of: pairs with `ios-debugger-agent` to reproduce the flow.

### ios-simulator-browser
- id: build-ios-apps:ios-simulator-browser (source path: plugins/build-ios-apps/skills/ios-simulator-browser/SKILL.md)
- description: "Mirror an iOS Simulator into the Codex in-app browser and render SwiftUI previews from importable Swift packages in that simulator with hot reload. Use when a user wants to watch or interact with an iOS app in the browser, see a SwiftUI preview outside Xcode Canvas, iterate live on a preview, or capture browser-visible simulator proof."
- use when: "Let me watch or drive the simulator in a browser," or see a SwiftUI preview outside Xcode Canvas with hot reload. Previews work only for Swift-package-backed `#Preview` or `PreviewProvider`.
- not for: `ios-debugger-agent` (drives the app through MCP tools, no browser); `swiftui-ui-patterns` (code structure, not rendering).
- needs: Codex in-app browser, Node/npx (`serve-sim@latest`, unpinned), a simulator UDID, a Swift package for previews.
- side effects: runs a long-lived helper process; generates a disposable host project outside the source tree, installs/launches it in Simulator and rebuilds/hot-swaps a dylib on package edits; never edits `.xcodeproj`, `Package.swift` or schemes to force previews.
- part of: standalone; obtains the UDID from the existing build/run workflow or `xcrun simctl list devices available`.

### swiftui-liquid-glass
- id: build-ios-apps:swiftui-liquid-glass (source path: plugins/build-ios-apps/skills/swiftui-liquid-glass/SKILL.md)
- description: "Implement and review iOS 26+ SwiftUI Liquid Glass UI. Use when adopting Liquid Glass or checking its correctness, performance, and design fit."
- use when: "Adopt or review iOS 26 Liquid Glass in this SwiftUI feature." Uses native glass APIs with `#available(iOS 26, *)` gating and a non-glass fallback.
- not for: `liquid-glass` (build-macos-apps, Mac apps); `swiftui-ui-patterns` (general component patterns).
- needs: SwiftUI code with an iOS 26+ target or availability gating.
- side effects: writes local files.
- part of: standalone.

### swiftui-performance-audit
- id: build-ios-apps:swiftui-performance-audit (source path: plugins/build-ios-apps/skills/swiftui-performance-audit/SKILL.md)
- description: "Audit SwiftUI runtime performance from code first. Use when diagnosing slow rendering, janky scrolling, expensive updates, or profiling needs."
- use when: "My SwiftUI screen is janky, updates too often or hangs; diagnose why." Code-first smell review; if inconclusive, the user captures an Instruments trace and the skill analyzes it, then verifies against a baseline.
- not for: `ios-ettrace-performance` (the agent captures a measured simulator profile); `swiftui-view-refactor` (restructures without performance analysis).
- needs: SwiftUI code, or the user's description; Instruments traces come from the user (the skill captures none).
- side effects: edits local source in the remediation step; asks the user to re-run profiling for verification.
- part of: standalone; a diagnosis step before fixes or `swiftui-view-refactor`.

### swiftui-ui-patterns
- id: build-ios-apps:swiftui-ui-patterns (source path: plugins/build-ios-apps/skills/swiftui-ui-patterns/SKILL.md)
- description: "Build and refactor SwiftUI UI with component patterns and examples. Use when shaping navigation, state, layouts, controls, or screen composition."
- use when: "Build this SwiftUI screen" or choose navigation, state, sheet, list or tab patterns. Default SwiftUI authoring skill; ends with a build and preview check.
- not for: `swiftui-view-refactor` (restructure an existing large view); `swiftui-performance-audit` (slowness); `swiftui-patterns` (build-macos-apps, Mac scenes and windows).
- needs: SwiftUI code and Xcode.
- side effects: writes local files.
- part of: standalone; the broad authoring skill, with specialists beside it.

### swiftui-view-refactor
- id: build-ios-apps:swiftui-view-refactor (source path: plugins/build-ios-apps/skills/swiftui-view-refactor/SKILL.md)
- description: "Refactor SwiftUI view files into stable, testable structure. Use when splitting large views, tightening data flow, or cleaning Observation ownership."
- use when: "This SwiftUI view file is huge; split it and clean up state ownership without changing behavior." Prefers MV over adding view models; splits files over about 300 lines.
- not for: `swiftui-ui-patterns` (new views); `view-refactor` (build-macos-apps, Mac scenes and AppKit escapes).
- needs: SwiftUI source.
- side effects: rewrites local files; keeps layout and logic intact unless asked.
- part of: standalone.
