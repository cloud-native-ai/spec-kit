# Analyze Findings — Wave W2（096-sdd-observer-agent）

**Stage**: analyze（并发波） | **Date**: 2026-11-10 | **Mode**: strictly read-only on artifacts
**Read domain (10 files)**: `plan.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `research.md`, `contracts/journal-engine.contract.md`, `contracts/journal-format.contract.md`, `contracts/observer-lifecycle.contract.md`, `contracts/observer-role.contract.md`, `contracts/observer-verification.contract.md`
**Authorities consulted**: `.specify/skills/internal/analyze-artifacts/SKILL.md` (+ its `references/detection-and-severity.md`), `.specify/constitution.md` (v1.19.0)
**Same-author gate**: not applicable — the artifacts were authored in earlier stage sessions (research.md R-14), and this wave ran in fresh context; detection was not self-review.

## Findings

| ID | Severity | Anchor | Fact (one sentence) | Suggested attribution |
|----|----------|--------|---------------------|-----------------------|
| W2-01 | MEDIUM | `quickstart.md:3` (cf. `plan.md:31`, `plan.md:139`, `plan.md:236`) | `quickstart.md` announces "Seven walk-through scenarios" but contains S-0…S-7 (eight sections), while `plan.md` counts 8 scenarios (S-0…S-7) in three places. | `/speckit.plan` — `quickstart.md`（对齐计数，或将 S-0 明确为 pre-check 不计入 scenario） |
| W2-02 | MEDIUM | `data-model.md:36` vs `data-model.md:127` | E-3 declares execution states `started → settled \| failed` and says they are recorded in the E-9 spine section, but E-9's closed `state` domain is `started \| failed \| disabled \| closed` — `settled` has no spine representation, so a non-terminal settled execution's spine record is undefined. | `/speckit.plan` — data-model E-3/E-9（补 `settled` 值，或明确映射到 `closed`/triplet `.status`） |
| W2-03 | MEDIUM | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:49` | On final-execution failure, E-9 says the driver writes `state=closed` (with the reason) after the final execution fails, while lifecycle C-08 says the driver records `state: failed` plus the reason — the terminal spine state is contradictory. | `/speckit.plan` — E-9 与 lifecycle C-08（择一终态规则；若 closed 覆盖 failed，须写明顺序） |
| W2-04 | MEDIUM | `contracts/journal-engine.contract.md:39` (cf. `:31`, `data-model.md:160-161`, `quickstart.md:59`) | `check` is required to validate V-16/V-17, but V-16 is an append-time execution-label identity refusal (C-07) and `check` receives only `--spec-dir`/`--repo` — no execution label or spine input — so V-16 cannot be discharged as written; `quickstart.md` S-3 repeats the V-1…V-13-only reading. | `/speckit.plan` — journal-engine C-09 与 V-16/V-17 归属（V-16 归 append；check 补 spine 输入或移除 V-17） |
| W2-05 | MEDIUM | `feature-ref.md:18-40` (cf. `:75`, `:77`) | The Delivered paths table's FR column never cites FR-019 or FR-021, although the FR → Contract map lists both, so 2 of 23 FRs have no delivered-path attribution. | `/speckit.plan` — feature-ref delivered-paths 表（补行归属，或注明经哪一行间接交付） |
| W2-06 | MEDIUM | `plan.md:248` (cf. `plan.md:243-245`, `feature-ref.md:33`, `:37`, `quickstart.md:83`) | WP-3's `test_sdd_observer_lifecycle.py` needs the start-failure / mid-run-kill failure builder that WP-1 owns in `tests/fixtures/sdd-observer/`, but the dependency note claims only pairwise write-domain disjointness and states no WP-1 → WP-3 ordering. | `/speckit.tasks` — 在 tasks.md 记录该 fixture 依赖（并修正 plan 的依赖句） |
| W2-07 | MEDIUM | `data-model.md:80-99` (E-6) + `contracts/journal-engine.contract.md:19`, `:23` | E-6 names each event's primary carrier but no rule maps carrier fields to the nine entry columns per event class, and C-05's "natural keys" for the idempotency identity are undefined — the claimed deterministic projection is not decidable from the read-domain artifacts. | `/speckit.plan` — data-model E-6 / journal-engine C-04/C-05（补 per-event 投影表并定义 identity keys） |
| W2-08 | MEDIUM | `data-model.md:163` (cf. `contracts/observer-lifecycle.contract.md:37`, `plan.md:76-84`, `contracts/observer-verification.contract.md:23`) | V-19 claims two parallel lines' journals "never share a path", but the path is derived from the spec key and the dual-line fixture uses two distinct spec dirs — the plan only excludes same-spec two-line work by T-001 decision, a precondition V-19/C-05 and the fixture do not state. | `/speckit.plan` — V-19 / lifecycle C-05 / observer-verification C-05（写明 distinct-spec 前提，或补 same-spec 判定） |
| W2-09 | MEDIUM | `plan.md:56` | Constitution Check row XV's evidence claims the quickstart "defines journal / observer / gap at first use", but `quickstart.md` contains no such definitions — the terms are used bare in S-1/S-2/S-5. | `/speckit.plan` — `quickstart.md`（补 first-use 定义）或修正 row XV 证据 |
| W2-14 | MEDIUM | `data-model.md:116` (E-8) + `contracts/journal-engine.contract.md:35` (C-08) | E-8 defines a gap window start from "the spine observer record section's `started_at`" when no entry exists, but C-08 only appends a gap when a previous entry exists and does not say which spine section's `started_at` to use — the start-failure/no-entry gap is unreachable or ambiguous. | `/speckit.plan` — E-8/C-08（补 no-entry 分支并消歧 spine section） |
| W2-10 | LOW | `plan.md:42` | Row I's evidence says "Every contract clause cites an FR", but the five contract pages cite FRs only in their page-level `Requirements:` lines; no individual C-NN clause body carries an FR reference. | `/speckit.plan` — 将 row I 证据改写为 page-level scope，或补 per-clause FR tag |
| W2-11 | LOW | `plan.md:47` | Row VI's evidence says every row carries a "resolvable pointer", but E-7 permits runtime pointers to cleaned-up files and E-6 gives `observer-error` `min_persistent: 0` — a row may carry only a runtime pointer that no longer resolves. | `/speckit.plan` — 改写 row VI 证据（persistent 指针须解析；runtime 指针仅标记） |
| W2-12 | LOW | `data-model.md:33` (cf. `research.md:28`, `quickstart.md:34`, `plan.md:195`) | The observer execution label's middle segment is named `run_stamp` in the data model and research, `run` in plan EP-007, and shown as the run id (`R1`) in the quickstart, with no mapping rule between the three names. | `/speckit.plan` — data-model E-3 / research R-03（统一 token 名并定义，示例对齐） |
| W2-13 | LOW | `contracts/journal-engine.contract.md:15` | C-03 calls `--settle` / `--final` "mutually exclusive semantics" but never states whether the flags may be combined or whether `--final` alone implies the `observer-settle` write it describes. | `/speckit.plan` — journal-engine C-03（写明互斥规则与 `--final` 单独语义） |

