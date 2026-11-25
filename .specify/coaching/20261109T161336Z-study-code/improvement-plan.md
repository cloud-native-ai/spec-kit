# Improvement plan — /study-code

**Run**: `20261109T161336Z-study-code` · entries ordered by priority; each names a concrete Trainee file and
section plus one tweak.

## Entries

| # | Trainee file / section | Tweak | Evidence |
|---|---|---|---|
| P-1 | `skills/external/study-code/SKILL.md` — § Workspace & inputs | Replace the single default with a **fallback ladder**: probe writability of `$WORK_DIR/../study-code/` first; if unwritable, fall to the host repo's sanctioned temp root (`.specify/.tmp/study-code/`) and then `~/tmp/study-code/`; record the chosen root + why in `strip-manifest.md`. | D-S1 / D-O3 |
| P-2 | `skills/external/study-code/SKILL.md` — § Step 1 strip-repo | Add a **source-integrity preflight**: before cloning, run `git fsck --no-dangling` / verify `refs` + index readability; on failure verify the object store and materialize the working tree with `cp -a`, recording the target commit hash — the exact path the run improvised. | D-S2 / D-P1 |
| P-3 | `skills/external/study-code/SKILL.md` — § Step 4 deep-study (point) | Add one line: when the diagram backend is unreachable, follow `references/uml-visualization-guide.md`'s degradation branch (Mermaid sketch + retained `.puml` + a visible degradation note) — never fail the step. | D-S3 |
| P-4 | `references/uml-visualization-guide.md` — render section | Make the unavailable-backend branch explicit (it exists only as a hint today): state the fallback outputs and the note format. | D-S3 |

## Run Status

- `run: success` — the Trainee's real work completed; the primary artifact exists and passed its own
  self-check; the target repo is untouched.
- `optimization: applied` — the plan is dispatched to `improve-skills` (target `study-code`) as one bounded
  improvement run; the result is recorded beside this plan, never inside the execution verdict.
