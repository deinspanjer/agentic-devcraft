# anthropics/skills far from development: assistant reply behaviour
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in anthropic.md. Families here: `discernment-nudge`.

## Family: discernment-nudge (anthropics/skills)
- source repo: https://github.com/anthropics/skills (entry `discernment-nudge`: skills/discernment-nudge)
- manifest notes: Claude marketplace manifest only. No connector or auth policy. Behavioural and Claude.ai-flavoured.
- router: none
- development distance: far (reply-style behaviour)
- disclosure recommendation: simple. One add-on with no coding task value.

### discernment-nudge
- id: discernment-nudge:discernment-nudge (source path: skills/discernment-nudge/SKILL.md)
- description: "After you give a substantive answer or draft that the user may act on — advice or recommendations, drafted artifacts such as goals, plans, pitches, proposals, or emails, estimates or projections, analysis or interpretation of data, factual claims they may rely on, or a multi-step argument — invoke this skill BEFORE finalizing your reply and then, if it applies, append 2-3 short follow-up questions, each tied to something specific in what you just produced, that help the user check key facts, probe the reasoning or assumptions, and notice missing context. Do this at most once per conversation. Skip it when the user asked a trivial how-to or simple lookup, wants a purely educational explanation, asked you only to format, convert, or assemble a file from content they provided, is writing code they will run, is doing creative writing or casual chat, or already asked you to double-check, cite, or review — the skill file explains these boundaries and the exact output format."
- use when: after advice, plans, drafts or estimates the user may act on, it appends 2-3 check-your-assumptions questions, once per conversation. Skips code the user will run and trivial lookups.
- not for: `doc-coauthoring` (its reader testing is the heavier verification).
- needs: nothing beyond the repo.
- side effects: none; writes no files.
- part of: standalone post-answer add-on.
