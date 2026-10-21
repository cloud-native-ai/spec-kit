# Contract — Snapshot Output Schema

**Owner**: `references/state-awareness.md` (semantics) and `scripts/loop-state.py` (emission). This contract is normative for slice A; clauses are numbered `SNP-NN`. Unknown fields are additive and MUST be ignored by old readers.

- **SNP-01**: The top-level document contains at least: `schema_version`, `action`, `line_id`, `run_id`, `stage`, `loop_state`, `verdict_source`, `watch_status`, `watch_verdict`, `completion`, `recovery_action`, `recovery_reason`, `recovery_detail`, `isolation_required`, `spine`, `registry`, `evidence`, `effective`, `salvage`, `interruptions`, `missing_artifacts`, `uncommitted_artifacts`, `stale_signals`, `evaluated_at`.
- **SNP-02**: `schema_version` is the integer `1`; `action` is the string `"snapshot"`.
- **SNP-03**: `line_id`, `run_id` and `stage` are strings or the literal `"unknown"`; `stage` is one of the eight known stage names or `"unknown"`.
- **SNP-04**: `loop_state` is one of `RUNNING/DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL/STALLED/REENTRY_REQUIRED/UNKNOWN`. `verdict_source` is `"watcher"` or `"derived"`.
- **SNP-05**: `watch_status` is `"available"` or `"unavailable"`; `watch_verdict` is a watcher verdict string or `null`. `available` requires a non-null verdict; `unavailable` requires `null`.
- **SNP-06**: `watch` is an object or `null`. When present it may carry `source`, `reason`, `attribution`, `pid`, `heartbeat`, `sentinel`, `rc` and `hook`; it MUST NOT carry `elapsed` or `at` numbers.
- **SNP-07**: `completion` is one of `complete/incomplete/unknown/not-applicable` and is computed independently of `loop_state`.
- **SNP-08**: `recovery_action` is one of `none/watch/verify/resume/retry/stop` and appears exactly once. `recovery_reason` is a stable snake-case token from the owner-document set; `recovery_detail` is one human-readable sentence.
- **SNP-09**: `isolation_required` is a boolean and is `true` only when a same-line `stale-run` drives a `retry`.
- **SNP-10**: `spine` is an object with `path`, `state`, `schema`, `consistent`, `fields`. `path` is an absolute path or `null`.
- **SNP-11**: `spine.state` is one of `running/retrying/stalled/reentry-required/done/unknown`; `spine.schema` is one of `v1/legacy/missing/unreadable`.
- **SNP-12**: `spine.consistent` is the JSON string `"true"`, `"false"` or `"unknown"`. The three-state string is deliberate (assumption A-P6): it keeps one JSON type across the three states; a reader MUST NOT treat `"false"` as a boolean `false`.
- **SNP-13**: `spine.fields` exposes at least `stage_base_commit`, `last_verdict`, `stall_reason`, `retry_reason`. Each missing value is the literal `"unknown"`; no default is filled.
- **SNP-14**: `registry` is an object with `status`, `entry`, `pointer`, `error`. `status` is `found/missing/unreadable/invalid`; `pointer` is the absolute `<line>.json` path or `null`; `error` is a string or `null`.
- **SNP-15**: `registry.entry`, when present, is a projected digest with at least `line_id`, `run_id`, `stage`, `state`, `spine_path`, `status_path`, `log_path`, `heartbeat_path`, `worktree_path`, `repo_root` and available identity fields. It is a projection, not a copy of the whole entry.
- **SNP-16**: `evidence` contains the keys `pid`, `status`, `log`, `heartbeat`, `watchbeat`, `artifacts`, `commits`. Every entry has `status`, `attribution`, `evidence_source` and `pointer` (or `null` where no path exists).
- **SNP-17**: `evidence.*.status` is one of `present/missing/na`; a signal that cannot be read is `missing`, never `0` or `"ok"`.
- **SNP-18**: `evidence.*.attribution` is one of `own/stale-run/unattributed/foreign`; artifact/commit projections use `own`.
- **SNP-19**: `evidence.*.evidence_source` is `local` or `probe`; one snapshot MUST NOT mix sources within the same evidence key.
- **SNP-20**: `evidence.artifacts` carries `status`, `attribution`, `evidence_source`, `pointer`, `required[]`, `present[]`, `missing[]`, `commit_required`, `no_change_allowed`, `map` (`known` or `unknown`) and `detail` when the map is unknown. The pointer is the absolute spec directory when it is resolvable, otherwise `null`.
- **SNP-21**: `evidence.commits` carries `status`, `attribution`, `evidence_source`, `pointer`, `base`, `commits[]`, `uncommitted[]`, `state` (`committed/missing/not-applicable/unknown`) and `detail` when unknown. The pointer is the absolute repo path when it is resolvable, otherwise `null`.
- **SNP-22**: `missing_artifacts` and `uncommitted_artifacts` are arrays of repo-relative POSIX paths. When the spec directory lies outside the repo, a repo-relative path with `..` segments is permitted; no absolute path is placed in these arrays.
- **SNP-23**: `effective` is an object keyed by `start_grace`, `deadline_grace`, `heartbeat_max_age`, `retry_limit`, `attempt`, `sentinel`. Each value is `{value, source}`; `value` is an integer, string, `null` (explicitly disabled sentinel) or the literal `"unknown"`.
- **SNP-24**: `effective.<key>.source` is one of `cli/probe/spine/stage-map/watcher-help/unknown`; every resolved value names its source.
- **SNP-25**: `salvage` is `{declared, evidence[], source}`. `declared` is true only with at least one non-empty evidence reference; `source` is `spine`, `argument` or `none`.
- **SNP-26**: `interruptions[]` entries are `{form, evidence[], detail, attribution}`. `form` is one of the eight closed forms; `evidence` contains at least one absolute pointer; `detail` is one sentence.
- **SNP-27**: `stale_signals[]` entries are `{pointer, attribution, reason}`. `reason` is one of `run-id-mismatch/before-stage-start/stage-mismatch/unprovable-envelope/legacy-stale`. `legacy-stale` is the envelope-less legacy case; the watcher's `legacy` attribution literal is normalized into the four-value attribution set and is not emitted as a fifth attribution.
- **SNP-28**: `evidence.watchbeat` carries `status`, `attribution`, `pointer`, `at`, `window`, `event` and `freshness` (`fresh/stale/missing/unknown`; `unknown` when `effective.deadline_grace` is unavailable). No age number is emitted.
- **SNP-29**: `evaluated_at` is an ISO-8601 UTC timestamp ending in `Z`; it is the only field allowed to differ between two identical-input runs.
- **SNP-30**: The snapshot contains no heartbeat age, elapsed duration, pid age or other derived time number. Ordering is pinned: interruptions by form order I1–I8 then attribution order; stale signals by pointer; artifacts by stage-map order; commit ids by git log order.
