# Research — 099-speckit-seal（Phase 0 实测记录）

**Feature**: 099 Speckit Seal（`/speckit.seal`） | **Date**: 2026-11-10 | **Plan**: [plan.md](plan.md)
**输入**: `requirements.md`（28 FR / 9 SC）+ clarify 裁定 + 访谈裁定 D-074-R1/R2/R3（台账在运行时会话目录，见 R-21）+ `.specify/constitution.md`

本页只记录**实测事实与既有先例**（含文件:行号锚点）；设计裁决在 `plan.md`（决策张力）与
`contracts/`（条款）中给出。全部读数来自 2026-11-10 在本工作树上的只读命令与检索。

## R-01 状态值域的真实分布（owner 与 carrier 不是同一文件）

- `shared/workflow/acceptance-hardening.md` § Feature Status（:35–64）只声明 `Blocked` 及其四条转移；
  它是 § Feature Status 的 owner，但**不列举**其余值。
- `templates/feature-details-template.md:63–79` § Canonical Status State Machine 是**声明式 carrier**：六值
  状态清单（:56–61）、九行转移表（`Ready for Review → Completed` 在 :79）、`[FEATURE_STATUS]` 词汇行（:118）。
- `templates/feature-index-template.md:20`：六值封闭词汇表。
- `shared/workflow/feature-integration.md:27–38` § Status State Machine：按命令登记转移的协议表
  （requirements→Draft、plan→Planned、tasks 维持、implement→Implemented、checklist/review→Ready for Review）。
- `skills/internal/manage-features/SKILL.md:129`：六值词汇行。
- `scripts/python/non-disposable-check.py:121`（`COMPLETION_CLAIMS`）、`:124`（`Relocated`）、`:487–503`
  （状态×裁决封闭表，12 格）；未知状态拼写在 `:696–701` 以 exit 2 拒绝。owner 页
  `shared/definitions/non-disposable-definitions.md:196` 列 7 值域（含 `Relocated`）。
- `scripts/python/closure-acceptance-check.py:258`（`CLAIMED_IMPLEMENTED`）、`:1505–1508`（audit 家族）。
- `README` 之外的其它字面消费面（每处一行）：`templates/commands/{review,checklist,implement,plan}.md`、
  `skills/internal/{create-checklist,create-plan,implement-feature,summarize-project}/…`、
  `docs/reference/commands/{feature,review}.md`、`.specify/constitution.md:541–544`。

## R-02 值域被测试钉死（必须在同一次变更内同步）

| 测试 | 位置 | 钉住内容 |
|---|---|---|
| `tests/contract/test_status_gate_owner.py` | :396–428 | 模板转移表状态集**恰等于**六值集合 |
| `tests/contract/test_acceptance_state_machine.py` | :90–99 / :491–517 | `FEATURE_STATUS_VALUES` 六值；manage-features 词汇行恰六值 |
| `tests/contract/test_acceptance_schema_ownership.py` | :279–318 | 域从 `[FEATURE_STATUS]` 行派生；全部投影必须落在域内 |

新增 `Sealed` 而不更新这三处，测试即红——这正是 FR-001「漂移守卫」的现成载体。

## R-03 `Ready for Review → Completed` 只被声明、从未被执行

`grep -rn "→ Completed"` 在 `scripts/ skills/ shared/ templates/ tests/` 只有一个带箭头的命中：
`skills/internal/summarize-project/references/consistency-rules.md:65`（生命周期映射的**叙述**）；
`templates/feature-details-template.md:79` 以表格行 `| Ready for Review | Completed |` 声明同一转移（无箭头）。
没有任何命令、技能或引擎**执行**该转移；因此 FR-003 的「关闭该出口」是声明面（表格行）+ 叙述面收敛，
不需要删除任何代码路径。

## R-04 现有归档/退休流程不查询任何状态

