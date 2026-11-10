# Spec Repair — 092-non-disposable

Repair of the stale references in the archived spec `.specify/archive/specs/092-non-disposable/`,
executed read-first against `master` @ `9ac56bf10` (2026-11-10). The prior audit measured
`6fb8093c4`; every path below was re-measured on the current HEAD. Only the eight files in
§ Edits were written. No commit, no push, no subagent.

## Inputs

- **Audit**: `090/test-evidence/spec-audit-092-non-disposable.md` (batch 11) — 181 distinct refs:
  137 alive / 17 archived-elsewhere / 27 dead.
- **Settled scan**: `090/test-evidence/spec-audit-settled.json` →
  `.specify/archive/specs/092-non-disposable`: refs 201, alive 172, moved 172, dead 29,
  `dead_list` 20 entries.
- **Fresh re-scan** (same artifact scope as the audit; tokenizer also catches `templates/`, `tests/`,
  `skills/` roots): 227 distinct literals — 168 alive / 19 archived-elsewhere / 30 dead /
  10 placeholder. Re-measuring the anchor-layout merge on today's tree moves
  `.specify/memory/{constitution,features,glossary,register}.md` and `.specify/memory/features/092.md`
  into the dead set; the audit's mid-merge counts are therefore not directly comparable.

Counting rules: an **occurrence** is one path literal on one line (two literals on one line count twice);
a **distinct literal** is one normalized spelling (a glob counts once; a brace list counts once). The
repair subject is every reference that did **not** resolve in the live tree as written — dead plus
archived-elsewhere — because the instruction accepts the archived copy as a fix target.

## Counts

| Disposition | Distinct literals | Occurrences |
|---|---:|---:|
| **Dead total (as written)** | **50** | **163** |
| live-fixed | 20 | 73 |
| dated-kept | 30 | 59 |
| non-reference | 10 | 31 |
| placeholder / example (also non-reference, outside the subject) | 9 forms | 17 |

- 73 + 59 + 31 = 163.
- Per-class distinct counts overlap: ten literals (`constitution`, `features`, `features/092`,
  `glossary`, `register`, the bare `092` directory, `092/**`, `coverage-baseline.txt`,
  `notes/input-review-080-090.md`, `requirements.md`) carry both fixed and kept occurrences; the union
  across the three classes is the 50-literal subject.
- Scope excluded, by the audit's own rule: `test-evidence/` (dated evidence, read for cross-reference
  only), `coverage-baseline.txt` and `notes/baseline-failed-tests.txt` (raw output). References into
  `test-evidence/` that appear in the audited artifacts are counted and are dated-kept by rule.

## Per-entry disposition

### Live-fixed — 73 occurrences / 20 literals

