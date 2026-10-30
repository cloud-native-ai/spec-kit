# Contract: Identity and Wiring

**Scope**: the rename `think-skills` → `coaching-skills` across its eight identity coordinates, the closed wiring surface, the derived faces that are regenerated rather than edited, the upgrade path, the frozen test updates, and the history boundary.

**Literal authority**: `coaching-skills` (STR-001), `think-skills` (STR-002), `skill:coaching-skills` (STR-003), `skill-coaching-skills-wrapup` (STR-004), `skills/external/coaching-skills/SKILL.md` (STR-005) are owned by [`../requirements.md`](../requirements.md) § Shared Strings.

## C-1 Eight Identity Coordinates

| Coordinate | New value |
|------------|-----------|
| Source directory | `skills/external/coaching-skills/` |
| frontmatter `name` | `coaching-skills` |
| `skill_id` / Resource ID canonical path | `<SKILL:.specify/skills/coaching-skills/SKILL.md>` / `.specify/skills/coaching-skills/SKILL.md` |
| Runtime unit id | `skill:coaching-skills` |
| flow-class ledger row | `skill:coaching-skills` \| `execution` \| `behavior-oracle` \| (no neutral flag) \| new one-line rationale |
| probe Object row | `skill-coaching-skills-wrapup` \| `skill-wrapup` \| `skill:coaching-skills` \| `wrap-up` |
| `/speckit.skills` route row | points at `skills/external/coaching-skills/SKILL.md`, call form `coaching-skills <trainee-name|trainee-path> <work>` |
| description triggers | 教练 / 陪练 / 观察执行 / 预期 vs 实际 / 执行偏差 / 微调建议 / coaching, plus the explicit call form |

Trigger rule: triggers that promise a side-effect-free mental simulation only (“thought experiment”, “思想实验”, “不要真的执行”) MUST NOT survive, because the skill dispatches a real subagent. Triggers that express “predict first, then look at the real execution” may stay.

## C-2 Hand-Edited Source Files (closed set)

- The closed set and its allowed difference set are **owned by** [`../requirements.md`](../requirements.md) § Assumptions **A10**: the hand-edited source files (count and category split stated there) plus the derived faces regenerated from them, with exactly one permitted occurrence of the old literal (the `_OBSOLETE_SKILLS` entry). This contract MUST NOT re-list that set — a second enumeration is a copy that drifts from the owner, and the residual audit needs one decidable list, not several.
- Per-file obligations are owned by the requirements' own phrasing: FR-018 (identity coordinates), FR-022 (live wiring references), FR-023 (frozen tests). This contract adds only the constraints the requirements leave to the design: C-6's comment restatement and C-7's dated notes.
- `shared/definitions/framework-map.md` gains the `.specify/memory/coaching/` row required by the new run directory (Constitution XVII). This is a new-directory registration, not a rename coordinate, and it introduces no occurrence of the old name.

## C-3 Derived Faces — Regenerated, Never Hand-Edited

Derived faces are not a list this contract owns either: they are whatever the generators below produce from A10's source members. The table maps **regeneration entry → face** so the implementation knows which command owns each face; it is not a second face enumeration.

| Derived face | Regeneration entry |
|--------------|--------------------|
| `.specify/skills/coaching-skills/**` | `python3 scripts/python/sync-mirrors.py --write --only skills/external` |
| `.specify/skills/think-skills/**` (removal) | **Explicit deletion** — `sync-mirrors.py` never deletes extras (archive-not-delete) |
| `.specify/shared/definitions/*.md` | same mirror entry, `--only shared` |
| `.specify/agents/templates/*.agent.md` | same mirror entry, `--only agents` |
| Per-tool command copies (`.claude/commands`, `.github/prompts`, `.opencode/command`, `.qoder/commands`) | `python3 scripts/python/regen-command-copies.py` (fan-out from `templates/commands/`) |
| Per-tool agent copies (`.qoder/agents/*.agent.md`; siblings via the same renderer) | `.venv/bin/specify render-agents --ai qoder` (and the other render tools when their directories are present) |
| Compiled `## Wrap-up` block in the skill body | `python3 scripts/python/probe-utils.py --action compile-embeds` |
| `.specify/memory/feedback/probe-map.md` | `python3 scripts/python/probe-utils.py --action map` |

## C-4 Upgrade Path

- The old directory name enters `src/specify_cli/__init__.py` `_OBSOLETE_SKILLS`.
- `cleanup_obsolete_framework_assets()` skips a path that is a symlink or absent and removes an entity directory. That is exactly the required behaviour: the entity directory is deleted, a user-authored symlink of the same name survives.
- No change to the cleanup code is required; the entry alone activates it.

## C-5 Route and Discovery Consistency

