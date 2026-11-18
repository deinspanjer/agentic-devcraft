# openai/plugins far from development: media and design production
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in openai-platforms.md. Families here: `adobe`, `canva`, `chatcut`, `higgsfield`, `creative-production`.

## Family: adobe
- source path: `plugins/adobe` (v8.0.0, author Adobe Inc)
- manifest notes: Codex manifest plus `.app.json` (Adobe for creativity connector, id `asdk_app_69312da8e4dc81919370cb86fd172b6c`); no MCP file, hooks or commands. Every skill says "Signed-In required" (401 re-authenticate, 403 plan lacks the feature) and starts with `adobe_mandatory_init`. User media is uploaded to Adobe Creative Cloud; results are presigned URLs. `adobe-create-mockups` declares `surface: [codex]` only; the others declare `[claude, codex]`.
- router: none. Six standalone skills, no hand-offs.
- development distance: far (media and design assets)
- disclosure: simple. Six unrelated standalone skills, none a coding task; short records.

### adobe-batch-edit-photos
- id: adobe:adobe-batch-edit-photos (source path: plugins/adobe/skills/adobe-batch-edit-photos/SKILL.md)
- description: "Apply consistent photo adjustments across a set of images so they look like they were edited together. Use this skill whenever the user says "make my photos look cohesive", "give all these the same style", "apply a warm and golden feel to all of these", "make this cinematic", "match the look across my photos", "edit all my travel photos the same way", "batch edit these", "make these consistent", "fix my phone photos", or uploads a folder of photos and wants a unified, polished result. Also triggers for requests like "apply a preset to all of these", "make these look professional", or "they were shot in mixed lighting — can you fix them all". Outputs direct final image URLs plus an in-chat preview grid and optional Firefly Board link. Access: 🔐 Signed-In required | Gen AI: ❌"
- use when: Make a whole set of photos look edited together (same style, mixed-lighting phone shots); requires approving a before/after sample of image 1 first. For portraits use `adobe-retouch-portraits`.
- needs: Adobe connector, sign-in; uploads files to Creative Cloud.
- side effects: creates a Firefly Board in the user's account.

### adobe-create-mockups
- id: adobe:adobe-create-mockups (source path: plugins/adobe/skills/adobe-create-mockups/SKILL.md)
- description: "Use when a user wants to see their logo, design, or sketch on a product or scene mockup — mugs, t-shirts, business cards, hats, phone screens, posters, billboards, or similar. Triggers on "create mockups", "show my logo on products", or any logo upload with a request to visualize it on items. Access: 🔐 Signed-In required | Gen AI: ✅ Adobe Firefly via `image_generate` used for design creation, sketch polishing, and mockup scene generation"
- use when: Show a logo, sketch or design on mugs, shirts, cards, screens or billboards; one pilot mockup must be approved before the rest.
- needs: Adobe connector, sign-in; Codex surface only; uses Firefly generation (credits).
- side effects: creates a Firefly Board and share link.

### adobe-create-social-variations
- id: adobe:adobe-create-social-variations (source path: plugins/adobe/skills/adobe-create-social-variations/SKILL.md)
- description: "Resize, crop, or export any image or video into platform-ready social media assets using Adobe Creative Cloud tools. Use this skill when a user wants to prepare a photo, image, or video for one or more social platforms — Instagram, TikTok, LinkedIn, Facebook, YouTube, Snapchat, Pinterest, Threads, or X/Twitter. Triggers on: "prepare my image for Instagram", "resize for TikTok", "get this ready to post", "make versions for all platforms", "social media sizes", "crop for stories", "export for LinkedIn", "resize my video for social", "make social media assets", or any request to adapt a photo or video for specific platforms. Handles subject-aware cropping, AI canvas expansion, test previews before full runs, and same-ratio video resizing."
- use when: Resize or crop an image or video into platform-ready social sizes (same-ratio video resize only).
- needs: Adobe connector, sign-in; uploads files to Creative Cloud.

