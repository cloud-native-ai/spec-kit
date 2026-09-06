---
id: "20260905T120355Z-speckit-skills"
unit_id: "/speckit.skills"
unit_type: "command"
run_id: "048-derive-command:skills-orchestration:2026-09-05T12:03Z"
scope: "local"
probe: "speckit-skills-wrapup"
kind: "internal"
slice: "commands"
feature: "048-derive-command"
feature_id: "049"
partial: false
created: "2026-09-05T12:03:55Z"
summary: "编排入口被用于「创建新命令 /speckit.derive」。路由本身正确(目标不存在 → create 分支),但 create 分支无条件委派 create-skills,而本仓的 /speckit.* 命令不是技能:命令真源是 templates/commands/<name>.md,经 regen-command-copies.py 扇出到 .claude/.github/.qoder/."
---

## Review
编排入口被用于「创建新命令 /speckit.derive」。路由本身正确(目标不存在 → create 分支),但 create 分支无条件委派 create-skills,而本仓的 /speckit.* 命令不是技能:命令真源是 templates/commands/<name>.md,经 regen-command-copies.py 扇出到 .claude/.github/.qoder/.opencode 四处,skills/ 与 .specify/skills/ 下没有任何 speckit.* 目录。于是 create-skills 的 SKILL_HOME、frontmatter、路径约定、Step 7 agent 传播对本请求全部不适用,执行者必须在运行时自行把工作流重新解释成命令路径,并自行发现命令独有的强制接线义务(probe Object 与模板同批、两个分类计数、short-description ≤50、门控预算零余量)。本次交付本身完整(Feature 049 / requirement 048:概念锚 + 命令模板 + 1690 行 stdlib 引擎 + 新顶层根 .specify/derive/ + 8 个测试文件 232 项全绿 + 4 份契约 + dogfood 真实运行),但入口对 command/skill 两类目标不做区分是可复现的摩擦点。

## Optimization Points
- `/speckit.skills` 的 Step 2「Check existence」只探 `.specify/skills/<name>/SKILL.md`,而本仓的 `/speckit.*` 命令**不是**技能(命令是 `templates/commands/<name>.md`,由 `regen-command-copies.py` 扇出到四个工具目录;`skills/` 与 `.specify/skills/` 下没有任何 `speckit.*` 目录)。因此「创建新命令 /speckit.derive」这一请求会因目标不存在而落入 create 分支、再被委派给 `create-skills`,而 `create-skills` 的整套工作流(SKILL_HOME、frontmatter、`${SKILL_HOME}` 路径约定、Step 7 传播到内置 role agents)对命令**全部不适用**,执行者必须在运行时自行把它重新解释成命令路径。建议:编排入口在 Step 1 就区分 target kind(`command` vs `skill`)——`/speckit.<name>` 形态或用户明说「命令」即判为 command,走 `templates/commands/<name>.md` + probe 登记 + 两个分类计数 + 四份副本再生成的命令路径,不再委派 `create-skills`。
- Step 4「Propagate to built-in agents」是技能专属动作(把 slug 追加进 agent 的 `skills:` frontmatter 与 `## Skill Enablement` 表),对命令无意义且其 Guard 清单只列了 6 个 meta 技能。建议把 Step 4 显式 gate 在 target kind == skill 上,命令路径直接跳过,避免执行者犹豫是否要给 7 个 role agent 登记一个命令。
- 命令路径有一组**技能路径完全没有的强制接线义务**,而编排入口一个字都没提,全靠执行者自己发现:feedback probe Object 必须与命令模板**同批**落地(否则 `--action probes --reconcile` 双向报错 exit 2)、复杂命令分类计数 +1(`test_feedback_command_classification.py`)、docs-step 分类计数 +1(`test_docs_step_injection.py`,且要求 `## Feedback` 在 `## Documentation` 之前并相邻)、`short-description` ≤50 字符、以及确认门控预算(本仓 total 23 / cap 23.25 **零余量**,新文件里一个 BLOCKING 匹配就打爆两个契约测试)。建议在编排入口为 command 分支补一张「命令接线义务」清单,或指向 `docs/reference/commands/` 下的单一真源。
