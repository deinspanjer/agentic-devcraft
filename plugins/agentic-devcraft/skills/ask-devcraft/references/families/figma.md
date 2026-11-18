# openai/plugins family: figma (Figma)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `figma` family. The catalog entry is in openai-platforms.md.

## Family: figma
- source path: `plugins/figma`
- manifest notes: Codex plugin manifest only (.codex-plugin, v2.0.20, Figma, license LicenseRef-Figma-Developer-Terms, category Creativity). MCP server `figma` at https://mcp.figma.com/mcp (OAuth) plus app connector in .app.json; marketplace authentication ON_INSTALL. Also ships four command documents, four agent prompt files and a draft PostToolUse hook that only echoes a reminder; the manifest declares only skills and apps, so do not promise a host exposes them. Code Connect needs an Organization or Enterprise plan; use_figma needs an existing file key. README is stale (names figma-implement-design and figma-create-design-system-rules, which are not skills here).
- router: none single router. Sequencing is by mandatory-prerequisite skills, each gating one MCP tool: figma-use before every use_figma call; figma-create-new-file before create_new_file; figma-generate-diagram before generate_diagram; figma-design-to-code before get_design_context. Companions load alongside figma-use (generate-design, generate-library, use-figjam, use-slides, use-motion, swiftui). figma-swiftui is a direction router (Figma to SwiftUI or SwiftUI to Figma) that asks when ambiguous.
- development distance: adjacent (design-to-code and code-to-design; most skills edit a Figma file rather than the repo)
- disclosure: rich. No router, and the skills cover different scenarios by direction (Figma to code vs code to Figma) and by editor (Design, FigJam, Slides, motion), each with its own gates.

### figma-design-to-code
- id: figma:figma-design-to-code (source path: plugins/figma/skills/figma-design-to-code/SKILL.md)
- description: "**MANDATORY prerequisite** — you MUST invoke this skill BEFORE calling the `get_design_context` Figma MCP tool. You MUST trigger this skill whenever the user wants to implement, build, port, or code up a Figma design as code. Example prompts (not exhaustive) are 'implement this Figma design', 'build this screen from Figma', 'turn this Figma into code', 'design to code'. This skill provides critical instructions and steps to the agent on how to correctly implement Figma designs in code and must NOT be skipped."
- use when: Implement, build or port this Figma design (URL with node-id) as code in my repo.
- not for: figma-generate-design (reverse direction, code to Figma). Swift targets and animation also use figma-swiftui and figma-implement-motion; they do not remove this prerequisite before get_design_context.
- needs: Figma MCP; a URL with node-id (ask if missing).
- side effects: writes local code; never writes to Figma. Committed code needs downloaded asset bytes, since exported asset URLs expire in about seven days
- part of: entry point for Figma-to-code; mandatory before get_design_context. Treat the React+Tailwind output as a reference to adapt to the project's stack.

### figma-implement-motion
- id: figma:figma-implement-motion (source path: plugins/figma/skills/figma-implement-motion/SKILL.md)
- description: "Translates Figma motion and animations into production-ready application code. Use when implementing animation/motion from a Figma design — user mentions "implement this motion", "add animation from Figma", "animate this component", provides a Figma URL whose node is animated, or when `get_design_context` returns motion data or instructs you to call `get_motion_context`."
- use when: Implement the animation from this Figma design in code (motion.dev, CSS keyframes, SwiftUI translation).
- not for: figma-use-motion (create or edit animation inside Figma); figma-design-to-code (static structure).
- needs: Figma MCP with get_motion_context and get_design_context; target codebase.
- side effects: writes local code
- part of: step alongside figma-design-to-code. Leaves node-specific TODOs for motion it cannot represent.

### figma-swiftui
- id: figma:figma-swiftui (source path: plugins/figma/skills/figma-swiftui/SKILL.md)
- description: "SwiftUI ↔ Figma translation. Use whenever the user mentions Swift, SwiftUI, iOS, iPhone, or iPad — in EITHER direction — translating a Figma design into SwiftUI (design → code), or pushing SwiftUI views / screens / tokens back into a Figma file (code → design). Triggers on phrases like 'implement this Figma design in SwiftUI', 'build this screen in Swift', 'push this SwiftUI view to Figma', 'mirror my Swift code in a Figma file', or whenever a Figma URL appears alongside `.swift` files / an `.xcodeproj`. Routes to a direction-specific reference doc; loads alongside `figma-use` for the code → design path."
- use when: Swift, SwiftUI or iOS work with Figma, in either direction (Figma to SwiftUI, or SwiftUI to Figma).
- not for: non-Swift targets; figma-design-to-code remains the shared prerequisite before get_design_context.
- needs: Figma MCP; for code-to-design, figma-use plus figma-generate-design or figma-generate-library.
- side effects: writes local Swift code, or mutates a Figma file for code-to-design
- part of: direction router with two references; asks the user when direction is ambiguous.

