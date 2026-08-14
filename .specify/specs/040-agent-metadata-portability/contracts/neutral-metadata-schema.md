# Contract: Neutral Metadata Schema

契约对象:`agents/` 与 `.specify/agents/{templates,instances}/` 下全部 `*.agent.md` 的 frontmatter。

## C-1 键集封闭性

frontmatter MUST 仅包含 data-model.md §E2 中立键集中的键。出现集合外的键时,渲染前校验 MUST 失败并指明文件与键名;MUST NOT 静默忽略或透传。

## C-2 必填与缺省

- `name`、`description` 为必填;缺失即校验失败。
- 其余键按 §E2 的缺省行为取值;缺省取值 MUST 与渲染产物中的实际输出一致(不得渲染时另行解释)。

## C-3 命名风格

全部键 MUST 为 kebab-case。camelCase 键(历史方言 `maxTurns` 等)出现在任何定义或模板中即测试失败。

## C-4 禁用词表扫描

契约测试 MUST 对以下三个目录做键名扫描并断言命中数为 0(SC-001):

- `agents/`
- `skills/create-agent/templates/`
- `skills/create-team/templates/agents/`

禁用词表:`maxTurns`、`disallowedTools`、`timeoutMins`、`mcpServers`、`permissionMode`、`background`、`isolation`、`tools`(以 `capability-tools` 取代)、`color`(以 `display-color` 取代)、`model`(以 `model-tier` 取代)。

## C-5 边界可判定

元信息提取 MUST 仅依赖 frontmatter 解析,不读取正文;正文 MUST NOT 出现分发/运行参数(轮次、配色、工具白名单)(FR-003)。

## C-6 框架键不外泄

`supervisor`、`capacity-scope`、`role-scope`(团队域作用域)、`project`(project-custom 标记)为框架装配键,MUST NOT 出现在任何渲染产物中(任何工具)。

## C-7 占位符隔离

frontmatter 中出现 `{{...}}` 占位符的定义 MUST NOT 进入渲染输入;渲染输入仅来自 `.specify/agents/{templates,instances}`(FR-026 的第一道闸)。

## C-8 发现机制兼容

仅凭 frontmatter 的 `name`/`description` MUST 能枚举全部可用 agent(FR-004);既有 glob 发现路径不得要求读取正文。
