# Quickstart: /speckit.docs 三段式调协编排

**Requirement**: `048-docs-reconcile` → Feature 037 Docs Command
**Date**: 2026-09-01

六个走查场景,覆盖 3 个用户故事与 6 条成功判据。场景 2/3/4 是 dogfooding 的测量源(本仓 `docs/` 上实跑)。

---

## 场景 1 — Bootstrap:无声明的新项目

**前置**: 项目无 `docs/` 结构,无 `.specify/docs/target-structure.md`。

```text
/speckit.docs
```

**期望**:
1. 盘点项目形态与现有内容 → 设计目标结构声明(信息不足则提问 ≤3 问)。
2. 声明与干跑计划**合并为一次确认**呈现(不是两道门)。
3. 确认后:声明写入 `.specify/docs/target-structure.md`(受管块);Bootstrap 骨架按 `.specify/skills/create-docs/SKILL.md` § Desired-State Baseline 收敛(行动者必须打开 owner,此处不复制其枚举)。
4. 审计日志追加;残差报告按技能分列。

**核验**: 声明含全部 T-4 必填字段;`静态基线引用` 为引用行且无基线枚举复制(T-5);站点层未被脚手架(移交 `create-pages`)。

**欠指定变体(FR-003)**: 构造一个无法从仓库事实判断目标读者或项目专属扩展的项目。命令 MUST 在生成声明前一次性提出 1–3 个必要问题；答案到达前不得写入声明、不得以猜测补齐字段。核验提问数 `1 <= n <= 3` 且未出现未证实的项目事实。

---

## 场景 2 — 稳态:零变更空间的重复运行(SC-001 防抖)

**前置**: 声明已确认;空间自上次运行未变。

```text
/speckit.docs
```

**期望**: 复用既定目标,**不重新设计**;全维度在容忍带内 → 收敛动作数 **0**;审计日志**照写**"零收敛/无净变化";残差报告如实报告无净变化。

**核验**: `.specify/docs/audit/` 新增一条;`git status` 对 `docs/` 零改动;声明文件 `最后确认` 未被无故刷新。

**实态脱节变体(FR-015)**: 在已确认声明之后加入一个会实质改变文档信息架构的新子系统及其证据。下一次运行 MUST 将“重设计目标声明”作为既有 R4 干跑计划中的待确认提议，说明检测依据；确认前声明字节不变，确认后才更新受管块并继续收敛。

---

## 场景 3 — 双类漂移:结构 + 内容(SC-002 路由正确率)

**前置**: 文档 A 放错分类目录(结构漂移);文档 B 已正确就位但含失效路径断言(内容漂移,有 `docs-utils.py --action validate` 或已核实的过时证据)。

```text
/speckit.docs
```

**期望**:
1. 动作清单同时含 A 的结构动作(owning=`create-docs`)与 B 的内容动作(owning=`improve-docs`,携带证据)。
2. A 属搬迁类 → 经干跑计划逐项确认;B 属安全本地写 → 自动执行。
3. 搬迁后经 `docs-utils.py --action fix-links` 机械修链,不逐处手改。
4. 残差报告分列两个技能的执行结果。

**核验**: 每个动作的技能归属可回查;无证据指瑕的其他文档零改动(SC-004)。

---

## 场景 4 — 带参叠加:调协 + 写作一次交付(SC-003)

**前置**: 空间已收敛;声明已确认。

```text
/speckit.docs "创建一个描述登录流程的文档"
```

**期望**: **两个结果同时产出** ——(a) 调协侧如实报告零收敛;(b) 写作动作先回答“写什么/放哪里”:内容计划列出目标读者、当前语境、用户输入、仓库证据与边界；落位计划先搜索同主题 owner,不存在时才创建唯一 canonical 文档并更新所属索引。若新路径应进入 Agent 项目知识入口,同次运行调度 `/speckit.instructions` 刷新 `.specify/instructions.md` Documentation Map。

