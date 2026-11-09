# Contract: 站点记忆文件格式与脱敏规则(需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill
**消费方**: site-memory.py 引擎(schema 校验真源)、tests/contract/test_browser_site_memory.py、references/site-memory.md(指针)

## 1. 通用规则

- F-1: 全部文件 UTF-8 JSON / JSONL;时间戳 ISO-8601 UTC(`YYYY-MM-DDTHH:MM:SSZ`);键名 snake_case。
- F-2: 四个状态字面量恰为 `[[STR-001]]` / `[[STR-002]]` / `[[STR-003]]` / `[[STR-004]]`;记忆根目录名恰为 `[[STR-005]]`。
- F-3: 新增可选字段向后兼容;既有字段禁改名、禁改语义。

## 2. state.json(schema)

必填:`site`(string,host[:port])、`state`(四态之一)、`updated_at`、`history`(array,≥1)。
history 条目必填:`from`(null 或四态)、`to`、`at`、`evidence`(string,非空)。

## 3. records/*.jsonl(schema)

信封必填:`seq`(int,从 1 连续)、`at`、`kind` ∈ {`dom`, `network`}、`ok`(bool)。
- `kind=dom`:另必填 `action`(click/fill/read/navigate/…)、`target`;`input`、`result` 可空。
- `kind=network`:另必填 `method`、`url`、`response_shape`(含 `status` int + `json_keys` array);`headers`、`body_template` 可空但出现即受脱敏规则约束。
- `ok=false`:另必填 `error`(string)。

## 4. 脱敏规则(写入时强制,FR-004)

- S-1: 敏感头集合(大小写不敏感):`cookie`、`authorization`、`x-csrf-token`、`x-xsrf-token`、任何含 `token`/`signature`/`secret` 的头名。其值 MUST 为占位符 `<header-name:source>`,如 `<cookie:aliyun>`。
- S-2: body/params 中的动态字段(令牌、签名、requestId 等)值 MUST 为 `<resolve:page-var:<名>|cookie:<名>|prev-request:<步骤号>.<字段>>` 解析来源占位符。
- S-3: 原值侦测(程序优先,引擎内确定性判定):值命中以下任一即拒绝写入——(a) 非占位符且长度 ≥ 16 的高熵串出现在敏感头/动态字段位;(b) `Bearer ` 前缀;(c) `Cookie:` 串拼接形态(`k=v; k=v`)。侦测规则宁严勿宽:误拒由 agent 改写为占位符解决。
- S-4: 响应体不落盘原文,只落 `response_shape`(status + 顶层 JSON 键集合);响应体内的业务数据不持久化。

## 5. recipe.json(schema)

必填:`task`、`distilled_from`(存在的 records 文件相对路径)、`distilled_at`、`steps`(array,≥1)。
steps 条目必填:`n`(int,从 1 连续)、`type` ∈ {`request`, `page`}。
- `type=request`:另必填 `method`、`url`、`expect`(含 `status` int、`json_keys` array);`params_template`、`dynamic_fields` 可空。
- `type=page`:另必填 `reason`(string,非空)、`action`。
- 验证期对照规则:`expect.status` 精确相等;`expect.json_keys` 为子集匹配(实际响应顶层键 ⊇ 声明集合)即判定该步通过。

## 6. validation/*.json(schema)

必填:`run_id`(UTC compact `YYYYMMDDTHHMMSSZ`)、`task`、`verdict` ∈ {`pass`, `fail`}、`steps_total`、`steps_passed`、`failures`(array)、`at`。
- `verdict=fail` 时 `failures` ≥ 1,条目含 `step`、`expected`、`actual`。
- `steps_passed ≤ steps_total`;`verdict=pass` 当且仅当 `steps_passed == steps_total` 且 `failures` 为空。

## 7. 目录命名

- host 小写;显式端口保留(`host:8080`);默认端口(80/443)省略;IPv6 以 `[...]` 包裹;目录名不含 scheme、路径、查询串。
