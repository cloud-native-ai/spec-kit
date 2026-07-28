# 02 · 命令与 CLI 工具体系

> 覆盖会话:`101d217a`(016 重构 /speckit.tools)、`207f8d40`(018 CLI 分层 + Codex)、`12df2298`(移除废弃 AI 工具)。时间跨度 2026-06-17 → 2026-06-22。

## A. `/speckit.tools` 从"发现"转向"定义"(016,101d217a)

### 核心决策与理由

- **definition-first 取代 discovery-first**:`define`(创建/修改)成为一等操作,`discover` 降级为草稿引导助手。**理由:防止 LLM 内置知识/上下文导致工具误用**,让用户编写的显式定义具有权威性。这是整个重构的初衷。
- **discovery 定位选 A"发现辅助定义"**:无记录时可扫描系统并生成待确认草稿(`DiscoveryDraft` 实体,恒标注 "Draft — pending user confirmation")。放弃 B(纯手工,摩擦大)、C(仅 fallback)。**用确认门(confirmation gate)而非输入门拦截 LLM 干扰**。
- **Behavioral Rules 用 RFC 2119 关键字前缀的 Markdown 项目符号**(MUST/MUST NOT/SHOULD/SHOULD NOT + 自由文本)。放弃纯散文(歧义,正是要消除的)和 key-value 结构(对多样工具行为太僵化)。
- **无需迁移**:向现有模板追加 Behavioral Rules 是纯增量;旧工具记录(无该字段)加载为空规则,兼容。
- **四种工具类型 + 作用域分层**:
  - `tool-project-script-template.md` — 项目范围(项目自带脚本)
  - `tool-shell-function-template.md` — shell session 级(source 引入的函数)
  - `tool-system-binary-template.md` — 系统级 binary(可能与发行版绑定)
  - **新增** `tool-webhook-template.md` — 网络级(HTTP 触发远端操作,字段含 Method/Content-Type/Auth/Timeout,参数带 Location 列 body/query/header/path)

### 最终产出

commit `685c4e2`(合入 master `8ab26b5`)。核心:`scripts/python/tools-utils.py` 新增 `BehavioralRule`(RFC 2119 校验)、`DiscoveryDraft`、`validate_strict()`、`discovery_origin` 字段,`_ALLOWED_TOOL_TYPES` 加 `webhook`;`templates/commands/tools.md` 重写为 10 步 definition-first 流程;6 实体数据模型;工具测试 140 通过。Feature 016 → Implemented。spec `016-refactor-tools-command/`。

> 本会话三个 clarify 用户均直接接受模型推荐(答 A),无实质分歧。

## B. CLI 工具分层体系 + Codex 接入(018,207f8d40)

### 核心决策与理由

- **引入 `_ASSISTANT_TIERS` 分层**:Tier 1 = claude/codex/qoder/copilot/opencode,Tier 2 = qwen。便于按层级差异化处理能力。
- **`generate_commands()` 保持 config-driven**:接入 Codex 只需在各 config dict 加 `codex` 键,无需改生成逻辑(最小改动)。Codex 专属 init 分三处补丁:命令生成 block、`codexignore` 拷贝、skills symlink(仿 opencode/claude pattern)。
- **能力矩阵审计**:`audit_capability_matrix()` + `audit_tool_dimension()`,6 维度 × 6 工具。
- **被放弃/退让**:
  - **不 amend constitution 模板**(T042):模板是通用脚手架,Principle V 是 "Observability" 而非 "AI Agent Integration",不该为 Spec-Kit 特有内容强塞,保持模板中立;仅改项目级 constitution(升 1.1.0)。
  - T052 `update-agent-context.sh` 在本仓库不存在(plan 从外部 context 引用),放弃。
  - `usage.md` 是 redirect stub(空壳),无内容可写 tier 说明。

### 最终产出

commit `feat(018-cli-priority-support)...`,36 files / +2166。新增 45 测试全过,最终 420 passed / 7 failed(全基线遗留)。`get_assistant_profile()` 加 `tier`/`skills_symlink`;`InitializationResultSummary` 加 `assistant_tiers`;README/installation/quickstart 加 tier 标注;constitution Principle V → 1.1.0。Feature → Implemented。

> 无实质分歧。踩坑详见 [[00-cross-cutting-lessons]] 第七、八节(工具数 5→6 打破一批硬编码断言:`test_five_official_assistants`、coexistence dict 的 `KeyError: 'codex'`、fixture 硬编码列表、跨 feature 契约 enum 需回填)。

## C. 移除废弃 AI 工具(12df2298 后半)

- **诉求**:彻底移除对通义灵码(`.lingma`)、Cline(`.clinerules`)、Trae(`.trae`)、iFlow(`IFLOW.md`)、Cursor(`.cursorrules`)的支持,并让 `init`/`instructions` 时**顺带自动清理**这些过期产物。
- **关键发现**:这些废弃目录只在 shell 脚本 `generate-instructions.sh` 中被创建,Python 源码零引用。
- **最终**:改 `generate-instructions.sh`(源 + `.specify/` 镜像)删除创建代码、新增清理逻辑(创建 symlink 前先检测删除废弃目录);`instructions-template.md`(源+镜像)、`.specify/instructions.md`、`templates/commands/instructions.md` + 3 个生成命令副本同步更新;删除 5 个废弃目录/文件。测试 377 passed / 5 failed(基线遗留)。

> 当前受支持工具的权威列表见 `AGENT_CONFIG` / `_ASSISTANT_TIERS`(`src/specify_cli/__init__.py`)。

## 跨节可复用经验

- 测试通过 `tests/script_api.py` 加载 `scripts/python/*-utils.py`(如 `tools-utils.py` 的 `ToolRecord`/`ToolInvocationSession`);TDD 下先改 utils 再写测试。
- 模板改动双写同步、脚本名复数问题、区分基线失败——见 [[00-cross-cutting-lessons]]。

---

**相关**:[[00-cross-cutting-lessons]] · [[01-agent-system-evolution]] · [[03-skills-system]]
