# Data Model: 浏览器站点记忆(需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill

全部实体为 agent 中立的 JSON/JSONL 文件(FR-009),落在 `site/<host:port>/` 记忆目录(FR-003)。字段名为稳定契约,新增可选字段向后兼容,禁止重命名既有字段。

## 1. Site Memory(站点记忆目录)

以 domain(host:port)为 key 的目录,技能 `site/` 子目录下,如 `site/g.aliyun-inc.com/`(默认 443/https 省略端口时按 host 记)。首次操作某站点时由引擎 `init` 创建。

| 路径 | 内容 | 写入者 |
|------|------|--------|
| `state.json` | Site State(状态机文件) | 仅引擎 |
| `records/<task-slug>.jsonl` | Operation Record 流(探索期留痕,追加写) | 引擎(校验后追加) |
| `recipe.json` | Request Recipe(优化期蒸馏产物) | 引擎(schema 校验后落盘) |
| `validation/<run-id>.json` | Validation Evidence(验证证据) | 引擎 |
| `notes.md` | 可选自由文本(站点特性、坑位提示) | agent 直接写 |

校验规则:
- `<host:port>` 目录名 MUST 可由 URL 确定性导出(小写 host、显式端口保留、默认端口省略);引擎 `init --url <url>` 负责导出,agent 不手工拼目录名。
- 目录被删除或 `state.json` 损坏 → 视为无记忆站点,`init` 幂等重建为 exploration(Edge Case: 损坏不阻塞任务)。

## 2. Site State(站点状态机)

`state.json`:

```json
{
  "site": "g.aliyun-inc.com",
  "state": "exploration",
  "updated_at": "2026-08-24T02:30:00Z",
  "history": [
    { "from": null, "to": "exploration", "at": "2026-08-23T10:00:00Z", "evidence": "init" },
    { "from": "exploration", "to": "optimization", "at": "2026-08-24T02:00:00Z", "evidence": "records/task-1.jsonl completeness=ok" }
  ]
}
```

- `state` ∈ { `[[STR-001]]`, `[[STR-002]]`, `[[STR-003]]`, `[[STR-004]]` }(exploration / optimization / validation / sealed)。
- `history` 每条 MUST 带 `evidence`(判定依据引用:记录文件、验证证据文件路径或 "init"),支撑 SC-004。

### 状态迁移(全部由引擎确定性判定,FR-009)

| 迁移 | 前置判定(程序优先) | 失败行为 |
|------|--------------------|----------|
| → exploration | `init` 幂等 | — |
| exploration → optimization | 目标 task 的 records 完整性校验通过(必备字段齐全;失败/重试步骤在场) | 拒绝迁移,输出缺失项清单 |
| optimization → validation | `recipe.json` 存在且 schema 校验通过 | 拒绝迁移,输出 schema 错误 |
| validation → sealed | 存在 verdict=pass 的 Validation Evidence | 拒绝迁移 |
| validation → optimization(回退) | verdict=fail 的 Validation Evidence 落盘 | 自动(验证失败即回退,FR-005/FR-008) |
| sealed → optimization(回退) | 固化执行失败,agent 调用 `transition --to optimization --evidence <漂移证据>` | 允许,提示重新蒸馏(FR-010) |
| 其它(如 exploration → validation 跳态) | — | 拒绝并输出合法迁移表 |

## 3. Operation Record(操作记录)

`records/<task-slug>.jsonl`,一行一条,时间序追加。两类记录共用信封:

```json
{ "seq": 7, "at": "2026-08-23T10:01:22Z", "kind": "dom", "ok": true, "action": "click", "target": "button#query", "input": null, "result": "navigated to list" }
{ "seq": 8, "at": "2026-08-23T10:01:23Z", "kind": "network", "ok": true, "method": "POST", "url": "https://g.aliyun-inc.com/console_api/api.json?ApiName=ListBaseline", "headers": { "content-type": "application/json", "cookie": "<cookie:aliyun>" }, "body_template": { "pageNum": 1, "pageSize": 20 }, "response_shape": { "status": 200, "json_keys": ["data", "total"] } }
```

校验规则:
- 必备字段:`seq, at, kind, ok`;`kind=dom` 另需 `action, target`;`kind=network` 另需 `method, url, response_shape`。
- `ok=false` 记录 MUST 带 `error` 字段(失败与重试留痕,FR-004)。
- **脱敏强制(写入时,FR-004/Q2)**: headers 中 `cookie`/`authorization`/含 `token` 的头,值 MUST 为占位符形态 `<header-name:source>`;body_template 中的令牌/签名字段值 MUST 为 `<resolve:page-var|cookie|prev-request:名称>` 解析来源占位符;引擎 `append-record` 检出疑似原值(与常见凭证形态正则匹配)即拒绝写入并指出字段。

## 4. Request Recipe(请求级步骤集)

`recipe.json`(FR-007):

```json
{
  "task": "task-1",
  "distilled_from": "records/task-1.jsonl",
  "distilled_at": "2026-08-24T02:10:00Z",
  "steps": [
    { "n": 1, "type": "request", "method": "POST", "url": "https://g.aliyun-inc.com/console_api/api.json?ApiName=ListBaseline",
      "params_template": { "pageNum": 1, "pageSize": 20 },
      "dynamic_fields": { "x-csrf-token": "<resolve:page-var:csrfToken>" },
      "expect": { "status": 200, "json_keys": ["data"] } },
    { "n": 2, "type": "page", "reason": "验证码步骤无法请求化", "action": "manual-captcha" }
  ]
}
```

校验规则:
- `steps` 有序;`type=request` 步骤 MUST 含 `method, url, expect`;动态字段 MUST 经 `dynamic_fields` 声明解析来源。
- `type=page` 步骤 MUST 含 `reason`(显式标注无法请求化,FR-007)。
- `expect` 为验证期对照基线(状态码 + 响应 JSON 关键键集合;精确匹配规则见 contracts/site-memory-formats.md)。

## 5. Validation Evidence(验证证据)

`validation/<run-id>.json`(FR-008):

```json
{
  "run_id": "20260824T023000Z",
  "task": "task-1",
  "verdict": "pass",
  "steps_total": 5, "steps_passed": 5,
  "failures": [],
  "at": "2026-08-24T02:30:00Z"
}
```

- `verdict` ∈ {`pass`, `fail`};fail 时 `failures` 非空(步骤号 + 期望/实际差异)。
- 引擎 `record-validation` 落盘证据后按 verdict 自动迁移状态(pass → sealed,fail → optimization),迁移拒绝手工绕过。

## 实体关系

```text
Site Memory 1—1 Site State(state.json)
Site Memory 1—n Operation Record(records/*.jsonl, 按 task 分组)
Site Memory 1—n Request Recipe(recipe.json 按 task 迭代覆盖, distilled_from 指回记录)
Site Memory 1—n Validation Evidence(validation/*.json, 追加累积)
Request Recipe n—1 Operation Record 集(蒸馏来源)
Validation Evidence n—1 Request Recipe(验证对象)
```
