# Contract: /speckit.sanitize 命令模板结构(需求 045 / Feature 047)

**Requirement → Feature**: `045-sanitize-command` → Feature 047 Framework Material Hygiene  
**消费方**: templates/commands/sanitize.md(源)、4 份工具副本(regen 传播)、tests/contract/test_sanitize_template.py、probe-definitions.md

## 1. 模板身份与分类

- C-1 源模板 `templates/commands/sanitize.md`,frontmatter 与既有复杂命令一致(script 指向 `scripts/python/sanitize-utils.py` 的调用形态);经 regen-command-copies.py 生成 4 副本:`.claude/commands/speckit.sanitize.md`、`.github/prompts/speckit.sanitize.prompt.md`、`.opencode/command/speckit.sanitize.md`、`.qoder/commands/speckit.sanitize.md`。
- C-2 属**复杂命令**:模板含标准 `## Feedback` 步骤(引用 shared/workflow/feedback-step.md)与 `## Documentation` 步骤(引用 docs-step.md);`tests/contract/test_feedback_command_classification.py` 的复杂命令计数 17 → 18。
- C-3 probe-definitions.md Objects 表新增两行(4 列格式 `object_id | class_id | unit | lifecycle_point`):
  - `| speckit-sanitize-wrapup | command-wrapup | /speckit.sanitize | wrapup |`
  - `| gate-sanitize-destructive-cleanup | command-gate | /speckit.sanitize | gate-sanitize-destructive-cleanup |`

## 2. 执行流(模板正文骨架)

- C-4 **Preflight**:探测 python3 与引擎脚本可执行;缺失则给出 actionable 提示(引擎三态探测惯例)。
- C-5 **Collect**:调用 `sanitize-utils.py --action collect`;向用户呈现台账摘要 + 语义候选数(摘要优先,不贴原始证据全文)。
- C-6 **Judge**:agent 仅对 collect 输出的 semanticCandidates 作过期/冗余判定,判定依据限于候选携带的证据包;判定结果写临时文件后经 `--action record --file` 并入台账。证据不足 → 不判定(计入摘要)。
- C-7 **Present**:呈现发现报告(分类/严重度/证据引用/处置建议含可逆性标注);delegate 项以指向既有命令的建议呈现(/speckit.docs、/speckit.instructions、sync-mirrors),不在本命令内执行其处置。
- C-8 **Confirm(破坏性前置门控)**:destructive 项(delete/archive)归并为一份清理计划,单次批量向用户确认;门控后挂单行指针:
  `> Gate probe: gate-sanitize-destructive-cleanup — after the user decision, record firing evidence per confirmation-gates.md §门控观察协议 (non-blocking).`
  指针措辞不得命中 scan-confirmation-gates.py 的阻塞模式。
- C-9 **Apply**:用户放行后——agent 先完成可逆修复(repair 项内容修改),将计划 `confirmed` 置 true,调用 `--action apply --plan`;引擎执行 delete/archive 与状态更新;向用户呈现三要素执行报告(执行内容/变更工件/修改途径)。用户否决 → 仅保留 pending 发现并报告,零删除零移动。
- C-10 **Wrap-up**:标准 Feedback 步骤 + Documentation 步骤;门控触发且用户决定后按门控观察协议记录观察事实(`--lifecycle-point gate-sanitize-destructive-cleanup`,正文含 `confirm-gate` 标记,非阻塞)。

## 3. 红线(模板必须显式声明)

- C-11 任何删除/移动不得发生在用户确认清理计划之前(FR-008/SC-003)。
- C-12 不评估、不修改、不报告用户源代码/产品脚本/测试用例;发现目标限于框架自有资料(FR-006)。
- C-13 检查阶段(collect/record)不修改任何被检材料本体(FR-001/SC-002)。
- C-14 执行中途失败如实报告失败点、原因与中间产物(FR-009)。

## 4. 传播与登记义务

- C-15 实现批次必须完成:regen-command-copies.py 传播 4 副本;sync-mirrors.py `--check` exit 0(引擎 strict 镜像 + probe-definitions 镜像);docs/reference/commands/sanitize.md 用户文档(命名与既有 23 个命令文档一致);`.specify/memory/tools/sanitize-utils.py.md` Tool 记录(Tool Reuse 纪律);044 门控基线 baseline.json 的 total +1 同步(新保留门控)。
- C-16 AGENTS.md Documentation Map 无需新增行(Command Reference 整目录单行已覆盖 docs/reference/commands/)。

## 5. 契约测试锚点

- `test_sanitize_template.py` 断言:模板含 C-4..C-10 各阶段锚文本;红线 C-11..C-14 显式存在;门控指针行存在且措辞不命中扫描器阻塞模式;`## Feedback` 步骤存在(分类测试联动);4 副本与源一致(regen 幂等)。
