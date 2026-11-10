# Analyze Repair Dispositions r3 — 098-suite-speed-optimizations（2026-11-10）

- **Stage**: analyze round-2 gate FAIL（1 CRITICAL / 0 HIGH）后的自主修复轮 r3（单写者，用户授权；无人值守：修复后直接续跑 analyze）。
- **Input**: `test-evidence/analyze-merged-round2-2026-11-10.md`（§0 verdict + C/H 表 + W1-01 证据边界）、`test-evidence/analyze-findings-round2-W1.md`（W1-01 原文）、`test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt`。
- **Authority**: 本特性 spec 全目录 + `.specify/constitution.md`（§XX v1.19.0）+ `.specify/shared/guidelines/test-execution-efficiency.md`（§「测量的四个锚点」/§「不可采纳的提速手段」）+ `.specify/skills/internal/analyze-artifacts/SKILL.md`（宪法冲突 CRITICAL、不可降级、以调整 spec 而非重解释处置）。
- **Discipline**: 先复核锚点（confirm/reject），再做最小修复；修复沿需求 → 设计 → 契约 → 任务全链同步；只提交本特性产物；不 push。
- **Quadruple（本轮解析）**: `flow_class=execution`；`source=declaration`；`marker=`；`error=-`。
- **结论**: 1/1 **confirm**、0 reject；修复已落盘；门禁复跑见 `analyze-repair-gates-r3-2026-11-10.txt`。

## 0. 处置汇总

| # | ID | 严重度 | 复核 | 修复 | 文件:行 | 一句话理由 |
|---|----|--------|------|------|---------|------------|
| 1 | W1-01 | CRITICAL | confirm | fixed | `requirements.md:28`（Overview）、`:36/:40`（US1）、`:125`（Edge Cases）、`:147`（FR-007）、`:170`（FR-021）、`:205`（SC-004）、`:219`（SC-004 Source）、`:252`（A3）、`:258`（A9）、`:261`（A12）；`plan.md:30/:47/:78/:99/:100/:101`（验收表 / Performance Goals / 宪法 XX 行 / T-001）；`contracts/tier-selection.contract.md:75–84`（C-016）；`quickstart.md:174–189`（S-13）；`tasks.md:215–216`（T055/T056） | SC-004 的 50% 判据由「缺省档 vs 全量基线」（跨选择集）重锚为「缺省档并行 vs **同选择集** `--serial`」，提速不再由 slow 排除兑现；FR-007/FR-021 补「范围裁决 / 不得充当提速来源」，覆盖保持由 SC-006 新增守门测试与两槽位全量背书 |

## 1. W1-01（CRITICAL）复核与修复细节

### 1.1 复核（confirm）

重读 round-2 锚点，逐条成立：

- `requirements.md:205`（原 SC-004）把「缺省档墙钟」与「implement 起点基线（同 runner 缺省并行、**全量选择**）」比较并要求 ≤ 50%——两侧选择集合不同；
- `FR-007`（原 `:147`）的机制正是缺省前置 `not slow` 排除；`FR-021`（原 `:170`）声明「MUST NOT 以 owner 清单中的任何方式兑现任何 SC」，与上述组合构成文本自相矛盾；
- owner（`test-execution-efficiency.md`）§「测量的四个锚点」的 **same selection**（L80：两次运行 MUST 覆盖同一测试集合）与 §「不可采纳的提速手段」的「缩小选择范围：用过滤条件、标记排除…换取数字下降」（L93，任何情形不可采纳）被直接命中；宪法 XX L437–439 原文即「a faster run MUST NOT be bought by shrinking the selection…」。
- finding **成立，不降级**。

### 1.2 裁决路径（用户授权方向 ②；①不可行）

- **选择方向 ②（按档位分别定义目标：缺省档在同选择集内提速 ≥ 50%，由新增覆盖保持守门测试背书）**。
- **方向 ①（"`-m "not slow"` 档 vs 历史同档位"）不可行的证据**: 变更前的树没有 `slow` marker（探针：`slow` 使用数 0），基线树上的 `-m "not slow"` 选择等于全量集合；「历史同档位」读数在语义上不存在。若要在变动前的树上取得**同一选择**基线，只能按事后确定的 slow 成员 node id 去选择后重跑近乎全量的一次基线——与 A9「不新增第三次全量运行（为度量）」及两槽位测量预算冲突，且把基线重取到结果旁边违反 owner「基线 MUST NOT 被重新取一次以匹配新结果」。
- **方向 ② 的锚点实现**: 复用同一棵树、同一 runner 入口、仅执行方式不同的两臂（缺省并行 vs `--serial`；`--serial` 不改变档位语义，FR-009 / C-007），四锚点（same selection / same command / same environment / name-level comparison）全部固定；该两臂本身也是 FR-002 并行正确性判据所要求的同树对照，属「一次执行，一份证据」。
- **提速的归因边界**: 该读数只归因于执行方式与 098 的测试基础设施改动；slow 排除带来的覆盖差异**兑现任何 SC**。

### 1.3 修复落点（与 owner / 宪法逐条对齐）

