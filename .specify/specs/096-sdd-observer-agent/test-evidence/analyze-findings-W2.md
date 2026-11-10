# Analyze Findings — Wave W2, Round 2（096-sdd-observer-agent）

**Stage**: analyze 第二轮（修复后重过门；并发波） | **Date**: 2026-11-10 | **Mode**: strictly read-only on artifacts
**Read domain (10 files)**: `plan.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `research.md`, `contracts/journal-engine.contract.md`, `contracts/journal-format.contract.md`, `contracts/observer-lifecycle.contract.md`, `contracts/observer-role.contract.md`, `contracts/observer-verification.contract.md`
**Authorities consulted**: `.specify/skills/internal/analyze-artifacts/SKILL.md` (+ its `references/detection-and-severity.md`), `.specify/constitution.md` (v1.19.0)
**Round-2 mode**: full severity re-adjudication（round-1 findings + 全严重度重扫），非 C/H-only；因此 C/H-only 的 residue 强制行不适用，但全部 14 条 round-1 ID 仍在下表逐一处置。
**Same-author gate**: not applicable — the artifacts were authored in earlier stage sessions；本波 fresh context、只读，非自我复核。

## Rerun delta — Round-1 W2 findings re-adjudicated

| ID | R1 severity | R2 disposition | R2 anchor / evidence | Reason (one line) |
|----|-------------|----------------|----------------------|-------------------|
| W2-01 | MEDIUM | open | `quickstart.md:3`; `plan.md:31`/`:139`/`:236` | quickstart 仍称 "Seven walk-through scenarios"，实含 S-0…S-7 八节；三处 plan 计数为 8。 |
| W2-02 | MEDIUM | open | `data-model.md:36` vs `:127` | E-3 的 `settled` 状态在 E-9 封闭域中仍无表示。 |
| W2-03 | MEDIUM | open | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:63`（cf. `contracts/observer-verification.contract.md:19`） | 终态冲突照旧（E-9 失败→closed vs C-08 失败→failed）；C-08 修复只补了缺口收束句。 |
| W2-04 | MEDIUM | open | `contracts/journal-engine.contract.md:55` vs `data-model.md:160-161`; `quickstart.md:59` | `check` 仍被要求校验 V-16/V-17，但接口无 label/spine 输入，V-16 按字面不可执行。 |
| W2-05 | MEDIUM | open | `feature-ref.md:22-40`（cf. `:75`、`:77`） | Delivered paths 的 FR 列仍缺 FR-019、FR-021。 |
| W2-06 | MEDIUM | **fixed** | `tasks.md:87-100`（Package Map 严格串行 wp01→wp02→wp03→wp04；据 `test-evidence/analyze-repair-dispositions-2026-11-10.md` W3-01 行）、`tasks.md:336-340` | 修复轮已把 WP-1 → WP-3 的 fixture 依赖落实为串行链，可执行顺序不再有缺口；`plan.md:248` 措辞保持旧文（已披露，无下游影响）。 |
| W2-07 | MEDIUM | open | `data-model.md:82-97`（E-6）+ `contracts/journal-engine.contract.md:31` | 仍无 per-event 投影表，C-05 的 "natural keys" 仍未定义。 |
| W2-08 | MEDIUM | open | `data-model.md:163`（V-19）；`contracts/observer-lifecycle.contract.md:45`；`contracts/observer-verification.contract.md:31`；`plan.md:81` | V-19 的 "never share a path" 仍缺 distinct-spec 前提（前提只在 T-001 决策记录里）。 |
| W2-09 | MEDIUM | open | `plan.md:56` vs `quickstart.md:15-83` | Row XV 证据仍声称 quickstart 定义了 journal / observer / gap，实际无定义（S-1/S-2/S-5 裸用）。 |
| W2-10 | LOW | **fixed** | 五页 58/58 条款体已载 per-clause FR citation group（`contracts/observer-role.contract.md:9` … `contracts/journal-engine.contract.md:81`） | 修复轮（E-01）落地的条款级 FR 引用使 `plan.md:42` row I「Every contract clause cites an FR」证据事实上成立（plan.md 未改）。 |
| W2-11 | LOW | open | `plan.md:47` vs `data-model.md:110`（E-7）+ `data-model.md:97` | Row VI「resolvable pointer」证据仍与 runtime 指针/`min_persistent: 0` 相悖。 |
| W2-12 | LOW | open | `data-model.md:33`（cf. `research.md:28`、`plan.md:195`、`quickstart.md:34`） | `run_stamp` / `run` / `R1` 三名并存，仍无映射规则。 |
| W2-13 | LOW | open（收窄） | `contracts/journal-engine.contract.md:19` | C-03 已明说 `--final` additionally writes `observer-settle`；剩余缺口是两 flag 能否同时出现及非法组合的退出码。 |
| W2-14 | MEDIUM | open（收窄） | `data-model.md:116`（E-8）+ `contracts/journal-engine.contract.md:49`（C-08）+ `contracts/journal-format.contract.md:61`（C-10） | C-10 已补 no-entry 回退值，但 engine C-08 触发条件仍要求 previous entry，且 "the spine record" 仍未指明是哪一节。 |

