# openai/plugins far from development: workspace documents, files and data
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in openai-platforms.md. Families here: `google-drive`, `notion`, `dropbox`, `airtable`.

## Family: google-drive
- source path: `plugins/google-drive`
- manifest notes: Codex plugin manifest only (.codex-plugin, v0.1.15, OpenAI, MIT, category Productivity). App connector in .app.json (google-drive) and .mcp.json (https://drivemcp.googleapis.com/mcp/v1, OAuth, drive, drive.readonly and drive.file scopes, placeholder client credentials; the manifest links the app config but not .mcp.json). Marketplace authentication ON_INSTALL. Needs authorized Google file access. Written for Codex local-plugin sessions. Net-new Docs, Sheets and Slides authoring depends on external Documents, Spreadsheets and Presentations plugins not in this repo. Name collision: Cursor's third-party google-drive, google-docs, google-sheets and google-slides skills share these frontmatter names.
- name collisions: `google-drive`, `google-docs`, `google-sheets` and `google-slides` are also skills in cursor/plugins (later in this file): different skills, usage guides for Cursor's MCP connectors. Distinguish them by source.
- router: `google-drive`. Single Workspace entry point: ground the file first (URL/ID, else search), stay in Drive for lifecycle (fetch, move, share, copy, export, revisions; native export capped at 10 MB), then route by artifact: comments to google-drive-comments, prose to google-docs, ranges and formulas to google-sheets, decks and templates to google-slides. Preserve sharing and parents; verify creates before returning a link. Sources disagree on forced DOCX/PPTX/XLSX import for new files; follow each specialist skill, not the router's wording.
- development distance: far (workspace documents)
- disclosure: router-delegated. The router covers all five skills, so records stay one-liners.

### google-drive
- id: google-drive:google-drive (source path: plugins/google-drive/skills/google-drive/SKILL.md)
- description: "Use connected Google Drive as the single entrypoint for Drive, Docs, Sheets, and Slides work. Use when the user wants to find, fetch, organize, share, export, copy, or delete Drive files, or summarize and edit Google Docs, Google Sheets, and Google Slides through one unified Google Drive plugin."
- use when: Entry router for Workspace files: find a file before editing, organize/share/copy/move/delete, retrieve prior revisions, export or download; then routes to the narrowest sibling.
- needs: Authorized Google Drive connector.
- side effects: may change sharing, move or delete files, create copies

### google-docs
- id: google-drive:google-docs (source path: plugins/google-drive/skills/google-docs/SKILL.md)
- description: "Prompt- and template-complete Google Docs creation and editing with explicit-instruction-authoritative structural preservation, including semantic roles, relationships, comparison dimensions, and instructed extensions; full-topology native-copy routing; source-grounded per-tab adaptation for past/example references; style-preserving hyperlink and table edits; canonical smart-chip-first authoring for dates and relevant supported people or Google resources; a file-backed advisory trusted read before existing-document writes; automatic protected-control awareness; direct connector APIs by default; DOCX-first import only when no supplied Google Doc template/reference constrains the output; and checked-in code mode only for exact native dropdown mutation. Use when Codex must create, edit, fill, adapt, redesign, or verify Google Docs without overriding explicit user/template instructions, adding unrequested document scope, or carrying stale reference facts into a new deliverable."
- use when: Create, fill, adapt or edit a Google Doc, preserving native template structure and tabs; also exact native dropdown changes.
- needs: Drive/Docs connector; Codex local-plugin environment; Documents plugin for polished reference-free authoring.
- side effects: writes live Docs. The router's 'all new Docs via DOCX import' wording conflicts with the skill, which allows direct native create for basic docs; follow the skill.

### google-sheets
- id: google-drive:google-sheets (source path: plugins/google-drive/skills/google-sheets/SKILL.md)
- description: "Analyze and edit connected Google Sheets with range precision. Use when the user wants to create Google Sheets, find a spreadsheet, inspect tabs or ranges, search rows, plan formulas, create or repair charts, clean or restructure tables, write concise summaries, or make explicit cell-range updates."
- use when: Repair a formula or chart, clean a table, build a tracker from a template, or import a local workbook into native Sheets.
- needs: Drive/Sheets connector; uses the registered Spreadsheets capability for new non-reference workbooks when available, otherwise creates directly via Sheets MCP.
- side effects: writes live shared sheets. The Final Answer Requirement's broad XLSX-import mandate reads as covering edits too, but Default Routing and the location rule both keep existing-sheet edits in place: assume an in-place connector edit, with XLSX import only for new sheets.

### google-slides
- id: google-drive:google-slides (source path: plugins/google-drive/skills/google-slides/SKILL.md)
- description: "Route Google Slides authoring requests and derive a design system from a native template or reference deck. Use this skill when the user provides an existing native Google Slides deck as a template, reference, or prior-period source, or asks to edit, update, repair, restyle, or clean up an existing native Google Slides deck. Use the Presentations skill instead for net-new presentation creation when no existing native Google Slides deck must be followed."
- use when: Adapt a native Slides deck, follow a template, or repair/restyle an existing deck with native structure kept. Net-new decks with no native reference go to the external Presentations plugin.
- needs: Slides/Drive connector; pdftoppm and local image inspection for QA.
- side effects: writes or copies live decks

### google-drive-comments
- id: google-drive:google-drive-comments (source path: plugins/google-drive/skills/google-drive-comments/SKILL.md)
- description: "Write, reply to, and resolve Google Drive comments on Docs, Sheets, Slides, and Drive files with evidence-backed location context. Use when the user asks to leave comments, review a file with comments, respond to comment threads, or resolve Drive comments."
- use when: Leave, reply to or resolve comments on a Doc, Sheet, deck or Drive file instead of editing content.
- needs: Connector with bulk_update_file_comments.
- side effects: writes externally visible comments and thread state

## Family: notion
- source path: `plugins/notion` (v0.1.7)
- manifest notes: Codex manifest declares the app connector `notion` and an HTTP MCP server `https://mcp.notion.com/mcp` (OAuth). MIT; category Productivity. Each skill's step 0: if Notion tools are missing, enable the bundled Notion app, complete auth, start a new session if tools still do not appear, then finish the answer and tell the user to retry. Shared guardrails: treat a "Tool not found" error as unavailable for the task; one literal search query per `Notion:search`; fetch before updating; create pages with an explicit `parent`.
- router: none (four standalone skills, no declared sequence)
- development distance: far (workspace documents); `notion-spec-to-implementation` plans tasks in Notion and writes no code
- disclosure: simple. Four standalone skills with distinct outputs, far from development, so short records suffice.

### notion-knowledge-capture
- id: notion:notion-knowledge-capture (source path: plugins/notion/skills/notion-knowledge-capture/SKILL.md)
- description: "Capture conversations and decisions into structured Notion pages; use when turning chats/notes into wiki entries, how-tos, decisions, or FAQs with proper linking."
- use when: Turn this conversation, decision, how-to or FAQ into a durable Notion page or wiki entry.
- needs: Notion app/MCP authorized.
- side effects: creates or updates Notion pages and follow-up tasks.

### notion-meeting-intelligence
- id: notion:notion-meeting-intelligence (source path: plugins/notion/skills/notion-meeting-intelligence/SKILL.md)
- description: "Prepare meeting materials with Notion context and supplemental research; use when gathering context, drafting agendas/pre-reads, and tailoring materials to attendees."
- use when: Prepare a meeting: an agenda or pre-read built from Notion context and research.
- needs: Notion app/MCP authorized.
- side effects: creates an agenda page and optional tasks in Notion.

### notion-research-documentation
- id: notion:notion-research-documentation (source path: plugins/notion/skills/notion-research-documentation/SKILL.md)
- description: "Research across Notion and synthesize into structured documentation; use when gathering info from multiple Notion sources to produce briefs, comparisons, or reports with citations."
- use when: Synthesize several existing Notion pages into a cited brief, comparison or report.
- needs: Notion app/MCP authorized.
- side effects: creates a report page in Notion.

### notion-spec-to-implementation
- id: notion:notion-spec-to-implementation (source path: plugins/notion/skills/notion-spec-to-implementation/SKILL.md)
- description: "Turn Notion specs into implementation plans, tasks, and progress tracking; use when implementing PRDs/feature specs and creating Notion plans + tasks from them."
- use when: A PRD or feature spec lives in Notion and I want a plan page and tracked 1-2 day tasks; writes no code.
- needs: Notion app/MCP authorized; a task database.
- side effects: creates plan and task pages in Notion, updates their progress/status, and may add implementation links to the source spec.

## Family: dropbox
- source path: `plugins/dropbox` (v5.0.1)
- manifest notes: Codex manifest references an `.app.json` connector; a separate `.mcp.json` names HTTP server `https://mcp.dropbox.com/mcp`, but the manifest has no `mcpServers` field, so whether it loads is not established. OAuth scopes and install steps are unstated; access respects existing Dropbox permissions. No skill defines an upload/save route, revision listing, restore, or sharing to named recipients, although the manifest text mentions saving content.
- router: none. Shared path: discovery/metadata -> one action skill -> exact confirmation -> track async jobs. Finding, downloading or creating a file never authorizes sharing.
- development distance: far (file storage)
- disclosure: simple. Six standalone skills with explicit neighbor exclusions, far from development, so short records suffice.

### find-dropbox-content
- id: dropbox:find-dropbox-content (source path: plugins/dropbox/skills/find-dropbox-content/SKILL.md)
- description: "Find Dropbox files and folders relevant to a user request. Use when the user asks to search Dropbox, find a document, locate recent files, browse a folder, identify likely source files, or narrow down where content lives before reading, sharing, organizing, or restoring it."
- use when: Where is the Q4 planning deck? Search or browse Dropbox when the target is not pinned down; read-only entry before other Dropbox skills.
- needs: authenticated Dropbox connector.

### inspect-dropbox-file
- id: dropbox:inspect-dropbox-file (source path: plugins/dropbox/skills/inspect-dropbox-file/SKILL.md)
- description: "Inspect a Dropbox file or folder by checking metadata, shared links, and file content when needed. Use when the user asks what a file is, whether it is shared, when it changed, what access links exist, or asks to read/analyze a Dropbox file."
- use when: What is this file, when did it change, summarize it, or what links exist; for a pure shared-link question use `share-dropbox-content`.
- needs: authenticated Dropbox connector.
- side effects: none; read-only.

### share-dropbox-content
- id: dropbox:share-dropbox-content (source path: plugins/dropbox/skills/share-dropbox-content/SKILL.md)
- description: "Share Dropbox files or folders by creating shared links, inspecting existing shared links, or explaining current shared-link state. Use only when the user explicitly asks to create a shared link, check access, or inspect a Dropbox shared link."
- use when: Create a shared link or check who a link gives access to; explicit request only, and it cannot grant named recipients.
- needs: authenticated Dropbox connector.
- side effects: creates links that change external access, after explicit confirmation.

### organize-dropbox-folder
- id: dropbox:organize-dropbox-folder (source path: plugins/dropbox/skills/organize-dropbox-folder/SKILL.md)
- description: "Organize Dropbox files and folders by creating folders, copying content, or moving content into a cleaner structure. Use when the user asks to organize, archive, consolidate, restructure, copy, or move Dropbox content."
- use when: Archive, consolidate, copy or restructure Dropbox content; never deletes.
- needs: authenticated Dropbox connector.
- side effects: creates folders and copies or moves remote files after a confirmed plan.

### clean-up-dropbox-content
- id: dropbox:clean-up-dropbox-content (source path: plugins/dropbox/skills/clean-up-dropbox-content/SKILL.md)
- description: "Clean up Dropbox content by identifying obsolete, duplicate, temporary, or unwanted files and deleting only after explicit review. Use when the user explicitly asks to delete, remove, or clean up Dropbox files or folders."
- use when: Delete duplicate, obsolete or temporary Dropbox files after an exact reviewed list.
- needs: authenticated Dropbox connector.
- side effects: deletes exact confirmed remote files/folders; the current MCP tools expose no restore or revision listing; optional preserving copy must complete successfully before deletion confirmation.

### collect-files-with-request
- id: dropbox:collect-files-with-request (source path: plugins/dropbox/skills/collect-files-with-request/SKILL.md)
- description: "Create, inspect, and manage Dropbox file requests for collecting uploads from other people. Use when the user asks to collect files, request uploads, create an upload portal, check a file request, or list existing file requests."
- use when: Create an upload link to collect files from other people, or check open file requests.
- needs: authenticated Dropbox connector; the destination must be a child folder, never a root.
- side effects: creates a file request and possibly a folder, after confirmation.

## Family: airtable
- source path: `plugins/airtable` (v6.0.1, author Airtable)
- manifest notes: `.codex-plugin/plugin.json` has no `skills` field (only `apps: ./.app.json`), so whether a host picks up the skills is not established. App connector `.app.json` (id `asdk_app_693ca6ce2db08191bb52d66743c65184`). `.mcp.json` points at `https://mcp.airtable.com/mcp` but its OAuth `client_id` is the unfilled placeholder `<AIRTABLE_PUBLIC_CLIENT_ID>` and the manifest does not reference it: do not treat it as a working route. `airtable-cli` needs `npm install -g @airtable/mcp-cli` and a personal access token (`AIRTABLE_TOKEN`, or `airtable-mcp configure`, stored in `~/.airtable/cli.json`).
- router: none. `airtable-overview` is a glossary; `airtable-cli` hands compound, date and per-type filters to `airtable-filters`.
- development distance: far (workspace data)
- disclosure: simple. Three small skills outside typical development; short records.

### airtable-cli
- id: airtable:airtable-cli (source path: plugins/airtable/skills/airtable-cli/SKILL.md)
- description: "Lists bases, reads and writes records, manages tables and fields, filters and searches data in Airtable via the `airtable-mcp` CLI. Use when the task involves Airtable data or the user mentions airtable-mcp, bases, tables, records, or fields."
- use when: List bases, read, write or search records, manage tables and fields in Airtable from the terminal via `airtable-mcp`.
- needs: `@airtable/mcp-cli` installed globally and an Airtable token. The skill is silent on CLI versus the plugin's app connector: recommend it only when the user wants terminal or scripted access, or the connector is unavailable.
- side effects: writes and deletes Airtable records; confirm before any tool whose `access` is `destructive`; installs an npm package.

### airtable-filters
- id: airtable:airtable-filters (source path: plugins/airtable/skills/airtable-filters/SKILL.md)
- description: "Use this skill when the user wants to find, filter, or narrow down Airtable records by field values, even when they don't explicitly say "filter.""
- use when: Narrow Airtable records by field values, whether or not the user says "filter"; builds the JSON `filters` parameter. Read the table schema first and use field IDs (`fld...`) and choice IDs (`sel...`).
- needs: Airtable MCP or CLI tools to run the query.

### airtable-overview
- id: airtable:airtable-overview (source path: plugins/airtable/skills/airtable-overview/SKILL.md)
- description: "Explains what Airtable is and how data is structured — bases, tables, fields, records, views, automations, and interfaces. Use when you need context about the Airtable data model."
- use when: Plain explanation of Airtable's data model (bases, tables, fields, records, views, automations, interfaces); runs nothing.

# cursor/plugins far from development: Google Workspace connector guides
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in cursor.md. Families here: `google-drive`, `google-docs`, `google-sheets`, `google-slides`.

## Family: google-drive (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/google-drive/`
- manifest: Cursor (min 3.13.0). Bundles an MCP server `google-drive` at `https://api.cursor.com/rest-mcp/google-drive/mcp` (Cursor's gateway). Auth policy not declared in the manifest; the grant is `drive.file`. The skill is a usage guide for that connector and is useless without it. Same skill name exists in OpenAI's catalog as a different skill.
- router: none; other Google skills defer to it for folder placement and export.
- development distance: far (workspace files)
- disclosure recommendation: simple: one short guide; far from development.

### google-drive
- id: google-drive:google-drive (source path: third_party/google-drive/skills/google-drive/SKILL.md)
- description: "Work with Google Drive through its MCP tools - search, read, create, organize, share, comment, and export files. Use when creating files in specific folders, moving or renaming, converting Markdown/CSV into Docs/Sheets, managing comments, or exporting a rendered PDF."
- use when: Searching, reading, creating, moving, sharing, commenting on or exporting Google Drive files, including converting Markdown or CSV into a Doc or Sheet in a named folder.
- needs: the `google-drive` MCP connection (Google sign-in). File ids come from search, listings or a user-provided URL, never guesses; writes or moves involving files/folders the app neither created nor the user picked can return a permission 403, not a retry case.
- side effects: writes and moves Drive files; `share_file` widens access (only when asked); trash only, no permanent delete.

## Family: google-docs (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/google-docs/`
- manifest: Cursor (min 3.22.0; also Grok Bot, Sand). Bundles an MCP server `google-docs` through Cursor's gateway. Usage guide for that connector only.
- router: none
- development distance: far (office documents)
- disclosure recommendation: simple: one short guide.
- name collision: OpenAI's `google-drive` family, earlier in this file, has a different skill with this name; distinguish them by source.

### google-docs
- id: google-docs:google-docs (source path: third_party/google-docs/skills/google-docs/SKILL.md)
- description: "Author and edit Google Docs with the google-docs tools - structured writing, character and paragraph styling, lists, tables, images, headers/footers. Use when creating a formatted document, editing document content, or applying styles."
- use when: Writing or styling a Google Doc: structured text, lists, tables, images, headers and footers.
- needs: the `google-docs` MCP connection and `google-drive` for folder placement (`create_document` makes a blank doc and cannot target a folder; for known content prefer Drive's Markdown import).
- side effects: edits the Doc.

## Family: google-sheets (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/google-sheets/`
- manifest: Cursor (min 3.22.0; also Grok Bot, Sand). Bundles an MCP server `google-sheets` through Cursor's gateway. Usage guide for that connector only.
- router: none
- development distance: far (office documents)
- disclosure recommendation: simple: one short guide.
- name collision: OpenAI's `google-drive` family, earlier in this file, has a different skill with this name; distinguish them by source.

### google-sheets
- id: google-sheets:google-sheets (source path: third_party/google-sheets/skills/google-sheets/SKILL.md)
- description: "Build and edit Google Sheets with the google-sheets tools - values, formatting, charts, conditional formatting, structure, validation, named and protected ranges. Use when creating a spreadsheet or dashboard, formatting cells, adding or fixing charts, or reorganizing tabs and rows."
- use when: Building or formatting a spreadsheet or dashboard: values, formatting, charts, validation, named and protected ranges.
- needs: the `google-sheets` MCP connection; `google-drive` to place it in a folder.
- side effects: writes the sheet; no revision guard (last write wins); row and column deletes are not undoable through the API.

## Family: google-slides (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/google-slides/`
- manifest: Cursor (min 3.22.0; also Grok Bot, Sand). Bundles an MCP server `google-slides` through Cursor's gateway. Usage guide for that connector only.
- router: none
- development distance: far (office documents)
- disclosure recommendation: simple: one short guide.
- name collision: OpenAI's `google-drive` family, earlier in this file, has a different skill with this name; distinguish them by source.

### google-slides
- id: google-slides:google-slides (source path: third_party/google-slides/skills/google-slides/SKILL.md)
- description: "Build and edit Google Slides through the google-slides MCP tools - slides, grids of cards and columns, text boxes, shapes, images, tables, styling, layout inspection, and per-slide PNG rendering. Use when creating a deck, laying out slide elements, matching a template, or verifying how a slide looks."
- use when: Building or editing a Google Slides deck, laying out elements, matching a template, or checking how a slide looks.
- needs: the `google-slides` MCP connection; `google-drive` for folder placement and whole-deck PDF export.
- side effects: edits the deck; pass `requiredRevisionId` so concurrent edits fail instead of corrupting.
