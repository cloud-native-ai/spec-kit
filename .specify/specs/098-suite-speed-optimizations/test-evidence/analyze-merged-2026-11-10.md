# Analyze Merged Report — 098-suite-speed-optimizations（analyze Round 1，2026-11-10）

- **Stage**: analyze（串行集成 · Round 1）
- **输入**: `test-evidence/analyze-findings-W1.md`（requirements + checklists，34 条）、`analyze-findings-W2.md`（plan / data-model / quickstart / contracts，12 条）、`analyze-findings-W3.md`（tasks.md，11 条）
- **权威**: 本特性 spec 全目录 + `.specify/constitution.md`（v1.19.0）+ `.specify/skills/internal/analyze-artifacts/`（SKILL.md、`references/detection-and-severity.md`、`references/validation-and-report.md`）
- **性质**: 只读集成。未修复任何 finding；本阶段写入仅：本报告、`test-evidence/analyze-coverage-accounting-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback，按派发纪律不提交）。
- **Rerun delta**: N/A（`test-evidence/` 下无更早 analyze 报告，本特性首轮）
- **检测波分工**: W1 = 通道 A/B/C/D/F/H（requirements 域）；W2 = 通道 A/B/C/E/F（plan 设计域）；W3 = 通道 A–I（tasks 域）。通道 G（feature registry/linkage）未被三波覆盖，由本集成者补做一次有界检查（见 §6、G-01）。

## 0. Gate verdict 与 CRITICAL/HIGH 汇总

**Verdict: 未通过（FAIL）** —— 1 条 CRITICAL + 7 条 HIGH 全部处于 **open 且 validated** 状态；按 SKILL §9，CRITICAL 必须在 `/speckit.implement` 前处置，HIGH 与之一并归属后续修复 pass。MEDIUM/LOW 不阻断实施。

| 严重度 | 条数 | 处置要求 |
|--------|------|----------|
| CRITICAL | 1 | 实施前必须修复（宪法冲突，不可降级） |
| HIGH | 7 | 实施前处置；归属见各行的建议 owner |
| MEDIUM | 37 | 不阻断；随对应阶段收敛 |
| LOW | 13 | 建议性 |
| **合计** | **58** | 主表 50 行 + overflow 8 行（§2.2） |

### 0.1 验证路径声明（显式披露，非静默）

- **路径**: 按本次派发 §③，CRITICAL/HIGH 的锚点复核由**串行集成者直接重读**完成（每行给出 `evidence_supported` / `evidence_not_supported` 边界），**未**派发 fresh-context 验证子代理波。
- **独立性**: 集成者不是 W1/W2/W3 任何检测结论的作者，与三波检测集合不相交；但按 SKILL `validation-and-report.md` § 5.5 的严格标准，直接重读弱于 fresh-context 子代理。若后续 stage 需要更严证据，可按同一 finding ID 重派验证波。
- **W2 例外**: W2-01（检测时 HIGH）已由 W2 波内的独立验证子代理裁决 **downgrade → MEDIUM**（降级率 1/1）；本报告原样携带其 `(validated: downgraded)` 注记与边界。

### 0.2 CRITICAL/HIGH 汇总与指针（全部 **validated**，无 proposed）

| # | ID | 严重度 | 一句话事实 | 指针（worker 行 → 锚点） | 状态 |
|---|----|--------|------------|---------------------------|------|
| 1 | W1-01 | CRITICAL | FR-021 重述宪法 XX 拥有的捷径禁止集却漏掉「宣告 flaky」，且违反 XX「引用 owner、不得重述」的 MUST | `analyze-findings-W1.md#W1-01`；`requirements.md` §Overview(L28)、§FR-021(L170) vs `constitution.md` §XX(L431–439) | validated |
| 2 | W1-02 | HIGH | SC-010 的度量面只数「新增装饰器」，函数体内 `pytest.skip()`、条件跳过、手写重跑至绿不在检测面内，无法支撑 FR-021 的全称谓禁止 | `analyze-findings-W1.md#W1-02`；`requirements.md` §SC-010(L211)、§Measurement Sources SC-010(L225) vs §FR-021(L170) | validated |
| 3 | W1-08 | HIGH | FR-024 的「披露排除数 = 本次选择内 slow 成员数」未按档位限定；caller 自带 `-m` 时 slow 成员被选中而非排除（排除数应为 0），与 FR-007/FR-009 冲突 | `analyze-findings-W1.md#W1-08`；`requirements.md` §FR-024(L173) vs §FR-007(L147)/§FR-009(L149)；Q2(L243) | validated |
| 4 | W1-09 | HIGH | FR-024 的「`--full` 时收集集合回到全量」未限定「无调用方 `-m`」，与 FR-009「`--full` + 调用方 `-m` 时选择仍归调用方」冲突 | `analyze-findings-W1.md#W1-09`；`requirements.md` §FR-024(L173) vs §FR-009(L149)、§FR-008(L148) | validated |
| 5 | W1-17 | HIGH | SC-008 的零计数声明以未枚举的「runner 相关测试」为作用域，该全称否定断言缺少可判定边界 | `analyze-findings-W1.md#W1-17`；`requirements.md` §SC-008(L209)/§FR-016(L162)/§FR-017(L163)；SC-008 Source(L223) | validated |
| 6 | W1-21 | HIGH | FR-026/A16 声称 30 秒截止「与既有 runner 测试约定一致」，但共享等待辅助当前缺省实测为 5.0 秒（`tests/fixtures/line_fixtures.py:396`；tasks P-7）；共享缺省的行为变更未声明 | `analyze-findings-W1.md#W1-21`；`requirements.md` §FR-026(L175)/§A16(L265)；`tasks.md:57`(P-7) | validated |
| 7 | W3-01 | HIGH | 六份契约的条款 id 为前缀形态（`TS-01`…`IC-10`），规范条款引擎只认 `C-<n>`：68 条款全部不可解析、27/27 FR 落入 `fr-uncovered`；两套框架引擎对该制品集判读不一致 | `analyze-findings-W3.md#W3-01`；`tasks.md:384–389`、`:67`(T002)；本报告 §1 覆盖核算运行 | validated |
| 8 | W3-11 | HIGH | DoD-7 / GATE-1 / Notes 宣称「恰好两次全量运行」，但 T061 一条命令执行两次全量（`--full --names-out` + 同树 `--full --serial`）→ 实际 3 次；预算计数矛盾 | `analyze-findings-W3.md#W3-11`；`tasks.md:21`(DoD-7)、`:27`(GATE-1)、`:394`(Notes) vs `:221`(T061) | validated |