### figma-code-connect
- id: figma:figma-code-connect (source path: plugins/figma/skills/figma-code-connect/SKILL.md)
- description: "Creates and maintains Figma Code Connect template files that map Figma components to code snippets. Use when the user mentions Code Connect, Figma component mapping, design-to-code translation, or asks to create/update .figma.ts or .figma.js files."
- use when: Map Figma components to code components by writing Code Connect templates (.figma.ts).
- not for: figma-design-to-code, which consumes the mappings.
- needs: Figma MCP tools get_code_connect_suggestions and get_context_for_code_connect; published components; Organization or Enterprise plan; URL with node-id.
- side effects: writes local .figma.ts files; leaves an existing .figma.tsx untouched
- part of: standalone; dependency lookup for figma-generate-design and figma-generate-library. Confirms the code component match with the user before writing.

### figma-use
- id: figma:figma-use (source path: plugins/figma/skills/figma-use/SKILL.md)
- description: "**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically."
- use when: Before any use_figma call: creating or editing nodes, variables, components or auto-layout in a Figma file. It is the API rulebook; it makes no artifact itself.
- not for: figma-generate-design (screens) and figma-generate-library (components/tokens), which are loaded alongside it.
- needs: Figma MCP/connector with OAuth; target fileKey; Design editor for design-mode APIs.
- side effects: read-only inspection or mutation of the user's Figma file, depending on the script
- part of: foundational step inside every use_figma workflow (generate-design, generate-library, figjam, slides, motion, swiftui code-to-design). Return data explicitly; work incrementally; stop on error.

### figma-generate-design
- id: figma:figma-generate-design (source path: plugins/figma/skills/figma-generate-design/SKILL.md)
- description: "Use this skill alongside figma-use when the task involves translating an application page, view, or multi-section layout into Figma. Triggers: 'write to Figma', 'create in Figma from code', 'push page to Figma', 'take this app/page and build it in Figma', 'create a screen', 'build a landing page in Figma', 'update the Figma screen to match code', 'convert this modal/dialog/drawer/panel to Figma'. This is the preferred workflow skill whenever the user wants to build or update a full page, modal, dialog, drawer, sidebar, panel, or any composed multi-section view in Figma from code or a description. Discovers design system components, variables, and styles from Code Connect files, existing screens, and library search, then imports them and assembles views incrementally section-by-section using design system tokens instead of hardcoded values."
- use when: Build or update a page, modal, drawer or multi-section screen in Figma from code or a description, using the published design system.
- not for: figma-generate-library (reusable components and tokens, not composed views); figma-design-to-code (reverse direction).
- needs: figma-use loaded alongside; Figma MCP; target fileKey; published design system; generate_figma_design capture for web sources with images.
- side effects: mutates the user's Figma file
- part of: companion of figma-use; may call figma-create-new-file and figma-code-connect. Gates: Code Connect check and Step 2 checklist before canvas mutation; one section per call.

### figma-generate-library
- id: figma:figma-generate-library (source path: plugins/figma/skills/figma-generate-library/SKILL.md)
- description: "Build or update a professional-grade design system in Figma from a codebase. Use when the user wants to create variables/tokens, build component libraries, create individual components with proper variant sets and variable bindings, set up theming (light/dark modes), document foundations, or reconcile gaps between code and Figma. Also use when the user asks to create or generate any component in Figma — even a single one — since components require proper variable foundations, variant states, and design token bindings to be production-quality. This skill teaches WHAT to build and in WHAT ORDER — it complements the `figma-use` skill which teaches HOW to call the Plugin API. Both skills should be loaded together."
- use when: Build or update a design system in Figma from my codebase: variables/tokens, component libraries, theming, or even one component.
- not for: figma-generate-design (screens that use an existing design system).
- needs: figma-use loaded; Figma MCP; code tokens.
- side effects: writes extensively to a Figma file (20-100+ use_figma calls); state ledger in /tmp
- part of: entry point of its own five-phase sequence, with explicit user approval after Phase 0. Never parallelize use_figma here, unlike figma-use's multi-page fan-out.