| 流程 | 决策点 | 查状态？ |
|---|---|---|
| `/speckit.sanitize` 物料 lane | `skills/internal/sanitize-materials/SKILL.md:209–233`（确认后 apply，archive-not-delete） | 否 |
| `/speckit.docs` lane | `templates/commands/docs.md:32,48` → `skills/external/create-docs/SKILL.md:104–115` | 否 |
| `/speckit.feature` 归档指针（`Relocated`） | 归档-not-delete 策略见 `skills/internal/manage-features/SKILL.md:59–74`；`Relocated` 字面只出现在 `shared/definitions/non-disposable-definitions.md` 与 `.specify/features.md` 的活行 | 只记账，不判定 |
| `/speckit.goal migrate-archive` | `skills/internal/manage-goal/SKILL.md:173–183` | 否（且对象是 goal/team 树） |

结论：FR-023 的归档准入是**真正的新代码**，只能在 seal 引擎内实现一次，其余入口按指针查询。

## R-05 命令模板先例（薄入口 + 技能委派）

- `templates/commands/sanitize.md`（54 行）是最薄形态：frontmatter 仅 `description` / `short-description`；
  `## Delegation` 只指向一个 internal 技能（:20–26）；`## Wrap-up` 为编译嵌入（7 步）。
- `templates/commands/clarify.md:39–48`：`**Load and follow** .specify/skills/internal/…/SKILL.md`，明说
  「The skill owns the entire workflow」。
- per-tool 副本：`src/specify_cli/__init__.py:802–819` 定义六工具目录；本仓现存在树四份
  （`.claude/commands`、`.github/prompts`、`.opencode/command`、`.qoder/commands`），由
  `scripts/python/regen-command-copies.py` 生成；`--check` 零漂移，目标在 `.specify/scripts/python/` 镜像内运行被拒（:23–32）。

## R-06 internal 技能先例与装配面

- frontmatter 四键：`name` / `description` / `classification: internal` / `skill_id`（值指向**运行时镜像路径**，
  例 `skills/internal/clarify-artifact/SKILL.md:1–6`）。
- `## Wrap-up` 是由 `probe-utils.py --action compile-embeds` 生成的嵌入块；probe 注册在
  `shared/definitions/probe-definitions.md`（现有 `skill-clarify-artifact-wrapup` :182、`skill-sanitize-materials-wrapup` :203）。
- 命令/技能名册被测试冻结：`tests/contract/test_migration_distribution.py:98–128,266–285`（29 commands / 56 skills）、
  `tests/contract/test_flow_class_ledger.py:280–330`（台账 85 行 = 29 + 56）、
  `tests/contract/test_humanize_command_surface.py:1881–1892`。新命令与新技能必须同步这些基线。
- 流程类别台账 owner：`shared/definitions/flow-class-definitions.md` § 逐流程台账（`/speckit.*` 与 `skill:*` 各一行）。

## R-07 引擎脚本先例（stdlib-only + 三值退出码）

- `scripts/python/closure-acceptance-check.py`：`_sig_guard` 预解析（:1792–1822）、`configure_parser` 追加
  `side-effects:` / `exit-codes:` 标签（`script_interface_cli.py:315–345`）、`--version` 由
  `script_interface_cli.py:81–85` 从 `pyproject.toml` 解析；退出码 `0 accept / 1 block / 2 input`
  （:81–83）；`--json` 输出 `json.dumps(..., indent=2, sort_keys=True)`（:1750–1766）。
- 仓库根解析先例（:275–281）：`Path(__file__).resolve().parents[2]`，若名字为 `.specify` 再上一级；
  `regen-command-copies.py:23–32` 则是拒绝在镜像内运行的反例。seal 引擎取「解析自身路径的**字面**
  `.specify` 组件」做法，不用「向上找最近 `.specify`」启发式（Dogfooding § 2.1 路径陷阱）。
- 子进程复用先例：`non-disposable-check.py:104–107` 以子进程调用闭包引擎并逐字复用其裁决，MUST NOT 重算。

## R-08 镜像与生成面（基线漂移实测为 0）

`scripts/python/sync-mirrors.py:93–100`：