### 0.3 每条 C/H 的证据边界（集成者直接重读，2026-11-10）

- **W1-01** — `evidence_supported`: 宪法 XX L431–436 要求消费者引用 owner 指南、不得重述（MUST），L438–439 列「shrinking the selection, skipping, declaring flakiness, or retrying until green」；Overview L28 明确禁止「宣告 flaky」；FR-021 L170 的封闭清单含重试至绿/随机丢参/skip/xfail/缩小参数化/放宽时限/无上限 worker，**独缺宣告 flaky**。`evidence_not_supported`: 未主张下游 plan/tasks 已复制该漂移（其传播面是推断的修复链，不是已观测副本）。
- **W1-02** — `evidence_supported`: SC-010 L211 的判据是「新增的 skip / xfail / 重试装饰器数为零」，Source L225 明示「装饰器与参数化计数」；FR-021 L170 的「任一出现即 MUST 判红」是全称谓。`evidence_not_supported`: 未断言存在其他守门面能覆盖非装饰器形态（spec 链内没有具名检测面）。
- **W1-08** — `evidence_supported`: FR-024 L173 的等式未按档位限定；FR-007 L147「调用方自带 `-m` 时 MUST NOT 前置缺省」、FR-009 L149「选择由调用方的单一 `-m` 拥有」；Q2 L243 复制同一未限定等式。`evidence_not_supported`: 「caller 档披露排除数应为 0」是从 FR-007/FR-009 语义推出的结论，原文未逐字写 0。
- **W1-09** — `evidence_supported`: FR-024 L173「[[STR-003]] 时…收集集合回到全量」无「无调用方 `-m`」限定；FR-009 L149「[[STR-003]] 与调用方选择同时出现时，执行一个不含缺省排除的完整选择」。`evidence_not_supported`: 无（两侧条款均为原文）。
- **W1-17** — `evidence_supported`: SC-008 L209 的作用域写作「runner 测试作用域」；FR-016 L162 只写「runner 相关测试」，未枚举文件集合；FR-017 L163 以「FR-015 与 FR-016 的作用域内」反向引用该未定边界。`evidence_not_supported`: 未判定哪些文件应入作用域（设计映射到四个文件，但需求文本未拥有）。
- **W1-21** — `evidence_supported`: FR-026 L175 与 A16 L265 均称 30 秒「与既有…约定一致」；`tests/fixtures/line_fixtures.py:396` 实测 `wait_until(predicate, timeout: float = 5.0, interval: float = 0.05)`；tasks P-7 记录同一读数。`evidence_not_supported`: 「086 runner 测试存在 30 秒约定」未被任何被引证据证实；本波未审计 086 测试的个别调用点，只证实共享缺省为 5.0 秒。
- **W3-01** — `evidence_supported`: `tasks.md:384–389` 自述该偏差；本阶段覆盖核算运行（§1）输出 `[clause-unparsable] fail (113)`，`--list-named` 显示 098 的 6/6 契约文件全部在列，`[fr-uncovered] fail (27) — 0 of 27`。`evidence_not_supported`: T002 尚未执行，因此「冻结会钉住坏基线」是同一运行结果支撑的前向推断，不是一个已发生的冻结。
- **W3-11** — `evidence_supported`: DoD-7 L21「The two-slot test budget stays exactly two … no third full run is added for measurement」；GATE-1 L27「the only post-change full run is slot 2」；Notes L394「exactly two full runs … Every other run in this file is a targeted run or a collection」；T061 L221 同一条命令含 `--full --names-out` 与同树 `--full --serial` 两次全量执行。`evidence_not_supported`: requirements 的 Q2(L242)/A14(L263) 明确把串行全量验证运行置于两槽预算之外且不受 FR-020「为度量」禁令约束——因此缺陷在**计数措辞**（GATE-1/Notes），预算政策本身未被推翻；修复须由 plan（预算 owner）与 tasks 共同对齐。

## 1. 方法与执行轨迹