**Delta totals**: 14 → fixed 2（W2-06、W2-10）· open 12 · rejected 0 · new 0。

## Open findings (round 2)

| ID | Severity | Anchor | Fact (one sentence) | Suggested attribution |
|----|----------|--------|---------------------|-----------------------|
| W2-01 | MEDIUM | `quickstart.md:3` vs `quickstart.md:5`/`:94`；`plan.md:31`、`:139`、`:236` | quickstart 首行宣布 "Seven walk-through scenarios"，但文件含 S-0…S-7（八节），而 plan 三处均计 8 个场景（S-0…S-7）。 | `/speckit.plan` — `quickstart.md` 开头（对齐计数，或声明 S-0 为 pre-check 不计入 scenario） |
| W2-02 | MEDIUM | `data-model.md:36` vs `data-model.md:127` | E-3 声明执行状态 `started → settled \| failed` 并称记入 E-9 spine 节，但 E-9 的封闭 `state` 域为 `started \| failed \| disabled \| closed` —— `settled` 无 spine 表示。 | `/speckit.plan` — data-model E-3/E-9（补 `settled` 值，或明确映射到 E-3 状态机里的非 spine 语义） |
| W2-03 | MEDIUM | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:63`（cf. `contracts/observer-verification.contract.md:19`） | 终态失败时 E-9 说 driver 写 `state=closed`（带原因），C-08 说 driver 记 `state: failed` 加原因；反向地，终态成功时 C-08 又未点名 E-9 要求的 spine `closed` 写入 —— 两个终态分支都没有一致的 spine 规则。 | `/speckit.plan` — E-9 与 lifecycle C-08（为成功/失败各写一条唯一终态规则） |
| W2-04 | MEDIUM | `contracts/journal-engine.contract.md:55` vs `data-model.md:160-161`、`quickstart.md:59` | C-09 要求 `check` 校验 V-16/V-17，但 V-16 是 append 时的身份拒绝（需 execution label 与 spine），而 `check` 只有 `--spec-dir`/`--repo` —— V-16 按字面不可执行；quickstart S-3 重复 V-1…V-13-only 读法。 | `/speckit.plan` — journal-engine C-09 与 V-16/V-17 归属（V-16 归 append；check 补 spine 输入或从清单移除 V-17） |
| W2-05 | MEDIUM | `feature-ref.md:22-40`（cf. `:75`、`:77`） | Delivered paths 表的 FR 列从未引用 FR-019 或 FR-021（两者在 FR → Contract map 有归属），23 个 FR 中 2 个无交付路径归属。 | `/speckit.plan` — feature-ref delivered-paths 表（补行归属或注明经哪一行间接交付） |
| W2-07 | MEDIUM | `data-model.md:82-97`（E-6）+ `contracts/journal-engine.contract.md:31` | E-6 只给每事件的主载体，无「载体字段 → 九列」的 per-event 投影规则；C-05 的 idempotency「natural keys」未定义 —— 确定性投影与幂等 append 在读域内不可判定。 | `/speckit.plan` — data-model E-6 / engine C-04/C-05（补 per-event 投影表并定义 identity keys） |
| W2-08 | MEDIUM | `data-model.md:163`（V-19）；`contracts/observer-lifecycle.contract.md:45`；`contracts/observer-verification.contract.md:31`；`plan.md:81` | V-19 声称两条并行线的 journal "never share a path"，但路径由 spec key 派生、双线 fixture 用的是两个不同 spec 目录；same-spec 两线仅由 T-001 决策记录排除，V-19 与两处 C-05 均未写明该前提。 | `/speckit.plan` — V-19 / lifecycle C-05 / verification C-05（写明 distinct-spec 前提，或补 same-spec 判定） |
| W2-09 | MEDIUM | `plan.md:56` vs `quickstart.md:15-83` | Constitution Check row XV 的证据声称 quickstart "defines journal / observer / gap at first use"，但 quickstart 无这些定义 —— 术语在 S-1/S-2/S-5 裸用。 | `/speckit.plan` — `quickstart.md`（补首次使用定义）或修正 row XV 证据 |
| W2-14 | MEDIUM | `data-model.md:116`（E-8）+ `contracts/journal-engine.contract.md:49`（C-08）+ `contracts/journal-format.contract.md:61`（C-10） | C-10 已给 no-entry 时的窗口起点回退，但 engine C-08 的触发仍要求 previous entry（"if the previous entry's `observed_at` is earlier than the spine record's `started_at`"），且 "the spine record" 未指明取哪一节（latest vs 该执行自己的启动节）—— start-failure/no-entry 缺口在引擎契约层不可达或歧义。 | `/speckit.plan` — E-8 / engine C-08（补 no-entry 分支并消歧 spine 节） |
| W2-11 | LOW | `plan.md:47` vs `data-model.md:110`（E-7）+ `data-model.md:97`（`observer-error` `min_persistent: 0`） | Row VI 证据称每行都有 "resolvable pointer"，但 E-7 允许指向已清理文件的 runtime 指针、`observer-error` 允许零 persistent —— 一行可以只带一个不再解析的 runtime 指针。 | `/speckit.plan` — 改写 row VI 证据（persistent 指针须解析；runtime 指针仅标记） |
| W2-12 | LOW | `data-model.md:33`（cf. `research.md:28`、`plan.md:195`、`quickstart.md:34`） | 执行 label 中段在 data-model/research 叫 `run_stamp`、在 plan EP-007 叫 `run`、在 quickstart 示例中显示为 run id（`R1`），三者无映射规则。 | `/speckit.plan` — data-model E-3 / research R-03（统一 token 名并定义，示例对齐） |
| W2-13 | LOW | `contracts/journal-engine.contract.md:19` | C-03 以 "mutually exclusive semantics" 命名 `--settle` / `--final`（且已写明 `--final` 追加 `observer-settle`），但从未说明两 flag 能否同次出现、非法组合落到哪个退出码 —— 组合规则仍未决。 | `/speckit.plan` — journal-engine C-03（写明互斥/组合规则与退出码） |

**Total open**: 12 — CRITICAL 0 · HIGH 0 · MEDIUM 9 · LOW 3. No artifact was modified.

## New findings (round 2)

None. The fresh full-severity pass over the ten files raised no finding beyond the carried set. The repair-introduced per-clause FR citation groups were checked mechanically: on all five pages the union of clause-level citations equals that page's `Requirements:` line, and no clause cites an FR outside its page line — the repair introduced no new inconsistency.

## Coverage accounting (W2 read domain, round 2)

- **Counts verified steady**: 23 FR / 7 SC; 19 delivery rows; 5 contract pages = 58 clauses (`observer-role` 10 + `observer-lifecycle` 12 + `journal-format` 13 + `journal-engine` 13 + `observer-verification` 10); 10 entities (`E-1`…`E-10`); 20 rules (`V-1`…`V-20`); 16 event classes; 9 entry columns; 5 header keys; 8 spine-record keys; 4 work packages / 19 items. The only count drift remains the quickstart scenario count (W2-01).
- **Clause ↔ FR (new this round)**: 58/58 clause bodies carry an FR citation group (E-01 repair verified); page-level set = clause union on 5/5 pages. `plan.md:42` row I evidence is now true (W2-10 fixed).
- **FR → Contract map**: all FR-001…FR-023 rows resolve to existing clauses; no orphan FR. FR-019 and FR-021 still lack delivered-path attribution (W2-05).
- **SC → Measurement map**: all SC-001…SC-007 name a measurement and evidence module; the dual-line isolation proof scope is narrower than V-19's claim (W2-08).
- **Duplication pass (A)**: no actionable finding — the repeated format facts are the declared information face (fact file owns the spellings), the plan restates none, and the repaired citation groups add no duplicated normative content.
- **Constitution pass (D)**: no MUST violation found; three Constitution Check evidence statements re-adjudicated — row I now true (W2-10 fixed), row VI and row XV overstatements persist (W2-11, W2-09).
- **Decision-tension pass (I)**: 5 records `T-001`…`T-005`, section directly after Constitution Check and before Project Structure; all field labels present, two-pole `binding_constraints`, `expected_sacrifice` each maps to a declared SC source; plan.md unchanged, so round-1's validator reading (`status: ok`, 5 records) remains applicable.
- **Registry pass (G)**: `.specify/features.md` and `.specify/features/096.md` remain outside this wave's read domain and were not assessed; within the domain, `feature-ref.md` and `plan.md:43` agree on the 096 row + `Planned` status.
- **Checklist pass (H)**: `checklists/*.md` is outside this wave's read domain; not assessed here (owned by the stage-level checklist wave / driver).
- **Coverage accountant**: the skill's fixed `account-clause-coverage.py` step needs `requirements.md` / `tasks.md`, which are outside this wave's read domain, so it was not run by W2.

## Method / limits

- Eight-pass detection (A/B/C/D/E/F/G/I) applied to the ten-file slice only; no edits, no remediation, no push, no dirty-file restore.
- No CRITICAL/HIGH raised, so the skill's independent C/H validation precondition is vacuous for this wave; if the merged gate re-rates any W2 row to HIGH, an independent validation subagent is still owed.
- The fact file `journal-format.yaml` is outside the read domain: claims that "the fact file owns the spellings" were checked for internal consistency only, not against the fact file itself.
- Round 2 is full-severity re-adjudication, so the C/H-only residue-list requirement does not apply; every round-1 ID is nevertheless dispositioned in the rerun-delta table.

## Wrap-up bookkeeping

- Identity three steps executed under `skill:analyze-artifacts`, run `r20261110T081104Z-b096`:
  - Run Determination → `duplicate`（该 unit+run 已由 W1 并发波记录；引擎确定响应，exit 0）。
  - Exec Quant → `duplicate record ... no second row written`（exit 0）。
  - Feedback Record → `duplicate: true`，返回既有条目 `.specify/memory/feedback/20261110T092908Z-skill-analyze-artifacts.md`；W2 第二轮的 review 以本 findings 文件为准（同一 unit+run 禁止二次记录）。
- Threshold notice: `should_prompt=true` × run-record `trigger_feedback=0`（经 run-determination `--action history --target` 复核）→ 不弹非阻塞提示（两真才弹）。
- `WRAPUP-DEFERRED` 不适用：三步均得到引擎的确定响应（duplicate 为已记录，不是记账失败）。
