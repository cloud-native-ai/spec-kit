# 03 · Skills 体系建设

> 覆盖会话:`031835d1`(017 草稿合并)、`46a705d0`(git-workflow 三模式)、`5878b07d`(021 Agent 特定配置)。时间跨度 2026-06-18 → 2026-06-25。

## A. 草稿合并为正式 skill(017,031835d1)

把 `draft/skills/` 下 9 个草稿改写并合并为 3 个正式 skill:

| 目标 skill | 合并来源 | 关键设计 |
|-----------|----------|----------|
| `document-utils` | docx/pdf/pptx/theme/xlsx (5) | 共享 `scripts/office/` 去重(三份 office 脚本字节相同,只留一份);格式专属脚本放 `scripts/<format>/`。这是本次**净删除 25042 行**的主因 |
| `database-utils` | mysql/postgres (2) | 统一 `query.py` 读 `connections.json`,按 `protocol` 字段或端口推断(3306/9030→mysql,5432/9005→postgres)动态 import;ClickHouse 归 postgres 生态、Doris/SelectDB 归 mysql 生态;定位为**只读查询** |
| `browser-utils` | playwright/web-test (2) | 语言分层:JS 自动化 `scripts/js/`,Python 测试 `scripts/python/` |

- **绑定既有 Feature 013(Skills Command)而非新建**:历史 skill 相关 spec(005/007/008/012/013)均挂 013 下,合并是自然迭代。
- **实现用 3 个并行 subagent** 分别构建(目录互相独立,US1/US2/US3 可并行)。
- 产出:分支 `017-consolidate-draft-skills`,commit `e2549f9`(291 files,+12439/-25042);删除 9 个草稿目录;50/50 任务关闭。

> 全程无分歧(用户仅答 "A" 和 "yes")。

## B. git-workflow 重构为三模式技能(46a705d0)

通过 `/speckit.skills` 入口(目标已存在→路由 improve-skills)优化 `skills/git-workflow`,做成**单一入口按上下文自动路由的三模式**:

- **Mode 1 Setup**:`docs/git-workflow.md` 不存在 → 协助建立工作流。
- **Mode 2 Maintain**:文档已存在 + 无参数 → 输出结构化健康/维护报告。
- **Mode 3 Execute**:文档已存在 + 有指令 → 匹配预定义操作执行(5 类:A full sync / B DEV→PRE / C PRE→MAIN / D 基于主干 rebase / E custom,用触发词做意图匹配)。

- **三层分支模型**:主干(main/master)、预发(自定义/`prepu*`)、开发(自定义),外加 `docs/git-workflow.md`;**文档 frontmatter 是所有模式共享的分支名单一真相源**。
- improve-skills 两阶段:即使只提行为优化,也**必须先跑 Phase A 规范合规检查**(本次全合规,零现代化编辑),再 Phase B 重构。
- 把 instructions 查找优先级表抽到 `references/instructions-lookup.md`,守住 SKILL.md <500 行上限(319 行)。

## C. Agent 特定配置(021,5878b07d)

为高相关的 command 和 skill 加"Agent-Specific Configuration"章节,让框架**区分不同 AI Agent 工具而非一视同仁用通用配置**。三步机制:①识别当前 Agent;②加载工具特定参考文档;③捕获执行阻碍生成 feedback。

- **7 个目标**:3 个 command 模板(agents/skills/tools.md)+ 4 个 skill(browser-utils/create-agent/improve-agent/improve-skills)。
- **command 用内联,skill 用外置 `references/<agent-slug>-guide.md`**:command 保持单文件(改成目录会破坏被 symlink 引用的现有结构)。
- **发布阶段只做 2 个 Agent**:每 skill 出 Claude Code + Copilot 两份参考,共 8 份。
- 产出:commit `9dcf236`,32 files/+2030;37 任务全过;新建 `.specify/memory/feedback/` 目录。绑定 Feature 022(AI Tools Support)。

### 用户 ↔ 模型的冲突/分歧点(021)

| 议题 | 用户主张 | 模型原本 | 最终 |
|------|----------|----------|------|
| references 归属 | 只给 skill,command 不用 | Option B(command 用共享 references 目录) | skill 外置 references/、command 内联 |
| feedback 存储 | 集中 `.specify/memory/feedback/` | 就近 `${SKILL_HOME}/feedback/` | 集中式(便于跨切面分析) |

> 这个"集中式 feedback"决策是后来 Feature 028 反馈机制(见近期 commit `ed4fc0a`)的前身。

## 可复用经验

- skill 双份镜像 `skills/` ↔ `.specify/skills/`,构建后校验字节等价;新 skill 会被系统 prompt 自动发现。
- office 脚本这类跨草稿重复内容,合并前先 diff 确认一致再去重。
- 契约测试踩坑:`tools.md` 无 `## Handoffs` 段,默认"章节插在 Handoffs 前"的 C-007 需改为"放文件末尾即可";skill 编排流程自身的 "Step 1/2/3" 会被可加性校验误当引用,需人工确认;`${SKILL_HOME}` 字面量匹配用 Python 别用 shell grep(见 [[00-cross-cutting-lessons]] 第六节)。

---

**相关**:[[00-cross-cutting-lessons]] · [[01-agent-system-evolution]] · [[04-draw-plantuml-optimization]]