| Owner 条款 | 修复后的承载 |
|-----------|--------------|
| same selection（L80） | `SC-004` 判据固定为同选择集两臂，且要求两组 `--collect-only -q` 读数证明选择集合相等（`requirements.md:205`、`SC-004 Source:219`、`C-016:75–84`） |
| 标记排除不得换取数字下降（L93） | `SC-004` 明文「提速 MUST NOT 由慢档排除兑现」，排除条数与两档原始墙钟降为范围披露读数；`FR-007:147`、`FR-021:170`、`A3:252` 三处声明「选择差异不得兑现任何提速判据」 |
| 默认运行覆盖的集合由内容而非耗时决定（残余机制层张力） | 机制本身是用户 Input 声明的范围裁决（`A3`），本轮按用户授权的 ② 方向保留；补偿面：排除数枚举披露（FR-007/C-009）、登记册守门 + 收集集合等式（FR-024/SC-006 的新增 `test_suite_tier_contract.py`）、两槽位强制全量（FR-010/SC-005）。**残余风险与重开条件**记录在 `plan.md` T-001 `revision_trigger`：下游把缺省档误当全量 ≥ 2 次，或 closure 出现可归因于缺省档漏跑的失败名 ≥ 1 → 重开并改为缺省全量 |
| 宪法 XX「别以缩小选择买更快的运行」 | 修复后的 SC-004 不可能靠少跑测试达成；宪法未改，owner 文件未改（分析技能禁止以重解释消化 MUST，本轮是调整 spec 判据而非重解释原则） |

### 1.4 同步链（需求 → 计划 → 契约 → 任务 → quickstart）

- **requirements.md**: Overview `:28` 改为「全量覆盖与判据不变 + 缺省档排除是范围裁决 + 效率判据同选择集」；US1 叙事/Why/Independent Test `:36/:40` 把「比全量快」改为「同选择集并行快于串行」；Edge Cases `:125` 增「不同选择之差不是效率证据」；FR-007 `:147`、FR-021 `:170`、A3 `:252` 补范围裁决与不得兑现条款；SC-004 `:205`、Source `:219` 重写；A9 `:258` 明确两臂是定向运行、不构成第三次全量运行；A12 `:261` 限定「不改变**全量档**的测试选择判据」。
- **plan.md**: § Acceptance preservation 表行 2 `:30` 增「speed claim 只在同一选择集内测量」；Performance Goals `:47` 改为同选择集 50%；宪法 Check XX 行 `:78` 改为指向 SC-004 同选择集测量 + SC-006 守门 + C-016（不再重述 owner 清单）；T-001 `:99/:100/:101` 的 pole_b、discriminating_evidence、expected_sacrifice 同步（`expected_sacrifice` 保持校验器要求的 `<SC-NNN> Source <↑>` 闭式）。
- **contracts/tier-selection.contract.md**: C-016 `:75–84` 重写为同选择集判定 + 范围披露读数 + 全量档 110% 非回归保持；条款总数仍 16。
- **tasks.md**: T055 `:215` 改为「范围披露读数，非效率主张」；T056 `:216` 改为同选择集两臂（含两组 `--collect-only` 选择相等证明与全部披露读数），`[green: C-016]` 归属不变。
- **quickstart.md**: S-13 `:174–189` 增加缺省串行臂与两臂选择相等校验，Proves 改为同选择集 50% + 全量档 110%。

## 2. 未处置（明确记录，不静默丢条）

- round-2 的 MEDIUM 17 条 / LOW 18 条均为非阻断项，保持 open，按 owner 收敛（其中 W1-11 测量协议的方差容忍问题与本轮 SC-004 重锚相邻但未被本轮吞并；`checklists/suite-speed-2026-11-10.md` 是 dated 记录，未改）。
- round-1 residue 46 条 deferred 状态不变。
- 本轮只处置 W1-01；不声称「clean rerun」，headline verdict 由续跑的 analyze 重新给出。

## 3. Fast-Fail 声明

- 本轮无「决定型」异常需要上报：全部修复均沿用户在本轮派发中给出的方向 ② 与既有 A3/Q2 裁决展开；未改宪法、未改 owner 文件、未改 086 契约（C-001…C-016 文本未动）。
- 运行中确认的一处计划内约束：`validate-decision-tensions.py` 要求 `expected_sacrifice` 以 `<SC-NNN> Source <↑|↓>` 闭式开头——T-001 的改写保留该前缀。
- 未触碰：`checklists/*`（dated record）、`research.md`、`data-model.md`、`feature-ref.md`（经检索不含旧判据落点）、`.specify/features*`、086 状态；既有脏工作树文件（memory/session、exec-quant、feedback 记录、`checkpoints/`）不提交、不还原。

## 4. 本轮触碰的制品

- 修改：`requirements.md`、`plan.md`、`quickstart.md`、`tasks.md`、`contracts/tier-selection.contract.md`（1 份契约）。
- 新增：`test-evidence/analyze-repair-dispositions-r3-2026-11-10.md`（本文件）、`test-evidence/analyze-repair-gates-r3-2026-11-10.txt`。
- 复跑门禁：`validate-requirements`、`pre-analyze-check --stage requirements|plan|tasks`、`decomposition-check --mode tasks`（必跑）；`validate-decision-tensions`、`validate-tasks`（受本轮编辑直接影响的补充校验）。