### figma-create-new-file
- id: figma:figma-create-new-file (source path: plugins/figma/skills/figma-create-new-file/SKILL.md)
- description: "**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `create_new_file` tool call. NEVER call `create_new_file` directly without loading this skill first. Trigger whenever the user wants a new blank Figma file — a new design, FigJam, or Slides file — or when you need a fresh file before calling `use_figma`. Usage — /figma-create-new-file [editorType] [fileName] (e.g. /figma-create-new-file figjam My Whiteboard, /figma-create-new-file slides Q3 Review)"
- use when: I need a blank Figma, FigJam or Slides file, or one is needed before use_figma or generate_figma_design.
- not for: figma-generate-diagram (creates its own file; do not call this first).
- needs: Figma MCP; uses a supplied planKey, otherwise resolves it via whoami and asks if there are several plans.
- side effects: creates a draft file in the user's Figma drafts
- part of: step before other Figma skills; hands off to figma-use. Mandatory before every create_new_file call.

### figma-generate-diagram
- id: figma:figma-generate-diagram (source path: plugins/figma/skills/figma-generate-diagram/SKILL.md)
- description: "MANDATORY prerequisite — load this skill BEFORE every `generate_diagram` tool call. NEVER call `generate_diagram` directly without loading this skill first. Trigger whenever the user asks to create, generate, draw, render, sketch, or build a diagram — flowchart, architecture diagram, sequence diagram, ERD or entity-relationship diagram, state diagram or state machine, gantt chart, or timeline. Also trigger when the user mentions Mermaid syntax or wants a system architecture, decision tree, dependency graph, API call flow, auth handshake, schema, or pipeline visualized in FigJam. Routes to type-specific guidance, sets universal Mermaid constraints, and tells you when to use a different diagram type or skip the tool entirely (mindmaps, pie charts, class diagrams, etc.)."
- use when: Draw a flowchart, architecture, sequence, ER, state or Gantt diagram in FigJam from Mermaid.
- not for: figma-use-figjam (freeform board content); uml-and-software-architecture-visualization (diagrams for a web artifact, in build-web-data-visualization).
- needs: Figma MCP. Only flowchart, sequence, state, gantt and ER; pie, mindmap and class are unsupported.
- side effects: creates a FigJam file in drafts unless a fileKey is passed; reusing a fileKey does not replace the old diagram
- part of: mandatory before generate_diagram; hands annotations and colors to figma-use-figjam. Stops after two failed attempts.

### figma-use-figjam
- id: figma:figma-use-figjam (source path: plugins/figma/skills/figma-use-figjam/SKILL.md)
- description: "This skill helps agents use Figma's use_figma MCP tool in the FigJam context. Can be used alongside figma-use which has foundational context for using the use_figma tool."
- use when: Build or edit content on a FigJam board: stickies, sections, connectors, tables, retros, brainstorms.
- not for: figma-generate-diagram (Mermaid diagrams).
- needs: Figma MCP; figma-use loaded alongside.
- side effects: mutates a FigJam board; upload_assets is the only image path
- part of: companion of figma-use; also used for figma-generate-diagram's hybrid edits.

### figma-use-slides
- id: figma:figma-use-slides (source path: plugins/figma/skills/figma-use-slides/SKILL.md)
- description: "This skill helps agents use Figma's use_figma MCP tool in the Slides context. Can be used alongside figma-use which has foundational context for using the use_figma tool."
- use when: Create or edit a Figma Slides deck, including speaker notes, sections and restyling.
- not for: reports-pdfs-and-slide-automation (packaging charts into decks outside Figma); the generate_deck tool (templates only, no custom reference, no follow-up edits).
- needs: figma-use; Slides file (figma-create-new-file slides).
- side effects: mutates a Figma file; never deletes existing slides unless told to start over
- part of: companion of figma-use. For five or more slides: plan first, then build 3-5 slides per call.

### figma-use-motion
- id: figma:figma-use-motion (source path: plugins/figma/skills/figma-use-motion/SKILL.md)
- description: "Motion / animation context for the `use_figma` MCP tool — animating Figma nodes via manual keyframes, animation styles, easing, and timeline duration. Load alongside figma-use whenever a task involves adding, editing, or inspecting animation on a node."
- use when: Add, edit or inspect animation (keyframes, easing, timeline duration) on nodes inside Figma.
- not for: figma-implement-motion (opposite direction: Figma motion to code).
- needs: figma-use; the user's metronome feature flag (else bail out, do not retry); ffmpeg only for export-based verification.
- side effects: mutates a Figma file; export_video is slow and expensive
- part of: companion of figma-use.