### adobe-design-from-template
- id: adobe:adobe-design-from-template (source path: plugins/adobe/skills/adobe-design-from-template/SKILL.md)
- description: "Create any visual design using Adobe Express templates — flyers, posters, social media posts (Instagram, Facebook, LinkedIn), business cards, invitations, greeting cards, resumes, cover letters, brochures, newsletters, certificates, presentations, YouTube thumbnails, email headers, logos, menus, and labels. Use this skill whenever the user wants to make, design, or build any visual — even if they just say "make me a flyer", "design a poster", "I need something for Instagram", "create an event invite", or "make a business card". Also handles browsing templates, editing text, replacing images, changing backgrounds, animating, and exporting designs. Access: 🔐 Signed-In required | Gen AI: ❌ by default — image replacement only where the surface permits generative AI (e.g. Codex); none on Claude"
- use when: "Make me a flyer, poster, card, invitation, thumbnail" from an Adobe Express template; never auto-selects a template.
- needs: Adobe connector, sign-in; no upload.
- side effects: creates temporary Express documents (deleted after 12 hours).

### adobe-edit-quick-cut
- id: adobe:adobe-edit-quick-cut (source path: plugins/adobe/skills/adobe-edit-quick-cut/SKILL.md)
- description: "Create a punchy sizzle reel from a video using Adobe Quick Cut. Use this skill whenever a user wants to cut, trim, or shorten a video into highlights — including phrases like "make a sizzle reel", "make a highlight reel", "quick cut this", "cut the best parts", "shorten this video", "make a highlight clip", "summarize this video visually", or any request to produce a shorter edited version of a video. Use this skill for Quick Cut requests before suggesting manual editing in Premiere. Requires the user to upload a video file."
- use when: Shorten a video into a highlight or sizzle reel (three variants); selects moments, cannot trim to timestamps.
- needs: Adobe connector, sign-in; video uploaded to Creative Cloud; plan may 403.

### adobe-retouch-portraits
- id: adobe:adobe-retouch-portraits (source path: plugins/adobe/skills/adobe-retouch-portraits/SKILL.md)
- description: "Bulk-retouch a folder of portrait photos using Adobe tools — designed for wedding photographers and event photographers who need fast, walk-away batch processing. Use this skill when the user says "retouch my photos", "batch process these portraits", "process my wedding photos", "clean up this folder of images", "run my headshots through Adobe", or uploads/selects a folder of photos and wants them polished and ready to review. Automatically applies auto-straighten, auto-tone, and auto-light to every image. Outputs a preview grid and download folder. Access: 🔐 Signed-In required | Gen AI: ❌ by default — optional background-only cleanup only where the surface permits generative AI (e.g. Codex); none on Claude"
- use when: Batch-polish a folder of portraits (wedding, event, headshots) with mood and person presets; requires approving a sample preview first. For non-portrait style matching use `adobe-batch-edit-photos`.
- needs: Adobe connector, sign-in; uploads files to Creative Cloud.
- side effects: creates a Firefly Board in the user's account.

