# Contract: site-memory.py 引擎 CLI(需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill
**消费方**: browser-utils SKILL.md(路由段)、tests/contract/test_browser_site_memory.py、三个 Tier 的执行路径

## 1. CLI 形态

- 引擎为 `${SKILL_HOME}/scripts/site-memory.py`(源 `skills/browser-utils/scripts/site-memory.py`,镜像 `.specify/skills/browser-utils/scripts/site-memory.py`),stdlib-only,Python ≥ 3.8。
- 参数风格沿用框架引擎惯例:`--action <name>`(必填)+ `--format text|json`(引擎输出恒 JSON 信封;`--format text` 仅影响摘要行)。
- 通用退出码:`0` 成功;`1` 校验/迁移拒绝(JSON `{"ok": false, "error": ...}`);`2` 参数/schema 错误。
- `--action` 取值恰为 7 个:`init` / `get-state` / `append-record` / `validate-records` / `write-recipe` / `record-validation` / `transition`。未知 action 退出 2。

## 2. 动作语义

### init
- 输入:`--url <url>`(或显式 `--site <host:port>`)+ `--skill-home <path>`(定位 site/ 根)。
- 行为:从 URL 确定性导出目录名(小写 host;默认端口省略;显式端口保留);幂等创建 `site/<host>/` 与 `state.json`(初始态 exploration,history 记 `evidence: "init"`);已存在则不改动,输出现状。
- 输出:`{"ok": true, "site": "g.aliyun-inc.com", "dir": ".../site/g.aliyun-inc.com", "state": "exploration", "created": true}`

### get-state
- 输入:`--site <host:port>` + `--skill-home`。
- 行为:零写入;`state.json` 缺失/损坏 → 输出 `{"ok": true, "site": ..., "state": null, "memory": "absent"}`(调用方按无记忆站点处理,Edge Case 对应)。
- 输出:state.json 全量 + `recipe_present` / `records` 任务清单摘要。

### append-record
- 输入:`--site`、`--task <slug>`、`--record <json-line>`(或 `--record-file <path>`)+ `--skill-home`。
- 行为:schema 校验(必备字段按 kind);**脱敏强制**——headers/body 中敏感字段值必须匹配占位符语法 `<...>`,检出疑似凭证原值(高熵串/已知头形态)即退出 1 并指出字段路径;`seq` 必须接续文件现有序号;校验通过追加一行。
- 输出:`{"ok": true, "seq": 9, "file": "records/task-1.jsonl"}`

### validate-records
- 输入:`--site`、`--task`。
- 行为:零写入;判定记录完整性(exploration → optimization 迁移前置):必备字段齐全、`ok=false` 记录带 `error`、seq 连续、≥1 条 network 记录。
- 输出:`{"ok": true, "complete": true, "missing": [], "counts": {"dom": 12, "network": 5, "failed": 1}}`

### write-recipe
- 输入:`--site`、`--file <recipe.json>`。
- 行为:schema 校验(request 步骤含 method/url/expect;page 步骤含 reason;动态字段经 dynamic_fields 声明);校验通过写 `recipe.json`(覆盖式,蒸馏迭代);`distilled_from` 指向的 records 文件必须存在。
- 输出:`{"ok": true, "steps": 5, "page_steps": 1}`

### record-validation
- 输入:`--site`、`--file <evidence.json>`。
- 行为:schema 校验(verdict ∈ pass/fail;fail 时 failures 非空);写 `validation/<run-id>.json`;随后**自动迁移**:verdict=pass 且当前 validation → sealed;verdict=fail → optimization(回退);状态不符时迁移拒绝(退出 1)但证据仍落盘。
- 输出:`{"ok": true, "verdict": "pass", "state": "sealed"}`

### transition
- 输入:`--site`、`--to <state>`、`--evidence <描述或文件路径>`。
- 行为:按 data-model §2 迁移表做确定性前置判定(records 完整性 / recipe 存在且合法 / 验证证据 verdict);非法迁移拒绝并输出合法目标集合;回退类迁移(→optimization)始终允许但 `--evidence` 必填;成功写 history。
- 输出:`{"ok": true, "from": "exploration", "to": "optimization"}`

## 3. 不变量

- C-1: 状态文件的写入口径唯一——全部经引擎;agent 永不手工编辑 `state.json`。
- C-2: 迁移判定零自然语言裁量:全部前置条件为文件存在性 + schema + verdict 的确定性检查(FR-009 / SC-004)。
- C-3: 脱敏在写入侧强制(append-record 拒绝原值),而非事后扫描清理(FR-004)。
- C-4: 引擎对 Tier 无感知:只读写 JSON 文件,三 Tier 调用方式相同(agent 各自以 Bash/等价能力调用 CLI)。
- C-5: 任一校验拒绝都不留下半成品写操作(先校验、后落盘、单文件原子写:临时文件 + rename)。