```
templates → .specify/templates（排除 commands）; skills/external → .specify/skills（排除 site/internal）;
skills/internal → .specify/skills/internal; agents → .specify/agents/templates;
scripts → .specify/scripts（strict extras）; shared → .specify/shared
```

`python3 scripts/python/sync-mirrors.py --check` → exit 0；`python3 scripts/python/regen-command-copies.py --check`
→ exit 0（2026-11-10 实测，见 `test-evidence/plan-stage-checks.txt`）。本特性涉及的全部镜像对当前**零漂移**，
因此「无新增漂移」判据可从零基线起算。

## R-09 闭包引擎的输入语法（seal 只读消费，不复算）

- SC 定义行：`^- \*\*SC-(\d{3})\*\*:`；同一行必须**恰有一个** `**Path**` 标记且位于行尾，
  取值来自 `shared/declarations/facts/success-criterion-path-values.yaml`（`final` / `supporting`）。
- `verification.md` 状态行是**纯 key=value**（非表）：`SC-NNN_status=pass|fail|partial|blocked|deferred|unknown`；
  ladder 五键、smoke 四键、`RS-NNN_joint_acceptance`。
- 任务行：`^\s*- \[(.)\]`（`closure-acceptance-check.py:298`）；行 ID：`^- \[.\] (T\d{3})`（:325）。
- 裁决负载含 `verdict` / `reasons` / `final_path` 七键 / `claimed_status`；seal 的回执 MUST 逐字复制该负载。
- 实测（2026-11-10）：对父 074 运行闭包引擎 → **exit 2**，stderr 为
  `.../requirements.md:392 SC-001 carries 0 **Path** markers; exactly one is required (AS-01)`。
  这正是 FR-027(a) 的输入缺陷，MUST NOT 读作 accept。

## R-10 074 树的实测状态（本日读数）

| 目录 | `^- \[ \]` | `^- \[X\]` | `review.md` / `code-review.md` | `verification.md` |
|---|---|---|---|---|
| 父 `074-goal-team-sdd-unification` | **57** | 0 | 无 / 无 | 有（41 行，聚合指针集，8 条判据全 `pass`，每行指向分片测量） |
| `074a-authorized-routing` | 0 | **32** | 有（P0=0 / P1=3 / P2=3）/ 有（blocking=0） | 有（6 条判据 `pass`） |
| `074b-nested-governance` | 0 | **26** | 有（**P0=1** / P1=3 / P2=2）/ 有（blocking=0） | 有（2 条判据 `pass`） |

父目录另有 plan / data-model / research / quickstart / feature-ref / 5 contracts / 1 checklist / 3 test-evidence；
无 `notes/`、无 `checkpoints/`。父 `requirements.md:5` 的 `**Status**: Draft` 是**规格文档状态行**，不是特性状态，
`state-drift` 判定只读注册表行与特性详情（与闭包引擎 `resolve_claimed_status` 同源）。

## R-11 拆分顺序的声明位置与形态

- 074 的声明顺序只存在于 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（:128–140）：
  `proposed_slices` 是**有序 bullet 列表**（`074a-authorized-routing` 在前、`074b-nested-governance` 在后，
  含 FR 范围与确认行 `confirmed-user`）；父 `requirements.md` 与其 `tasks.md` 均不含拆分节。
- 069 先例：`.specify/specs/069-execution-expression-sdd/notes/decomposition-gate.md`（表行顺序即声明顺序）。
- **不存在拆分记录解析器**（`grep -rn "拆分记录" scripts/ skills/` 无代码命中）——seal 引擎必须自带解析；
  回退依据为字母后缀字典序，且 MUST 写入所用依据（FR-011）。

## R-12 共享字符串冲突（074 实测，确认 FR-027(b)(c)）

- 父 `requirements.md:439–451` STR 表：`STR-004="sdd"`、`STR-005="direct"`、`STR-006="adjudicate"`、
  `STR-007="completed"`、`STR-008="blocked"`、`STR-009="failed"`、`STR-010="## Nested SDD Runs"`、`STR-011="seats"`。
