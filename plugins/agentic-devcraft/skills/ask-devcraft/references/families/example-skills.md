# anthropics/skills family: example-skills
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `example-skills` family. The catalog entry is in anthropic.md. Core-dev records first, then the adjacent one, then one-line entries for the far members.

## Family: example-skills
- source repo: https://github.com/anthropics/skills (entry `example-skills`: 12 skills under skills/)
- manifest notes: Claude marketplace manifest only; no Codex or Cursor manifest. No MCP servers, app connectors, hooks, commands or agents; no auth policy. Skills ship scripts and templates. Written for Anthropic surfaces (claude.ai artifacts, `present_files`, `create_file`/`str_replace`, Cowork); `skill-creator`'s description optimizer needs the `claude` CLI.
- router: none. No skill sequences the others; hand-offs are implicit (`theme-factory` styles what another skill built).
- development distance: core-dev for mcp-builder, skill-creator, frontend-design, webapp-testing, doc-coauthoring; adjacent for web-artifacts-builder; far for algorithmic-art, brand-guidelines, canvas-design, internal-comms, slack-gif-creator, theme-factory.
- disclosure recommendation: rich. Skills cover genuinely different scenarios (MCP servers, skill authoring, UI design, browser checks, spec writing) and no router exists; far members get one-line entries.

### mcp-builder
- id: example-skills:mcp-builder (source path: skills/mcp-builder/SKILL.md)
- description: "Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK)."
- use when: "Build an MCP server that wraps this API or service" in TypeScript (recommended; SDK v2 by default, v1 only if the project already uses it) or Python FastMCP. Four phases: research and plan, implement, review and test, write 10 evaluation questions.
- not for: `claude-api` (calling Claude with an MCP connector is the client side), `skill-creator` (skills, not servers).
- needs: web fetch for MCP spec and SDK docs; Node or Python toolchain; the wrapped service's credentials, which the user supplies.
- side effects: writes local project files. The bundled evaluation script needs `pip install anthropic mcp` and `ANTHROPIC_API_KEY`, spends API tokens and calls the live service, hence read-only questions. No deploy step.
- part of: standalone; internal four-phase sequence.

### skill-creator
- id: example-skills:skill-creator (source path: skills/skill-creator/SKILL.md)
- description: "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy."
- use when: "Turn this into a skill", improve an existing skill, run evals or benchmarks on one, or fix a skill that triggers badly. Tests and evals are the user's choice; subjective skills often skip them.
- not for: `claude-api` (SDK code, and its `prompt-audit` for dated instructions in prompts or config), `mcp-builder` (servers), `template-skill` (bare placeholder).
- needs: subagents for the full loop (without them it runs cases serially, no baselines); Python scripts in the skill; a browser for the eval viewer (or `--static` headless; Claude.ai can collect feedback inline); the `claude` CLI (`claude -p`) for description optimization, which works in Claude Code and Cowork.
- side effects: writes or edits the skill and bundled files; every test and baseline run spends tokens; the browser-viewer branch starts a local server and opens a browser, while `--static` writes HTML without a server. Writes `<skill-name>-workspace/iteration-N/` beside the skill and description-review HTML under `/tmp`; may package a `.skill` file.
- part of: standalone; internal loop (intent, write, test, review, improve).

### frontend-design
- id: example-skills:frontend-design (source path: skills/frontend-design/SKILL.md)
- description: "Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults."
- use when: "Build or redo this UI so it looks distinctive, not templated." A design plan (hex colours, type roles, ASCII wireframes), a check against the brief, then code and self-critique. Any framework.
- not for: `web-artifacts-builder` (a fixed React/Tailwind/shadcn build toolchain), `theme-factory` (preset themes), `brand-guidelines` (fixed Anthropic palette, which this skill flags as a generic tell on a user's own brief).
- needs: code-writing tools and the project's frontend toolchain; screenshots for critique only if the host supports them.
- side effects: writes or edits UI code; no bundled execution script.
- part of: standalone aesthetic layer used alongside whatever builds the code; the brief's own words override it.

### webapp-testing
- id: example-skills:webapp-testing (source path: skills/webapp-testing/SKILL.md)
- description: "Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs."
- use when: "Check this local web app in a real browser": verify frontend behaviour, debug the UI, take screenshots, read console logs, using Playwright scripts. `scripts/with_server.py` starts the dev servers first if they are not running.
- not for: `web-artifacts-builder` (building, not testing). It is ad hoc scripting, not a test-suite framework, and overlaps with browser tools some hosts already have.
- needs: Python Playwright with Chromium (install not covered by the skill), a local app.
- side effects: writes Playwright scripts and screenshots; starts and stops the dev-server commands it is given and drives the app, which can change app data; always headless.
- part of: standalone.

### doc-coauthoring
- id: example-skills:doc-coauthoring (source path: skills/doc-coauthoring/SKILL.md)
- description: "Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks."
- use when: "Help me write this PRD, design doc, RFC, decision doc, technical spec or proposal." Three stages the user must accept: context gathering, section-by-section refinement, reader testing on a fresh agent. Overkill for short docs.
- not for: `internal-comms` (fixed company-format updates), `docx` (Word file mechanics), `discernment-nudge` (a lighter check).
- needs: file or artifact creation and editing; optional Slack, Teams, Drive or SharePoint connectors (asks before searching unknown entities); subagents for automated reader testing, else the user pastes into a fresh conversation.
- side effects: writes a doc file or artifact; reads user-linked documents and mentioned channels via connected tools, announcing the read. Searching unknown entities/projects requires confirmation; automated reader checks use subagents.
- part of: standalone; entry of its own three-stage sequence; declining the offer means freeform work.

### web-artifacts-builder
- id: example-skills:web-artifacts-builder (source path: skills/web-artifacts-builder/SKILL.md)
- description: "Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts."
- use when: "Build a complex claude.ai artifact" that needs state, routing or shadcn/ui, delivered as one `bundle.html` (React 18, TypeScript, Vite, Tailwind, Parcel).
- not for: `frontend-design` (aesthetics for any stack), simple single-file HTML or JSX artifacts (no skill needed), `webapp-testing` (testing).
- needs: Node 18+, npm, bash, network; `index.html` in the project root.
- side effects: its scripts install npm packages; writes a project directory and `bundle.html`.
- part of: standalone; internal five-step flow, testing optional and after showing the artifact.

## Far members (one line each; full records under ../far/)
- example-skills:algorithmic-art: generative art in code (p5.js flow fields, particle systems, seeded variations) as one interactive HTML file -> ../far/media.md
- example-skills:canvas-design: a poster, art piece or other static design as PNG or PDF -> ../far/media.md
- example-skills:slack-gif-creator: animated GIFs sized for Slack emoji or messages -> ../far/media.md
- example-skills:theme-factory: a preset or generated colour and font theme applied to an existing deck, doc or HTML page -> ../far/media.md
- example-skills:brand-guidelines: Anthropic's own brand colours and fonts on an artifact (Anthropic-only) -> ../far/media.md
- example-skills:internal-comms: internal communications in four example formats (3P updates, newsletters, FAQ answers, status and incident reports) -> ../far/documents.md
