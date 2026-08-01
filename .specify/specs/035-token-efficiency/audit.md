# 存量审计:Token 效率两纪律违规清单(audit.md)

**Spec**: 035-token-efficiency | **判据**: `shared/guidelines/token-efficiency.md` | **冻结时间**: 2026-08-02
**审计面**(动态枚举实测): 命令模板 19 个(`templates/commands/*.md`)、技能 26 个(`skills/*/SKILL.md`)、共享文档 17 个(`shared/workflow|guidelines|constants/*.md`)、数据引擎 9 个(`scripts/python/*-utils.py`)
**注入量口径**: 被整读文件/语料的 `wc -l` / `wc -c` 实测(2026-08-02 时点);严重度 = 触发频率 × 注入量的全清单名次
**冻结不变量**: 排序定稿后不增删行;整改只改"状态/备注"列

## 违规清单(按严重度名次排序)

| ID | 单元 | 违规纪律 | 证据 (file:line + 原句摘录) | 注入量代理(实测) | 触发频率 | 严重度 | 状态 | 备注(前后对比) |
|----|------|----------|------------------------------|-------------------|----------|--------|------|----------------|
| V-001 | templates/commands/plan.md | summary-first | plan.md:111 "Read `.specify/memory/features.md` and all files in `.specify/memory/features/`" | features/ 全目录 40 文件 2234 行 / 169,555 B + features.md 69 行 / 18,805 B ≈ **188 KB** | high(每次 /speckit.plan) | 1 | remediated | 已整改(含同单元同类问题 plan.md:110 docs/ 全读一并收敛为定向节选) |
| V-002 | templates/commands/clarify.md | summary-first | clarify.md:53 "Load common context: `.specify/memory/constitution.md`, `README.md`, relevant `docs/`, `.specify/memory/features.md`, `research.md`" | constitution 198 行 / 19,668 B + README 49 行 / 2,471 B + features.md 18,805 B 固定 ≈ **41 KB**;docs/ 无界(74 文件 / 445,982 B) | high(每次 /speckit.clarify) | 2 | remediated | 整改设计:按需投影(features.md grep 行、constitution 定向节选;docs/ 仅定向节选) |
| V-003 | templates/commands/implement.md | summary-first | implement.md:41 "Load context: tasks.md (REQUIRED), plan.md (REQUIRED), data-model.md, contracts/, research.md, quickstart.md (IF EXISTS)" | 一次性预载全工件(034 实测 728 行 / **57,559 B**) | high(每次 /speckit.implement) | 3 | remediated | 整改设计:预载仅 tasks.md + plan.md,其余工件按任务需要定向读取 |
| V-004 | templates/commands/tasks.md | program-first | tasks.md:99 "parse `.specify/memory/constitution.md` and detect any principle whose name or body contains `MUST`…" | constitution 198 行 / **19,668 B** 整读做关键词检测(grep 可完成) | high(每次 /speckit.tasks) | 4 | remediated | 整改设计:grep 关键词检测(程序侧),LLM 仅接收匹配的原则标题行 |
| V-005 | templates/commands/requirements.md | summary-first | requirements.md:51 "skim the highest-numbered existing spec under `.specify/specs/`" | 最新规格整读(034 实测 247 行 / **30,844 B**) | high(每次 /speckit.requirements) | 5 | remediated | 整改设计:有界节选(标题结构 + 单故事样例 + FR 抽样) |
| V-006 | templates/commands/checklist.md | summary-first | checklist.md:48 "Load feature context from REQUIREMENTS_DIR"(全工件) | 需求工件集(034 口径 ~**57 KB**) | medium(可选命令) | 6 | backlogged | 后续迭代:按检查域定向读取 |
| V-007 | templates/commands/research.md | summary-first | research.md:39 "Read `.specify/memory/constitution.md`"(整读) | constitution 198 行 / **19,668 B** | medium(可选命令) | 7 | backlogged | 后续迭代:定向节选相关原则 |
| V-008 | templates/commands/feature.md | program-first | feature.md:60 ID 分配 "from scanning `.specify/memory/features/*.md`" | features/ 语料 **169,555 B**(ls+排序可完成) | medium | 8 | backlogged | 后续迭代:`ls`/`grep` 派生最高 ID |
| V-009 | scripts/python/history-utils.py | summary-first(引擎缺口) | 仅 `extract` 整会话转储,无摘要级输出模式(data-model.md §4 矩阵) | 单会话转储可达 MB 级(随会话体量) | low(/speckit.history 偶发) | 9 | backlogged | 后续迭代:增 per-session 摘要 action(T019 条件分支:未入 top-5,记录留档) |

## 排除项(非违规,判据引用)

| 单元 | 排除理由 |
|------|----------|
| skills/improve-tools/SKILL.md:27(Tool 记录整读) | 例外 (a):该文件是编辑目标(read-before-edit) |
| glossary-utils.py `list` 全表 / `.specify/memory/glossary.md` | 例外 (b):33 行 / 2,970 B,低于小文件阈值(≤ 100 行 且 ≤ 10 KB) |
| skills/git-workflow(读 git-workflow.md) | 该文件当前不存在(首跑生成);生成后典型体量低于小文件阈值,不构成违规 |
| templates/commands/analyze.md:75 | 合规反例:"Load only the minimal necessary context from each artifact" |
| skills-utils.py `skill-read` / tools-utils.py `record-load` 全文输出 | 消费场景为编辑/生成目标(例外 (a));引擎程序侧读原文本身合规 |

## Top-5 整改前后对比(SC-003 判据汇总)

| ID | 整改前注入(实测) | 整改后注入(实测) | 降幅 |
|----|-------------------|-------------------|------|
| V-001 | 188,360 B(features.md 全文 + features/ 40 文件) | 索引行投影 + 绑定 Feature 详情 = 21,277 B(实测) | **88.7%** |
| V-002 | 41,000 B 固定 + docs/ 无界 | 索引行投影 17,503 B(实测;constitution/README/docs 改按需定向) | **57.3%**(固定部分;无界部分归零) |
| V-003 | 57,559 B 预载 | 预载 tasks+plan = 36,851 B(实测,034 口径) | **36.0%**(预载口径;其余 4 工件 20,708 B 转按需,未计入) |
| V-004 | 19,668 B 整读 | grep 匹配行 52 行 / 8,520 B(实测) | **56.7%** |
| V-005 | 30,844 B 整读 | 标题结构 + 单故事 + FR/SC 抽样 = 5,308 B(实测) | **82.8%** |

> 注:V-001…V-005 的"整改后注入"以整改后指令的目标读取集实测/推算(同一流程前后相对比较口径,不作跨流程绝对排名;整改落地由 `tests/contract/test_token_efficiency_remediation_*.py` 钉扎)。
