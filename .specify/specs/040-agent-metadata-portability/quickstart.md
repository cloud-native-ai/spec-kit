# Quickstart: Agent Metadata Portability (Feature 044)

实现完成后的开发者动线。命令示例按 `/speckit.plan` 质量门要求钉住:渲染/init 类命令由 `tests/integration/test_init_agents.py` 与 `tests/contract/`(改写后)钉住;镜像/测试类命令为仓库既有命令。

## 1. 编辑一个 Meta Agent 定义

```bash
# 中立源:frontmatter 只用中立键集(neutral-metadata-schema.md §E2)
$EDITOR agents/skill-verifier.agent.md
```

校验(契约测试即校验器):

```bash
pytest tests/contract/test_shipped_agent_presets.py -q   # 预置集 = Meta,中立 frontmatter
pytest tests/contract/test_role_templates.py -q          # Worker 能力模板契约
```

## 2. 同步镜像并渲染到目标工具

```bash
python3 scripts/python/sync-mirrors.py --write && python3 scripts/python/sync-mirrors.py --check
```

在消费项目里(渲染替代软链接,产物为真实文件):

```bash
specify init my-project --ai qoder     # → my-project/.qoder/agents/*.agent.md(Qoder 格式,真实文件)
specify init my-project --ai claude    # → my-project/.claude/agents/*.md(Claude 格式)
```

init 反馈示例(R-9):`rendered 2 agents for qoder; 0 backups; unmapped intents: skill-verifier → display-color`。

## 3. 检查渲染产物与清单

```bash
ls -la my-project/.qoder/agents/          # 期望:常规文件,0 个符号链接(SC-002)
cat my-project/.specify/agents/.render-manifest.json   # E4 清单
```

## 4. 手改保护与再渲染

```bash
# 用户手改产物后再次 init:备份 + 覆盖 + 报告(R-5)
specify init my-project --ai qoder
ls my-project/.specify/agents/.backups/qoder/          # 手改内容可取回(FR-021)
```

## 5. 组建 Team 时的取件(T-2)

- Meta Agent:从 `agents/`(经 `.specify/agents/templates/`)直接选取。
- Worker Agent:经 `create-agent` / `create-team` 技能从能力/职责模板实例化;7 个原预置角色不再随 init 分发。

## 6. 回归验证

```bash
pytest -q                                # 对照改造前基线,零新增失败(SC-008)
pytest tests/integration/test_init_agents.py -q
```