## Family: canva
- source path: `plugins/canva`
- manifest notes: Codex plugin manifest only (.codex-plugin, v14.0.0, Canva Pty Ltd., category Creativity). MCP server `canva` (http, https://mcp.canva.com/mcp) plus app connector in .app.json; marketplace authentication ON_INSTALL. Requires connecting a Canva account (invoked `@Canva`); Bulk Create needs an eligible Canva Enterprise plan; a missing-scope error means disconnect and reconnect the connector.
- router: none. `canva-edit-design` is the edit engine the others build on (a transaction: start, edit, preview, explicit approval, commit or cancel; uncommitted changes are lost). Critique skills are read-only and offer to hand off to it.
- development distance: far (design and media, not code)
- disclosure: rich, but with short records since the family is far: no router and eight skills for different Canva jobs.

### canva-edit-design
- id: canva:canva-edit-design (source path: plugins/canva/skills/canva-edit-design/SKILL.md)
- description: "Make edits to an existing Canva design — change or fix text, replace/insert/delete images and videos, reformat text (size, weight, style, color, alignment, lists, line height), reposition or resize elements, and update the title. Use when the user wants to change, edit, update, fix, translate, replace, or reformat content in a specific Canva design. This is the safe edit engine that other Canva skills (e.g. implement-feedback) build on."
- use when: Change text, replace images, reposition or retitle in one specific existing Canva design. The edit engine the other Canva skills build on.
- needs: Canva connector; design ID or URL.
- side effects: permanently modifies the design on commit; shows a preview and needs explicit yes first

### canva-design-feedback
- id: canva:canva-design-feedback (source path: plugins/canva/skills/canva-design-feedback/SKILL.md)
- description: "Read a Canva design and return structured, actionable design feedback — visual hierarchy, copy/messaging, layout & spacing, consistency, readability, and accessibility. Read-only; makes no changes to the design. Use when the user asks to "review my design", "give me feedback on this", "critique my deck/poster/flyer", "how can I improve this design", or "what's wrong with this slide"."
- use when: Review or critique my Canva design, deck or poster. Read-only; offers canva-edit-design for fixable items.

### canva-brand-check
- id: canva:canva-brand-check (source path: plugins/canva/skills/canva-brand-check/SKILL.md)
- description: "Check a Canva design against a brand kit and report where it diverges — off-palette colors, non-brand fonts, logo misuse, and off-tone copy. Read-only; makes no changes. Use when the user asks "is this on brand", "check this against our brand kit", "do a brand review", "does this match our brand guidelines", or "brand-check my design"."
- use when: Is this Canva design on brand, checked against our Brand Kit. Read-only critique with the Brand Kit as rubric.
- needs: Canva connector with brandkit:read scope.

### canva-implement-feedback
- id: canva:canva-implement-feedback (source path: plugins/canva/skills/canva-implement-feedback/SKILL.md)
- description: "Implement reviewer feedback on a Canva design. Reads all comment threads, synthesises what reviewers want, makes the clear-cut changes directly, and flags anything that needs a human decision. Use when the user asks to "implement feedback on my deck", "address comments on a design", "apply review feedback", "fix the comments on my presentation", or "implement the feedback"."
- use when: Address the reviewer comments on my Canva deck; acts on human comment threads, not generated critique.
- side effects: commits edits and posts replies visible to reviewers after one up-front approval

### canva-translate-design
- id: canva:canva-translate-design (source path: plugins/canva/skills/canva-translate-design/SKILL.md)
- description: "Translate all text in a Canva design to another language, creating a translated copy. Faster than manually copying and editing each text box in Canva's editor. Use when users say "translate my design to [language]", "make a Spanish/French/etc version", or "localize my Canva design"."
- use when: Translate or localize a Canva design into another language as a new copy.
- side effects: creates a copy; original untouched; approval before commit

### canva-resize-for-social-media
- id: canva:canva-resize-for-social-media (source path: plugins/canva/skills/canva-resize-for-social-media/SKILL.md)
- description: "Resize a Canva design into multiple social media formats (Facebook post, Facebook story, Instagram post, Instagram story, LinkedIn post). Use this skill when users want to resize Canva designs specifically for multiple social media platforms in one operation, rather than resizing to a single format manually."
- use when: Turn one Canva design into Facebook, Instagram or LinkedIn formats. Asks which formats, then runs with no further approval.
- needs: Canva connector with the resize-design tool.
- side effects: creates new designs

### canva-branded-presentation
- id: canva:canva-branded-presentation (source path: plugins/canva/skills/canva-branded-presentation/SKILL.md)
- description: "Create on-brand Canva presentations from an outline or brief. Use when the user asks to create a branded presentation, make an on-brand deck, turn an outline into slides, or generate a presentation from a brief. Input can be text directly in the message, a Canva design ID, a reference to a Canva doc by name, or a Canva design link (e.g., https://www.canva.com/design/...)."
- use when: Turn an outline or brief into an on-brand Canva deck; the user picks a generated candidate. One deck, not many designs from rows (canva-bulk-create).
- side effects: creates a design in the user's account

### canva-bulk-create
- id: canva:canva-bulk-create (source path: plugins/canva/skills/canva-bulk-create/SKILL.md)
- description: "Bulk-create Canva designs from tabular data using a brand template with autofill fields, producing one design per row. Use when users say "bulk create designs from this CSV", "generate one design per row", "create a design for each product", "batch generate from a template", or "autofill a template from a spreadsheet". Accepts any tabular data source — uploaded files, pasted tables, JSON, or URLs."
- use when: One Canva design per spreadsheet, CSV or JSON row from a brand template with autofill fields.
- needs: Eligible Canva Enterprise plan; brand template with autofill fields.
- side effects: creates many designs with no bulk undo; confirm the column mapping; offers a three-row test at 50+ rows

## Family: chatcut
- source path: `plugins/chatcut`
- manifest notes: Codex plugin manifest only (.codex-plugin, v1.0.4, ChatCut, GPL-3.0-only, category Creativity). Skill-only: README says it deliberately has no installer scripts, MCP manifest or editing skills; empty .app.json. The installed ChatCut Desktop app registers the local `chatcut_desktop` MCP server and syncs its editing skills. Skill policy products [CODEX]; user signs in inside the app; the skill must not handle credentials or edit config.toml. Linux unsupported.
- router: none (single skill).
- development distance: far (video editing app installer)
- disclosure: simple. One skill.

### connect-chatcut-desktop
- id: chatcut:connect-chatcut-desktop (source path: plugins/chatcut/skills/connect-chatcut-desktop/SKILL.md)
- description: "Install, open, connect, or repair ChatCut Desktop when the chatcut_desktop MCP tools are missing or unavailable. Do not use from a managed agent already running inside ChatCut Desktop, or when chatcut_desktop tools are already available."
- use when: I want to edit video with ChatCut but the chatcut_desktop tools are missing: download, install, open or repair ChatCut Desktop. Contains no editing capability.
- needs: macOS 13+ or Windows x64; Codex only (policy.products: CODEX); sign-in inside the app.
- side effects: downloads, installs and opens an app outside the sandbox from official api.chatcut.io URLs only; the app registers local MCP and syncs editing skills, requiring a new Codex task

## Family: higgsfield
- source path: `plugins/higgsfield`
- manifest notes: Codex plugin manifest only (.codex-plugin, v1.2.1, Higgsfield AI, Inc., category Creativity, empty capabilities). App connector in .app.json and MCP server `higgsfield` (https://mcp.higgsfield.ai/mcp, no auth fields declared); marketplace authentication ON_INSTALL. Needs a connector exposing authorized paid generation plus a sandbox with preinstalled media tools (sandbox_exec, media_upload, media_confirm, ffmpeg, Whisper). All three skills set allow_implicit_invocation: true. Interactive intake uses the ChatGPT ask_user_input popup. Cost is paid and unspecified; the assembler and validator scripts the pipeline calls are not in the repo.
- router: `faceless-channel`. Pipeline: intake (type, style, topic, duration, aspect, subtitles, voice) with locked voice, style anchor, asset roster, script and block plan, clip generation, narrator (phase 5), sandbox assembly, subtitles (phase 7), optional platform report. Interactive runs stop for Continue / Stop review after image, video and audio stages. Special modes (Picture Story, Kids song, long-form History) override the order.
- development distance: far (media production)
- disclosure: router-delegated. `faceless-channel` orchestrates `narrator` and `subtitles`, which are also usable alone for narrow jobs.

### faceless-channel
- id: higgsfield:faceless-channel (source path: plugins/higgsfield/skills/faceless-channel/SKILL.md)
- description: "Use only when the user asks to produce a finished multi-scene narrator-led video and explicitly requests a faceless channel, YouTube automation, narrated explainer/story/education, documentary, storybook or myth retelling, or kids song video. Topic alone is never enough: a generic video of/about something, including a historical topic, uses ordinary video generation. Do not use for planning or ideas, single clips, silent animation, image-to-video, footage edits, ads, product demos, or UGC. This workflow requires a consistent non-photoreal style, reusable assets, narrator voiceover, and burned subtitles."
- use when: Entry router for a finished narrator-led faceless episode: explainer, story, documentary, myth, storybook or kids-song video with generated illustrated scenes. A topic alone does not qualify; ads, product demos, UGC and single clips are excluded.
- needs: Higgsfield connector with paid generation; sandbox media tools (sandbox_exec, media_upload, media_confirm); ChatGPT-style interactive intake.
- side effects: paid image, video and audio generation; hosts one final.mp4; stops before publishing. The inspected repo lacks the assembler scripts it expects in the sandbox.

### narrator
- id: higgsfield:narrator (source path: plugins/higgsfield/skills/narrator/SKILL.md)
- description: "Activate when the user explicitly names the narrator skill or requests production-ready narration in either case: (1) numbered takes fitted to fixed video windows, or (2) one continuous long-form story read in a locked voice that must be measured and retried for timbre or internal pauses. Collect missing text, voice_id, or voice_type after activation; their absence is not a reason to skip this workflow. Own pacing, speech-duration gates, retries, and ready audio delivery; never time-stretch. Do not use for ordinary TTS, "read this aloud", an unconstrained voiceover, voice browsing, music, SFX, singing, dubbing existing speech, or voice cloning."
- use when: Numbered narration takes must fit fixed video windows in one locked voice, or a long read needs measured pacing. Not ordinary read-aloud TTS.
- needs: Ordered text and a verified voice_id and voice_type; Higgsfield audio tools.
- side effects: sends text to paid external TTS

### subtitles
- id: higgsfield:subtitles (source path: plugins/higgsfield/skills/subtitles/SKILL.md)
- description: "Burn timed subtitles onto a finished video or configure Whisper-timed caption burning during faceless-video assembly. Takes video/audio generation jobs or a local finished video, optionally with authored narration text, and returns a captioned video or the exact backend subtitle configuration. Timings always come from Whisper on the video's own audio — never estimated. THREE looks: `paper` (torn cream paper label, handwritten ink), `bold` (UGC ALL-CAPS, white with black stroke, platform safe zones), `clean` (slim white CAPS, no plate, tiny at the bottom — no Pillow needed). Use when: adding/burning subtitles or captions to an existing video, restyling captions, or when a production workflow needs its finished cut subtitled. NOT for: generating the video, translating speech, or live/soft subtitle tracks (this burns them into the picture)."
- use when: Burn clean, paper or bold captions onto a finished video, or configure caption burn during faceless assembly. No animation, karaoke, translation or soft tracks.
- needs: Sandbox with Whisper and ffmpeg.
- side effects: replaces the deliverable with the captioned file; do not promise the original survives

## Family: creative-production
- source path: `plugins/creative-production`
- manifest notes: v0.1.25, OpenAI, capabilities Interactive and Write. Marketplace policy: no product restriction, authentication ON_USE, but it depends on the Codex desktop app (board widget, built-in ImageGen, Desktop subagents, `$CODEX_HOME`). Bundled local MCP server `creative_production_mcp` (Node; one tool `creative_production_board`). `.app.json` declares no apps; README mentions optional Figma and Canva capabilities that are not declared.
- router: none. `intake` is the no-brief entry and hands the same `boardId` to `produce`, which opens the board once and iterates in it.
- development distance: far (generated marketing and visual imagery, not code)
- disclosure: simple. Two skills; far from development, so short records.

### intake
- id: creative-production:intake (source path: plugins/creative-production/skills/intake/SKILL.md)
- description: "Use when Creative Production is explicitly invoked or mentioned without a concrete request, when the user asks what Creative Production can do, or when the user wants help getting started without enough context to choose a workflow."
- use when: Open Creative Production or ask what it can do, with no concrete brief; opens the starter board once and stops.
- needs: Codex desktop (board widget) and the `creative_production_board` MCP tool.
- side effects: Creates a board under `$CODEX_HOME/creative-production`; hands the same `boardId` to `produce`.

### produce
- id: creative-production:produce (source path: plugins/creative-production/skills/produce/SKILL.md)
- description: "Use when the user wants to create, explore, adapt, refine, polish, or review visual creative such as campaigns, ads, social posts, product imagery, scenes, offers, logos, brand systems, styles, charts, decks, or related marketing and design assets."
- use when: Make campaign, ad, social, product, scene, offer, logo or style image directions from a brief or source image; iterate on a board.
- needs: Codex desktop with built-in ImageGen and the `creative_production_board` MCP tool; Desktop subagents are required starting at two uncached native images, while one is generated directly (no `codex exec` fallback).
- side effects: Writes generated images to local files and board state under `$CODEX_HOME/creative-production`; does not deploy or send.

# anthropics/skills far from development: art and design assets
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in anthropic.md. Families here: `example-skills (far members)`.

## Family: example-skills (anthropics/skills; far members: algorithmic-art, canvas-design, slack-gif-creator, theme-factory, brand-guidelines)
- source repo: https://github.com/anthropics/skills (entry `example-skills`). The family header and its core-dev and adjacent records are in ../families/example-skills.md.
- manifest notes: Claude marketplace manifest only; no MCP servers, app connectors, hooks, commands or agents; no auth policy. Written for Anthropic surfaces.
- router: none.
- development distance: far

### algorithmic-art
- id: example-skills:algorithmic-art (source path: skills/algorithmic-art/SKILL.md)
- description: "Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations."
- use when: "Make generative art in code": flow fields, particle systems, seeded variations with sliders. Output is a philosophy `.md` and one interactive HTML file with the algorithm inline.
- not for: `canvas-design` (static PNG or PDF), `web-artifacts-builder` (React app), `frontend-design` (product UI).
- needs: bundled `templates/viewer.html` (read first, mandatory); the browser loads p5.js 1.7.0 from a CDN.
- side effects: writes local files; fixed Anthropic-branded layout.
- part of: standalone; internal two-step (philosophy, then code).

### canvas-design
- id: example-skills:canvas-design (source path: skills/canvas-design/SKILL.md)
- description: "Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations."
- use when: a poster, art piece or other static design as PNG or PDF, after a design-philosophy step.
- not for: `algorithmic-art` (interactive code art), `pdf` (document processing).
- needs: tools to render and write PDF/PNG (not specified); bundled `canvas-fonts` and network access if downloading more fonts.
- side effects: writes local `.md`, `.png`, `.pdf`.
- part of: standalone.

### slack-gif-creator
- id: example-skills:slack-gif-creator (source path: skills/slack-gif-creator/SKILL.md)
- description: "Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack.""
- use when: "Make a GIF of X for Slack", emoji (128x128) or message (480x480).
- not for: `canvas-design` (static art).
- needs: `pip install pillow imageio numpy`; no Slack access.
- side effects: writes a local GIF; uploads nothing.
- part of: standalone.

### theme-factory
- id: example-skills:theme-factory (source path: skills/theme-factory/SKILL.md)
- description: "Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly."
- use when: apply one of 10 preset or a generated colour and font theme to an existing slide deck, doc or HTML page.
- not for: creating the artifact's content; `brand-guidelines` supplies Anthropic-only styling and `frontend-design` bespoke design. Can complement `pptx`; its theme mechanism is not an exclusion.
- needs: an existing artifact, a way to display `theme-showcase.pdf`, and tools to edit the artifact; the user must choose the theme before it applies.
- side effects: modifies the artifact's colours and fonts through the host's editing tools; no bundled script.
- part of: later step after the artifact exists.

### brand-guidelines
- id: example-skills:brand-guidelines (source path: skills/brand-guidelines/SKILL.md)
- description: "Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply."
- use when: styling an artifact in Anthropic's own colours and Poppins/Lora fonts. Anthropic-only.
- not for: `theme-factory` (presets or custom), `frontend-design` (user's own brief).
- needs: system fonts (Poppins/Lora preferred, Arial/Georgia fallbacks); the described slide styling uses `python-pptx`.
- side effects: none; reference only, no script.
- part of: standalone.
