# Data Model: Review × Code-Review Composition (071)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner note**: this file owns the entity list, the field sets, and the validation rules of the composed review. The clause-level normative statements are owned by `contracts/`; where this file and a contract state the same rule, the contract is the normative text and this file is the shape. Literal values that requirements pin are referenced as `[[STR-NNN]]`, never copied.

## Entity map

| ID | Entity | Written by | Lives in |
|----|--------|-----------|----------|
| E1 | Review run | `/speckit.review` (command unit) | `.specify/specs/<key>/review.md`, `code-review.md` |
| E2 | Process segment | `review-sdd-process` (skill unit) | `review.md` |
| E3 | Code segment | `code-review` (skill unit) | `code-review.md` |
| E4 | Applicability triage | `/speckit.review` | `review.md` § code segment; its value is repeated in the feature detail entry |
| E5 | Feature-slice base and head | `git-delta-review.sh base` | `code-review.md` header, receipt block |
| E6 | Code segment record | `git-delta-review.sh start` + `note` + `receipt` | `code-review.md` |
| E7 | Coverage receipt | `git-delta-review.sh receipt` | inside E6 (delimited block) |
| E8 | Per-file verdict | `git-delta-review.sh note` / `receipt` | inside E7 |
| E9 | Segment verdict | `git-delta-review.sh receipt` + the `blocking` presence count of the current record | inside E7, mirrored in E13 |
| E10 | Gate verdict | `git-delta-review.sh report --summary --file` | E6, E13, feature detail entry |
| E11 | Archived record | `git-delta-review.sh start` (rotation) | `<spec>/code-review-<YYYYMMDDTHHMMSSZ>.md` |
| E12 | Feedback entry attribution | `feedback-utils.py` via each unit's wrap-up | `.specify/memory/feedback/` (existing store) |
| E13 | Process-report code section | `review-sdd-process` (fills from E3) | `review.md` § 2.1 |

## E1 — Review run

| Field | Type | Rule |
|-------|------|------|
| `requirement_key` | string | the spec directory name, e.g. `071-review-code-integration` |
| `segments` | ordered list | exactly `[process, code]`; order fixed; no reordering, no omission of `process` |
| `started_at` / `finished_at` | ISO 8601 | both segment conclusions are recorded; the closing summary may restate them and carries no obligation of its own |
| `run_id` | string | one stable id per run, shared by all three units' wrap-up records |
| `artifacts` | list of paths | `review.md` always; `code-review.md` only when triage = [[STR-005]] (C-11 of `contracts/command-orchestration.md`); a [[STR-001]] or [[STR-002]] run writes no record file |

**Transitions**: `started → process-running → (process-done | process-not-evaluated) → code-triage → (code-running | code-skipped-with-value) → both-artifacts-written → status-check → closed`.

**Rule V1**: the run is `closed` only after both segment conclusions exist as values — a segment that produced nothing is `not-evaluated` with a reason, never absent.
**Rule V2**: `code-triage` must resolve before `code-running`; there is no path from `process-running` directly to `code-running` (FR-003).
**Rule V3**: a `process-not-evaluated` state does not block `code-triage` (FR-002 failure propagation).

## E2 — Process segment

| Field | Type | Rule |
|-------|------|------|
| `judgment_object` | literal | the SDD process and the artifact chain that produced the feature |
| `severity_vocabulary` | closed set | `P0`, `P1`, `P2` — owned by `skills/internal/review-sdd-process/SKILL.md`; not touched by this feature |
| `report_path` | path | `<spec>/review.md`, structure owned by `templates/review-template.md` |
| `verdict` | literal | `done` or [[STR-002]] (with `reason`); an aborted process segment is [[STR-002]] and its record may be a command-authored minimal report |

**Rule V4**: this segment runs unconditionally; no field of E1 or E4 may be read as an exemption (FR-002).

## E3 — Code segment

| Field | Type | Rule |
|-------|------|------|
| `judgment_object` | literal | verifiable defects in this feature slice's committed code delta |
| `severity_vocabulary` | closed set | `blocking`, `important`, `suggestion`, `nitpick`, `question`, `praise` — owned by `skills/internal/code-review/SKILL.md` |
| `record_path` | path | `<spec>/code-review.md` ([[STR-004]]) — written only when triage = [[STR-005]] |
| `archive_path` | path or [[STR-009]] | `<spec>/code-review-<YYYYMMDDTHHMMSSZ>.md` when the run rotated a previous record; [[STR-009]] on a first run |
| `verdict` | E9 value | derived, never assigned by hand |

