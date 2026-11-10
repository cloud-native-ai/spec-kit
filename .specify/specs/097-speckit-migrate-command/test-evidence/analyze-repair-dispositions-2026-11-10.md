# Analyze Repair Dispositions — 097-speckit-migrate-command

**Stage**: analyze 修复轮（analyze 门失败后的上游修复，一轮为限）· **Date**: 2026-11-10
**Input**: `test-evidence/analyze-merged-2026-11-10.md`（CRITICAL 2 + HIGH 9 = 11 条 C/H；该文件明示验证波未做）
**Authority**: 本特性 spec 全目录 + `.specify/constitution.md` + `.specify/skills/internal/analyze-artifacts/SKILL.md`
**Method**: 逐条重读 finding 锚点原文与 owner 文件（constitution L223–L224、`scripts/python/sync-mirrors.py` `MIRROR_PAIRS`、requirements / contracts / data-model / tasks / checklists），先判 `confirm` / `reject`，再对 confirm 项做最小修复；未静默丢条（11/11 有裁定）。
**Summary**: `confirm=11, reject=0`；`fixed=11, accepted-risk=0`（W3-02 附机制侧残差说明，见 § 残差）。

| ID | 原严重度 | 复核裁定 | 处置 | 文件:行（修复后锚点） | 理由 |
|----|----------|----------|------|------------------------|------|
| W3-01 | CRITICAL | confirm | fixed | `tasks.md:77`（Task State Sigil） | 复核：宪法 L224 逐字要求 `[~]` 携带行内 `<!-- deferred: reason -->`；修复前 sigil 把唯一载体定为 `verification.md` `deferred_tasks=`，按之执行将缺失宪法规定的标记。修复：sigil 改为行内 `<!-- deferred: reason -->` 承载原因（宪法 VII），`deferred_tasks=` 降为不替代行内标记的汇总索引。contracts / requirements 无该载体引用，无需同步。 |
| W3-02 | CRITICAL | confirm | fixed | `tasks.md:39`（DoD-7）、`tasks.md:51`（GATE-4）、`tasks.md:264`（T048）；`plan.md:103`（同步） | 复核：宪法 L223 要求每条 SC 的状态行写入 `verification.log`；修复前三处载体均为 `verification.md`，无法满足宪法字面。修复：三处载体与 plan 目录树注释统一改为 `verification.log`；GATE-4 保留条件集 owner 指针并注明「carrier name per constitution VII」。机制侧残差见 § 残差。 |
| W1-01 | HIGH | confirm | fixed | `requirements.md:134`（FR-018） | 复核：FR-006（:116）干跑 MUST NOT 写入任何文件/数据；FR-018 要求干跑与应用每次都产出回执且落点 `receipts/`——两条 MUST 直接冲突。设计侧 E-3「FR-018 解释记录」已给出确定性解释（干跑回执随输出流、零落盘），但需求层未裁定。修复：FR-018 明示「干跑回执 MUST 以输出流承载、不落盘；应用回执落点固定」——冲突消解于需求层，FR-006 零写入不变。 |
| W1-02 | HIGH | confirm | fixed | `requirements.md:134`（FR-018）、`requirements.md:139`（FR-020） | 复核：SC-004（:175）要求回执载明源/目标版本，SC-006（:177）与 FR-017 需运行状态与续跑标识，但 FR-018 字段清单缺这三类；FR-020 未定义源版本读取来源与回退。修复：FR-018 补「源版本与目标版本、运行状态、续跑标识」；FR-020 补「源版本读 `.specify/source.json`，缺失/不可读记 `unavailable` + 原因，不推断」——与 E-3 source/target/resumedFrom、R-5、EP-005 一致。 |
| W1-03 | HIGH | confirm | fixed | `requirements.md:145`（FR-023） | 复核：SC-001（:172）要求五类维度各自在移除收敛处置时转红；FR-023 原构成清单只有四类（退役条目、旧代状态文件、平铺 internal、旧锚点），缺模板/镜像内容漂移与兼容链接缺失，两清单不自洽。修复：构成清单补「已编辑的模板文件、被删除的镜像脚本文件、缺失或断链的兼容链接」并 REQUIRE 覆盖 SC-001 全部五类维度——与 engine C-8 的声明驱动构造一致。 |
| W1-04 | HIGH | confirm | fixed | `requirements.md:135`（FR-019） | 复核：`clean` 与 `applied` 同为退出 0，FR-019 未规定机器可读 outcome token 或输出格式，SC-003 的结局判定无判定基。设计侧 C-4 已有 `outcome` 键但需求层未授权。修复：FR-019 要求结局以机器可读 token 载明（文本输出与 `--format json` 包络均含），不新增旗标（选项集仍归 C-1）。 |
| W1-05 | HIGH | confirm | fixed | `requirements.md:135`（FR-019） | 复核：FR-014 六值处置到 FR-019 四类结局无聚合规则；部分项已应用而仍有 refuse/blocked 时 `applied` 与 `blocked` 双成立。修复：FR-019 补优先级聚合——存在任一 `refuse`/`blocked` 项或执行期 I/O 失败 → `blocked`（退出 3），否则 `applied`（退出 0）；干跑按计划空/非空取 `clean`/`planned`——与 E-5、C-3 的 blocked 触发行一致。 |
| W1-06 | HIGH | confirm | fixed | `requirements.md:115`（FR-005） | 复核：FR-005 未定义「当前已安装版本」的判定方式，也未钉名 CLI 源与工作区 `.specify/scripts/` 副本并存时的权威。设计侧 C-2 引擎装载点已给出答案但需求层缺授权。修复：FR-005 补「当前已安装版本 = 运行本命令的 CLI 进程所加载的包资源（`get_resource_path()`）；框架源工作区（`skills/external/` 为目录）以自身声明与脚本副本为源（宪法 XI）；客户端模式 MUST NOT 读工作区可能过期的副本」——与 C-2、E-6 一致。 |
| W2-01 | HIGH | confirm | fixed | `data-model.md:121`（E-8 templates-generated 行） | 复核：实读 `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` = **6 对**（templates、skills/external、skills/internal、agents、scripts、shared），故 C-2 的「六个镜像对」正确；E-8 把 skills 写成「一个镜像对」，其 templates-generated 行只列「templates / skills / agents 三个」。修复：E-8 该行改为 templates / skills/external / skills/internal / agents **四个镜像对**，与 mirror-consistency 行的 scripts / shared 两对合计 6，与 owner 一致。C-2 不改。 |
| W2-04 | HIGH | confirm | fixed | `contracts/migrate-cli.md:39`（C-3 补充）、`:66`（C-4 补充）；`data-model.md:102`（E-5 补充） | 复核：`error` 在 E-5/C-3 中被列为 outcome 并给 exit 2，但 C-4 `outcome` 枚举、C-6、T-2 与 plan XIX 均只含四类；json 包络在 error 情形无定义。修复：显式声明 `error` 是输入/前置条件错误的**退出类别、不是 outcome token**——不进入 `outcome` 枚举、不输出计划包络、不产生回执；`outcome` 取值域固定为 `clean`/`planned`/`applied`/`blocked`。T-2 与 plan XIX 原本即为四类，无需改动。 |
| W3-03 | HIGH | confirm | fixed | `tasks.md:33`（DoD-1） | 复核：原 Check 对全文件做 FR 去重计数；追溯表（L334–L358）与 DoD-1 自身行内清单已含全部 25 个 FR，故删除全部任务行引用仍返回 25——绿色检查非证据。修复：Check 改为只统计任务行（`grep -E '^- \[[ xX>~]\] T[0-9]{3} '` 过滤后再取 FR token），实测返回 25；并补「删除任一任务行的 FR 引用必须使计数 < 25」的变异判据（追溯表与 DoD 行文本不参与计数）。 |

