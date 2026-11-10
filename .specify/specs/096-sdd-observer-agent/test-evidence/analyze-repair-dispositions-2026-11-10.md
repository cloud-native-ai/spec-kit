# Analyze repair dispositions — 096-sdd-observer-agent — 2026-11-10

- **Round**: analyze 门失败后的上游修复轮（单写者，一轮为限）
- **Input**: `test-evidence/analyze-merged-2026-11-10.md`（CRITICAL 0 / validated HIGH 4；W1-03 已由校验波 reject 并保留在 Appendix A）
- **Scope of this round**: `requirements.md`、`tasks.md`、`contracts/`（5 页）的定点修复；证据 = 本文件 + `test-evidence/analyze-repair-gates-2026-11-10.txt`。未执行其他修复。

| Finding | Verdict | Anchors (post-repair) | One-line reason |
|---------|---------|-----------------------|-----------------|
| W1-02 | fixed | `requirements.md:137`（FR-009：终态收束执行 + 收束缺口写入义务 + 失败回退披露）; `requirements.md:144`（FR-013：缺口终点＝终态收束执行）; `requirements.md:157`（FR-020：披露与 journal 写入互不替代）; `requirements.md:191`（SC-001 失败线判据指回 FR-009/FR-013）; `requirements.md:197`（SC-007 改写为「线终态收束执行」并指回）; `contracts/observer-lifecycle.contract.md:61`（C-08：`--final` 同时关闭开放缺口窗口） | SC 侧失败线覆盖与缺口披露判据现在由 FR-009 的收束写入义务支撑，SC 与 FR 两侧同步，契约 C-08 随同一口径更新。 |
| W3-01 | fixed | `tasks.md:87-100`（Package Map 重切：wp01 T006–T017,T036 / wp02 T018–T020,T037–T038 / wp03 T023–T030,T034 / wp04 T021–T022,T031–T033,T035,T039–T047；严格串行链）; `tasks.md:296`（并行机会限定为同 phase [P]）; `tasks.md:336-340`（Parallel Team Strategy 同步） | T037 移入 wp02（其 T020/T036 依赖均在前序包内），T031/T032 移入 wp04；四包按 wp01→wp02→wp03→wp04 严格串行，全部跨包行边指向更早的包，三种顺序声明收敛为一种可执行顺序；分区机械复核 13+5+9+15=42、无重叠、47 行全覆盖。 |
| W3-04 | fixed | `tasks.md:11`（红证据按包分文件的总则）; `tasks.md:108`（T001 创建 wp01/wp02/wp03 三份 landing 文件）; `tasks.md:139`（T008→wp01）; `tasks.md:162`（T016→wp01）; `tasks.md:163`（T018→wp02）; `tasks.md:187`（T024→wp03）; `tasks.md:232`（T037→wp02）; `tasks.md:98`（partition check 证据布局）; `tasks.md:377`（Notes 同口径） | red-first 证据改为每包一文（`notes/red-first-evidence-wp01.md` / `-wp02.md` / `-wp03.md`），写行不再跨包共享同一路径，符合 AGENTS.md § Concurrent Development Safety「记录类数据一文一件」；其余证据文件均为单行写者。 |
| E-01 | fixed | `tasks.md:38`（GATE-9 增 FR lane 判据）; `tasks.md:254`（T047 同步）; `tasks.md:248`（T041 认领 `observer-role#C-01`）; `tasks.md:187`（T024 认领 `observer-verification#C-03`）; `tasks.md:231`（T036 认领 `#C-05`）; `tasks.md:162`（T016 认领 `#C-07`）; `tasks.md:356-373`（§ Green Attribution 重写：58/58 认领 + disclosed-warnings 表）; `contracts/*.md` 全部 58 条条款体末尾新增 FR citation group；五页页级 `Requirements:` 行同步（`journal-engine:3`、`observer-lifecycle:3`、`observer-role:3`、`observer-verification:3`，`journal-format:3` 不变） | 4 条未认领条款以 [green:] 认领后 clause lane 58/58、beyond-baseline 0；58 条条款体全部携带 citation group，FR lane 23/23；实测 `account-clause-coverage.py` exit 0、`status: ok` —— GATE-9/T047 按字面可达（4 条机械警告已逐条披露于 § Green Attribution，validate-tasks exit 0）。 |
| W1-03 | not processed（Appendix A reject，按指令不处置） | — | 校验波已 reject（下游 T003/T033/DoD-6/plan T-005 已具名基线），保留原 ID 于 analyze-merged 附录，不静默丢弃。 |

**Gate re-runs**（全文见 `test-evidence/analyze-repair-gates-2026-11-10.txt`）：

- `validate-requirements.py` → `status: ok`，0 error / 0 warning，exit 0
- `pre-analyze-check.py --stage requirements` → `decision: pass`，0 error（advisory 均为本特性待创建路径），exit 0
- `pre-analyze-check.py --stage plan` → `decision: pass`，0 error，exit 0
- `pre-analyze-check.py --stage tasks` → `decision: pass`，0 error，exit 0
- `decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks，均低于上限），exit 0
- supporting：`validate-tasks.py` → `0 error(s), 4 warning(s)`，exit 0（4 条警告 = 3 green-cross-phase + 1 green-path-divergence，全部列入 § Green Attribution disclosed-warnings 表）
- supporting：`account-clause-coverage.py` → `status: ok`、claimed clauses 58、uncovered beyond baseline 0、FR claimed 23/23，exit 0

**In-passing notes（本轮 4 条之外，仅披露，不改变其 finding 状态）**：

- W3-02（MEDIUM）：重写 Package Map 时一并把 `tests/fixtures/sdd-observer/failure_builder.py`（T023）补入 wp03 写域（`tasks.md:95`）。
- W2-10（LOW）：E-01 的 per-clause citation group 落地后，「每条条款引用 FR」的证据陈述实际成立（`plan.md` 未改，归后续轮次复核）。
- 其余 MEDIUM/LOW（W1-01、W2-*、W3-03/W3-05/W3-06 等）保持原状，交后续轮次。

**Anomaly**: none —— 未发现需上报的异常；无静默丢条（4 条 validated HIGH 全部处置并留痕，W1-03 reject 依指令保留）。
