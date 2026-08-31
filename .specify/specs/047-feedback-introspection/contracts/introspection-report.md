# Contract: Introspection Report 文件 Schema(047)

自省报告的**字节级格式契约**。逻辑实体定义见 `data-model.md`;引擎校验行为见 `engine-cli.md`。契约条目以 `C-N` 编号,供契约测试逐条断言。

## 文件位置与命名

- **C-1**: 报告文件 MUST 位于 `<workspace>/.specify/memory/feedback/introspection/` 子目录,文件名 `<report-id>.md`;`report-id` 形如 `introspection-<YYYYmmddTHHMMSSZ>`(与条目/包同一时间戳风格,冲突时追加 `-N` 序号)。
- **C-2**: 报告 MUST NOT 位于 feedback 存储根目录(`reindex` 对根目录 `*.md` glob 重建条目索引,报告落根会被误当条目)。
- **C-3**: 报告为 UTF-8 Markdown,结构 = YAML frontmatter + 固定章节正文;`yaml.safe_dump` 写出时 MUST `allow_unicode=True`(中文不转义)。

## Frontmatter

- **C-4**: frontmatter 字段恰好为:`id`(string)、`created`(ISO-8601 UTC)、`status`(`draft|confirmed|superseded`)、`scope_filter`(string)、`scope_entries`(list[string])、 `supersedes`(string 或 null)、`confirmed_at`(ISO-8601 或 null)。
- **C-5**: `id` MUST 等于文件名去 `.md`;`scope_entries` 内 id MUST 无重复。

## 正文章节(固定顺序)

- **C-6**: 正文 MUST 依次含:`# Introspection Report: <report-id>`、`## Findings`、`## Excluded`(可为"无")。
- **C-7**: `## Findings` 下每个问题为 `### F-<nn>: <问题陈述>`(nn 从 01 起连续编号),其下含且仅含以下子字段行(粗体键):
  - `**根因**: …`
  - `**证据锚点**: …`(≥1 条,形如 `path:line` 或单元锚点;多条以 `;` 分隔)
  - `**成员条目**: <entry-id>(<核验结论>), …` — 每条成员条目附核验结论,结论 ∈ `成立|部分成立|已过时|不成立`
  - `**分流决定**: local-sink(<channel>)` 或 `upstream-bound(package-attachment)`
  - `**优化方案**: …`
  - `**用户覆盖**: …`(可选;记录原决定 → 覆盖后决定)
  - `**建议处置**: <entry-id>:<processed|ignored>, …`(可选;confirm 批量处置的机读载体,见 engine-cli C-5)
- **C-8**: `## Excluded` 下列出显式排除的条目,每行 `- <entry-id> — <排除理由>`。
- **C-9**: 五要素(问题陈述=标题、根因、证据锚点、分流决定、优化方案)任一缺失或为空,报告 MUST 被 register 拒绝(对应 data-model V-2)。

## 承继与生命周期

- **C-10**: `supersedes` 非空时,被承继报告 MUST 已存在;register 成功后其 `status` 由引擎置为 `superseded`(幂等:已 superseded 不报错)。
- **C-11**: `confirmed`/`superseded` 报告内容 MUST NOT 再被改写;修正 = 新一轮自省产出新报告并声明承继。
- **C-12**: 报告引用的条目 id 缺失(用户手动删改)时,消费方读取 MUST 标注"条目失效"而非报错(报告本身不改写)。

## 示例(最小合法报告)

```markdown
---
id: "introspection-20260828T060000Z"
created: "2026-08-28T06:00:00Z"
status: "draft"
scope_filter: "disposition=open, kind=internal"
scope_entries: ["20260820T062957Z-skill-improve-skills", "20260823T145827Z-speckit-requirements"]
supersedes: null
confirmed_at: null
---

# Introspection Report: introspection-20260828T060000Z

## Findings

### F-01: improve-skills 的 evidence-step 引用路径在嵌套技能下解析失败

- **根因**: 技能模板用相对路径引用 evidence-step.md,嵌套技能工作目录不同导致解析落空
- **证据锚点**: skills/improve-skills/SKILL.md:42;templates/skills/SKILL-template.md:18
- **成员条目**: 20260820T062957Z-skill-improve-skills(成立)
- **分流决定**: upstream-bound(package-attachment)
- **优化方案**: 模板改为经 `${SKILL_WORKDIR}` 绝对锚定引用;契约测试补嵌套技能场景

## Excluded

- 20260823T145827Z-speckit-requirements — 核验为"不成立"(所述行为当前版本已不存在)
```
