# Far from development: learning resources and study plans
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in anthropic.md and cursor.md. Families here: `academy-guide`, `teaching`.

## Family: academy-guide (anthropics/skills)
- source repo: https://github.com/anthropics/skills (entry `academy-guide`: skills/academy-guide)
- manifest notes: Claude marketplace manifest only. No connector or auth policy; it fetches a public catalog JSON from academy.claude.com once per conversation.
- router: none
- development distance: far (learning resources for Claude products)
- disclosure recommendation: simple. One post-answer add-on with no coding task value.

### academy-guide
- id: academy-guide:academy-guide (source path: skills/academy-guide/SKILL.md)
- description: "Stop and check this skill before finishing any reply to a question about how to use Claude or a Claude product — it recommends matching courses, tutorials, and use cases from Claude Academy (academy.claude.com), Anthropic's learning hub. Trigger on: "how do I", "how can I", "getting started with", "what can Claude do", "teach me", "learn to use"; questions about artifacts, projects, skills, plugins, connectors, MCP; requests about rolling Claude out to a team, class, or organization; and any ask for training materials, onboarding content, or learning resources. Use it when the user is learning how to use a feature or product — not when they are mid-task and just want the task done. This skill composes with other skills: after consulting product documentation to answer how a Claude feature works, also check here for a matching course or tutorial — a docs-grounded answer and an Academy recommendation belong together. Only recommend on a strong match; never invent Academy content."
- use when: someone is learning how to use Claude or a Claude product, or rolling it out to a team; it appends at most two Academy items after the normal answer.
- not for: doing the user's mid-task work or replacing a technical answer; can supplement `claude-api` answers when the user wants to learn and a strong resource match exists.
- needs: web fetch of the Academy catalog; some items need an Academy sign-in.
- side effects: none; read-only network fetch, writes no files.
- part of: standalone post-answer add-on.

## Family: teaching (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `teaching/`
- manifest: Cursor packaging only (`.cursor-plugin/plugin.json`; no Codex or Claude manifest); no MCP server or app connector. Skills only; both say "Use Ask user tool", so they need an interactive question capability. No account or file output named.
- router: none; natural order is roadmap, then retrospective after each milestone; not enforced.
- development distance: far (learning plans for any topic, not software development)
- disclosure recommendation: simple: two short skills; far from development, so keep to one-line index pointers.

### create-learning-path
- id: teaching:create-learning-path (source path: teaching/skills/create-learning-path/SKILL.md)
- description: "Build a personalized learning roadmap with milestones and practice checkpoints"
- use when: A learner wants a multi-session roadmap with milestones, practice projects and a schedule for a topic.
- needs: topic, baseline, target outcomes and schedule gathered through an interactive ask-user tool.
- part of: entry; follow with `run-learning-retrospective` after a milestone.

### run-learning-retrospective
- id: teaching:run-learning-retrospective (source path: teaching/skills/run-learning-retrospective/SKILL.md)
- description: "Evaluate learning progress, identify blockers, and adjust the learning plan"
- use when: A milestone is done and the learner wants to see what improved, what blocks them, and an adjusted plan with the next checkpoint.
- needs: completed work or progress evidence and an existing plan (any origin); interactive ask-user tool.
