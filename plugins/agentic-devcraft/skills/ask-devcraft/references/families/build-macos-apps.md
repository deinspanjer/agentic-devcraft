# openai/plugins family: build-macos-apps (Build macOS Apps)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `build-macos-apps` family. The catalog entry is in openai-platforms.md.

## Family: build-macos-apps
- source path: `plugins/build-macos-apps` (v0.1.4)
- manifest notes: Codex manifest only; no MCP server, app connector, hooks or auth policy. Shell-first (`xcodebuild`, `swift`, `open`, `lldb`, `codesign`, `spctl`, `plutil`, `log stream`). An Xcode-aware MCP is used only if already available and explicitly requested. Ships three command documents (`/build-and-run-macos-app`, `/fix-codesign-error`, `/test-macos-app`) that the manifest does not register; host discovery is unverified. Declared out of scope: mobile simulator control, desktop UI automation, App Store Connect release management, pixel-perfect design-system generation. The Run-button file `.codex/environments/environment.toml` is Codex-app specific; the shell loop is not.
- router: none. Two entry points: `swiftui-patterns` (new scaffold, bootstraps through `build-run-debug`) and `build-run-debug` (owns `script/build_and_run.sh`: stop app, build, launch fresh; hands event logging to `telemetry`). `telemetry`, `window-management` and `liquid-glass` call back into `build-run-debug`; four skills hand to `appkit-interop` only for a real SwiftUI capability gap.
- development distance: core-dev
- disclosure: rich. No router, and the eleven skills cover different scenarios (scaffold, launch, signing, shipping, tests, windows, glass, AppKit bridge), each with its own gates.
- source inconsistency: `swiftpm-macos` recommends `swift run <product>` with no GUI exception, while `build-run-debug` forbids raw SwiftPM GUI launch (stages a `.app` and uses `open -n`). Route GUI launch to `build-run-debug`.

### appkit-interop
- id: build-macos-apps:appkit-interop (source path: plugins/build-macos-apps/skills/appkit-interop/SKILL.md)
- description: "Bridge macOS SwiftUI into AppKit narrowly. Use when implementing representables, reaching NSWindow or panels, handling menus, or using the responder chain."
- use when: "This SwiftUI Mac feature needs an open/save panel, first-responder control, menu validation or an AppKit-only view." Names the capability gap first, then the smallest bridge; SwiftUI stays the state owner.
- not for: `swiftui-patterns` or `window-management` when SwiftUI scenes and modifiers already suffice; `view-refactor` (organize an existing bridge).
- needs: SwiftUI/AppKit source and the macOS Swift toolchain.
- side effects: writes local files.
- part of: standalone specialist; also the escape step from `swiftui-patterns`, `window-management`, `liquid-glass` and `view-refactor`.

### build-run-debug
- id: build-macos-apps:build-run-debug (source path: plugins/build-macos-apps/skills/build-run-debug/SKILL.md)
- description: "Build, run, and debug macOS apps with shell-first Xcode and Swift workflows. Use when launching apps or diagnosing build, startup, or runtime failures."
- use when: "Make this Mac app run," wire the Codex Run button, fix build or startup errors, read launch logs, or diagnose a symbolized crash.
- not for: `swiftpm-macos` (package graph, CLI products); `signing-entitlements` (verified signing blocker); `test-triage` (failing tests).
- needs: `.xcworkspace`, `.xcodeproj` or `Package.swift`; Xcode/Swift tools, git, `open`; Codex app only for the Run button.
- side effects: may `git init` an unversioned project; writes `script/build_and_run.sh` and the environment file; kills the matching process before build; launches the app.
- part of: entry point of the build/run/debug sequence and shared bootstrap for `swiftui-patterns`, `window-management`, `liquid-glass`; hands to `telemetry`.

### liquid-glass
- id: build-macos-apps:liquid-glass (source path: plugins/build-macos-apps/skills/liquid-glass/SKILL.md)
- description: "Implement and review macOS SwiftUI Liquid Glass UI. Use when adopting system glass, removing conflicting custom chrome, or building glass surfaces."
- use when: "Our Mac sidebar, toolbar or sheet has opaque or custom blur that fights system glass; modernize it." Standard system structure first, custom glass only where uncovered.
- not for: `window-management` (window chrome and placement); `swiftui-liquid-glass` (build-ios-apps, iOS). Do not borrow the 15+ figure from `window-management`: its minimum target is unstated.
- needs: SwiftUI scenes and an SDK with `glassEffect` APIs; a runnable `.app` to judge behavior.
- side effects: writes local files.
- part of: standalone; hands to `swiftui-patterns`, `view-refactor`, `appkit-interop` or `build-run-debug` by problem type.

### packaging-notarization
- id: build-macos-apps:packaging-notarization (source path: plugins/build-macos-apps/skills/packaging-notarization/SKILL.md)
- description: "Prepare macOS packaging and notarization workflows. Use when archiving apps, validating bundles, or explaining distribution-only failures."
- use when: "Can I ship this archive or exported app?" or a failure that appears only in distributed builds. Reports readiness and the top missing prerequisite.
- not for: `signing-entitlements` (diagnose a specific signature, trust or entitlement fault); `build-run-debug` (local run). Notarization is not needed for local debug.
- needs: An archive or exported `.app` preferably; signing identity evidence.
- side effects: none; read-only. Does not submit, upload or set up credentials.
- part of: standalone distribution-readiness specialist.

