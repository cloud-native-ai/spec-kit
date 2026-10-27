# Data Model: Review × Code-Review Composition (071)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner note**: this file owns the entity list, the field sets, and the validation rules of the composed review. The clause-level normative statements are owned by `contracts/`; where this file and a contract state the same rule, the contract is the normative text and this file is the shape. Literal values that requirements pin are referenced as `[[STR-NNN]]`, never copied.

## Entity map

| ID | Entity | Written by | Lives in |
|----|--------|-----------|----------|
| E1 | Review run | `/speckit.review` (command unit) | `.specify/specs/<key>/review.md`, `code-review.md` |
| E2 | Process segment | `review-sdd-process` (skill unit) | `review.md` |
| E3 | Code segment | `code-review` (skill unit) | `code-review.md` |
| E4 | Applicability triage | `/speckit.review` | `review.md` § code segment, closing summary |
| E5 | Feature-slice base | `git-delta-review.sh base` | `code-review.md` header, receipt block |
| E6 | Code segment record | `git-delta-review.sh start` + `note` + `receipt` | `code-review.md` |
| E7 | Coverage receipt | `git-delta-review.sh receipt` | inside E6 (delimited block) |
| E8 | Per-file verdict | `git-delta-review.sh note` / `receipt` | inside E7 |
| E9 | Segment verdict | `git-delta-review.sh receipt` + unresolved-blocking count | inside E7, mirrored in E13 |
| E10 | Gate verdict | `git-delta-review.sh report --summary --file` | E6, E13, closing summary |
| E11 | Archived record | `git-delta-review.sh start` (rotation) | `<spec>/code-review-<ts>.md` |
| E12 | Feedback entry attribution | `feedback-utils.py` via each unit's wrap-up | `.specify/memory/feedback/` (existing store) |
| E13 | Process-report code section | `review-sdd-process` (fills from E3) | `review.md` § 2.1 |

## E1 — Review run

| Field | Type | Rule |
|-------|------|------|
| `requirement_key` | string | the spec directory name, e.g. `071-review-code-integration` |
| `segments` | ordered list | exactly `[process, code]`; order fixed; no reordering, no omission of `process` |
| `started_at` / `finished_at` | ISO 8601 | the closing summary reports both segments' conclusions |
| `run_id` | string | one stable id per run, shared by both units' wrap-up records |
| `artifacts` | list of paths | `review.md` always; `code-review.md` unless the code segment is `not-applicable` |

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
| `verdict` | literal | `done` or `not-evaluated` (with `reason`) |

**Rule V4**: this segment runs unconditionally; no field of E1 or E4 may be read as an exemption (FR-002).

## E3 — Code segment

| Field | Type | Rule |
|-------|------|------|
| `judgment_object` | literal | verifiable defects in this feature slice's committed code delta |
| `severity_vocabulary` | closed set | `blocking`, `important`, `suggestion`, `nitpick`, `question`, `praise` — owned by `skills/internal/code-review/SKILL.md` |
| `record_path` | path | `<spec>/code-review.md` ([[STR-004]]) |
| `archive_path` | path or `none` | `<spec>/code-review-<ts>.md` when the run rotated a previous record |
| `verdict` | E9 value | derived, never assigned by hand |

**Rule V5**: the two severity vocabularies never convert into one another; no field exists that stores a mapped or weighted value (FR-007).
**Rule V6**: `verdict = pass` requires `gap_files = 0`, `skipped_files = 0`, and `unresolved_blocking = 0` simultaneously (FR-014).

## E4 — Applicability triage

| Field | Type | Rule |
|-------|------|------|
| `value` | closed set | `run`, [[STR-001]] (`not-applicable`), [[STR-002]] (`not-evaluated`) |
| `basis` | string | mandatory for `not-applicable`: "feature produces no code deliverable" or "feature has no committed code delta" |
| `reason` | string | mandatory for `not-evaluated`: the environment or resolution failure |
| `resolved_base` | E5 or `none` | present when `value = run` |
| `worktree_uncommitted` | boolean | when true, the report discloses the unreviewed scope |

**Rule V7**: four values do not exist — an unspecified value, an empty value, a silently skipped segment, or a `pass` on a non-`run` triage (FR-003).
**Rule V8**: `not-applicable` for an expression-class feature must leave the process segment's reader-baseline conclusion untouched (FR-027).

## E5 — Feature-slice base

| Field | Type | Rule |
|-------|------|------|
| `base_sha` | 40-hex or short | the resolved diff base |
| `head_sha` | 40-hex or short | the resolved diff head (`HEAD` unless overridden) |
| `base_source` | closed set | `explicit`, `feature-first-commit`, `trunk-merge-base` |
| `resolve_command` | string | the reproducible command, recorded when resolution fails |