**Rule V5**: the two severity vocabularies never convert into one another; no field exists that stores a mapped or weighted value (FR-007).
**Rule V6**: `verdict = [[STR-006]]` requires `gap_files = 0`, `skipped_files = 0`, and zero `blocking` entries in the current record, simultaneously. The third conjunct is a presence test over the current record, not a resolution test: the model has no "cleared" state and no clearing operation, so a re-run that writes a record with no `blocking` heading is the whole mechanism (FR-014).

## E4 — Applicability triage

| Field | Type | Rule |
|-------|------|------|
| `value` | closed set | [[STR-005]] (`run`), [[STR-001]] (`not-applicable`), [[STR-002]] (`not-evaluated`) |
| `basis` | string | mandatory for [[STR-001]]: "feature produces no code deliverable" or "feature has no committed code delta"; the second basis is decided by the code-path predicate owned by the skill script (closed default set + `--code-paths`), which this model cites and does not re-implement |
| `reason` | string | mandatory for [[STR-002]]: the environment or resolution failure |
| `resolved_base` | E5 or [[STR-009]] | E5 when `value = [[STR-005]]`; [[STR-009]] otherwise |
| `worktree_uncommitted` | boolean | when true, the same disclosure sentence is written in two carriers: the record and `review.md` § 2.1 |

**Rule V7**: four values do not exist — an unspecified value, an empty value, a silently skipped segment, or a [[STR-006]] verdict on a non-[[STR-005]] triage (FR-003).
**Rule V8**: [[STR-001]] for an expression-class feature must leave the process segment's reader-baseline conclusion untouched (FR-027).
**Rule V29**: the record exists only when `value = [[STR-005]]`; [[STR-001]] and [[STR-002]] create no record file, not even an empty one, and their conclusion and reason live in E13 (FR-010).
**Rule V30**: `value = [[STR-005]]` iff the committed delta contains at least one code path under the predicate's owner (the skill script's closed default set, or the caller's `--code-paths` override); an empty changed set — base and head at the same commit, zero changed files — is [[STR-001]] with the basis "no committed code delta", decided before the receipt runs, so it can never be reported as a clean review of nothing (FR-003).

## E5 — Feature-slice base and head

| Field | Type | Rule |
|-------|------|------|
| `base_sha` | 40-hex or short | the resolved diff base |
| `head_sha` | 40-hex or short | explicit `--head`, else `HEAD` resolved once at run start; the value is fixed for the whole run even if new commits land |
| `base_source` | closed set | `explicit`, `feature-first-commit`, `trunk-merge-base` |
| `resolve_command` | string | the reproducible command, recorded when resolution fails |

