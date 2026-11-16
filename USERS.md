# Using Agentic Devcraft

Only skills under `plugins/agentic-devcraft/skills/` are released. Candidate
skills under `proposals/` are not installed by either marketplace.

## Marketplace installation

The shared plugin is `agentic-devcraft@agentic-devcraft`, version `0.3.0`.
For development or uncommitted changes, register the local checkout as the
marketplace. Replace `/absolute/path/to/agentic-devcraft` with your checkout:

```sh
env -u CODEX_HOME codex plugin marketplace add /absolute/path/to/agentic-devcraft
env -u CODEX_HOME codex plugin add agentic-devcraft@agentic-devcraft
claude plugin marketplace add /absolute/path/to/agentic-devcraft --scope user
claude plugin install agentic-devcraft@agentic-devcraft --scope user
```

These are native marketplace installs of the shared plugin, not standalone skill
symlinks. Both catalogs reference `plugins/agentic-devcraft/`. A local catalog
makes the current checkout available; it does not publish changes to GitHub.
After a release is committed and published, `deinspanjer/agentic-devcraft` can be
used as the marketplace source instead of the local path.

Verify with `env -u CODEX_HOME codex plugin list --marketplace agentic-devcraft --json`,
`claude plugin list --json`, and `claude plugin details agentic-devcraft`.
The plugin should be installed/enabled and its inventory include
`agent-instructions-cleanup`, `documentation-pattern-refactor`, `capture-agent-issue`,
and `status`. Refresh/reopen the clients after installation. Claude also supports
`/reload-plugins`; Codex local plugin updates may require restarting the app.

For local updates, keep the source checkout available, update the plugin version,
and reinstall/update using the native plugin commands. Claude local-marketplace
installs can read directly from the plugin folder; Codex keeps an installed cache.
Run `$agentic-devcraft:status` in Codex or `/agentic-devcraft:status` in Claude to
check the version a session sees.

The Codex commands above target `~/.codex`, even when the current session sets
`CODEX_HOME` to another directory. Install Codex plugins only in `~/.codex`;
let Air manage its other configuration directories and generated skill views.
Do not duplicate the installation into the session's alternate `CODEX_HOME`.
For an existing Claude
installation, use `claude plugin update agentic-devcraft@agentic-devcraft --scope user`.

## Agent instructions and documentation refactoring

| Skill | Codex | Claude |
| --- | --- | --- |
| Preserve guidance while simplifying agent instructions | `$agentic-devcraft:agent-instructions-cleanup` | `/agentic-devcraft:agent-instructions-cleanup` |
| Audit or refactor documentation by audience | `$agentic-devcraft:documentation-pattern-refactor` | `/agentic-devcraft:documentation-pattern-refactor` |

The cleanup skill creates a preservation map and dated shallow mirror before
requesting approval for in-place replacements. The documentation skill supports
audit, scaffolding, and restructuring, with root scope by default and confirmation
before refactoring. Both remain available for automatic skill selection.

When migrating, first verify the marketplace installation contains both skills,
then remove only their old standalone links under `~/.codex/skills/`.
Leave Air-managed directories to Air. Unlinking a symlink leaves its source
directory intact. Retain real directories as backups until their contents have
been compared with the packaged version.

## Air in JetBrains IDEs

Air documents skill directories and external registries, rather than compatibility
with the Claude/Codex marketplace JSON catalogs. Use the same skill sources with
one of these management approaches:

- **Local checkout:** under **Settings → AI → Skills → Manage Skill Directories**,
  add `<checkout>/plugins/agentic-devcraft/skills` as a global directory. Select the
  desired skills for IDE use. This keeps discovery tied to the shared source.
- **Published registry:** after publishing the changes, add
  `https://github.com/deinspanjer/agentic-devcraft/tree/main/plugins/agentic-devcraft/skills`
  through **Manage External Registries**, then install the two skills for the IDE.
  This offers an Air-managed installation from published content, but does not
  provide the plugin namespace or establish identical update behavior to a
  Codex/Claude marketplace installation.

Attach the skills by name in Air. Avoid importing them back into **Codex (Global)**
or **Claude Agent (Global)** when those clients already use the marketplace plugin.
Manage Air sources through its Skills settings; do not manually retarget IDE
storage links or edit generated `air-views` directories.
Air may expose IDE skills to hosted agents separately from their native plugins.
The current session can retain old skill paths until it is restarted.

See JetBrains' [Air skill management documentation](https://www.jetbrains.com/help/air/air-in-ides-extend-agent-capabilities.html#install-and-use-skills).

## Capture an agent issue

`capture-agent-issue` is packaged under
`plugins/agentic-devcraft/skills/capture-agent-issue/`. It remains explicit-only.
Its marketplace names are `/agentic-devcraft:capture-agent-issue` in Claude and
`$agentic-devcraft:capture-agent-issue` in Codex. Remove old standalone
`~/.claude/skills/capture-agent-issue` and `~/.codex/skills/capture-agent-issue`
links if migrating from the former candidate installation; do not delete other skills.

The Desktop side-entry shape was verified with the disposable explicit-only probe
on Claude embedded runtime 2.1.317 and Codex 0.167.0-alpha.3.2. Packaged names use
the plugin namespace. Paste the first form in Claude Desktop and the second in
Codex Desktop, replacing the issue statement:

```text
/btw /agentic-devcraft:capture-agent-issue Explain the mistake in the recent task and capture its evidence.
/side $agentic-devcraft:capture-agent-issue Explain the mistake in the recent task and capture its evidence.
```

In a confirmed tool-capable side/fork chat, capture runs directly. An ordinary
chat invocation delegates once. Unknown identity/capabilities produce a focused
question or concrete limitation, not recursive isolation or a bulk investigation
in the original chat. Claude terminal `/btw` has a separate tool-less implementation;
these Desktop forms are not a claim of universal CLI support. The user confirmed
that the installed skill was tested and successfully captures an issue packet.

The collector reads original records directly, keeping source session/cutoff and
collector identity separate. It saves one Markdown packet with attributed accounts,
self-assessment when supplied, evidence/counterevidence, effective instructions,
findings, recovery, execution constraints, scoped runtime/session metrics, and
candidate experiments. Missing metrics are explicit. It returns a path, brief
synopsis, and material gaps rather than a transcript dump.

Default output is:

```text
<host-temp>/agent-issues/<Subject Project>/<Original Session>/<YYYY-MM-DDTHH-mmZ>-<unique>/packet.md
```

Project/session names stay recognizable, including case, spaces, and supported
Unicode. Only filesystem-required character changes are made. The timestamp is
frozen capture-start in UTC, not the subject session's start. An explicit output
path overrides the default, never overwriting an existing packet; normal host
approval applies where needed. Packets and drafts default outside worktrees with
private permissions. OS cleanup can remove temporary files; deliberately retain
any packet you need long-term.

Payloads are de-identified by default. Specify `full-detail payload` to retain
context where policy permits, or name particular details to retain. This preference
does not anonymize the output filename. Review the packet before sharing. Nothing
is published, uploaded, committed, made into a remote issue, or fixed upstream.
Other agents can follow the same Markdown, but their invocation controls and
runtime retrieval support depend on the host.

## Retaining private packets in this worktree

The skill still defaults to host temp. For packets you deliberately keep locally,
use `captures/agent-issues/` in this checkout. That directory is git-ignored and is
not part of the plugin or published documentation. Existing retained packets were
moved there unchanged. An explicit skill output path can target a file in that
folder when desired; output directories must exist and normal write permissions apply.
