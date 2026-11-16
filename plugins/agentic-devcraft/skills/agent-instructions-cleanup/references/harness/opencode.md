# OpenCode instruction files

Apply these rules only when OpenCode V2 is a target.

## File selection

- OpenCode reads `AGENTS.md`. It finds these files from the working directory up to
  the project root and combines them; a nearer file adds to its ancestors and does
  not replace them.
- OpenCode does not read `AGENTS.override.md`. Do not create or recommend one as an
  OpenCode override.
- Nested `AGENTS.md` files are normal scoped instructions.

## Existing override files

- Guidance in an `AGENTS.override.md` is invisible to OpenCode. Inventory it and
  keep every line in the preservation map anyway.
- Do not delete or empty the file because OpenCode ignores it. If OpenCode needs
  that guidance, propose a destination in `AGENTS.md` or another document and wait
  for approval like any other move.

## Output files

- `AGENTS.md` at each level that needs instructions.

## Ignore recommendation

None for override files. Do not make an `AGENTS.override.md` ignore rule a
prerequisite when OpenCode is the only target.

## Red flags

- Applying override precedence or a one-file-per-level rule to OpenCode.
- Telling the user a nearer `AGENTS.md` replaces its ancestors.
