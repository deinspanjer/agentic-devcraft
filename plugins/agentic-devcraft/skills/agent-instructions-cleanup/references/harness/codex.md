# Codex instruction files

Apply these rules only when Codex is a target.

## File selection

- At each directory level Codex checks `AGENTS.override.md` before `AGENTS.md` and
  uses only the first non-empty file at that level.
- This is a per-directory choice of file. An override replaces the `AGENTS.md`
  beside it; it does not erase instructions from ancestor directories.
- Enforce one effective instruction file per directory level: choose exactly one of
  `AGENTS.override.md` or `AGENTS.md`, never both, unless the user explicitly asks
  to keep both files on disk.
- Choose `AGENTS.override.md` only when replacing the `AGENTS.md` at that level is
  actually required (for example a temporary or directory-specific replacement).
  Otherwise keep or create `AGENTS.md` as the single effective file for that level.
- If both files already exist at one level, treat this as conflict-risk and stop to
  ask unless the user explicitly asks to keep both.

## Output files

- `AGENTS.md` is the default single effective file.
- `AGENTS.override.md` only when a replacement is intended; include an explicit
  “replaces AGENTS.md here” marker.
- Do not output both at the same directory level unless explicitly requested.

## Ignore recommendation

Only inside a Git repo, and only when override files are actually used or proposed,
recommend adding `AGENTS.override.md` to `.gitignore` and explain why:

- `AGENTS.override.md` commonly contains temporary or user-local overrides.
- Ignoring it reduces accidental commits of personal/local guidance.

## Rationalization counters

- "We should always generate both AGENTS.md and AGENTS.override.md." -> "Codex reads one file per level by precedence; choose one effective file unless user explicitly wants both present on disk."
- "A minimal AGENTS.md plus full AGENTS.override.md is always safer." -> "That creates avoidable ambiguity; default to a single effective file and document the choice."

## Red flags

- Creating both `AGENTS.md` and `AGENTS.override.md` at the same directory level by default.
- Treating `AGENTS.override.md` as additive instead of replacement-precedence.
- Describing an override as removing ancestor instructions.
- Omitting the `AGENTS.override.md` ignore recommendation in Git repos when override files are involved.