- The `/speckit.skills` route table keeps five rows; only the modify-family row changes name and gains the two-parameter call form.
- The skill keeps `classification: external` and stays under `skills/external/`.
- The description advertises the new call form so a reader who never saw the old skill can invoke it.

## C-6 Residual Rule

- The closed wiring surface and its allowed difference set are owned by [`../requirements.md`](../requirements.md) § Assumptions **A10**: inside that surface the old literal appears exactly once, and the one permitted difference is the `_OBSOLETE_SKILLS` tuple entry. This clause neither re-lists the surface nor restates its count.
- Consequence for `src/specify_cli/__init__.py`: the historical comment that currently spells the old name (inside the OBSOLETE-ASSET-REGISTRY region) is restated without the literal — it keeps the rename-chain meaning and points at Feature 078 instead of repeating the token.
- Historical records are outside the surface: the boundary is owned by FR-024 / A9, not enumerated here.
- **Residual audit derivation (no fifth hand-written enumeration)**: the audit's candidate path list is derived at run time by the guard copy — `tests/contract/test_coaching_wiring_contract.py` (plan § Project Structure; tasks T020/T026). It combines (i) the six mirror pairs declared by `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` (source side plus mirror side), (ii) the per-tool copy targets declared by `scripts/python/regen-command-copies.py`, and (iii) A10's residual hand-edited members not reachable through either generator, pinned as a literal **inside that test** — the one place one-source-of-truth admits a duplicate (a guard copy). The assertion is: exactly one surviving occurrence, in `src/specify_cli/__init__.py`. A change to A10 must land in the requirements first; the guard then fails until it is updated, and that failure is the point.

## C-7 Frozen Baseline Tests

- All four test files are updated explicitly, each carrying a dated note with the reason (2026-10-30, Feature 078 rename).
- Counts stay consistent with the directory: 52 skills (15 external + 37 internal), 27 command templates, 49 hash-manifest skills.
- The hash manifest of 069a is a dated record and is not rewritten. `test_expression_compatibility.py` gains a retired-path register mapping the old manifest path to the new one with date and reason, so the C-5 “no new skill” assertion stays decidable instead of degrading into an empty assertion (see plan § Decision Tensions T-001).
- No test count may change silently; a change without its date-and-reason note fails review.

## C-8 Verifiable Surface

After implementation the following commands are the verification surface for SC-006 / SC-008. Each is expected to be run once against the real tree during `/speckit.implement`, and their outputs recorded in that stage's evidence:

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"
python3 .specify/scripts/python/flow-class-check.py --action check
python3 scripts/python/probe-utils.py --action probes --validate
python3 scripts/python/probe-utils.py --action compile-embeds --check
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
python3 scripts/python/scan-confirmation-gates.py --summary
```

The residual-audit verdict is **not** a prose pathspec: it is the guard copy named in C-6 (`tests/contract/test_coaching_wiring_contract.py`, run through the project's pytest). It derives the candidate set and asserts the single permitted hit; a concrete `git grep` path list here would be exactly the duplicate this contract removed. An ad-hoc `git grep -n` over A10's surface is a diagnostic, not the verdict; a repo-wide `git grep -c` counts records and proves nothing, because SC-006 is scoped to A10.

### New-line gate (SC-008 third condition / FR-027)

The judged unit is the **added line**, not the total. The pathspec is the scanner's own scan surface (`SCAN_DIRS` + `SCAN_ROOT_FILES` declared in `scripts/python/scan-confirmation-gates.py`), which is a subset of A10's closed surface — so the surface is derived from the scanner, never re-listed here.

```bash
BASE=<feature baseline commit>   # A10 baseline; its SHA is recorded in the stage evidence before the run
git diff "$BASE" -- templates/commands skills shared 'templates/*.md' \
  | grep '^+' | grep -v '^+++' \
  | python3 -c '
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gates", "scripts/python/scan-confirmation-gates.py")
gates = importlib.util.module_from_spec(spec); spec.loader.exec_module(gates)
lines = [line[1:].rstrip("\n") for line in sys.stdin if line.startswith("+")]
hits = [(i, line) for i, line in enumerate(lines, 1) if gates.BLOCKING_RE.search(line)]
print("added_lines=%d blocking_hits=%d" % (len(lines), len(hits)))
for i, line in hits: print("hit %d: %s" % (i, line))
sys.exit(1 if hits else 0)
'
```

Expected: `blocking_hits=0`, exit 0. The baseline reading (same command, same pattern source, taken before the change) MUST be recorded in the stage evidence; the current reading is `test-evidence/gate-newline-baseline.txt` (added_lines=0, blocking_hits=0; total blocking=27 = destructive 20 + governance_kept 7, violations=0).