| # | Before (literal) | After (actual target) | Anchors |
|---|---|---|---|
| 1 | `.specify/goal/**` | `.specify/anchoring/**` (goal archive renamed; `scripts/python/goal-utils.py` `ARCHIVE_DIRNAME = ".specify/anchoring"`) | team/team.md:48, team/team.md:269 |
| 2 | `.specify/memory/constitution.md` | `.specify/constitution.md` | feature-ref.md:48, plan.md:53, requirements.md:388 |
| 3 | `.specify/memory/features.md` | `.specify/features.md` | contracts/acceptance-readability.contract.md:32, contracts/acceptance-readability.contract.md:68, feature-ref.md:16, feature-ref.md:39, plan.md:201, plan.md:378, plan.md:493, requirements.md:295, tasks.md:10, tasks.md:271, tasks.md:324, team/team.md:29, team/team.md:74, team/team.md:79, team/team.md:82 |
| 4 | `.specify/memory/features/092.md` | `.specify/features/092-non-disposable.md` | checklists/2026-11-09-requirements-quality.md:8, feature-ref.md:15, feature-ref.md:40, plan.md:58, plan.md:202, plan.md:315, plan.md:493, requirements.md:295, tasks.md:33, tasks.md:325, team/team.md:30 |
| 5 | `.specify/memory/glossary.md` | `.specify/glossary.md` | feature-ref.md:38, plan.md:200, plan.md:492, requirements.md:294, team/team.md:28 |
| 6 | `.specify/memory/register.md` | `.specify/register.md` | feature-ref.md:41, feature-ref.md:102, plan.md:203, plan.md:455, plan.md:496, requirements.md:298, tasks.md:33, tasks.md:327, team/team.md:31 |
| 7 | `.specify/memory/{glossary,features,register}.md` | `.specify/{glossary,features,register}.md` | plan.md:315, tasks.md:72 |
| 8 | `.specify/specs/088-*/efficiency-model.md` | `skills/external/sdd-loop-driver/references/efficiency-model.md` (§ 证据路径拼写, the live owner spelling; the target file was verified to exist and to carry B4's evidence-path section) | tasks.md:278 |
| 9 | `.specify/specs/092-non-disposable` | `.specify/archive/specs/092-non-disposable` | research.md:216, research.md:218, tasks.md:29, tasks.md:43, tasks.md:323, team/team.md:6 |
| 10 | `.specify/specs/092-non-disposable/` | `.specify/archive/specs/092-non-disposable/` | feature-ref.md:9, plan.md:172, tasks.md:11 |
| 11 | `.specify/specs/092-non-disposable/**` | `.specify/archive/specs/092-non-disposable/**` | team/team.md:20 |
| 12 | `.specify/specs/092-non-disposable/checkpoints/` | `.specify/archive/specs/092-non-disposable/checkpoints/` | team/team.md:265 |
| 13 | `.specify/specs/092-non-disposable/checkpoints/**` | `.specify/archive/specs/092-non-disposable/checkpoints/**` | team/team.md:147 |
| 14 | `.specify/specs/092-non-disposable/coverage-baseline.txt` | `.specify/archive/specs/092-non-disposable/coverage-baseline.txt` | plan.md:216 |
| 15 | `.specify/specs/092-non-disposable/goal/092-non-disposable/goal.md` | `.specify/archive/specs/092-non-disposable/goal/092-non-disposable/goal.md` | team/team.md:181 |
| 16 | `.specify/specs/092-non-disposable/notes/` | `.specify/archive/specs/092-non-disposable/notes/` | plan.md:217 |
| 17 | `.specify/specs/092-non-disposable/notes/input-review-080-090.md` | `.specify/archive/specs/092-non-disposable/notes/input-review-080-090.md` | plan.md:5, requirements.md:26, requirements.md:399 |
| 18 | `.specify/specs/092-non-disposable/notes/quickstart-run.md` | `.specify/archive/specs/092-non-disposable/notes/quickstart-run.md` | tasks.md:157, tasks.md:166, tasks.md:190 |
| 19 | `.specify/specs/092-non-disposable/requirements.md` | `.specify/archive/specs/092-non-disposable/requirements.md` | plan.md:5, research.md:217 |
| 20 | `.specify/specs/092-non-disposable/tasks.md` | `.specify/archive/specs/092-non-disposable/tasks.md` | tasks.md:29, tasks.md:41 |

Fix rule applied: a *locator* — a reference a reader or a gate command must follow to a surviving
artifact — was re-pointed. Present-tense normative text (FR landing points, plan layout/face tables,
reference card, DoD/GATE checks, open task rows, team territory fields, research R12 gate table) was
included; completed `[X]` task rows were not (see dated-kept).

### Dated-kept — 59 occurrences / 30 literals (text unchanged)

| # | Literal | Anchors | Why kept |
|---|---|---|---|
| 1 | `.specify/archive/.tmp-probe` | notes/quickstart-run.md:53 | dated run-log scratch reading |
| 2 | `.specify/goal` | notes/refactor-anchoring-merge.md:12 | dated rename record; old spelling is the subject |
| 3 | `.specify/goal/` | notes/refactor-anchoring-merge.md:7, :13 | same |
| 4 | `.specify/memory/constitution.md` | notes/pre-change-measurements.md:47, :84 | dated measurement commands + raw output |
| 5 | `.specify/memory/features.md` | notes/input-review-080-090.md:23; notes/measurement-corpus.md:62; notes/pre-change-measurements.md:101; tasks.md:119 | dated review/corpus/measurement records; `tasks.md:119` is a completed `[X]` row |
| 6 | `.specify/memory/features/088.md` | notes/pre-change-measurements.md:101 | dated measurement record |
| 7 | `.specify/memory/features/092.md` | tasks.md:120 | completed `[X]` row (what was done) |
| 8 | `.specify/memory/glossary.md` | notes/pre-change-measurements.md:57; tasks.md:116 | dated `git status` output; completed `[X]` row |
| 9 | `.specify/memory/register.md` | plan.md:462; tasks.md:121 | plan's executed measurement snippet; completed `[X]` row |
| 10 | `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/` | tasks.md:281 | dated defect record — the pre-rename path is the rename task's subject; repair landed at `.specify/teams/089-script-interface-contract/team.md` |
| 11 | `.specify/specs/092-non-disposable` | notes/refactor-anchoring-merge.md:3; tasks.md:123 | dated directive record; completed `[X]` row with executed command |
| 12 | `.specify/specs/092-non-disposable/**` | checkpoints/01-requirements.md:40, checkpoints/03-plan.md:41 | dated checkpoint territory records |
| 13 | `.specify/specs/092-non-disposable/coverage-baseline.txt` | tasks.md:123 | completed `[X]` row (executed command) |
| 14 | `.specify/specs/092-non-disposable/notes/input-review-080-090.md` | notes/measurement-corpus.md:3 | dated corpus source record (2026-11-09) |
| 15 | `.specify/specs/092-non-disposable/notes/measurement-corpus.md` | tasks.md:122 | completed `[X]` row |
| 16 | `.specify/specs/092-non-disposable/notes/pre-change-measurements.md` | tasks.md:118 | completed `[X]` row |
| 17 | `.specify/specs/092-non-disposable/plan.md` | notes/measurement-corpus.md:4 | dated corpus source record |
| 18 | `.specify/specs/092-non-disposable/requirements.md` | checkpoints/01-requirements.md:7; requirements.md:397 | dated checkpoint; A12 stage write-boundary record |
| 19 | `.specify/specs/092-non-disposable/team/092-non-disposable/runs/**` | team/team.md:147 | never produced; the path never existed (no target to point at) |
| 20 | `.specify/specs/092-non-disposable/team/092-non-disposable/team.md` | checkpoints/07-parallel-wave.md:41; notes/pre-change-measurements.md:59 | dated defect-symptom record (`git status` output) |
| 21 | `.specify/specs/092-non-disposable/test-evidence/` | contracts/four-stage-command.contract.md:90; notes/quickstart-run.md:130; plan.md:219; quickstart.md:196; requirements.md:246; tasks.md:434 | cleaned `test-evidence/` path — dated by rule |
| 22 | `.specify/specs/092-non-disposable/test-evidence/**` | team/team.md:147 | cleaned `test-evidence/` path — dated by rule |
| 23 | `.specify/specs/092-non-disposable/test-evidence/INDEX.md` | tasks.md:326 | never produced (T153 open; no target) |
| 24 | `.specify/specs/092-non-disposable/test-evidence/repair-*.md` | feature-ref.md:44; plan.md:320 | planned "NEW at execution time"; never produced |
| 25 | `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md` | tasks.md:268, :286 | never produced (T119/T137 open) |
| 26 | `.specify/specs/092-non-disposable/test-evidence/reporter-092-non-disposable.live.log` | team/team.md:148 | never produced (no archive copy, no target) |
| 27 | `.specify/specs/092-non-disposable/test-evidence/shift-092.md` | tasks.md:300, :301, :302, :303, :306, :307 | never produced (T139–T142/T145/T146 open) |
| 28 | `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` | tasks.md:321, :322 | cleaned `test-evidence/` path; the file survives in the archive, but the citation is a dated gate-output instruction |
| 29 | `.specify/specs/092-non-disposable/test-evidence/u15-report.txt` | notes/quickstart-run.md:73, :75, :76 | dated run-log record |
| 30 | `.specify/specs/092-non-disposable/verification.md` | plan.md:215, plan.md:322, tasks.md:42, tasks.md:320 | never produced anywhere (T147 open); no target to point at |

Rule applied: notes, checkpoints, `[X]` task rows, executed commands, test-evidence citations and
never-produced artifacts are records of what happened or was intended — not locators — so they were
not rewritten.

### Non-reference — 31 occurrences / 10 literals (text unchanged)

| # | Literal | Anchors | Why ignored |
|---|---|---|---|
| 1 | `.specify/.tmp/086-*` | feature-ref.md:85; notes/input-review-080-090.md:91; notes/measurement-corpus.md:51, :145; plan.md:437; quickstart.md:143; requirements.md:282, :414 (x2), :452; tasks.md:303 | registered exclusion (H3, legitimate historical measurement paths) |
| 2 | `.specify/.tmp/probe` | notes/quickstart-run.md:50; quickstart.md:179 | illustrative ignore-leg example |
| 3 | `.specify/.tmp/x.tmp` | plan.md:263 | illustrative ignore-leg example (EP-008) |
| 4 | `.specify/history/.work/a.txt` | plan.md:263 | illustrative ignore-leg example (EP-008) |
| 5 | `.specify/history/.work/probe` | notes/quickstart-run.md:51; quickstart.md:181 | illustrative ignore-leg example |
| 6 | `.specify/memory/sanitize/` | contracts/renumber-and-supersede.contract.md:55 | `MACHINE_PREFIXES` constant value (`scripts/python/renumber-utils.py`), not a path pointer |
| 7 | `.specify/memory/sanitize/findings.json` | contracts/four-stage-command.contract.md:92; requirements.md:246; tasks.md:185 | explicitly **prohibited** evidence destination |
| 8 | `.specify/skills/external/` | notes/input-review-080-090.md:89; notes/measurement-corpus.md:49, :143; plan.md:379, plan.md:435; requirements.md:414 | named defect H1 — "a directory that never existed"; the defect's subject, not a target |
| 9 | `.specify/specs/.archive/` | contracts/renumber-and-supersede.contract.md:54; research.md:81 | `EXCLUDED_PREFIXES` constant value (`scripts/python/renumber-utils.py`), legacy prefix |
| 10 | `.specify/templates/commands/` | feature-ref.md:35; plan.md:241 | retired by design; both sentences say so (`scripts/python/sync-mirrors.py:18-19`) |

### Placeholder / example — 17 occurrences / 9 forms (outside the subject; non-reference)

`.specify/.tmp/<plan>` (quickstart.md:197) · `.specify/anchoring/<slug>/anchor.md` and
`.specify/goal/<slug>/goal.md` (notes/refactor-anchoring-merge.md:18, rename-map placeholders) ·
`.specify/memory/{sanitize…}` brace constant list (research.md:82) ·
`.specify/specs/<NNN-slug>/team/team.md` (tasks.md:276) · `.specify/specs/<spec-dir>/test-evidence/`
(7 occurrences: contracts/four-stage-command.contract.md:89, data-model.md:134, feature-ref.md:65,
notes/quickstart-run.md:130, plan.md:41, requirements.md:246, tasks.md:185) ·
`.specify/specs/{085…}` (tasks.md:466) · `.specify/{archive…}` (notes/input-review-080-090.md:95,
requirements.md:9, :241) · `templates/commands/{goal…}` (notes/refactor-anchoring-merge.md:27).

## Settled-scan `dead_list` reconciliation — 20/20

| # | `dead_list` entry | Disposition |
|---|---|---|
| 1 | `.specify/specs/069` | non-reference — tokenizer prefix of the live glob `.specify/specs/069*/**`; `069-execution-expression-sdd`, `069a-*`, `069b-*` exist |
| 2 | `.specify/specs/.archive/` | non-reference — `EXCLUDED_PREFIXES` constant value |
| 3 | `.specify/memory/sanitize/findings.json` | non-reference — prohibited destination |
| 4 | `.specify/specs/087-` | non-reference — prefix of `.specify/specs/087-*/`; `087-arch-diagram-docs` exists |
| 5 | `.specify/history/.work/probe` | non-reference — illustrative ignore leg |
| 6 | `.specify/specs/067-` | non-reference — prefix of `.specify/specs/067-*/`; `067-loop-efficiency-hardening` exists |
| 7 | `.specify/goal` | **live-fixed** in team/team.md:48, :269 (→ `.specify/anchoring/**`); dated-kept in notes/refactor-anchoring-merge.md:12 |
| 8 | `.specify/specs/082-` | non-reference — prefix; `082-self-explanatory-integration` exists |
| 9 | `.specify/.tmp/x.tmp` | non-reference — illustrative ignore leg |
| 10 | `.specify/templates/commands/` | non-reference — retired by design |
| 11 | `.specify/specs/081-` | non-reference — prefix; `081-acceptance-hardening` exists |
| 12 | `.specify/.tmp/probe` | non-reference — illustrative ignore leg |
| 13 | `.specify/history/.work/a.txt` | non-reference — illustrative ignore leg |
| 14 | `.specify/specs/077-` | non-reference — prefix; `077-doc-sdd-integration` exists |
| 15 | `.specify/specs/088-` | non-reference — prefix; `088-speckit-visualization` exists |
| 16 | `.specify/goal/` | **live-fixed** in team/team.md:269 (→ `.specify/anchoring/**`); dated-kept in notes/refactor-anchoring-merge.md:7, :13 |
| 17 | `.specify/specs/084-` | non-reference — prefix; `084-harness-triple-structure` exists |
| 18 | `.specify/memory/sanitize/` | non-reference — `MACHINE_PREFIXES` constant value |
| 19 | `.specify/specs/083-` | non-reference — prefix; `083-mechanism-policy-separation` exists |
| 20 | `.specify/specs/090-` | non-reference — prefix; `090-re-anchoring` exists |

## Audit dead-list reconciliation

- Rows 18–24 (seven promised-but-never-produced artifacts) → dated-kept rows 19, 20, 23–30 above.
- Row 25 `.specify/goal/**` → live-fixed (team.md) / dated-kept (rename record).
- Row 26 088 `efficiency-model.md` → live-fixed (tasks.md:278).
- Row 27 089 old team dir → dated-kept defect record (tasks.md:281); the repair landed at
  `.specify/teams/089-script-interface-contract/team.md`.
- Rows 28–36 (constants, retired/defect paths, prohibited destinations, illustrative scratch) →
  non-reference.
- Rows 37–39 (`<plan>`, `<NNN-slug>`, `<spec-dir>` placeholders) → placeholder/non-reference.
- Rows 40–44 (anchor-layout moves) → **43 occurrences live-fixed**, 11 dated-kept across the five
  moved literals (constitution 2, features.md 4, features/092 1, glossary 2, register 2); one further
  moved-detail literal (`.specify/memory/features/088.md`, notes/pre-change-measurements.md:101) is
  dated-kept. The 090 merged slice's downstream rows are outside this spec's directory and were not touched.

## Edits (scope proof)

Eight files, all inside `.specify/archive/specs/092-non-disposable/`:

`requirements.md`, `plan.md`, `tasks.md`, `feature-ref.md`, `research.md`, `team/team.md`,
`contracts/acceptance-readability.contract.md`,
`checklists/2026-11-09-requirements-quality.md`.

`git diff -U0` = 51 changed line pairs, 73 path substitutions; normalizing the known path spellings and
comparing each `-`/`+` pair leaves **0** non-path differences. No spec/source file outside the spec
directory was modified; this evidence file is the only write outside it. The other modified paths in
`git status` belong to concurrent sibling repair forks and were not touched here.

## Validator readings

Run before and after the edits, on the archived artifacts:

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/archive/specs/092-non-disposable/requirements.md
status: ok  (id-contiguous / doc-order / ref-resolvable / marker-count / dup-id / path-marker all pass)
0 error(s), 0 warning(s)   rc=0                # identical before and after

$ python3 .specify/scripts/python/validate-tasks.py .specify/archive/specs/092-non-disposable/tasks.md
PASS: .specify/archive/specs/092-non-disposable/tasks.md — 0 error(s), 0 warning(s)   rc=0
                                                # identical before and after
```

Additional validators for the two other changed normative files:

```text
$ python3 skills/internal/create-team/scripts/validate-roster.py .specify/archive/specs/092-non-disposable/team/team.md
conforming: team 092-non-disposable carries exactly one reporter seat (agent: reporter)   rc=0

$ python3 scripts/python/validate-decision-tensions.py --spec .specify/archive/specs/092-non-disposable
status: ok  (all six checks pass; 7 record(s); 0 error(s), 0 warning(s))   rc=0
```

## Anomaly

**Anomaly**: the settled scan's 20-entry `dead_list` is partly a tokenizer artifact — 11 entries are glob
prefixes (`.specify/specs/{067-,069,077-,081-,082-,083-,084-,087-,088-,090-}` and
`.specify/memory/sanitize/`) of live glob literals or constant-value lists, so they were classified
non-reference rather than repaired; every true dead literal in both input lists is accounted for above,
and no spec/source file outside the 092 archive was modified.

SPEC-REPAIR-8-DONE