**Total**: 14 findings — CRITICAL 0 · HIGH 0 · MEDIUM 10 · LOW 4. No artifact was modified.

## Coverage accounting (W2 read domain)

- **Counts verified steady**: 23 FR / 7 SC; 19 delivery rows; 5 contract pages = 58 clauses (`observer-role` 10 + `observer-lifecycle` 12 + `journal-format` 13 + `journal-engine` 13 + `observer-verification` 10); 10 entities (`E-1`…`E-10`); 20 rules (`V-1`…`V-20`); 4 work packages / 19 items; 16 event classes; 9 entry columns; 5 header keys; 8 spine-record keys. The only count drift found is the quickstart scenario count (W2-01).
- **FR → Contract map**: all FR-001…FR-023 rows resolve to existing clauses; no orphan FR. Individual-clause → FR tagging is page-level only (W2-10).
- **SC → Measurement map**: all SC-001…SC-007 name a measurement and evidence module; the dual-line isolation proof scope is narrower than V-19's claim (W2-08).
- **Delivered-path attribution**: FR-019 and FR-021 absent from the delivered-paths FR column (W2-05).
- **Duplication pass (A)**: no actionable finding. The repeated format facts (nine columns, sixteen events, spine shape) are the declared information face (data-model / contract) while the fact file owns spellings; the plan restates none; the copies agree, so the One-Source-of-Truth stale-copy test does not fire. Evidence: `data-model.md:3`, `contracts/journal-format.contract.md:3` + C-01.
- **Registry pass (G)**: `.specify/features.md` and `.specify/features/096.md` are outside this wave's read domain and were not assessed; within the domain, `feature-ref.md` and `plan.md:43` agree on the 096 row + `Planned` status.
- **Constitution pass (D)**: no principle violation found; three Constitution Check evidence overstatements (rows I, VI, XV → W2-10, W2-11, W2-09).
- **Checklist pass (H)**: `checklists/*.md` is outside this wave's read domain; not assessed here (owned by the stage-level checklist wave / driver).
- **Coverage accountant**: the skill's fixed `account-clause-coverage.py` step needs `requirements.md` / `tasks.md`, which are outside this wave's read domain, so it was not run by W2; the FR/SC counts above were checked directly against the read-domain tables.

## Method / limits

- Eight-pass detection (A/B/C/D/E/F/G/I) applied to the ten-file slice only; no edits, no remediation, no push, no dirty-file restore.
- No CRITICAL/HIGH raised, so the skill's independent C/H validation precondition is vacuous for this wave; if the final gate re-rates any row to HIGH, an independent validation subagent is still owed.
- Findings are pointers to owners; remediation belongs to `/speckit.plan` / `/speckit.tasks` as noted.

## Wrap-up bookkeeping

- Identity three steps executed under `skill:analyze-artifacts`, run `r20261110T081104Z-b096`:
  - Run Determination → `duplicate`（该 unit+run 已由 W1 并发波记录；同一 unit+run 不重复记录）。
  - Exec Quant → `duplicate`（同上）。
  - Feedback Record → `duplicate: true`，返回既有 W1 条目 `.specify/memory/feedback/20261110T092908Z-skill-analyze-artifacts.md`；W2 的 review 以本 findings 文件为准（同一 unit+run 禁止二次记录）。
- Threshold notice: `should_prompt=true` × run-record `trigger_feedback=false` → 不弹非阻塞提示（两真才弹）。
- `WRAPUP-DEFERRED` 不适用：三步均得到引擎的确定响应（duplicate 为已记录，不是记账失败）。
