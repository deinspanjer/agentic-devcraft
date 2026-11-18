# openai/plugins family: expo (Expo)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `expo` family. The catalog entry is in openai-platforms.md.

## Family: expo
- source path: `plugins/expo`
- manifest notes: Codex plugin manifest only (.codex-plugin, v1.0.2, Expo Team, MIT, category Developer Tools; marketplace products [CODEX]). No MCP, app connector or hooks. Ships one command document `/setup-codex-run-actions` (sets up the Codex app Run button). No auth declared in the manifest; deployment, dev-client and api-routes skills assume `eas-cli` and `eas login`.
- router: none. Skills are independent; informal hints only (building-native-ui and expo-dev-client both say try Expo Go first; expo-module leads to expo-dev-client; expo-deployment includes EAS Workflows examples but does not explicitly name expo-cicd-workflows).
- development distance: core-dev
- disclosure: rich. No router, and the 13 skills cover genuinely different scenarios (UI, networking, server routes, native modules, builds, release, upgrades), with one styling split: inline styles by default (`building-native-ui`), `expo-tailwind-setup` only when the user asks for Tailwind.

### building-native-ui
- id: expo:building-native-ui (source path: plugins/expo/skills/building-native-ui/SKILL.md)
- description: "Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native tabs."
- use when: I'm building screens, navigation, tabs, sheets or styling in an Expo Router app and want it to feel native (iOS-style). Default skill for any Expo Router UI work.
- not for: expo-tailwind-setup (this skill says use inline styles, not Tailwind; choose by whether the user wants Tailwind); expo-ui-swift-ui and expo-ui-jetpack-compose (native views instead of React Native views).
- needs: An Expo Router project; partly iOS-centric.
- side effects: local UI/config edits, including removal of old routes when restructuring; starts Expo Go for verification and may create custom native builds when required
- part of: standalone; try Expo Go before a custom build.

### expo-tailwind-setup
- id: expo:expo-tailwind-setup (source path: plugins/expo/skills/expo-tailwind-setup/SKILL.md)
- description: "Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling"
- use when: Set up Tailwind/NativeWind in my Expo app.
- not for: building-native-ui takes the opposite stance (inline styles, no Tailwind); choose by whether the user wants Tailwind.
- needs: npx expo install of pinned preview/nightly packages (nativewind 5 preview, react-native-css nightly).
- side effects: modifies metro config, package.json and CSS; may delete babel.config.js
- part of: standalone.

### expo-ui-swift-ui
- id: expo:expo-ui-swift-ui (source path: plugins/expo/skills/expo-ui-swift-ui/SKILL.md)
- description: "`@expo/ui/swift-ui` package lets you use SwiftUI Views and modifiers in your app."
- use when: Use SwiftUI views from Expo (@expo/ui/swift-ui) on iOS. SDK 55 only.
- not for: expo-ui-jetpack-compose (Android); expo-module (when a view or modifier is missing and a local module is needed; confirm with the user first).
- needs: npx expo install @expo/ui; native rebuild (npx expo run:ios).
- side effects: writes local files; adds a dependency
- part of: standalone.

### expo-ui-jetpack-compose
- id: expo:expo-ui-jetpack-compose (source path: plugins/expo/skills/expo-ui-jetpack-compose/SKILL.md)
- description: "`@expo/ui/jetpack-compose` package lets you use Jetpack Compose Views and modifiers in your app."
- use when: Use Jetpack Compose / Material 3 views from Expo (@expo/ui/jetpack-compose) on Android. SDK 55 only.
- not for: expo-ui-swift-ui (iOS side); building-native-ui (React Native views).
- needs: npx expo install @expo/ui; native rebuild (npx expo run:android).
- side effects: writes local files; adds a dependency
- part of: standalone; mirror of expo-ui-swift-ui.

### use-dom
- id: expo:use-dom (source path: plugins/expo/skills/use-dom/SKILL.md)
- description: "Use Expo DOM components to run web code in a webview on native and as-is on web. Migrate web code to native incrementally."
- use when: Run web-only React code (recharts, syntax highlighters, rich text, canvas/WebGL) inside an Expo app using 'use dom' components.
- not for: expo-module (deep native integration); building-native-ui (native UI).
- needs: An Expo app; runs in a webview with serializable props only.
- side effects: writes local files
- part of: standalone.

### native-data-fetching
- id: expo:native-data-fetching (source path: plugins/expo/skills/native-data-fetching/SKILL.md)
- description: "Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, and Expo Router data loaders (`useLoaderData`)."
- use when: Any network, API, fetch, caching, offline, auth-token or env-var work in an Expo app; the skill declares itself mandatory for networking.
- not for: expo-api-routes (server-side code).
- needs: nothing beyond the repo; optional React Query, NetInfo, expo-secure-store.
- side effects: writes local files
- part of: standalone. Rules: prefer expo/fetch over axios; no secrets in EXPO_PUBLIC_*; tokens in SecureStore.