## 复核证据（重读记录）

- 宪法 L223–L224（`verification.log`、行内 `<!-- deferred: reason -->`）实读确认；机制侧 `templates/tasks-template.md:121`、`shared/workflow/acceptance-hardening.md:46`、`shared/workflow/feature-integration.md:47` 仍使用 `verification.md`（R5 事实复核成立）。
- `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` 实读 = 6 对（见 W2-01）。
- `requirements.md` 全部锚点（:115/:116/:130/:133/:134/:135/:139/:145/:172/:174/:175/:177）逐条重读；checklists/requirements-quality-2026-11-10.md 的 CHK001/002（:17–18）、CHK010（:29）、CHK011（:30）、CHK014（:33）、CHK025（:53）、CHK026（:54）、CHK032（:63）逐条核对。
- `contracts/migrate-cli.md`（C-3/C-4/C-6）、`contracts/migrate-engine.md`（C-2）、`contracts/migrate-template.md`（T-2）、`data-model.md`（E-3/E-5/E-8）、`tasks.md`（DoD-1/DoD-7/GATE-4/sigil/T048）逐条重读。
- 修复后门禁复跑全绿：`validate-requirements`（0 error/0 warning）、`pre-analyze`（stage=tasks，decision=pass，0 error）、`decomposition`（mode=tasks，decision=proceed）；另跑 `validate-tasks`（0 error/0 warning）。完整读数见 `analyze-repair-gates-2026-11-10.txt`。

## 残差（不静默丢弃）

- **W3-01 / W3-02 机制侧残差（accepted upstream observation）**：本修复按驱动指令把**本特性产物**的载体收敛到宪法字面（行内标记、`verification.log`），未改机制 owner（`templates/tasks-template.md`、`shared/workflow/acceptance-hardening.md`、`shared/workflow/feature-integration.md` 仍用 `verification.md`）。机制侧与宪法字面的收敛（宪法修订或机制修订二选一）超出本特性切片，留待上游处理；本特性内不再稀释。
- **`verification.log` 的版本控制风险（实现阶段注意）**：仓库 `.gitignore` L37 规则 `*.log` 会忽略 `verification.log`（历史教训：022 review F1，提交 `ddc3655` 曾把 `verification.log` 改名为 `verification.md` 以避开忽略）。T048 执行时必须保证该载体受版本控制（例如对该路径加负规则或改用机制层认可的等价载体），否则 SC 状态记录会从版本库中消失。
- **MEDIUM / LOW 31 条**：按 merged 报告保留，不在本轮（C/H 修复轮）处置范围。
