# cursor/plugins far from development: network connectivity
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in cursor.md. Families here: `tailscale`.

## Family: tailscale (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/tailscale/`
- manifest: Marked `cursor: "never"` (Grok Bot and Sand only, 0.49.0+); README says Cursor must not list it. Ships no `mcp.json`: the connection is served by the Cursor backend and driven through the Grok Bot desktop UI. A company tailnet needs a team admin to enable it at cursor.com and Tailscale Premium or Enterprise.
- router: none
- development distance: far (network connectivity for Grok Bot)
- disclosure recommendation: simple: one guide; far from development.

### tailscale-setup
- id: tailscale:tailscale-setup (source path: third_party/tailscale/skills/tailscale-setup/SKILL.md)
- description: "Connect Grok Bot to Tailscale on a company tailnet (a team admin enables it at cursor.com; each member authenticates their own device and an admin limits it with custom:grokbot postures) or a personal tailnet (one-click Connect when the member owns or administers the tailnet). Several tailnets can be connected at once. Use when the user asks to set up, troubleshoot, change the default tailnet, or disconnect Grok Bot's Tailscale connection."
- use when: Setting up, troubleshooting, changing the default tailnet of, or disconnecting Grok Bot's Tailscale connection.
- needs: Grok Bot desktop; company tailnets need team-admin enablement and Tailscale Premium/Enterprise, then each member authenticates their own device (admin device approval if required); personal tailnets require owner/admin rights. Grok Bot shows Allow/Deny before removing a device, adding a tailnet or changing the default.
- side effects: joins a Grok Bot device to the user's tailnet; supplies a policy snippet for `custom:grokbot` postures to merge into the tailnet policy.
