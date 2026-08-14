# Data Model: Agent Metadata Portability (Feature 044)

Entities、字段、关系与状态迁移。所有实体均为文件或内存结构,无外部存储。

## E1. Agent Definition(agent 定义,唯一真源)

载体:单个 `*.agent.md`(FR-002)。位置:`.specify/agents/templates/`(预置镜像)与 `.specify/agents/instances/`(项目自写)。

| 组成 | 位置 | 判定规则 |
|------|------|----------|
| Neutral Metadata | YAML frontmatter 中属于中立键集(D2)的键 | 键归属,程序可判定(FR-001) |
| Agent Body | frontmatter 之后的全部正文 | 补集;不得含分发/运行参数(FR-003) |

约束:
- frontmatter 中出现中立键集之外的键 → 渲染前校验失败并报告(MUST NOT 静默忽略)。
- 发现机制只读 frontmatter 的 `name`/`description`(FR-004)。

## E2. Neutral Agent Metadata(中立元信息)

中立键集(D2,全部 kebab-case):

| 键 | 语义 | 取值域 | 缺省行为 | 是否渲染给工具 |
|----|------|--------|----------|----------------|
| `name` | 显示名 | 非空字符串 | 必填,缺失即校验失败 | 是(按工具命名规则) |
| `description` | 用途描述 | 非空字符串 | 必填 | 是 |
| `user-invocable` | 可否被用户直接调用 | bool | `true` | 是(有对应物时) |
| `disable-model-invocation` | 是否禁止模型自动调用 | bool | `false` | 是(有对应物时) |
| `model-tier` | 模型档位偏好 | `auto\|efficient\|performance\|ultimate\|none` | `auto` | 是(映射到工具枚举) |
| `capability-tools` | 能力白名单(工具调用面) | 字符串数组 | 空=不限制(按工具语义) | 是(工具名映射) |
| `skills` | 技能白名单 | 字符串数组 | 空 | 是(有对应物时;无则按 D3) |
| `run-turn-budget` | 单次运行规模上限 | 正整数 | `10` | 是(有对应物时;无则按 D3) |
| `display-color` | 展示标识 | 颜色名枚举 | 无(不输出) | 是(有对应物时) |
| `supervisor` | 框架装配:督导角色 | bool | `false` | **否**(纯框架语义) |
| `capacity-scope` | 框架装配:能力作用域 slug | 字符串 | 无 | **否** |

禁用词表(SC-001 扫描对象):`maxTurns`、`disallowedTools`、`timeoutMins`、`mcpServers`、`permissionMode`、`background`、`isolation`,以及任何未在上表中的工具专属键。

## E3. Tool Metadata Mapping(工具映射,单一真源)

载体:`src/specify_cli/__init__.py` 常量 `_AGENT_METADATA_MAPPING`(D4)。

```python
_AGENT_METADATA_MAPPING = {
    "<tool-key>": {
        "mode": "render" | "annotated",
        "target_dir": ".qoder/agents" | ...,        # render 行
        "file_naming": "<name>.agent.md" | ...,      # render 行
        "fields": { "<neutral-key>": <转换规则或 None> },
        "provenance": "<官方文档 URL 或 源码核实>",
        "unmapped_policy": "<D3 策略引用>",
        "note": "<annotated 行的不渲染依据>",       # annotated 行
    },
    ...
}
```

关系:键域 = `AGENT_CONFIG` 的全部 6 个工具键(SC-003 完备性断言的对照面)。

初始内容(出处见 contracts/tool-mapping.md):

| 工具 | mode | 出处 |
|------|------|------|
| qoder | render | https://docs.qoder.com/cli/subagent |
| claude | render | https://code.claude.com/docs/en/sub-agents(字段清单第二轮核实前标"待核实") |
| copilot | render | https://code.visualstudio.com/docs/copilot/customization/custom-agents + https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents |
| opencode | render | https://opencode.ai/docs/agents/ |
| codex | annotated | openai/codex 源码 `agent_roles.rs`(TOML、config 层落点,越出项目作用域) |
| hermes | annotated | 官方文档无成文的项目级 agent 约定 |

## E4. Render Manifest(渲染清单)

载体:`.specify/agents/.render-manifest.json`。写入者:渲染函数;读者:再渲染的漂移检测(FR-021)与失效清理(FR-020)。

```json
{
  "version": 1,
  "tool": "<tool-key>",
  "rendered_at": "<UTC ISO-8601>",
  "entries": {
    "<目标目录相对路径>": {
      "source": "templates/<slug>.agent.md | instances/<slug>.agent.md",
      "sha256": "<上次渲染产物的哈希>"
    }
  }
}
```

## E5. Backup Record(手改备份)

载体:`.specify/agents/.backups/<tool>/<name>.<UTC-compact-timestamp>.agent.md`。仅当清单内文件哈希不一致或清理目标曾被手改时产生;路径必须出现在 init 反馈中(FR-021)。

## 状态迁移:渲染产物生命周期

```text
(不存在) --init/再渲染--> FRESH(哈希=清单)
FRESH --再渲染--> FRESH(直接覆盖刷新)
FRESH --用户编辑--> MODIFIED(哈希≠清单)
MODIFIED --再渲染--> BACKED_UP(.backups/ 落备份)+ FRESH(新渲染)
FRESH|MODIFIED --中立源删除--> PRUNED(手改过先备份)
不在清单 且 无中立源对应 --> USER_ASSET(永不覆盖)
```

同名冲突:instances 层条目压过 templates 层同名条目,渲染时只产出一份(FR-017,沿用 instance 优先)。