- 074b 本地表（`074b-nested-governance/requirements.md:229–237`）：`STR-004="completed"`、`STR-005="blocked"`、
  `STR-006="failed"`、`STR-007="## Nested SDD Runs"`；其 § Parent Mapping 明写 `STR-004→STR-007`、
  `STR-005→STR-008`、`STR-006→STR-009`、`STR-007→STR-010`。→ **同号不同义成立**（父与 074b 的 004–006 指向不同字面量）。
- 出厂文档 `skills/internal/create-team/SKILL.md:99,101` 以 `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]` 引用
  outcome 字面量；在合并后父级语义下会解析为 `sdd`/`direct`/`adjudicate` → 必须重指向（`STR-007/008/009`）或改逐字字面量。
- 074a 本地表与父级 001–010 同义（`STR-010↔父 STR-011`），不产生同号不同义。

## R-13 `**Path**` 标记：三份 requirements 均为 0 个

父、074a、074b 的 requirements.md 都不含 `**Path**` 标记（闭包引擎 exit 2 的直接原因）。回合必须为每条 SC
记录显式取值；若走默认，只允许更严格的 `final`，且必须记录（clarify 裁定）。

## R-14 既有编号机制的边界（不可整体复用）

- `scripts/python/renumber-utils.py`：只修**重号**，**不压缩空洞、不复用空号**（docstring 道义），
  且 `SPEC_DIR_RE=^\d{3}-` 不识别 `074a-` 形态。
- `scripts/python/validate-requirements.py`：`id-contiguous` 要求主 ID 家族**无洞**；`ref-resolvable` 校验
  `[[STR-NNN]]` 双向可解析；字母后缀是格式违规而不是可归一化形态。
- `skills/external/sdd-loop-driver/scripts/overlap-check.py:33`、`check-prerequisites.sh` 的精确前缀分支同样
  把字母分片目录排除在外（074b review P0 F1 即此缺陷）。
- 结论：合并的编号重排必须由 seal 引擎**自行派生**（父映射复用 + 分片独有按合并顺序追加），不能借用
  renumber-utils 的「不压缩」语义；合并产物用 `validate-requirements.py` / `validate-tasks.py` 做**事后校验**。

## R-15 57 行拆前记录的处置词汇

- `shared/definitions/non-disposable-definitions.md`：处置集封闭四值 `archive` / `supersede` / `correct` / `exempt`
  （:274–322）；`supersede` 要求**原文保留 + superseded 标记 + 指向新承载**（:415–444），记录行字段
  `superseded{path,line}` / `superseded_by{path,line}` / `disposition` / `evidence` / `guard_status`。
- 适用值是 `supersede`：`archive` 会移动文件（违反「不移动 spec 目录」）、`exempt` 给永久历史强加到期日、
  `correct` 面向活文本。
- 检出引擎是**零写盘**（模块 docstring `scripts/python/non-disposable-check.py:2`）：没有处置写入器——处置记录由 `merge-manifest.json` 承载，不新建台账。

## R-16 确定性序列化先例

`scripts/python/evidence-utils.py:199–201`（`json.dumps(..., separators=(",", ":"), sort_keys=True, ensure_ascii=False)` + sha256）；
`non-disposable-check.py:2068`、`status-digest.py:1183`（`indent=2, sort_keys=True`）。manifest 自摘要采用
`skills/external/sdd-loop-driver/references/decomposition-model.md:68–70` 的「排序键紧凑 JSON、剔除易变键」形态。

## R-17 特性注册与 074 现状

- `.specify/features.md` 现 89 个特性行（文件 122 行）；末号为 094；099 无行、`.specify/features/099-*.md` 不存在（bound-but-unregistered）。
- 074 行（:84）与 `.specify/features/074-goal-team-sdd-unification.md:7` 状态均为 `Ready for Review`，
  两载体一致（`state-drift` 不触发）；074 详情的 `## Latest Review` 记录 074b review 时写有
  「P0 F1 … 驱动记录为显式豁免（P0 waiver）」——**驱动者记录，不是用户裁定**（FR-006/FR-027(d)）。