### expo-api-routes
- id: expo:expo-api-routes (source path: plugins/expo/skills/expo-api-routes/SKILL.md)
- description: "Guidelines for creating API routes in Expo Router with EAS Hosting"
- use when: I need server-side code in my Expo app (hide an API key, proxy an API, webhook, database access) using Expo Router +api.ts routes.
- not for: native-data-fetching (client-side calls); expo-deployment (store and web release). Skill lists when not to use it: public data, simple CRUD, uploads, auth-only.
- needs: Expo Router; for deploy, eas-cli, eas login and an EAS project.
- side effects: eas deploy to EAS Hosting and eas env:create write production secrets and deploy
- part of: standalone; deploy path overlaps expo-deployment.

### expo-module
- id: expo:expo-module (source path: plugins/expo/skills/expo-module/SKILL.md)
- description: "Guide for writing Expo native modules and views using the Expo Modules API (Swift, Kotlin, TypeScript). Covers module definition DSL, native views, shared objects, config plugins, lifecycle hooks, autolinking, and type system. Use when building or modifying native modules for Expo."
- use when: Write a native Swift/Kotlin module or native view for Expo with the Expo Modules API, including config plugins and autolinking.
- not for: expo-ui-swift-ui (use existing @expo/ui SwiftUI views rather than writing a module).
- needs: Node; Xcode/Android toolchain to build; pod install after renaming the scaffold.
- side effects: writes local files; scaffolds with create-expo-module
- part of: standalone; leads into expo-dev-client to run the native code.

### expo-dev-client
- id: expo:expo-dev-client (source path: plugins/expo/skills/expo-dev-client/SKILL.md)
- description: "Build and distribute Expo development clients locally or via TestFlight"
- use when: I need a custom development build (native modules or Apple targets) on a device or TestFlight because Expo Go is not enough.
- not for: expo-deployment (production); expo-module (writes the native code that makes a dev client necessary).
- needs: eas-cli and login; Xcode for local iOS builds; Apple credentials for TestFlight.
- side effects: edits eas.json; local or cloud builds, device/simulator installation, dev-server startup and optional TestFlight submission
- part of: standalone; downstream of expo-module or 'Expo Go insufficient'.

### upgrading-expo
- id: expo:upgrading-expo (source path: plugins/expo/skills/upgrading-expo/SKILL.md)
- description: "Guidelines for upgrading Expo SDK versions and fixing dependency issues"
- use when: Upgrade the Expo SDK or fix dependency problems after an upgrade.
- needs: Package manager; pods/Gradle for bare projects.
- side effects: modifies dependencies and config; removes node_modules/.expo and clears Watchman watches; prebuild --clean regenerates native directories only when native changes are needed, at least one native directory exists, and the app is not bare workflow
- part of: standalone.

### expo-deployment
- id: expo:expo-deployment (source path: plugins/expo/skills/expo-deployment/SKILL.md)
- description: "Deploying Expo apps to iOS App Store, Android Play Store, web hosting, and API routes"
- use when: Ship my Expo app: EAS production builds, TestFlight/App Store/Play Store submission, web deploy via EAS Hosting, version management.
- not for: expo-dev-client (development builds, not production); expo-cicd-workflows (automation YAML).
- needs: eas-cli and eas login; Apple and Google credentials and store accounts.
- side effects: installs EAS CLI, edits local config, runs cloud builds, store submissions and production deploys; the skill has no confirm-before-submit gate
- part of: standalone; includes EAS Workflows examples and links workflow references; expo-cicd-workflows is the related automation specialist, not an explicit handoff.

### expo-cicd-workflows
- id: expo:expo-cicd-workflows (source path: plugins/expo/skills/expo-cicd-workflows/SKILL.md)
- description: "Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation."
- use when: Write or fix EAS Workflow YAML in .eas/workflows/ for build pipelines and deploy automation.
- not for: expo-deployment (manual eas build/submit commands and store guides).
- needs: Node; network to api.expo.dev and raw.githubusercontent.com (fetches the live schema first).
- side effects: runs npm install inside the skill's own scripts directory if modules are missing; otherwise writes workflow YAML
- part of: standalone; complements expo-deployment's automated-deployment examples.

### codex-expo-run-actions
- id: expo:codex-expo-run-actions (source path: plugins/expo/skills/codex-expo-run-actions/SKILL.md)
- description: "Wire Expo projects into the Codex app with project-local run scripts and .codex/environments/environment.toml actions. Use when the user wants the Codex app Run button, build/run actions, action buttons, or a stable Expo start/run workflow from Codex."
- use when: I want the Codex app's Run button or action buttons to start my Expo project.
- not for: expo-dev-client (builds) and expo-deployment (cloud); this is local dev-server wiring only.
- needs: Expo app root; Codex app specific (.codex/environments). Defaults to expo start / Expo Go.
- side effects: writes local files: script/build_and_run.sh and .codex/environments/environment.toml; does not wire eas build/submit unless asked
- part of: standalone; paired with the plugin command /setup-codex-run-actions.
