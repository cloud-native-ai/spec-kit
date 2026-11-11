# 2026-11-11 — archive-first auto-execution (routing override record)

## User instruction (verbatim)

> migrate 和 house keeping这类动作都应该尽可能少的要求用户确认, 减少非必要的交互

and, on the real/real anchor conflict:

> migrate语义本来就包含了针对现有文件的重新整理,因此需要将新的和就旧的进行合并, 即便是用户已经写了内容,如果存在两个冲突的文件,就是应该由migrate来解决这种新旧冲突

## Routing verdict and override

- Declared inputs: `change_nature=feature`, `traceability=required`, `blast_radius=cross-cutting`, `reversibility=reversible`, `complexity=standard`.
- Engine verdict: `sdd` (condition `nature-feature`; the capability contract changes).
- Override: **direct modification**, per the user's explicit instruction above. The 097 live artifacts (requirements, contracts, data model, plan, tasks, quickstart, verification) and the `024` feature detail were updated in the same change; dated review records were not rewritten.
- Reason: the user asked for the existing `/speckit.migrate` and `sdd-house-keeping` behavior to be corrected now, not for a new capability chain.

## Behavior change

- `--apply` is the single write authorization. Archive-first items (`replace` / `archive` / `relocate` / `merge`) execute automatically in interactive and non-interactive environments; the run receipt records every archive and its `recover` path.
- Old/new anchor conflicts are resolved by the anchor engine: a placeholder target is replaced by the legacy real content; two real contents are merged (`features.md` table-row union, other anchors append with a fixed marker); both originals are archived. Only an unmergeable structural target (non-empty directory, broken link, unreadable content) is refused and names both candidates.
- `specify init` no longer copies a placeholder anchor when the legacy anchor exists under `.specify/memory/`.
- House-keeping's `check` mode auto-executes reversible repairs, git-clean duplicate-only renumber and docs dead-link fixes; true deletes and retention retirement keep the single batch confirmation.

## Evidence

- `test-evidence/us2-safety-v2.txt` — 26 passed (US2 safety, anchor engine, US1 convergence, init stub prevention).
- Targeted migrate/sanitize/housekeeping suites green; `sync-mirrors.py --check` and `regen-command-copies.py --check` clean.
- Full suite: 202 failed / 8874 passed vs 203 failed / 8877 passed at HEAD; failure-set diff shows no new deterministic failure (one parallel-flaky `status_digest` test passes in isolation).
