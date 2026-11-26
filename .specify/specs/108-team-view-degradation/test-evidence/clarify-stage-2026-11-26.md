# Clarify Stage Evidence — 2026-11-26

Line `team-view-degradation`; run `r20261126T071500Z-108a`; stage `clarify`; baseline `7e0874dad`; branch `108-team-view-degradation` (worktree).

## Mode & target

- **Mode A (post-requirements)** — `plan.md` absent in the spec dir; target `.specify/specs/108-team-view-degradation/requirements.md`. Writability confirmed by the landed edits (no root-owned path).
- **Unattended adjudication, no blocking questions** (precedent: 105 / 106 / 107 clarify sessions). The candidate queue was the brief's five explicit points plus Feature binding; every answer stayed inside the recorded adjudications (A-1…A-17) — no option space was invented.

## Feature binding (lookup evidence)

- Registry lookup (`grep -E '^\| [0-9]{3} ' .specify/features.md`): **`103-team-view` is not a Feature ID** — Feature 103 = Technical Debt Governance. The team command surface belongs to **Feature 027 (Team Management, `Ready for Review`)** whose Spec Path is `.specify/specs/103-team-view/requirements.md`.
- **Binding-precedent heuristic**: `036-team-summary`, `042-goal-team-creation` and `103-team-view` are all bound directly to Feature 027 (evidence: 027 detail `## Related Specifications/Requirements`; 103 requirements § Related Feature).
- **Verdict**: bind Feature 027 (bind branch; no new Feature). Index slice row **108** registered as `Draft` with detail pointer `.specify/features/027-team-management.md`; parent status stays `Ready for Review` (no-status-regression). Registry edited in the same pass as the spec (header `Total Features` 103 → 104 and the row together; 104 counted rows verified).
- The brief's leading candidate label is a finalized spec number, not a Feature ID — the lookup the brief ordered resolved it to the parent Feature; disclosed as an in-passing correction below.

## Five-point adjudication (written back in place; record appended under `## Clarifications` > `### Session 2026-11-26（无人值守 clarify 阶段…）`)

| Brief point | Decision | Where integrated |
|---|---|---|
| Report-name recognition closed set + named residue rule | Timestamp grammar closed at date `YYYYMMDD` / `YYYY-MM-DD` × time `hhmmss` / `hhmm` / `hh:mm:ss` / `hh-mm-ss`, `T`…`Z`, valid UTC instant; report form remainder `(?:-[0-9a-f]{4})?-(?:report|stage)`; name-only, order-fixed three-way classification (report / auxiliary / residue); canonical `latest_report_timestamp` (`YYYYMMDDThhmmssZ`); tie = lexicographic filename ascending (incumbent stable order) | FR-001, FR-002, FR-003; Session row 2 |
| Degradation exit-code mapping + no-inference boundary | Closed reasons `{engine-degraded, report-recognition-uncertain}` → `5` (2/2), co-occurrence names each reason; file-level four-state labels alone produce no reason and no exit change; unreadable latest report is FR-009 state only; overview produces no reasons and keeps its `0/2` domain with per-row uncertainty annotation; exit domain unchanged `0/2/3/4/5` | FR-017, FR-018, Edge Case (overview), FR-019 unchanged; Session rows 3–4 |
| Binding/goal normalization: guidance only vs repair | **Guidance only, zero writes on view** — `/speckit.team modify` as the definition-repair entry, `goal-utils.py bind` / `migrate` named as engine write surface only; any `goal` key declaration is a naming state (value shape never changes identity); identity order `anchor_slug` > `goal_slug` > inferred preserved | FR-013 amended; FR-011/FR-012/FR-014 unchanged; Session row 5 |
| Roster-matrix anomaly presentation | Matrix group carries `形态异常` + names the missing `agent` column; parsed matrix rows still rendered; `roster_delta` = `不可比对（not comparable）` + reason; frontmatter members in full; `seats` / `stage_seats` `未声明` + owner pointer; no silent empty sections | FR-015/FR-016 semantics unchanged (labels pinned); Session row 6 |
| Healthy behavior + one engine + migration/refusal | Healthy-predicate fixture at baseline `54c6efa8c` byte-identical stdout + same exit code; single recognition/latest entry incl. the overview column; sole delivery surface `scripts/python/team-view.py`; `goal-utils.py` zero modification; naming owner and schema unchanged → no migration; any shape change requires migration or deterministic refusal | FR-021/FR-022/FR-023 unchanged; Session row 7 |

Residue-uncertainty predicate pinned in FR-005: `runs/` present ∧ residue ≥ 1 ⇒ uncertainty (`report-recognition-uncertain`, exit 5) — no sanctioned "prove it is older" path (mtime/content inference rejected as non-deterministic and outside the read-only engine contract); missing/empty `runs/`, or stamped auxiliaries only, produce no uncertainty. This also reconciles A-5's "progress snapshot" auxiliary example with the measured corpus: a date-only prefix (`2026-10-07-progress-snapshot.md`) has no parseable timestamp → residue (46-file corpus count preserved: 28 conforming + 16 stamped non-conforming + 2 unstamped).

## Gates (verbatim captures)

- `validate-requirements.py .specify/specs/108-team-view-degradation/requirements.md` → exit 0, `status: ok`, **0 error / 0 warning**, `scanned: 239 lines, 33 definition rows, 3 shared strings` → `test-evidence/clarify-validator.txt`.
- `pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage requirements --repo .` → `decision=pass errors=0 advisories=0`, `fr=25 sc=8` → `test-evidence/pre-analyze-clarify.json` + `.txt`.
- **Derived-count revisit**: no FR / SC / STR addition, removal or renumbering (live counts stay 25 / 8 / 3; 33 definition rows unchanged), so no renumbering map and no checklist count correction task — the checklist gained an appended clarify note recording the new line-count reading (239) next to the requirements-stage reading (228), which stays as dated history.

## Workspace guard

- Pre-edit snapshot `.specify/.tmp/sdd-loop/tmp/team-view-degradation/workspace-guard-clarify.json` → post-write `--check`: **clean (rc 0)** — branch, full ref list and `.specify/specs` listing identical (no branch switch, no new spec dir).
- Persisted post-write signature `test-evidence/workspace-clarify.json` (self-check `clean`, rc 0). Readings: `test-evidence/workspace-clarify-readings.txt`.
- Working tree changes are exactly this feature's artifacts plus the two protocol-mandated registry files (`features.md`, `features/027-team-management.md`); nothing else.

## Concurrency

- `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded assignment; the five adjudication points are not independent units (they share one artifact and one integration pass).

## Corrections applied in passing (disclosed)

1. **Brief's leading candidate label**: `103-team-view` is a finalized spec number, not a Feature ID (Feature 103 = Technical Debt Governance). The brief explicitly ordered "lookup first", and the lookup resolved the binding to its parent Feature 027 — exactly one protocol-consistent reading, no option space.
2. **Brief constraint vs execution directive wording**: Constraints say "no spine/registry edits" while Execution mandates "register the slice row in `.specify/features.md` + parent detail". Read as: the state spine (read-only per the stage block) and the ID register (`.specify/register.md`) stay untouched; `features.md` row 108 + the 027 detail are the mandated Feature-binding duties and were edited. Nothing else was touched; no status transition was made.
3. **A-5 example vs corpus classification**: the auxiliary-artifact example "progress snapshot" is now explicitly scoped to stamped snapshots; the unstamped date-only snapshots classify as residue per FR-003/FR-005 (recorded in Session row 3, no assumption row rewritten).

## Anomalies

未发现异常 — no state required adjudication at this layer; the three items above are corrections applied in passing, not open decisions.
