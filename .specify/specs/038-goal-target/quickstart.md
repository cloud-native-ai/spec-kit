# Quickstart: 038-goal-target 端到端走查

验证「授权 → 指派 → 归属 → 总结」闭环的最小路径。所有命令示例由 `contracts/` 三份契约逐条 pin(实现尚未落盘,示例按契约文法书写;实施阶段 MUST 重跑本走查并回写结果)。

## 前置

- 一个已归档 goal:`.specify/goal/demo-goal/goal.md`(`status: active`,含 objective 与 ≥1 条判据)。
- 一个绑定该 goal 的团队:`.specify/teams/demo-team/team.md` frontmatter `goal_slug: demo-goal`。

## 1. 授权 Target(US1 / targets-engine.contract)

```bash
# 添加 3 条成果形 Target
python3 scripts/python/goal-utils.py targets demo-goal --add "日志组件拆分完成"
python3 scripts/python/goal-utils.py targets demo-goal --add "指标采集链路独立可部署"
python3 scripts/python/goal-utils.py targets demo-goal --add "告警规则全量迁移"

# 查看(机器可解析)
python3 scripts/python/goal-utils.py targets demo-goal --list
# 期望:T-001\topen\t日志组件拆分完成(三行,ID 单调)
```

验证点:
- `goal.md` 出现引擎渲染的 [[STR-001]] 节(表格式,§D3 文法);`## History` 各追加一行 `target T-00x added`。
- 步骤形候选(如 "首先拆分日志组件,然后迁移告警")→ 退出码 2,信息指明改写方向(GD-2,SC-003)。
- 复述判据的候选 → 退出码 2(FR-004)。
- 放弃一条:`targets demo-goal --set dropped --id T-003` → 条目保留在节内携带终态;再 `--add` 得到 T-004(不复用 T-003)。

## 2. run 指派(US2 / run-target-assignment.contract)

```text
/speckit.team run demo-team --target T-001
```

验证点(preview → confirm → execute):
- 确认门禁披露行:`本次 Target: T-001 — 日志组件拆分完成(open)`。
- 执行后 `runs/<ts>-report.md` 含 `**Target 指派**: T-001(日志组件拆分完成)`;新台账条目携带 `"target_ref": "T-001"`(SC-001)。

非法路径(SC-004,各应 preview 停止、零执行痕迹):
- `--target T-999` → 悬空引用,提议 `/speckit.goal targets --add`。
- `--target T-003`(dropped)→ 报出终态并停止;复核二分——属实则结束,证据不符则 `targets demo-goal --set open --id T-003` 后重新发起。
- `--target other-goal.T-001` → 跨 goal 拒绝。

回归基线(SC-002):
- `/speckit.team run demo-team`(不带参数)→ 与引入前逐字节等价的报告与 summary 状态行。

## 3. 归属与总结(US3 / target-ref-ledger.contract)

run 产生台账条目后触发总结刷新,检查 `.specify/goal/demo-goal/summary/`:

- 表单含 `targets:` 块:`T-001` 的 `attributed_items` / `completed_items` 计数正确;`coverage` 按 authored 终态计。
- 无 `target_ref` 的存量条目归属 goal 整体(`unattributed_to_target` 计数)。
- 判据轴与切片轴**分列**呈现;全文无 "targets done ⇒ achieved" 推导(SC-005)。
- 构造不一致:全部 T-001 归属条目 `completed` 而 authored 仍 `open` → 报告列出"待批准完成",两侧不自动翻转(FR-015)。

## 4. 里程碑吸收(US4, P3)

```bash
python3 scripts/python/goal-utils.py targets demo-goal --set done --id T-001
```

再次刷新总结:
- 里程碑组同时含判据投影行(`source` 指向 goal.md 判据)与 Target 来源行(`source: goal-target:demo-goal/goal.md#T-001`),带区分标记(FR-016)。
- 判据为空的 goal:里程碑组由 Target 来源条目填充并声明来源。

## 5. 零迁移回归

- 从未添加过 Target 的既有 goal:`view` / `validate` / `status` / `criteria` 输出与引入前一致;`validate` 退出码 0(US1 场景 5)。
- 存量内联团队(无 goal 定义):一切照旧;尝试 `--target` → 报"依赖 goal 定义"并指向 `migrate`(US2 场景 5)。

---

## 走查记录(实施回写)

### 2026-08-12 — US1 首跑(T011,临时沙箱 `mktemp -d`,`--repo-root` 指向沙箱)

**§1 授权**:全部通过——
- 3 条 `--add` 依次发放 T-001/T-002/T-003,`--list` 输出机器可解析三行(ID 单调);
- `goal.md` 出现引擎渲染表格节(表头 `| ID | Target | Status |`,行正则逐字匹配),`## History` 各追加 `target T-00x added: <语句>`;
- 步骤形候选「首先拆分日志组件，然后迁移告警」→ 退出码 2,GD-2 信息指明改写为子成果方向(SC-003);
- 判据复述候选「日志链路端到端延迟低于 500ms。」→ 退出码 2,指明判据权威互斥(FR-004);
- `--set dropped --id T-003` 后条目保留携带终态;再 `--add` 发放 T-004(T-003 不复用)。