- 最近 detail 文体（090/094）未逐字沿用 `feature-details-template.md` 的章节骨架；本阶段新建 099 详情按
  同一近邻文体落地，字段与状态语义以模板为准（见 plan § Disclosed rulings）。

## R-18 词汇协议的既有入口

`shared/workflow/glossary.md`：新术语经 `glossary-utils.py --action detect-conflict` → `--action add`
（`origin=auto, status=proposed`）进入 `.specify/glossary.md`；spec 内不建第二份术语表。
`validate-requirements.py:276–338` 已实现 `[[STR-NNN]]` 的双向解析与 `Consumed by` 互证——词汇对齐的
「解析到唯一注册表」可复用该判定口径。

## R-19 CLI 面：新增命令模板不需要改 `src/specify_cli/`

`generate_commands()` 运行时 glob `templates/commands/*.md`（`src/specify_cli/__init__.py:1599–1633`），
`specify check` 的 `command_templates` 能力动态计算；仅 `specify init` 的 “Next steps” 帮助文本硬编码了命令
名册（:3318–3326），属可选准确性修改。打包按整个 `templates` 树（`pyproject.toml:42–45`）。
写后必须运行 `regen-command-copies.py`（写模式）与 `sync-mirrors.py --write`。

## R-20 阶段门脚本

- `pre-analyze-check.py --stage plan`：只扫正式产物（requirements / plan / tasks / data-model / quickstart /
  research / feature-ref + `contracts/` + `checklists/`）；`notes/`、`review.md`、`verification.md` 在其视野外
  （模块 docstring `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:10`）——因此合并引擎对 `verification.md` / `review.md` 的写入必须由引擎自身守卫（FR-019）。
- `decomposition-check.py --mode plan`：plan 门（FR ≤ 120 / 任务 ≤ 160）已实测 `proceed`（fr_count=28）。
- `validate-decision-tensions.py`：六字段行文法校验器（`- **decision**: …`、`  - pole_a:` 两缩进子行等）。

## R-21 访谈裁定 D-074-R1/R2/R3 的台账位置

台账 `.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md` 位于主仓运行时会话目录，
**不在本分支的受版本控制文件集内**（本工作树 `git ls-files` 计数为 0）。三条裁定的可携带形式是
`requirements.md` § Clarifications 与状态脊 U0/拆分记录；本页按原意转述，不把台账路径当作可解析引用：

- D-074-R1：074a/074b 回合到 074 的含义 = 分片同名输出件合并回写父级（编号重排/语义对齐/词汇表对齐），
  所有输出件走同一流程，最终确认在 `/speckit.seal`。
- D-074-R2：新增 `/speckit.seal`；`sealed` 是 `Ready for Review` 之后的最终态，sealed 后方可归档。
- D-074-R3：074 回合推迟到 seal 开发完成后，以 074 作为真实测试与验证用例。

## 未决项 → 由计划裁决

| # | 事实带来的开放问题 | 落点 |
|---|---|---|
| Q1 | 散文类输出件的「合并」如何做到确定性又不拖入模型语义 | plan § Decision Tensions T-001 + `contracts/merge-back` C-021 |
| Q2 | `Sealed` 与遗留 `Completed` 的叙述收敛范围（含宪法生命周期段） | T-002 + `contracts/status-sealed` C-027 |
| Q3 | 编号追加与 renumber-utils 道义冲突的边界 | T-003 + `contracts/merge-back` C-015 |
| Q4 | 归档准入的唯一实现点与四个 lane 的接线 | T-004 + `contracts/status-sealed` C-030 |
| Q5 | 074 回合允许以阻断结束的验收口径 | T-005 + `contracts/records-and-boundaries` C-043 |
| Q6 | 合并写面与「不移动/不删除/不归档」的边界 | T-006 + `contracts/seal-engine` C-008 / C-009 |
