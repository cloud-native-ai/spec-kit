# Analyze Findings — Round 3, Wave W13 (098-suite-speed-optimizations)

**Date**: 2026-11-10
**Round**: analyze r3（修复 r3 后重过门；并发 N=2）
**Read domain (read-only, no fixes applied)**: `requirements.md`、`checklists/suite-speed-2026-11-10.md`、`tasks.md`

**Round-3 focus verification (SC-004 re-anchoring)**: 「缺省档同选择集并行/串行两臂 ≤50%，慢档排除差异只作披露读数」已在 requirements §Overview L28 / US1 L36–L40 / FR-007 L147 / FR-021 L170 / SC-004 L205 / SC-004 Source L219 / A3 L252 与 tasks T055–T056 (L215–216) 一致落位；未发现以慢档排除兑现任何提速判据的残留表述。本轮 **0 CRITICAL / 0 HIGH**。

**Anomalies**: 无；无就地修复（本轮不做修复）。

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|---|---|---|---|---|
| W13-01 | MEDIUM | requirements.md L170 (FR-021), L211 (SC-010), L225 (SC-010 Source); tasks.md L217 (T057) | FR-021 要求 SC-010 的程序化 diff 扫描对三类 098 增量判据「任一命中即 MUST 判红」，但 SC-010 的扫描规则、其 Measurement Source 与 T057 都只含「参数化条目数不减少」，未含「等待截止被放宽超过 FR-026 上限」与「worker 数解析超出 runner 契约既有规则」两类，MUST 级判据缺承载面。 | requirements FR-021 ↔ SC-010（补齐扫描规则）；tasks T057 同步 |
| W13-02 | MEDIUM | requirements.md L169 (FR-020), L214–L226 (Measurement Sources); tasks.md L68 (T003), L215–L220 (T055–T060) | FR-020 的 MUST「记录运行期子进程调用数」既无测量方法定义（动态调用计数 vs 静态 AST 普查，CHK032），也无任何任务行产出该读数——T003 只做静态 subprocess 普查（P-4），T045 的清单仅覆盖转换面。 | requirements FR-020（定义方法并落测量源）＋ tasks（新增读数行或改写为静态口径） |
| W13-03 | MEDIUM | requirements.md L174 (FR-025), L193 (Key Entities 会话级扫描缓存), checklists L33 (CHK015); tasks.md L140 (T025) | FR-025/Key Entities 把缓存键定义为（会话，worker，受管扫描面）三元组，而 T025 实现键为 (worker, surface, root, variant)，root/variant 两个身份组件在需求侧无定义，键身份以哪一侧为准不可判定。 | requirements FR-025（吸收 root/variant 或将它们声明为扫描面身份的一部分） |
| W13-04 | MEDIUM | requirements.md L176 (FR-027), L260 (A11), L266 (A17), checklists L52 (CHK028); tasks.md L200 (T049) | FR-027 的保留类封闭枚举（含 A11/A17 扩展）不含 `copy-topology`，而 T049 依赖该保留类登记 keep 行；按 FR-027「其余只验证纯 Python 引擎或 CLI 的调用 MUST 改进程内直调」的字面判据，该保留属违约。 | requirements FR-027 / A11 / A17（补入该类或将其归并到既有保留类） |
| W13-05 | MEDIUM | requirements.md L165 (FR-015), L187 (RS-004), L194 (Key Entities 注入时钟), L261 (A12), checklists L42 (CHK021); tasks.md L165–L166 (T032–T033) | 需求把注入时钟描述为「测试夹具输入」、RS-004 的 in-scope 面不含 `scripts/python/feedback-utils.py`，而 T032 新增该 shipped engine 的 `--now` CLI 选项（含 `--help` 与具名错误面）并触发镜像义务，需求侧未授权也未约束任何产品代码接口变更。 | requirements（FR-015 / RS-004 / A12 / Key Entities 明示载体与边界）；plan/contracts 对齐 |
| W13-06 | LOW | requirements.md L25, L30; tasks.md L53 (P-3), checklists L64 (CHK034) | 同一 `time.sleep` 普查的文件数在两处不一致：requirements 记「20 处 / 8 文件」，tasks P-3 记「20 occurrences in 10 files」，且 A6 未指定验收以哪一读数为准。 | requirements §Overview（与 P-3 对账，或标注一律以 implement 起点重测为准） |
| W13-07 | LOW | tasks.md L91 (T012), L118 (T021), L31 (GATE-5) | T012 声明运行 tier 契约「obligations 1–11」全绿，但 obligation 11 由更晚的 T021 追加、T012 的 blockedBy 不含 T021，按行序该绿记录不可能覆盖 obligation 11，之后也无重跑行（仅 GATE-5 兜底）。 | tasks（T012 改为 obligations 1–10，或增加 T021 后的重跑行/依赖） |
| W13-08 | LOW | tasks.md L395–L396（Clause Attribution 表） vs L89/L91（T010/T012）、L108/L112–L114/L221（T014–T017/T061） | Clause Attribution 表与实际 `[green:]` 标签错位：slow-membership C-005…C-009 表记 T010 而标签在 T012；parallel-consistency 的 C-001…C-006/C-009…C-012 表分散记于 T014/T015/T016/T017 而标签集中于 T017（+T061）；标签自身构成合法 68/68 单次分区。 | tasks §Clause Attribution（按实际标签重写表） |
| W13-09 | LOW | requirements.md L228–L236 (Shared Strings), L47 (US1 AS4), L126 (Edge), L173 (FR-024), L252–L253 (A3/A4), checklists L27 (CHK012); tasks.md L86 (T007), L88 (T009) | Shared Strings 的 Consumed by 列不完整（[[STR-001]] 漏 FR-007/FR-024；[[STR-003]] 漏 US1 AS4/Edge/FR-024/A3/A4；[[STR-002]] 漏 US1 AS4/Edge），且本特性新增、被守门测试逐字消费的 `tier=` / `excluded_slow=` / 登记册类别值未按该约定挂接单一所有者。 | requirements §Shared Strings（补 Consumed by；决定新字面量入表或显式指向契约 owner） |
| W13-10 | LOW | requirements.md L168 (FR-019), L176 (FR-027), L210 (SC-009), checklists L50 (CHK026) | SC-009 的「转换前后同一断言集合全绿」与 FR-027 允许把退出码断言改为 CliRunner 等价结果之间存在形式冲突，「等价性」未定义可判定的比较口径。 | requirements SC-009 / FR-027（给出等价性判据措辞） |
| W13-11 | LOW | tasks.md L27 (GATE-1), L68 (T003), L221 (T061) | GATE-1 与 T061 均以 `baseline-failed.txt` 为比较基线，但没有任何行声明该文件为产出物（T003 只记「the --names-out reading」未落路径），gate 的比较对象无产出归属。 | tasks（T003 显式以 `--names-out` 写 `baseline-failed.txt`，或在 GATE-1 注明该路径由槽位 1 产出） |

**Summary**: 11 findings — 0 CRITICAL, 0 HIGH, 5 MEDIUM, 6 LOW.