| 步骤 | 命令 / 动作 | 结果 |
|------|-------------|------|
| 前置脚本 | `bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` | exit 0；`REQUIREMENTS_DIR` 指向本 spec；`FEATURE_ID=086`；`AVAILABLE_DOCS` 全齐 |
| 覆盖核算（固定步骤，**未** `--freeze`） | `python3 scripts/python/account-clause-coverage.py .specify/specs/098-suite-speed-optimizations` | exit 2，`status: baseline-missing`；`[fr-uncovered] fail (27)`；`[clause-unparsable] fail (113)`；`[coverage-baseline-delta] fail (640)`；完整输出见 `test-evidence/analyze-coverage-accounting-2026-11-10.txt` |
| 决策张力（pass I 的确定性段） | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/098-suite-speed-optimizations --json` | `status: ok`，全部标签 count 0 / severity 0 |
| 检测波 | W1 / W2 / W3 只读波（派发结果文件） | 34 + 12 + 11 = 57 条 finding |
| 确定性归并 | 本报告 §2 | 主表 50 行 + overflow 8 行 |
| C/H 复核 | 集成者直接锚点重读（§0.1、§0.3） | 8/8 validated；0 proposed；0 reject；W2 波内降级 1 条（W2-01） |
| Pass G 补做 | 读 `.specify/features.md` 086 行、`.specify/features/086-efficient-test-execution.md`、`feature-integration.md` § Core Protocol | 绑定正确；stage 记录漂移 → G-01（LOW，integrator addendum） |

**覆盖核算的阶段可见问题（SKILL §3 强制披露）**: `status: baseline-missing` —— 098 的 `coverage-baseline.txt` 尚不存在（T002 冻结行未执行），所以本次运行无法判定增量，print 的是全语料 640 条 uncovered。remedy 是两步且**有顺序**：(1) plan 阶段先把六份契约的条款 id 重编号为 `C-<n>` 并同步全部引用（W3-01 的 plan-owned remedy）；(2) 再由 `/speckit.tasks` 重跑冻结（C-6 义务）或执行 T002 冻结。若先冻结，会把「27/27 FR uncovered + 68 条款不可解析」钉成基线（W3-01 已预言，本阶段运行已实测）。

## 2. 合并 Findings

**归并规则（确定性，可复现）**: 三波 finding 原样保留其 ID、严重度、锚点、事实与建议；主表按「严重度降序 → 波次（W1<W2<W3<G）→ 同波内 ID 升序」排列；前 50 行入表，其余逐条进入 §2.2 overflow 摘要。`propagation_surface` 取自 worker 的「建议归属」链（W1 = `plan → tasks → 实现`；W2 = `tasks → 实现`；W3 = `实现`；G = `none`），严重度不做重评分。

### 2.1 主表（50 行）

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| W1-01 | D 宪法对齐 | plan → tasks → 实现 | **CRITICAL**（validated） | `requirements.md` §Overview(L28)/§FR-021(L170) vs `constitution.md` §XX(L431–439); CHK001(L13) | FR-021 重述宪法 XX 的禁止捷径集却漏掉「宣告 flaky」，且未按 XX 的指针规则引用 owner | requirements §FR-021 对齐宪法 XX 的 owner，仅保留 098 特有增量 |
| W1-02 | E 覆盖 | SC-010 → 守卫实现 | **HIGH**（validated） | `requirements.md` §SC-010(L211)/§Measurement Sources SC-010(L225)/§FR-021(L170); CHK002(L14) | SC-010 只数新增装饰器；函数体内 skip、条件跳过、手写重跑至绿不在检测面内 | requirements §SC-010/§FR-021 定义非装饰器形态的检测面 |
| W1-08 | F 不一致 | FR-024 → 守门测试 → 实现 | **HIGH**（validated） | `requirements.md` §FR-024(L173) vs §FR-007(L147)/§FR-009(L149); Q2(L243); CHK010(L25) | 排除数等式未按档位限定；caller `-m` 档 slow 成员被选中而非排除 | requirements §FR-024 按 tier 限定披露算式，与 FR-007/FR-009 对齐 |
| W1-09 | F 不一致 | FR-024 → 守门测试 → 实现 | **HIGH**（validated） | `requirements.md` §FR-024(L173) vs §FR-009(L149)、§FR-008(L148); CHK011(L26) | 「`--full` 回到全量」未排除「`--full` + 调用方 `-m`」情形，此时不会回到全局全量 | requirements §FR-024 限定为「无调用方 `-m`」 |
| W1-17 | B 歧义 | SC-008 → 扫描守卫 → 实现 | **HIGH**（validated） | `requirements.md` §SC-008(L209)/§FR-016(L162)/§FR-017(L163); SC-008 Source(L223); CHK019(L40) | 零计数声明的作用域「runner 相关测试」未枚举文件集合，全称否定断言不可判定 | requirements §FR-016/§FR-017/§SC-008 枚举作用域 |
| W1-21 | F 不一致 | 等待辅助 → runner 测试 → 实现 | **HIGH**（validated） | `requirements.md` §FR-026(L175)/§A16(L265); CHK023(L44); `tests/fixtures/line_fixtures.py:396`; `tasks.md:57`(P-7) | 30 秒「既有约定」与实测共享缺省 5.0 秒矛盾；共享缺省行为变更未声明 | requirements §FR-026/§A16 与 tasks/plan 的等待辅助对齐（或显式声明变更） |
| W3-01 | F 不一致 | plan（契约重编号）→ tasks → 实现 | **HIGH**（validated） | `tasks.md:384–389`、`:67`(T002)、`:7`; 覆盖核算运行（本报告 §1） | 六契约条款 id 前缀形态不被规范引擎解析：68 条款全不可解析、27/27 FR 判 uncovered；两引擎判读不一致 | plan 阶段把条款 id 重编号为 `C-<n>` 并同步全部引用；tasks 之后重发归属标签 |
| W3-11 | F 不一致 | 预算台账 → closure → 实现 | **HIGH**（validated） | `tasks.md:21`(DoD-7)/`:27`(GATE-1)/`:394`(Notes) vs `:221`(T061) | 声明「恰好两次全量运行」，T061 实执行两次全量（含同树串行验证）→ 计数 3 次 | plan（预算 owner）+ tasks 对齐计数措辞；requirements A14 已把验证运行置于槽预算外 |
| W1-03 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-021(L170); CHK003(L15) | 「无上限 worker 数」「随机丢参」没有具名上限或可比口径，不可机械判红 | requirements §FR-021 补具名判据 |
| W1-04 | B 歧义 | plan → tasks → 实现 | MEDIUM | `requirements.md` §FR-021(L170)/§SC-010(L211); CHK004(L16) | 「缩小参数化」未定义比较单位（逐文件/逐测试）与范围 | requirements §FR-021/§SC-010 定义比较单位 |
| W1-05 | B 歧义 | requirements → 登记册 → 实现 | MEDIUM | `requirements.md` §FR-006(L146); CHK007(L22) | 「少数」全语料扫描型 contract 测试无数量/占比上限，成员增长可持续缩小缺省档 | requirements §FR-006 加上限或占比上限 |
| W1-06 | B 歧义 | requirements → 分档测试 → 实现 | MEDIUM | `requirements.md` §FR-006(L146); CHK008(L23) | 「integration 类测试」判定基未定（目录/marker/行为），contract 下的进程边界测试归属不可判 | requirements §FR-006 定义判定基 |
| W1-07 | C 欠指定 | requirements → 登记册 → 实现 | MEDIUM | `requirements.md` §FR-006(L146)/§FR-024(L173); CHK009(L24) | 双属（进程边界+语料扫描）测试的归类规则缺失，登记册每条只记一个类别 | requirements §FR-006/§FR-024 规定归类规则 |
| W1-10 | C 欠指定 | requirements → 契约/守门 → 实现 | MEDIUM | `requirements.md` §Shared Strings(L232–234)/§FR-024(L173); CHK012(L27) | 登记册类别值、登记册路径、`tier=`/`excluded_slow=` 字段名被逐字消费却无单一 owner | requirements §Shared Strings/§FR-024 补钉或声明 owner |
| W1-12 | B 歧义 | FR-009 → runner → 实现 | MEDIUM | `requirements.md` §FR-009(L149); CHK014(L29) | 调用方 `-m` 检测面未定：命令行拼写还是含 `addopts` 配置；下游 runner「不产生两个 `-m`」不可判 | requirements §FR-009 定义检测面 |
| W1-13 | C 欠指定 | requirements → plan 缓存设计 → 实现 | MEDIUM | `requirements.md` §FR-025(L174); CHK015(L33) | 缓存键需求只拥有（会话、worker、受管扫描面），设计另加 `root`/`variant`，条目身份成分未全由需求拥有 | requirements §FR-025 与 plan 收敛缓存键 owner |
| W1-14 | B 歧义 | requirements → 缓存设计 → 实现 | MEDIUM | `requirements.md` §FR-012(L155)/§FR-025(L174); CHK016(L34) | 「受管扫描面」「框架根文件」未枚举，「每面每会话一次」脱离设计查找不可判 | requirements §FR-012/§FR-025 枚举集合 |
| W1-15 | E 覆盖 | FR-013 → 守卫 → 实现 | MEDIUM | `requirements.md` §FR-013(L156)/§FR-014(L157); CHK017(L35) | FR-014 的突变只证明内容篡改转红，没有「改写者消费了共享缓存」的检测面 | requirements §FR-013/§FR-014 补检测面 |
| W1-18 | C 欠指定 | FR-017 → 豁免清单 → 实现 | MEDIUM | `requirements.md` §FR-017(L163); CHK020(L41) | 豁免清单无载体路径与行模式，扫描守门无法消费 | requirements §FR-017 或 plan 定义豁免清单 owner |
| W1-19 | C 欠指定 | FR-015 → 引擎/测试边界 → 实现 | MEDIUM | `requirements.md` §FR-015(L161)/§A12(L261); CHK021(L42) | A12 对产品代码沉默；注入时钟可以是 shipped engine 新选项还是必须测试侧未定 | requirements §FR-015/§A12 明确允许面 |
| W1-20 | B 歧义 | FR-017 → 豁免判断 → 实现 | MEDIUM | `requirements.md` §FR-017(L163); CHK022(L43) | 「承担同步/顺序语义的 sleep」与真实时间语义（TTL）无可判定分类规则 | requirements §FR-017 补分类规则 |
| W1-22 | C 欠指定 | FR-019 → 转换清单 → 实现 | MEDIUM | `requirements.md` §FR-019(L168); CHK024(L48) | 转换清单完整性分母未定义：计数单位与普查人群（是否含 fixtures/conftest 的 AST 扫描） | requirements §FR-019 定义分母 |
| W1-23 | B 歧义 | FR-027 → 转换清单 → 实现 | MEDIUM | `requirements.md` §FR-027(L176); CHK025(L49) | 保留优先规则非穷尽式；不属任何列类且不可转换的调用无处置规则 | requirements §FR-027 写成穷尽式并规定残余处置 |
| W1-24 | F 不一致 | FR-019/FR-027 → SC-009 → 实现 | MEDIUM | `requirements.md` §FR-019(L168)/§FR-027(L176)/§SC-009(L210); CHK026(L50) | 「同等行为断言」/「同一断言集合全绿」/CliRunner 等价结果对「等价」无可判定比较规则 | requirements 定义等价比较规则 |
| W1-25 | C 欠指定 | FR-019 → 清单计数 → 实现 | MEDIUM | `requirements.md` §FR-019(L168); CHK027(L51) | helper wrapper 的分类单位未定（每 wrapper 一行还是每被包裹调用点一行） | requirements §FR-019 定义分类单位 |
| W1-26 | E 覆盖 | FR-027/§A11 → 清单 → 实现 | MEDIUM | `requirements.md` §FR-027(L176)/§A11(L260); CHK028(L52) | 保留边界枚举缺少设计依赖的 `copy-topology` 类 | requirements §FR-027/§A11 补该类 |
| W1-27 | B 歧义 | FR-023 → 契约 → 实现 | MEDIUM | `requirements.md` §FR-023(L172); CHK029(L56) | 「前缀兼容」无可判定不变量（字段位置/拼写、尾部追加、分隔符解析） | requirements/098 契约面定义不变量 |
| W1-29 | E 覆盖 | FR-010 → 驱动者文档 → 实现 | MEDIUM | `requirements.md` §FR-010(L150); CHK031(L58) | 「驱动者文档」无 owner 路径，两槽位 `--full` 更新不可追踪到具名文件 | requirements §FR-010 指名 owner 路径 |
| W1-30 | B 歧义 | FR-020 → 度量记录 → 实现 | MEDIUM | `requirements.md` §FR-020(L169); CHK032(L62) | 「运行期子进程调用数」测量方法未定（动态计数 vs 静态 AST 普查），数字不可复现 | requirements §FR-020 定义测量方法 |
| W1-31 | B 歧义 | SC-004/SC-005 → 闭包验收 | MEDIUM | `requirements.md` §SC-004(L205)/§SC-005(L206); CHK033(L63) | 50%/110% 墙钟阈值未定义运行间波动容忍度（单次还是重复测量） | requirements 定义测量协议 |
| W1-32 | F 不一致 | Overview/A6 → 实现读数 | MEDIUM | `requirements.md` §Overview(L30)/§A6(L255); CHK034(L64) | Overview 记 20 处/8 文件，tasks 重算 20 处/10 文件；A6 只说不常量，未决定验收读法 | requirements 与 tasks 证据统一计数口径 |
| W1-33 | C 欠指定 | Runtime Stack → plan → 实现 | MEDIUM | `requirements.md` §Runtime Stack & Dependency Ownership(L184–187) | Premises 列引用 EP-001…EP-004，但本制品内无 EP 定义或 owner 指针 | requirements 定义或指向 premises owner |
| W2-01 | F 不一致 | quickstart/plan → implement 起点 | MEDIUM（validated: downgraded） | `contracts/tier-selection.contract.md` TS-15/TS-16; `plan.md` §Summary row 2 + WP-9 item 1; `quickstart.md` S-13 | 基线读数锚点（implement-start、变更前）与 WP-9.1「baseline 槽带 `--full`」、Summary「两槽都带 `--full`」、S-13 注释三种拼写并存，可能把优化后读数当基线 | plan + quickstart S-13 收敛为单一 spellings |
| W2-02 | F 不一致 | scan-cache 契约 → 实现 | MEDIUM | `contracts/scan-cache.contract.md` CA-08 vs CA-06; `data-model.md` E-3; `plan.md` R-8 | CA-08 把 `c20` 列入「已转换为消费 payload」的调用者，而 CA-06/E-3/R-8 要求 `test_c20` 的字节一致性检查保留子进程且不碰缓存；无条款说明 `c20` 哪些断言可消费缓存 | scan-cache 契约（c20 例外条款） |
| W2-03 | F 不一致 | parallel-consistency 契约 → 守卫 | MEDIUM | `contracts/parallel-consistency.contract.md` PC-03/PC-12/PC-M2 | PC-M2 期望「记录树身份检查」对两棵树的名单判红，但 PC-12 的证据字段无树身份/指纹，任何记录或守卫都无法发现该突变 | parallel-consistency 契约补树身份字段 |
| W2-04 | E 覆盖 | scan-cache 契约 → quickstart → 守卫 | MEDIUM | `contracts/scan-cache.contract.md` CA-04/§E CA-M2; `quickstart.md` S-5 | CA-M2 必须以 CA-04（深拷贝隔离）转红，但 §D 证明义务与 S-5 的守卫内容都没有 copy-isolation 用例 | scan-cache 契约 §D + quickstart S-5 补可执行用例 |
| W2-05 | F 不一致 | event-wait 契约 → 守卫 | MEDIUM | `contracts/event-wait.contract.md` EW-07/EW-09; `data-model.md` E-5 | EW-09 守卫断言 `timeout <= 30`，EW-07/E-5 允许更长截止（逐条记录理由）→ 合法站点会让守卫转红，契约自相矛盾 | event-wait 契约（守卫与例外一致化） |
| W2-06 | F 不一致 | quickstart S-1/S-4 → 执行 | MEDIUM | `quickstart.md` S-1（S-4 同一构造） | `comm` 比较消费未排序、含 pytest 尾部汇总行的 `--collect-only -q` 原始输出，MUST-equal 检查按原文不可成立 | quickstart 补 sort/过滤步骤或排序前提 |
| W2-07 | D 宪法对齐 | quickstart 场景 → 执行 | MEDIUM | `quickstart.md` S-1/S-4/S-12/S-13 vs `plan.md` Constitution Check XVII | 场景把 agent scratch 指向裸 `/tmp/...`，违反项目临时目录纪律；plan XVII 的合规证据只覆盖 research 探针 | quickstart 场景改用受制裁临时根 |
| W3-02 | F 不一致 | tasks 语义 → 实现 | MEDIUM | `tasks.md:248` vs `:38`、`:382–389` | 「每条契约条款恰由一个 `[green:]` 行认领」与「本文件不携带归属标签」互斥；`green-dangling` 叙事预设了文件自述不存在的归属 | tasks 重写该句引用偏差节，或待 plan 重编号后再发标签 |
| W3-03 | E 覆盖 | trace 表 → implement | MEDIUM | `tasks.md:317–363`、`:335`(FR-015 行)、`:165–166`(T032/T033) | 7 行（T001/T002/T011/T032/T033/T059/T060）不在任何 FR/SC trace 表；FR-015 的实现行（T032/T033）无 traceability 行 | tasks 补 T032/T033→FR-015 映射与 setup/evidence 行 trace home |
| W3-04 | F 不一致 | 事件等待断言 → red-first → 实现 | MEDIUM | `tasks.md:161`(T031) vs `:170`(T037)、`:57`(P-7) | T031 的 `timeout <= 30`/`interval <= 0.2` 被实测前置缺省（5.0/0.05）先行满足，无法充当 red-first，也测不到回退到 5.0 | tasks 断言 enacted 值（如 `timeout == 30`）；若 EW 条款拥有边界则 plan 一并改 |
| W3-05 | F 不一致 | US1/US2 依赖 → 实现 | MEDIUM | `tasks.md:91–92`(T012/T013) vs `:118`(T021)、`:373`(TS carrier) | T012 声称跑「obligations 1–11」、T013 跑 TS-M drills（载体行指向 guard T021），但 obligation 11 由 US2 的 T021 编写且两行都不依赖 T021 | tasks 把 obligation-11 用例移入 US1，或补 blockedBy 并重排序 |
| W3-06 | F 不一致 | GATE-5 → 完成门 | MEDIUM | `tasks.md:31`(GATE-5) vs `:141–142`、`:167–173`、`:197–202` | GATE-5 声称覆盖「每个新增或变更测试文件」与「每条 red-first 记录」，机械检查只跑五个新契约文件并只测一个共享 red-first 文件非空 | tasks 扩展检查或收窄声明 |
| W3-10 | F 不一致 | US2 独立性声明 → 实现 | MEDIUM | `tasks.md:122`(US2 checkpoint)/`:242` vs `:114`(T017)、`:112–113`(T015/T016) | checkpoint 与故事依赖节声称并行一致性 drill（T014/T017）无 US1 依赖，但 T017 blockedBy T014/T015/T016，而 T015/T016 依赖 US1 行 | tasks 删除独立性声明或重构 T017 |
| W1-11 | C 欠指定 | FR-024 → 登记册维护 | LOW | `requirements.md` §FR-024(L173); CHK013(L28) | 只规定孤儿行转红，未规定成员失去判据时由谁、按何步骤更新登记册 | requirements §FR-024 或 plan 定义维护程序 |
| W1-16 | B 歧义 | FR-025 → 实现 | LOW | `requirements.md` §FR-025(L174); CHK018(L36) | 会话内快照语义未写明取于会话起点还是首次消费时刻，可能隐含消费顺序依赖 | requirements §FR-025 明确快照时点 |
| W1-28 | F 不一致 | FR-023 → 漂移守门 | LOW | `requirements.md` §FR-023(L172); CHK030(L57) | 「C-001…C-016 条款文本不得重开」未给检查形态（如 086 契约文件 diff 不变） | requirements 或 tasks 定义漂移守门 |
| W1-34 | A 重复 | requirements → 契约消费 | LOW | `requirements.md` §Shared Strings(L232–234) vs §FR-007(L147)/§FR-024(L173) | Shared Strings 的 Consumed by 列遗漏 FR-007/FR-024 对 STR-001/STR-003 的消费，消费枚举过期 | requirements §Shared Strings 补消费行 |
| W2-08 | F 不一致 | data-model → quickstart | LOW | `data-model.md` E-8 vs `plan.md` WP-3; `quickstart.md` S-9 | E-8 说「三处 owner/restatement 面」，WP-3 列四行（两个槽行 + 两处阶段提示重述），S-9 检查「both … both」——表面计数需钉死 | data-model E-8 钉计数 |

### 2.2 Overflow（8 行，全部 LOW；事实与建议原样保留于 worker 文件）

| ID | Severity | Location(s) | Summary（截断） |
|----|----------|-------------|-----------------|
| W2-09 | LOW | `contracts/parallel-consistency.contract.md` PC-07; `plan.md` R-10 | 两处引用 PC-10 承接「closure 验证运行不入预算台账」，但 PC-10 的条款主体是缺引擎 xdist shim——预算命题无自有条款 |
| W2-10 | LOW | `data-model.md` E-1 | `excluded_slow` 规则文本（「调用方选择内的 slow 成员」）与其自身不变量（`tier=full ⇒ excluded_slow=0`）冲突 |
| W2-11 | LOW | `contracts/scan-cache.contract.md` CA-07 vs CA-02/CA-11; `data-model.md` E-3 | CA-07 只为 `framework-specs-corpus` 定义构建器/装载/`traversals` 计数；第二个受管面 `framework-root-inputs` 无构建与计数机制，而 CA-11 的 `build_count=1` 义务覆盖全部受管面 |
| W2-12 | LOW | `contracts/tier-selection.contract.md` TS-16; `quickstart.md` S-13 | TS-16 允许记录一条反度量（marked set 重新并入缺省档 = 全量选择）同时在同条款禁止「第三次全量运行」——反度量的预算类未定义 |
| W3-07 | LOW | `tasks.md:143`(T028) vs `:141–142`(T026/T027) | T028 要求语料两文件「before/after」运行，但它 blockedBy T003/T026/T027，运行时 pre-conversion 状态已不存在；before 侧实为 T003 的记录名单，行文未说明 |
| W3-08 | LOW | `tasks.md:9`(Tests Mode) vs `:16`(DoD-2)/`:31`(GATE-5) | Tests Mode 段落把「5 个新守卫文件 + tier 契约文件」写成隐含 6 个文件，而 DoD-2/GATE-5 恰好只数五个新契约文件（tier 契约是其中之一） |
| W3-09 | LOW | `tasks.md:11`(Organization) vs `:310–311`(Work Package 表) | Organization 说「WP-9 → Polish 与 closure 行」，表却把 T003/T022 放入 WP-9、T061 放入独立的「Setup / closure handoff」包 |
| G-01 | LOW | `.specify/features.md` L94（086 行）; `.specify/features/086-efficient-test-execution.md`; `feature-integration.md` § Core Protocol | 绑定正确且状态保持；但 086 索引行记录的 098 最新阶段为 tasks，checklist 制品（`checklists/suite-speed-2026-11-10.md`，2026-11-10）无对应登记；`/speckit.checklist` 在 Core Protocol 的生命周期命令清单内，而 checklist 命令模板未携带该步骤——义务载体判读不一致（integrator pass G addendum，非三波 finding） |

## 3. 跨制品一致性（Cross-Artifact Consistency）

以下簇把跨 requirements → plan/contracts → tasks 的同一缺陷面合并观察；**不改写任何单行严重度**，归属只指向单一决策 owner。

| 簇 | 成员 | 共同缺陷 | 单一决策 owner |
|----|------|----------|----------------|
| **X-1 全量运行预算与基线语义** | W2-01、W2-12、W3-11；requirements Q2/A14/FR-020 | 「槽位」「全量运行次数」「度量运行」「验证运行」四个概念在三层制品中混用：requirements 把串行验证运行排除在槽预算外且只禁「为度量」的第三次全量，plan/quickstart 对 baseline 槽是否带 `--full` 有三种拼写，tasks 的 GATE-1/Notes 把「post-change 全量运行」数成 1 次而 T061 实跑 2 次 | requirements FR-010/FR-020（预算与运行分类）；plan 同步 spellings |
| **X-2 slow 排除数与档位语义** | W1-08、W1-09、W2-10、W1-10（字段 owner）；contracts TS/EW 侧消费 | `excluded_slow` 的算式在 requirements（FR-024）、clarify（Q2）、data-model（E-1 规则 vs 不变量）各有不同读法，caller 档与 `--full` 档的「应为 0 / 回到全量」未限定；`tier=`/`excluded_slow=` 被逐字消费却无单一 owner | requirements §FR-024（语义与 owner 一并收敛） |
| **X-3 等待截止与 red-first 空转** | W1-21、W1-17、W1-20、W2-05、W3-04 | 30 秒「既有约定」无证据且被实测 5.0 秒反驳；EW-09 守卫与其例外条款互斥；T031 的 `<=` 断言在前置缺省下先绿，无法作为判别面 | requirements §FR-026/§A16（数值与语义 owner）；EW 契约与 T031 随后对齐 |
| **X-4 全称谓断言 vs 机械检查面** | W1-02、W1-17、W3-06 | SC/GATE 的声明面系统性宽于其机械检查面：SC-010 只数装饰器、SC-008 作用域未枚举、GATE-5 只查五个新文件与一个 red-first 文件——三类 containment claim 的判据与检查不同宽 | requirements §SC-010/§SC-008 + tasks GATE-5（按 closed-set-claims 收窄声明或扩展检查） |
| **X-5 条款身份与引用可靠性** | W3-01、W3-02、W2-09 | 契约条款身份在 plan→tasks 链上不可靠：前缀 id 不可解析（W3-01）、tasks 对归属标签自述互斥（W3-02）、plan 对 PC-10 的预算命题引用错位（W2-09）——三者共同使「条款→任务→证据」的机器可判链断开 | plan（重编号 + 引用清扫）；tasks 重发归属 |
| **X-6 机器可消费证据面无单一 owner** | W1-10、W1-13、W1-18、W1-22、W1-25、W2-04、W2-11、W3-03 | 登记册字段、缓存键成分、豁免清单、转换清单分母/分类单位、scan-cache 第二面机制、转换清单 trace 各自被设计或守门逐字消费，但字段名、载体路径或计数单位无单一 owner | plan 阶段一次性收敛（字段/路径/单位各归一处），requirements 只留语义 |
| **X-7 跨阶段实测读数漂移** | W1-21、W1-32、W3-04 | 阶段间继承的读数未统一口径：30s vs 5.0s；20 处/8 文件 vs 20 处/10 文件；A6 只说「不是常量」未决定验收读法 | implement 起点 T003 为唯一读数点（tasks 已声明 MUST 重算），requirements 删除可被误读为常量的旧读数 |

## 4. Checklist 问责（pass H）

- 对象: `checklists/suite-speed-2026-11-10.md`（34 项，全部 `- [ ]`）。
- 处置: **34/34 dispositioned** —— 32 条 `raised-as-finding`（W1-01…W1-34 中的对应项）+ 2 条 `covered-by`（CHK005 → §SC-002/§SC-003；CHK006 → §SC-004），`undispositioned = 0`；10 个 `[Gap]` 项全部升为 finding。
- 可观察计数: `unchecked(0) + unraised(0) + undispositioned(0) = 0` → 不阻断。

## 5. Coverage Summary

| 指标 | 读数 | 证据 |
|------|------|------|
| FR 总数 | 27（FR-001…FR-027） | `requirements.md` |
| SC 总数 | 11（SC-001…SC-011；final 9 + supporting 2） | `requirements.md` §Measurable Outcomes |
| 任务行 | 61（T001…T061） | `tasks.md`；`tasks-gates.txt` |
| 任务→FR/SC trace | 54/61 行有 trace（88.5%）；7 行缺席（T001/T002/T011/T032/T033/T059/T060），其中 T032/T033 = FR-015 的实现行 → FR 级显式 trace 26/27 | W3-03 |
| 契约条款宇宙 | 6 文件 / 68 条款（TS 16 + SM 9 + PC 12 + CA 11 + EW 10 + IC 10） | W2 cross-check ledger |
| 条款机器可判覆盖 | **0/68** —— 六文件全部 `named-unparseable`（前缀 id 形态）；`[fr-uncovered] 0/27` | §1 覆盖核算运行；W3-01 |
| 覆盖核算状态 | **`baseline-missing`（阶段可见问题）**；remedy 两步有序：plan 重编号 → `/speckit.tasks` 重跑冻结或 T002 冻结 | `analyze-coverage-accounting-2026-11-10.txt` |

## 6. Feature Linkage Summary

| 项 | 读数 |
|----|------|
| 绑定 | `FEATURE_ID=086` / `086 Efficient Test Execution (Concurrent by Default)`；`check-prerequisites.sh` 与 requirements 元数据一致；索引行与详情文件均存在（绑定置信度 high） |
| 状态 | `Ready for Review` 保持（不回退）；requirements/clarify 的绑定条件满足 |
| Stage 记录 | 索引行（`features.md` L94）最新 098 记录 = tasks 阶段；详情文件 `Last Updated` = plan/clarify 条目 + tasks 提交的 Related Specifications 行；checklist 阶段无对应登记 → G-01（LOW） |

## 7. Systemic Observations

1. **全称谓 SC 的度量面偏窄**（W1-02、W1-17、W3-06）：三个「为零/全部」判据依赖的检测面都比声明窄；这是 gate 级风险簇，修复应按 `.specify/shared/guidelines/closed-set-claims.md` 让声明与检查同宽。
2. **机器可消费面缺单一 owner**（X-6）：六个 finding 指向同一模式；应在 plan 阶段一次性收敛字段名/载体路径/计数单位，而不是逐条补字。
3. **086 接口稳定性承诺仍停留在意图层**（W1-27、W1-28、W1-29、W3-01）：`前缀兼容`、`条款文本不重开`、`驱动者文档` 无可检查不变量，且 098 自己的契约面正因此落成不可解析形态——构成一条跨阶段的因果链。
4. **跨阶段事实漂移**（W1-21、W1-32、W3-04）：requirements 继承的阶段外读数需要 implement 起点统一重算；A6 的「不是常量」不足以决定验收读法。
5. **预算语汇三层混用**（X-1）：requirements 的分类（槽/度量/验证）清楚，plan→tasks 把三个概念折叠成「全量运行次数」，这是 W2-01/W2-12/W3-11 的共同根因。

## 8. Metrics

- **每波**: W1 = 34（1C/5H/24M/4L）；W2 = 12（0C/0H/7M/5L，检测时 HIGH 1 条已降级）；W3 = 11（0C/2H/6M/3L）；G（integrator）= 1（0/0/0/1）。
- **合并**: 58 条 = CRITICAL 1 / HIGH 7 / MEDIUM 37 / LOW 13；主表 50 + overflow 8；无重复合并（三波读域互斥）。
- **验证**: C/H 送审 8、validated 8、proposed 0、reject 0；W2 波内降级率 1/1（100%），已计入观察：检测侧对「基线锚点」类 finding 的定级偏高，建议后续收紧 propagation-surface 判据。
- **类别分布**（按本报告 Category 列）: A 1 · B 13 · C 11 · D 2 · E 7 · F 23 · G 1。
- **Checklist**: 34/34 disposed；undispositioned 0。
- **覆盖核算**: exit 2；`baseline-missing`；68 条款 0 可解析；FR 0/27 cited。

## 9. Artifacts Untouched 与只读证明

- `requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`quickstart.md`、`contracts/*`（6）、`checklists/*`、`feature-ref.md`、`.specify/features.md`、`.specify/features/086-efficient-test-execution.md` **零修改**（本阶段无 Edit/Write 作用于这些路径）。
- 本阶段唯一写入：本报告、`test-evidence/analyze-coverage-accounting-2026-11-10.txt`、wrap-up 运行时记录（session / exec-quant / feedback；按派发纪律不提交）。
- 覆盖核算按 SKILL §3 **未** `--freeze`；`git status --porcelain -- .specify/specs/098-suite-speed-optimizations/` 在报告落盘前只含既有 worker 证据与新证据文件，spec 制品无 diff。

## 10. Next Actions（不自动修复）

- CRITICAL → 实施前必须处置（W1-01，归属 requirements）。
- HIGH → 实施前处置（W1-02/08/09/17/21 归属 requirements；W3-01 归属 plan 重编号；W3-11 归属 plan 预算 owner + tasks 对齐）。
- MEDIUM/LOW → 不阻断，随对应阶段收敛（§2 各行建议 owner）。
- 修复不由本阶段执行；修复后重跑 `/speckit.analyze`（Round 2）以产生 rerun delta。