**核验**: 用户输入未取代基线调协(FR-009);同主题近重复新增数为 0;新文档可从目录/根索引及刷新后的 Agent Documentation Map 定位;不直接编辑兼容 instruction aliases;`docs-utils.py --action validate` 零新增违规。

---

## 场景 5 — 隐含结构变更:回写目标

**前置**: 声明已确认。

```text
/speckit.docs "把 reference/ 拆成 CLI 参考和技能参考两部分"
```

**期望**: 变更作为**待确认项**进入干跑计划;确认后 (a) 结构动作执行,(b) 变更回写声明受管块(只替换标记之间内容,块外字节保持),`最后确认` 更新。未确认则持久目标不变(FR-010)。

**核验**: 声明标记成对且块外人工加注(若有)未被改动。

---

## 场景 6 — 大规模内容扇出:告知与中止(FR-008 / A-6 / A-7)

**前置**: 空间内 20+ 份就位文档各有已证据化的内容问题。

```text
/speckit.docs
```

**期望**:
1. 分发**开始前**告知计划分发的文档数(不设上限、无隐式截断)。
2. 用户可在扇出启动前中止;每份文档之间亦为可中止点。
3. 若中途中止:已完成的逐文档结果**保留**(不回滚);未开始项标 `pending` 进入残差报告。
4. 后续运行从 pending 继续收敛。

**核验**: 无任何"仅处理前 N 份"的静默截断;中止不产生半写文档。

---

## 回归核验清单(实现后必跑)

```bash
# 契约与镜像
python3 scripts/python/regen-command-copies.py --check          # exit 0,4 份工具副本一致
python3 scripts/python/sync-mirrors.py --check                  # 见下方基线说明:本特性触及的镜像对须无新增漂移

# 门控零增量(本特性关键守卫)
python3 scripts/python/scan-confirmation-gates.py --json        # total 仍为 23,violations 0

# 相关测试套件
pytest tests/contract/test_docs_command_template.py \
       tests/contract/test_docs_skill_pair.py \
       tests/contract/test_docs_utils_cli.py \
       tests/contract/test_confirmation_gates_sweep.py \
       tests/contract/test_feedback_command_classification.py -q

# 文档空间自检
python3 scripts/python/docs-utils.py --action validate --root .  # 零新增违规
```

**实跑核验(2026-09-01 规划期)**: 上述四条引擎命令均已实跑。`regen-command-copies.py --check`、`scan-confirmation-gates.py --json`、`docs-utils.py --action validate` 三条 **exit 0**;`pytest` 五文件路径全部解析,收集到 75 个测试。

**`sync-mirrors.py --check` 基线说明(重要)**: 该命令**当前 exit 2**,原因是一处**与本特性无关的既有漂移** —— `git-fleet` 技能在 `skills/` 存在但 `.specify/skills/` 缺 6 个镜像文件(`SKILL.md` + 4 份 references + `scripts/git_fleet.py`),由上游提交 `fe70862e "add a git-fleet skill"` 引入;另有 14 条 `.migration-backups/` 仅存于镜像侧的 `note` 提示(非失败项)。实测 `templates/`(20 文件)、`agents/`、`scripts/`(101 文件)、`shared/`(32 文件)四对均为 `ok`。

因此本特性的镜像门禁是**"所触及镜像对无新增漂移"**,而非笼统的 exit 0:实现后须确认 `templates/docs-target-structure-template.md`、`skills/create-docs/SKILL.md`、`skills/improve-docs/SKILL.md` 三者的镜像均报 `ok`,且 `git-fleet` 之外无新 `MISS`/`DIFF` 行。修复 `git-fleet` 漂移**不属本特性范围**(应由其自身归属方处理)。

> 全量套件存在长期既有失败批次(基线),实现阶段 MUST 先冻结基线再比对,区分"基线失败"与"本次引入的回归"。