**Rule V9**: resolution order is `explicit` > `feature-first-commit` (parent of the first commit that added this feature's `requirements.md`) > `trunk-merge-base` (merge base with the repository default trunk) (FR-004).
**Rule V10**: the script's built-in `GIT_BASE` default is never the composed path's base; no branch name is hard-coded anywhere in the resolution (FR-004).
**Rule V11**: an unresolvable base yields E4 = [[STR-002]] with `resolve_command` and the failure reason; a guessed base is forbidden (FR-006).

## E6 — Code segment record

Header (fixed field order, one table row each):

| Field | Rule |
|-------|------|
| Branch | `git rev-parse --abbrev-ref HEAD` |
| Base / Head | E5 ids with short forms |
| Base source | E5 `base_source` |
| Renderer | the marker literal `renderer: delta` or `renderer: text` ([[STR-003]]) |
| Reviewer / Date | `git config user.name`, local date-time |

Body: the opinions (severity + file + optional line + text), the receipt block (E7), and the statistics table.

**Rule V12**: a re-run archives the previous file to E11 before writing; the writer refuses to overwrite an existing archive (exit 2) rather than losing a record (FR-010).
**Rule V13**: the record is not listed in `AVAILABLE_DOCS` and is not read as plan/tasks input; the feature detail's review-record row links it (FR-012).

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
| `file.<NN>.reason` | text | mandatory when the verdict is `skipped`; forbidden otherwise |

**Rule V14**: `judged_files + skipped_files + gap_files = changed_files` must hold; a block violating the identity is treated as a gap by every consumer.
**Rule V15**: `renderer` equals the header marker's mode because both are written by one `receipt` invocation; a contract test asserts the equality (this is the disclosed projection, DR1 in `research.md` § R4).
**Rule V16**: an unmeasurable numeric field means no block is written at all (exit 2); a fabricated or zero-filled value is forbidden.

## E8 — Per-file verdict

| Field | Rule |
|-------|------|
| `path` | must be a member of the delta's changed-file set; no path outside it appears |
| `verdict` | binary: `reviewed` or `skipped`; there is no third value |
| `reason` | free text for `skipped` — the focus/size-guard reason; counted as disclosed, never as coverage |

**Rule V17**: a set difference in either direction (a changed file with no entry, an entry outside the changed set) is a gap, and a gap forces exit 1 (FR-014).
**Rule V18**: a skip does not make the receipt red but removes the run's eligibility for `pass` (see E9).

## E9 — Segment verdict

Closed set, exactly four values: `pass`, `blocked`, [[STR-001]] (`not-applicable`), [[STR-002]] (`not-evaluated`).

**Derivation** (mechanical, no judgement step):

| gap_files | skipped_files | unresolved `blocking` | Verdict |
|-----------|---------------|-----------------------|---------|
| > 0 | any | any | [[STR-002]] (a gap is not a conclusion) |
| 0 | > 0 | > 0 | `blocked` |
| 0 | > 0 | 0 | [[STR-002]] |
| 0 | 0 | > 0 | `blocked` |
| 0 | 0 | 0 | `pass` |

**Rule V19**: no fifth value, no silent default, no verdict read off a single signal (FR-014).
**Rule V20**: `not-applicable` is reachable only through E4, never by an empty receipt.

## E10 — Gate verdict

| Field | Rule |
|-------|------|
| `source` | `report --summary --file <E6 path>` — one verdict source, never recomputed by the command |
| `value` | `allow` \| `deny` |
| `reason` | the unresolved `blocking` count when `deny` |
| `exit_code` | `0` = allow, `1` = deny, `2` = input error |

**Rule V21**: the verdict is computed from the explicit record path; implicit "newest file in the directory" selection is a legacy mode that labels itself and is never used by the composed path (FR-023).
**Rule V22**: `not-applicable` and `not-evaluated` do not deny the transition; they must be disclosed in E13, the closing summary, and the feature detail (FR-008).
**Rule V23**: the normative statement of the transition lives in `templates/feature-details-template.md` § Canonical Status State Machine; E10 carries values, not criteria.

## E11 — Archived record

| Field | Rule |
|-------|------|
| `path` | `<spec>/code-review-<YYYYMMDD-HHMMSS>.md`, same directory |
| `source` | always the previous `code-review.md` |
| `overwrite` | forbidden — an existing archive path aborts the rotation (exit 2) |

**Rule V24**: exactly one archive is produced per re-run; the stable name always denotes the latest run (FR-010).

## E12 — Feedback entry attribution

| Field | Rule |
|-------|------|
| `unit_id` | `/speckit.review` for the command unit, `skill:code-review` for the skill unit — two entries, not one merged entry |
| `run_id` | shared by both units in one run; the key is `(unit_id, run_id)`, so the two do not dedup each other |
| `content class` | framework friction only; a code-segment defect is not a legal payload |
| `scope` | `local`; transmission stays zero-automatic |

**Rule V25**: the nested run records both units; the command neither suppresses the skill's record nor writes it on the skill's behalf (FR-018).
**Rule V26**: no new store, no second aggregation, no upload path is created by this feature (FR-020).

## E13 — Process-report code section

Fixed content (nothing else belongs here):

| Field | Source |
|-------|--------|
| Base / Head ids + base source | E5 |
| Renderer mode | E6 header marker |
| Receipt counts: changed / judged / skipped / gap | E7 |
| Segment verdict | E9 |
| Gate verdict | E10 |
| [[STR-001]] / [[STR-002]] reason | E4 |
| Record path and this run's archive path | E6 / E11 |

**Rule V27**: opinion bodies and per-item counts are not copied here; the reader follows the path (FR-011).
**Rule V28**: the section lives under § 2 as a subsection so the report template's existing top-level numbering (and the contract test that parses § 5 / § 6) stays stable (FR-011, disclosed in `research.md` § R8).