### signing-entitlements
- id: build-macos-apps:signing-entitlements (source path: plugins/build-macos-apps/skills/signing-entitlements/SKILL.md)
- description: "Inspect macOS signing, entitlements, and Gatekeeper issues. Use when diagnosing code signing, sandbox, hardened runtime, or trust failures."
- use when: "macOS refuses to launch this app," signature invalid, sandbox access fails, entitlements mismatch, or Gatekeeper or hardened runtime is suspected.
- not for: `packaging-notarization` (shipping readiness); `build-run-debug` (compiler, linker, runtime failures outside signing).
- needs: The `.app` or binary and its entitlements; `codesign`, `spctl`, `plutil`, `security find-identity`.
- side effects: none; read-only. Explains the repair; never invents entitlements or re-signs automatically.
- part of: natural follow-on after `build-run-debug` classifies a signing blocker; mirrors the `/fix-codesign-error` command.

### swiftpm-macos
- id: build-macos-apps:swiftpm-macos (source path: plugins/build-macos-apps/skills/swiftpm-macos/SKILL.md)
- description: "Build, run, and test SwiftPM macOS packages and executables. Use when the repo is package-first or has no Xcode project."
- use when: "This repo is `Package.swift` only; build it, run the CLI product or run filtered tests."
- not for: `build-run-debug` for any GUI app, app bundle or foreground activation (this skill's `swift run` advice lacks the GUI exception); `test-triage` (classify failing tests). Library-only packages are not runnable.
- needs: `Package.swift` and the Swift toolchain.
- side effects: builds and runs local code; dependency resolution fetches packages.
- part of: standalone package-first workflow.

### swiftui-patterns
- id: build-macos-apps:swiftui-patterns (source path: plugins/build-macos-apps/skills/swiftui-patterns/SKILL.md)
- description: "Build macOS SwiftUI scenes and components with desktop patterns. Use when shaping windows, commands, toolbars, settings, split views, or inspectors."
- use when: "Create a native Mac app or scene," pick document, sidebar-detail or menu-bar behavior, add settings, commands, inspectors, or decide which window owns selection.
- not for: `view-refactor` (reorganize an oversized existing file); `window-management` (individual window policies); `liquid-glass` (materials); `swiftui-ui-patterns` (build-ios-apps, iOS screens).
- needs: Deployment target and SwiftUI/macOS toolchain; git; the `build-run-debug` bootstrap for new scaffolds.
- side effects: creates source and folders; may `git init` outside an existing repo; writes the run script.
- part of: entry point of the native UI/scaffold sequence; bootstraps via `build-run-debug`; hands to `appkit-interop`.

### telemetry
- id: build-macos-apps:telemetry (source path: plugins/build-macos-apps/skills/telemetry/SKILL.md)
- description: "Add and verify lightweight macOS runtime telemetry. Use when wiring Logger events or inspecting logs for windows, sidebars, menus, and actions."
- use when: "Did this sidebar selection, menu command or window action actually fire?" Adds the smallest feature-scoped `Logger` instrumentation and verifies it in the runtime logs.
- not for: `build-run-debug` (launch problems and crashes); `test-triage` (deterministic test failures).
- needs: App source, a runnable app, Console.app or `log stream`; no remote telemetry service.
- side effects: edits app code and emits local unified logs; no secrets or personal data in logs.
- part of: step inside `build-run-debug`; calls it for its own verify loop.

### test-triage
- id: build-macos-apps:test-triage (source path: plugins/build-macos-apps/skills/test-triage/SKILL.md)
- description: "Triage macOS tests across Xcode and SwiftPM. Use when narrowing failures, explaining assertions or crashes, or separating setup from regressions."
- use when: "A Mac test fails; is it a regression, or build, fixture, host-app, entitlement, crash or timing?" Runs the smallest failing scope and names the next step.
- not for: `swiftpm-macos` (general package build and test); `build-run-debug` (app startup); `frontend-testing-debugging` (browser-rendered web UI).
- needs: Xcode scheme and test target, or Swift package; `xcodebuild test` or `swift test`.
- side effects: runs the tests and their existing setup.
- part of: standalone; mirrors `/test-macos-app`.

### view-refactor
- id: build-macos-apps:view-refactor (source path: plugins/build-macos-apps/skills/view-refactor/SKILL.md)
- description: "Refactor macOS SwiftUI views and scenes into stable structure. Use when splitting large views, tightening scene state, or narrowing AppKit escapes."
- use when: "This giant SwiftUI file mixes entry point, views, state, services and AppKit objects," or selection swaps the whole root layout. Behavior is preserved; builds after each major split.
- not for: `swiftui-patterns` (new desktop structure); `appkit-interop` (add a missing capability); `swiftui-view-refactor` (build-ios-apps, iOS).
- needs: Buildable native SwiftUI source.
- side effects: rewrites and moves local files.
- part of: standalone; hands to `swiftui-patterns` or `appkit-interop`; may precede `liquid-glass`.

### window-management
- id: build-macos-apps:window-management (source path: plugins/build-macos-apps/skills/window-management/SKILL.md)
- description: "Customize macOS SwiftUI windows and scene behavior. Use when tuning window chrome, drag regions, placement, restoration, launch behavior, or borderless windows."
- use when: "Customize this Mac window": title and toolbar, drag region, borderless presentation, launch visibility, restoration, initial placement or Zoom sizing.
- not for: `swiftui-patterns` (overall scene design); `liquid-glass` (materials); `appkit-interop` when SwiftUI modifiers cannot express it.
- needs: `Window` or `WindowGroup` scenes; cited APIs need macOS 15+ (older targets need guards or AppKit).
- side effects: writes local files; verified by launching the app.
- part of: standalone specialist; verifies via `build-run-debug`.
