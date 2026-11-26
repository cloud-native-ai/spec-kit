# Contract — Run Report Recognition, Classification and Latest Selection

**Path**: implemented in `scripts/python/team-view.py`; unit pinning `tests/unit/test_team_view_report_recognition.py`; integration pinning `tests/integration/test_team_view_degradation.py`.
**Rule owners cited, never restated**: report naming `skills/internal/create-team/SKILL.md` § Report contract (unchanged); the recognition grammar below is this feature's read-side rule; the residue/auxiliary taxonomy is `contracts/view-labels.contract.md`.

**C-201** Closed timestamp grammar.

A file name is stamped when it **starts** with one of exactly five forms — `YYYYMMDDThhmmssZ`, `YYYYMMDDThhmmZ`, `YYYY-MM-DDThh:mm:ssZ`, `YYYY-MM-DDThh-mm-ssZ`, `YYYY-MM-DDThhmmssZ` — and the matched text is a valid UTC calendar instant. A date-only prefix, an invalid month/day/hour, a non-`Z` zone marker, or a stamp that does not begin the name is NOT a stamp. The program MUST NOT guess a stamp from a partial or fuzzy match. (FR-001)

**C-202** Report suffix and three-way classification.

After a valid stamp, the remainder determines the kind, judged in this fixed order on the file name only: (1) no valid leading stamp → `residue` (even when the name resembles `progress-snapshot` / `judgment-contract`, and even when the file is not `.md`); (2) valid stamp + remainder matching `(?:-[0-9a-f]{4})?-(?:report|stage)\.md` → run report; (3) valid stamp + any other remainder (e.g. `-verification.md`, `-seat-result.md`, `-93cc-verification.md`) → auxiliary artifact. Auxiliary artifacts MUST NOT compete for latest and MUST NOT be counted as residue; residue MUST NOT be counted as reports. (FR-003)

**C-203** Latest = maximum parsed timestamp.

The latest run report is the report with the maximum parsed UTC timestamp. Equal timestamps are decided deterministically by file name lexicographic ascending first. The program MUST NOT fall back to an older recognized report because some file does not match a narrow template, and MUST NOT infer recency from mtime or file content. (FR-002, FR-005)

**C-204** One normalized value.

The latest timestamp is normalized to UTC `YYYYMMDDThhmmssZ` (second precision). The same normalized value is written to `as_of.latest_report_timestamp` and to the overview's `最近运行（latest run）` column; for compact conforming names the normalized value equals the file name token. (FR-002, FR-006)

**C-205** Bounded residue presentation.

Residue is presented as one line carrying the total count, at most three example names and the omitted count; the program MUST NOT transcribe the directory without bound. Auxiliary artifacts use the same bounded form in their own line. (FR-004)

**C-206** Uncertainty predicate.

When `runs/` exists and is readable and the residue count is at least 1, the latest determination is unprovable: the program MUST activate `report-recognition-uncertain` (exit 5) and disclose the count. When `runs/` is missing or empty, or every non-report file carries a parseable stamp (auxiliary only), no uncertainty is produced. When no report is recognizable and only residue exists, the run-report state MUST express "residue only, latest undeterminable" and MUST NOT render `为空` or `缺失`; the residue line carries the count and bounded examples. A report list that still exists MUST be presented, with the uncertainty disclosed alongside. (FR-005, FR-004)

**C-207** Overview reuse, inline disclosure.

The overview MUST reuse C-201…C-204 through the same classifier and normalizer. A residue-bearing row appends `（report-recognition-uncertain：残留 N）` to its latest cell; the overview issues no degradation reason and keeps the existing `0 / 2` exit domain. An undeterminable row MUST NOT be left blank and MUST NOT take an older value. (FR-006, FR-005)

**C-208** Unreadable latest report.

When the selected latest report exists but cannot be read, the latest group MUST present `不可读` and name the path; the per-field lines of that group MUST NOT be silently rendered as `未记录`. This state is not a degradation reason and does not change the exit code by itself. (FR-009, FR-018)
