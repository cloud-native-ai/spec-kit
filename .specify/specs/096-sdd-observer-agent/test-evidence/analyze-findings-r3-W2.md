# Analyze Findings — Round 3 / Worker W2（plan 与设计产物）

- **Stage**: analyze（第三轮，修复后重过门；并发波 N=2）
- **Feature**: 096-sdd-observer-agent
- **Date**: 2026-11-10
- **Mode**: 对产物严格只读；未做任何修复（本文件是唯一写入）
- **Read domain（文件级互斥）**: `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`research.md`、`contracts/{journal-engine,journal-format,observer-lifecycle,observer-role,observer-verification}.contract.md`
- **Authority consumed**: `.specify/constitution.md`（v1.19.0，22 原则 I–XXII）；`analyze-artifacts` SKILL.md + `references/detection-and-severity.md`
- **Deterministic verdict consumed (pass I)**: `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` → `status: ok`，5 records，六类标签均 0（含 `dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped`），exit 0。按技能规则消费该判定，不再对其语义复评。
- **Run anomaly line**: 未发现异常（no run anomaly, no in-passing repair；本轮唯一写入即本报告）

## 本 lane 的边界（显式移交，均在本 worker 读域之外）

- `account-clause-coverage.py` 的 clause/FR 覆盖记账（读 `requirements.md`）→ W1 lane；本 lane 未运行，门报告须并入其判定。
- Checklist 通道 H（未勾选 `[Gap]` 项的可核查 disposition）→ W1 lane（`checklists/*.md` 不在读域）。
- `tasks.md` 的任务覆盖 / 反向映射 → W3 lane。
- Feature 注册表 index/detail 漂移（`.specify/features.md`、`.specify/features/096.md`）→ registry lane。
- 与 round-1/round-2 findings 的重跑增量与残项处置（residue）→ driver 合并阶段；往轮 findings 文件不在本 worker 读域。

## Findings（13 项：0 CRITICAL / 1 HIGH / 3 MEDIUM / 9 LOW）

| ID | Severity | 锚点 | 一句话事实 | 建议归属 |
|----|----------|------|------------|----------|
| W2-01 | HIGH | `contracts/journal-engine.contract.md` §C-09（L54–55）、§C-07（L41–43）；`data-model.md` V-16（L160） | `check`（仅声明 `--spec-dir` / `--repo` 两个输入）被 C-09 要求校验 V-16，但 V-16 是“外来/过期执行不得 append”的追加时拒绝规则、C-07 已把它归给 `append`；`check` 未被声明任何执行身份或状态脊输入，因此该条款按原文不可执行。 | journal-engine 合同 C-09（把 V-16 移出 `check` 的规则集，或为其声明可校验的输入与语义） |
| W2-02 | MEDIUM | `data-model.md` E-6 `line-start` 行（L82）、E-10（L141）；`research.md` R-07（L56）；`plan.md` L220；`contracts/journal-engine.contract.md` C-04 | E-6 把状态脊 U0 块声明为 `line-start` 的主载体，但引擎的封闭载体清单（E-10 / C-04）与 R-07“只解析两条窄状态脊 prose 语法”的解析面都不含 U0 块语法，故声明式投影产不出这条 `min_persistent: 1` 行。 | data-model E-6/E-10 + research R-07（把 U0 语法补入封闭解析面，或改正载体列） |
| W2-03 | MEDIUM | `contracts/observer-lifecycle.contract.md` C-04（标题 L23、正文 L25–41）；`data-model.md` E-9（L121–137）；`feature-ref.md` 第 9 行（L30） | 同一份八键观察者记录块在 lifecycle C-04 与 data-model E-9 各定义一次，而 C-04 一边自称“key and shape owner”、一边把形状所有权让给 `SKILL.md` § SDD Observer，导致该块没有唯一声明所有者、也无从防止与未来 SKILL.md 文本漂移。 | lifecycle C-04 / data-model E-9（择一为 owner，另一处改为引用；修正 C-04 标题） |
| W2-04 | MEDIUM | `data-model.md` E-3 States（L36）、E-9 state 行（L127）；`contracts/observer-lifecycle.contract.md` C-04 state 行（L31） | E-3 称执行状态 `started → settled | failed` 会“记录在状态脊观察者记录节”，但 E-9/C-04 的 `state` 值域是 `started|failed|disabled|closed`，`settled` 没有可记录取值。 | data-model E-3/E-9（把执行态映射到脊记录值域，或明确声明两套状态模型） |
| W2-05 | LOW | `quickstart.md` L3（对照 S-0…S-7，L5–102）；`plan.md` L31、L236 | `quickstart.md` 首句写“Seven walk-through scenarios”，实际列出八个（S-0…S-7），而 plan.md 两处均计为 8。 | quickstart.md 首句（改为 eight） |
| W2-06 | LOW | `quickstart.md` S-3（L59）；`contracts/journal-engine.contract.md` C-09 | Quickstart S-3 说 `check` 对“`data-model.md` V-1…V-13 中每条规则”报 `file:line`，而 C-09 声明的规则集是 V-1…V-13 加 V-16…V-17，quickstart 少报了两条规则。 | quickstart S-3（改为引用 C-09 的规则集而非枚举子集） |
| W2-07 | LOW | `data-model.md` V-12（L156）；`contracts/journal-format.contract.md` C-12（L71–73） | Journal-format C-12 把段落、列表与围栏代码块都判为 finding，而 `check` 被要求实现的 V-12 只点名“叙述性段落”，列表/围栏块的处理未被规定。 | data-model V-12（把范围对齐到 C-12） |
| W2-08 | LOW | `feature-ref.md` L57（FR-001 行）；`contracts/observer-role.contract.md` C-04（L23–27） | Role C-04（承载 SC-004 强制原文的「不评价、不建议、不推断」禁止条款）自身引用 FR-001，但 FR→Contract map 的 FR-001 行只列 role C-01…C-03 与 verification C-08，漏掉 C-04。 | feature-ref FR→Contract map |
| W2-09 | LOW | `plan.md` L277（§ Risks）；`feature-ref.md` L87（SC-003）、L91（SC-007） | Plan 风险表把“无 journal 收线”的缓解证据写成“SC-001 的 failure-path criterion”，但 feature-ref 的 SC 映射给 SC-001 的是覆盖夹具度量，failure path 属 SC-003/SC-007。 | plan § Risks |
| W2-10 | LOW | `plan.md` L43（Constitution Check 第 II 行） | Constitution 第 II 行证据引用“§ Feature Integration”，但 plan.md 无此章节，门证据指向不存在的锚点（注册表职责实际由 R-10、WP-4、feature-ref 第 18 行承载）。 | plan（补章节或改引用） |
| W2-11 | LOW | `plan.md` L56（Constitution Check 第 XV 行）；`quickstart.md`（全文） | Constitution 第 XV 行证据称 quickstart“在首次使用时定义了 journal / observer / gap”，但 quickstart.md 对这三个词没有任何定义句。 | plan 第 XV 行，或 quickstart（首次出现处各加一句定义） |
| W2-12 | LOW | `data-model.md` E-8（L114–118）、V-17（L161）；`contracts/journal-engine.contract.md` C-08 | E-8 规定“无任何条目时”gap 窗口起点取脊记录节的 `started_at`，但 C-08 与 V-17 只在“存在上一条目的 `observed_at`”时才触发 gap，故该无条目分支永不生效，两处对首次执行是否产生 gap 的语义不一致。 | data-model E-8 / engine C-08（单点声明首次 append 的 gap 语义） |
| W2-13 | LOW | `feature-ref.md` 第 1–19 行（第 4 行与 L42 的生成器句）；`plan.md` § Mirror Obligations 第 2 行（L175） | feature-ref 的 19 行“file-level inventory”把 agent、engine、skill 的镜像各自列为独立行，却漏掉 plan.md § Mirror Obligations 第 2 行要求“必须同样落地”的 `.specify/shared/declarations/facts/journal-format.yaml` 镜像。 | feature-ref delivered-path inventory（补镜像行） |

## 系统性观察

1. **`check` 的规则集与输入面缺少单一所有者**：W2-01、W2-06、W2-07、W2-12 分别从规则分配、子集枚举、规则范围、边缘触发四个方向指向同一处——engine C-09 / format C-12 / data-model V 规则之间的对应关系应在一处收敛，其余处引用。
2. **两处重复枚举需要收敛**：W2-03（脊记录节八键）与 W2-04（执行态 vs 脊 state 值域）都属“同一信息面在合同与 data-model 各写一份”，与 plan 第 XIV 原则“单一所有者、其余引用”的自评存在张力；本轮不判为宪法冲突（设计期声明可解释），但实现前应收敛。
3. **宪法对齐**：plan 的 Constitution Check 恰好覆盖 `.specify/constitution.md` v1.19.0 的全部 22 个 `### <numeral>. <name>` 标题、顺序一致；本 lane 未派生出 CRITICAL 级宪法冲突。仅第 II、XV 两行的证据事实不支持（W2-09/W2-10/W2-11 为同类，均为 LOW）。

## 指标与后续

- **Severity counts**: CRITICAL 0 · HIGH 1 · MEDIUM 3 · LOW 9（propagation surface：LOW 均为叙述/追溯面，按规则封顶；HIGH/‌MEDIUM 均传播到 tasks/implement 的合同测试与夹具设计）。
- **Validation duty**: W2-01（HIGH）在并入门报告前必须经独立 fresh-context 只读校验波（confirm / reject / downgrade + 两个证据边界字段）；本 worker 是检测方，未执行该校验波。
- **Zero-finding floor**: 本 lane 非零 findings，故不适用。
- **Rerun delta**: 待 driver 合并时对照 round-1/round-2 findings 计算；本 lane 未读往轮 findings（读域限制）。
- **Remediation**: 不在本技能/本 worker 范围；上述“建议归属”仅指向应修改的拥有者，未应用任何编辑。
