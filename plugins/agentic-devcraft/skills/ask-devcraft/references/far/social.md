# cursor/plugins far from development: social media
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in cursor.md. Families here: `x`.

## Family: x (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/x/`
- manifest: Cursor min 3.13.0. Bundles MCP server `x` at `https://api.x.com/mcp` with OAuth scopes including tweet.write, dm.write, list.write, calls.write, broadcast.write and developer.write. Sign-in is the plugin's Connect card only; the skill never accepts a bearer token or API key. Directory is `x-api-mcp-guide`; host-visible name is `X MCP guide`.
- router: none
- development distance: far (social media)
- disclosure recommendation: simple: one guide; far from development.

### X MCP guide
- id: x:x-api-mcp-guide (source path: third_party/x/skills/x-api-mcp-guide/SKILL.md)
- description: "Read before using any X tool (the X plugin, any X MCP, or Grok Bot's built-in public X reads) and on any X error. Covers reading and searching posts, users, news, trends, Spaces, communities, lists and bookmarks; posting with create_posts; scheduled X calls; livestreams; and X Chat (DMs, inbox, unread, message requests, Chat PIN, juicebox, xchat_lite)."
- use when: Before any X tool call and on any X error: reading and searching posts, users, news and trends, posting, lists, scheduled calls, livestreams, and X Chat DMs.
- needs: the X plugin's OAuth connection, except public reads may use Grok Bot's built-in X tools; X Chat needs a local helper and an unlockable saved key or PIN (request the PIN privately only if unavailable).
- side effects: public posts (only after a yes to that exact text), DMs, list and bookmark changes, scheduled calls that can email invitees, livestreams and moderation; X Chat reuses or clones `github.com/xdevplatform/xchat-grokbot-helper` into `~/xchat-lite`, pulls updates and conditionally creates a venv and pip-installs `chatxdk`. Writes mode-600 Juicebox config; saves a Chat key only with explicit consent. Opening a message request marks messages delivered; conversations may be marked read.
