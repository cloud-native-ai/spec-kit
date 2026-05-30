# Quickstart: Authoring a Skill with `${SKILL_HOME}` and `${SKILL_WORKDIR}`

**Branch**: `012-skill-home-workdir` | **Date**: 2026-05-30 | **Plan**: [plan.md](plan.md)

This quickstart walks a Skill author through the minimal end-to-end use of the new convention. Completing it once verifies User Story 1 and User Story 2 (both P1) from `requirements.md`.

## Prerequisites

- A working Spec Kit checkout on macOS or Linux.
- A POSIX shell (`/bin/bash`, `/bin/sh`, or equivalent). No GNU coreutils required.
- One existing or fresh Skill directory you control, e.g., `skills/my-skill/`.

## Step 1 — Create a script that uses both variables

Create `skills/my-skill/scripts/render.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Normative FR-016 idiom — copy verbatim, adjust the "/.." count only if your
# script is nested deeper than ${SKILL_HOME}/scripts/<name>.sh.
SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}"
SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"

# Skill-owned read: a template that ships with the Skill.
template="${SKILL_HOME}/assets/template.md"

# User-facing write: an output file in whatever directory the user invoked us from.
output="${SKILL_WORKDIR}/rendered.md"

cp "$template" "$output"
echo "Read template: $template"
echo "Wrote output:  $output"
```

Create the template the script reads:

```bash
mkdir -p skills/my-skill/assets
printf 'Hello from %s\n' '${SKILL_HOME}' > skills/my-skill/assets/template.md
chmod +x skills/my-skill/scripts/render.sh
```

## Step 2 — Run it from a user project directory

```bash
cd /tmp
mkdir -p alice-project && cd alice-project
/path/to/spec-kit/skills/my-skill/scripts/render.sh
```

Expected output:

```
Read template: /path/to/spec-kit/skills/my-skill/assets/template.md
Wrote output:  /tmp/alice-project/rendered.md
```

**Verification points**:
- `${SKILL_HOME}` resolved to the Skill's real on-disk directory regardless of where you ran the script from. ✅ User Story 1.
- `${SKILL_WORKDIR}` resolved to `/tmp/alice-project` — the directory you `cd`'d into, NOT the Skill's install directory. ✅ User Story 2.
- `rendered.md` appeared in `/tmp/alice-project/`, not under `skills/my-skill/`. ✅ FR-005.

## Step 3 — Verify the symlink case (User Story 1, Acceptance Scenario 3)

If your Spec Kit checkout has the compatibility symlink `.github/skills` → `.specify/skills`, run the Skill via the symlinked path:

```bash
cd /tmp/alice-project
/path/to/spec-kit/.github/skills/my-skill/scripts/render.sh   # via the symlink
```

The first line should print the same `/path/to/spec-kit/.specify/skills/my-skill/...` absolute path (or your `skills/...` source path, whichever is the real target) — never the `.github/skills/...` symlink path. This confirms `pwd -P` resolved the symlink correctly per FR-014.

## Step 4 — Verify runtime export precedence (Clarifications Q3)

Override `${SKILL_HOME}` from the environment to confirm the `${VAR:-fallback}` pattern preserves the export:

```bash
SKILL_HOME=/tmp/forced-home /path/to/spec-kit/skills/my-skill/scripts/render.sh
```

Expected: the first printed line uses `/tmp/forced-home/assets/template.md` (the export wins; the fallback is suppressed). This is the contract by which an agent runtime that exports `SKILL_HOME` automatically takes precedence over the script's self-computation.

## Step 5 — Migration drill (User Story 3)

Pick any line in your `SKILL.md` that still uses a legacy idiom and rewrite it using the migration mapping. Examples (these are the rows the template's Migration Mapping section will contain):

| Legacy | Rewrite |
|--------|---------|
| `./scripts/init.sh` | `${SKILL_HOME}/scripts/init.sh` |
| `${SKILL_ROOT}/references/spec.md` | `${SKILL_HOME}/references/spec.md` |
| `~/.copilot/skills/my-skill/assets/x.png` | `${SKILL_HOME}/assets/x.png` |

Re-run Step 2 to confirm the rewritten Skill behaves identically (this is the SC-004 regression check at the per-Skill level).

## Done

You have exercised:
- ✅ User Story 1 (Skill-owned reads work everywhere)
- ✅ User Story 2 (user-facing writes hit the user's directory)
- ✅ User Story 3 (legacy idioms rewrite mechanically)
- ✅ FR-016 (script self-computes with runtime-export precedence)
- ✅ FR-014 (symlinked entrypoints resolve to the real target)

If anything in this walkthrough fails after the convention is implemented, file it against the contract test `tests/contract/test_skill_home_workdir_template.py` — the structural assertion that should have caught the regression upstream.