**Rule V9**: base resolution order is `explicit` > `feature-first-commit` (parent of the first commit that added this feature's `requirements.md`) > `trunk-merge-base` (merge base with the repository default trunk). Trunk identification follows one closed order: explicit `--trunk` > a resolvable `refs/remotes/origin/HEAD` > an existing `main` > an existing `master` > [[STR-002]]; no heuristic outside that order exists (FR-004).
**Rule V10**: the script's built-in `GIT_BASE` default is never the composed path's base; no branch name is hard-coded anywhere in the resolution (FR-004).
**Rule V11**: an unresolvable base yields E4 = [[STR-002]] with `resolve_command` and the failure reason; a guessed base is forbidden (FR-006).
**Rule V31**: head carries **no source tier**, and that is a declared scope decision rather than an oversight: head has two forms (an explicit caller value, or the run-start `HEAD`) and no ordered search, so a `head_source` field would be a single-valued label restating `head_sha`'s provenance without adding a decision. `base_source` keeps its three tiers because the base really is searched. The reviewed range is `base..head`, MAY contain commits unrelated to this feature, and strict slicing requires an explicit head (FR-004, FR-006).

## E6 — Code segment record

Header (fixed field order, one table row each):

| Field | Rule |
|-------|------|
| Branch | `git rev-parse --abbrev-ref HEAD` |
| Base / Head | E5 ids with short forms; the head id is the run-start value, not a later read |
| Base source | E5 `base_source` |
| Renderer | the marker literal [[STR-008]] (`renderer: delta`) or [[STR-003]] (`renderer: text`) |
| Reviewer / Date | `git config user.name`, local date-time |

Body: the opinions (severity + file + optional line + text), the receipt block (E7), and the statistics table.

**Rule V12**: a re-run archives the previous file to E11 before writing. The archive name carries the run timestamp `YYYYMMDDTHHMMSSZ` (UTC, second resolution); the writer refuses to overwrite an existing archive (exit 2) rather than losing a record, and two runs inside one second either wait for the next second or take that exit 2 with the reason (FR-010).
**Rule V13**: the record is not listed in `AVAILABLE_DOCS` and is not read as plan/tasks input; the feature detail's `## Latest Review` review-record line links it (FR-012).
**Rule V32**: the renderer marker is [[STR-008]] only when the renderer is available **and** stdout is an interactive terminal; every other case — including an agent, a non-interactive call, or redirected output with `delta` on `PATH` — is [[STR-003]] (FR-013).

## E7 — Coverage receipt

Delimited block: `<!-- coverage-receipt:begin -->` … `<!-- coverage-receipt:end -->`. Lines are `name=value`, one per line. The name set is closed:

| Field | Type | Rule |
|-------|------|------|
| `receipt_version` | integer | currently `1` |
| `base` / `head` | commit id | copied from E5 in the same write |
| `base_source` | closed set | E5 value |
| `renderer` | `delta` \| `text` | must equal the header marker's mode (see V15) |
| `changed_files` | integer | size of the delta's changed-file set |
| `judged_files` | integer | entries with verdict `reviewed` |
| `skipped_files` | integer | entries with verdict `skipped` |
| `gap_files` | integer | changed files with no entry |
| `lines_added` / `lines_deleted` | integer | from `git diff --numstat` over E5's range |
| `file.<NN>.path` | repository-relative path | zero-padded ordinal, emitted in sorted path order |
| `file.<NN>.verdict` | `reviewed` \| `skipped` | exactly one per changed file |
| `file.<NN>.reason` | one of the closed reason set | mandatory when the verdict is `skipped`; forbidden otherwise; the set is owned by `requirements.md` FR-014 and cited here, never re-listed |

**Rule V14**: `judged_files + skipped_files + gap_files = changed_files` must hold; a block violating the identity is treated as a gap by every consumer.
**Rule V15**: `renderer` equals the header marker's mode because both are written by one `receipt` invocation; a contract test asserts the equality (this is the disclosed projection, DR1 in `research.md` § R4).
**Rule V16**: an unmeasurable numeric field means no block is written at all (exit 2); a fabricated or zero-filled value is forbidden.
**Rule V33**: the block is the single source of the four counts. E13 and the feature detail entry copy them field by field; neither recomputes nor re-aggregates them, and a contract test asserts both copies equal the block (the same guard shape V15 applies to the renderer literal) (FR-011).

## E8 — Per-file verdict

| Field | Rule |
|-------|------|
| `path` | must be a member of the delta's changed-file set; no path outside it appears |
| `verdict` | binary: `reviewed` or `skipped`; there is no third value |
| `reason` | for `skipped`, one of the five values of the closed reason set owned by `requirements.md` FR-014; a reason outside that set is not a legal skip and is counted as a gap, never as disclosed |

**Rule V17**: a set difference in either direction (a changed file with no entry, an entry outside the changed set) is a gap, and a gap forces exit 1 (FR-014).
**Rule V18**: a skip does not make the receipt red but removes the run's eligibility for [[STR-006]] (see E9).
**Rule V34**: an unrecognised skip reason is a coverage gap, not a skip: it moves the exit code to 1 and may not be read as a reasoned disclosure (FR-014).

## E9 — Segment verdict

Closed set, exactly four values: [[STR-006]] (`pass`), [[STR-007]] (`blocked`), [[STR-001]] (`not-applicable`), [[STR-002]] (`not-evaluated`).

**Derivation** (mechanical, no judgement step):

| gap_files | skipped_files | `blocking` entries in the current record | Verdict |
|-----------|---------------|------------------------------------------|---------|
| > 0 | any | any | [[STR-002]] (a gap is not a conclusion) |
| 0 | > 0 | present | [[STR-007]] |
| 0 | > 0 | none | [[STR-002]] |
| 0 | 0 | present | [[STR-007]] |
| 0 | 0 | none | [[STR-006]] |

**Rule V19**: no fifth value, no silent default, no verdict read off a single signal (FR-014).
**Rule V20**: [[STR-001]] is reachable only through E4, never by an empty receipt: an empty delta is triaged before the receipt runs (V30), so a 0/0/0 conjunction is never evaluated over nothing (FR-003, FR-014).
**Rule V35**: the third column is a presence test over the current [[STR-004]]: at least one `blocking` heading blocks, and a later record with zero such headings does not. No "cleared" state and no clearing operation exists in this model, so nothing is ever "unresolved" (FR-008).

## E10 — Gate verdict

| Field | Rule |
|-------|------|
| `source` | `report --summary --file <E6 path>` — one verdict source, never recomputed by the command |
| `value` | `allow` \| `deny` |
| `reason` | the number of `blocking` headings in the current record when `deny` |
| `exit_code` | `0` = allow, `1` = deny, `2` = input error; three codes, no fourth |

**Rule V21**: the verdict is computed from the explicit record path; implicit "newest file in the directory" selection is a legacy mode that labels itself and is never used by the composed path (FR-023).
**Rule V22**: [[STR-001]] and [[STR-002]] do not deny the transition; they must be disclosed on both carriers — E13 and the feature detail entry. The closing summary may restate them and carries no obligation of its own. When the transition is refused, [[STR-010]] is the named refusal literal for the unattended disposition (FR-008, FR-009).
**Rule V23**: the normative statement of the transition lives in `templates/feature-details-template.md` § Canonical Status State Machine; E10 carries values, not criteria.

## E11 — Archived record

| Field | Rule |
|-------|------|
| `path` | `<spec>/code-review-<YYYYMMDDTHHMMSSZ>.md`, same directory, UTC second resolution |
| `source` | always the previous `code-review.md` |
| `overwrite` | forbidden — an existing archive path aborts the rotation (wait for the next second, or exit 2 with the reason) |
| first run | no archive exists; the report's archive-path field carries [[STR-009]] |

**Rule V24**: exactly one archive is produced per re-run, in the `YYYYMMDDTHHMMSSZ` form; the stable name always denotes the latest run, and a first run records [[STR-009]] rather than leaving the field empty (FR-010, FR-011).

## E12 — Feedback entry attribution

| Field | Rule |
|-------|------|
| `unit_id` | `/speckit.review` for the command unit, `skill:review-sdd-process` for the process-skill unit, `skill:code-review` for the code-skill unit — three entries per run, not one merged entry and not two |
| `run_id` | shared by all three units in one run; the key is `(unit_id, run_id)`, so none dedups another |
| `content class` | framework friction only; a code-segment defect is not a legal payload |
| `scope` | `local`; transmission stays zero-automatic |

**Rule V25**: the nested run records all three units; the command neither suppresses a skill's record nor writes it on the skill's behalf (FR-018).
**Rule V26**: no new store, no second aggregation, no upload path is created by this feature (FR-020).

## E13 — Process-report code section

Fixed content (nothing else belongs here):

| Field | Source |
|-------|--------|
| Base / Head ids + base source | E5 |
| Renderer mode | E6 header marker |
| Receipt counts: changed / judged / skipped / gap | E7 — copied field by field, never recomputed (V33) |
| Segment verdict | E9 |
| Gate verdict and its named refusal literal | E10 ([[STR-010]] when the unattended disposition refuses) |
| [[STR-001]] / [[STR-002]] reason | E4 |
| Uncommitted-scope disclosure | E4 `worktree_uncommitted` (the same sentence lives in the record — one fact, two carriers) |
| Record path and this run's archive path | E6 / E11 ([[STR-009]] on a first run) |

**Rule V27**: opinion bodies and per-item counts are not copied here; the reader follows the path (FR-011).
**Rule V28**: the section lives under § 2 as a subsection so the report template's existing top-level numbering (and the contract test that parses § 5 / § 6) stays stable (FR-011, disclosed in `research.md` § R8).