**§5 零迁移(US1 侧)**:通过——无 Target goal `validate` 退出码 0、`list`/`status` 输出不含 Targets 痕迹;`status --set achieved` 后文件仍无 `## Targets` 节(SC-002 引擎侧;字节稳定性另由 `tests/unit/test_goal_utils.py::test_create_output_is_byte_stable_without_targets` pin)。

### 2026-08-12 — US4 首跑(T027)

**§4 里程碑吸收**:经 `tests/integration/test_target_milestones.py` 5 例全绿取证——done Target 以 `source: goal-target:<slug>/goal.md#T-001` 与 `status: achieved` 进入既有 milestones 组;判据投影行语义原样(036 FR-013,source 仍为定义 relpath);open/dropped 不入组;判据为空 + done Target 存在 → 里程碑组由 Target 来源填充并声明来源(material_gaps);DDL 无 goal-target 硬编码——区分仅靠既有 `source` 列(D7)。`git status skills/summarize-project/` 空:引擎与 DDL 零改动。

### 2026-08-12 — T032 全走查复跑(refresh-verify,单沙箱 `mktemp -d` 端到端)

- **§1 授权**:add×2 + `--set done` 复跑通过(身份单调、History D6 记法、表格文法)。
- **§2 run 指派**:preview 五判定对真实引擎复跑——`T-001→ok`、`T-999→dangling`、`T-002(done)→target-terminal`、`other-goal.T-001→cross-goal`、非法形→input-error,100% 拦截。
- **§3 归属与总结**:真实生成器折叠——`coverage: 1/2 done`、`unattributed_to_target: 1`、`invalid_refs: 0`,切片轴与判据轴分列。
- **§4 里程碑吸收**:milestones 组同时含判据投影行(source=定义 relpath)与 Target 来源行(`goal-target:demo-goal/goal.md#T-002`),来源标记区分。
- **§5 零迁移**:无 Target goal `validate` 退出码 0,输出无 Targets 痕迹。

**SC 取证来源对照**:SC-001 → 上述 §2/§3 归属与拦截取证 + `tests/integration/test_run_target_validation.py` / `test_target_fold.py`;SC-002 → `test_create_output_is_byte_stable_without_targets` + `test_targetless_goal_form_is_byte_identical`(diff 为空语义)+ §5 复跑;SC-003 → GD-2/GD-3 切片尺度样例 100% 拒绝(契约测试 + §1 复跑);SC-004 → preview 停止零痕迹(只读断言 `test_preview_check_is_read_only`);SC-005 → 负向扫描测试 + `axis_note` 分列;SC-006(概念锚)→ 词汇表与文档均链接 Target Decomposition 不复述。

### 2026-08-12 — US2 首跑(T016)

**§2 run 指派**:preview 五步校验的确定性核心已实现为引擎函数 `goal-utils.py::preview_target_check`(引擎 parse 为唯一事实源),判定经 `tests/integration/test_run_target_validation.py` 11 例全绿取证:合法 open 引用通过(携带绑定元数据)、悬空 T-999 判悬空并提议 `targets --add`、done/dropped 判终态并附复核二分指引(含 `--set open` 重开路径与无旁路声明)、限定形 `other-goal.T-001` 判跨 goal、goal 终态拒指派、无定义团队指向 `migrate`;全程只读(goal/team 文件字节不变)。门禁披露行与 report `**Target 指派**` 字段格式经 `tests/contract/test_run_target_assignment.py` pin 于 `templates/commands/team.md` 并扇出至 4 份 per-tool 副本。无 `--target` 路径声明逐字节等价(SC-002)。

### 2026-08-12 — US3 首跑(T024)

**§3 归属与总结**:对真实生成器端到端(subprocess + YAML 表单)经 `tests/integration/test_target_fold.py` 7 例全绿取证——合法 `target_ref` 行归入对应 Target(attributed/completed 计数正确,coverage 按 authored 计 `1/3 done`);无字段行计入 `unattributed_to_target`;非法引用(T-999、限定形)降级入整体 + `invalid_refs` 计数 + material_gaps 显式声明(未臆造 Target,FR-014);无 `## Targets` 节的 goal 表单无 `targets:` 键且既有输出不变(SC-002);`pending_approval` 两侧触发(open/全完成、done/未完成,FR-015);负向扫描无 "targets done ⇒ achieved" 推导(SC-005,axis_note 分列声明)。既有折叠族(`test_goal_aggregation` / `test_summary_four_patterns` / `test_team_item_ledger` / `test_goal_definition_sourcing` / `test_goal_progress_state`)合计 59 例零回归。台账契约 LC-11 叠加落盘(IL-1…IL-5/LC-1…LC-10 条款未动)。
