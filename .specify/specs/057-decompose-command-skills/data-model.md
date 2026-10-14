# Data Model: 057-decompose-command-skills

本特性为 template-only:实体是**内容实体**(Markdown 制品的结构化事实),无运行时数据存储。四个实体 + 两组状态迁移。

## 实体

### 1. Skill Descriptor(技能描述符)

技能的可定位身份。真源:requirements.md § Key Entities(2026-10-14 裁定:身份以 canonical 路径为准)。

| 字段 | 类型 | 约束/验证 |
|------|------|-----------|
| name | string | 与目录名一致;`[a-z0-9-]+`;全树唯一性不强制——同名跨 canonical 路径是两个技能(冲突经 FR-003 优先级消解) |
| layer | enum | `internal` / `external`(词汇表「技能分类标注」约束侧:internal 配合 .specify 结构,external 不依赖) |
| canonical_path | path | `skills/{external,internal}/<name>/SKILL.md`;**身份主键** |
| installed_mirror_path | path | `.specify/skills/{<name>,internal/<name>}/SKILL.md`;由 sync-mirrors 生成,非独立技能 |
| skill_md_valid | bool | frontmatter 含 `name`/`description`(+ internal 技能含 `classification: internal`、`skill_id`) |
| host_registered | observation | 宿主相关观测,非框架事实;本仓经由 `.claude/.qoder/.github/skills → .specify/skills` 符号链接近似可达 |

关系:一个 Skill Descriptor 恰属一层;installed 镜像**不是**独立 Descriptor(投影)。

### 2. Skill Location Search Order(技能位置搜索顺序)

run-skills 一次解析所 travers 的有序位置清单。真源:run-skills SKILL.md 体内(FR-006 内联最小操作事实)——本表为设计投影,落盘后以技能体为准。

| 序 | 位置 | 层 | 说明 |
|----|------|----|------|
| 1 | `skills/internal/<name>/SKILL.md` | dev canonical internal | 已裁定优先级最高 |
| 2 | `skills/external/<name>/SKILL.md` | dev canonical external | |
| 3 | `.specify/skills/internal/<name>/SKILL.md` | installed internal 镜像 | |
| 4 | `.specify/skills/<name>/SKILL.md` | installed external 镜像 | |

规则:首个命中即选,输出披露所选路径;显式路径输入 MUST 落于上述位置集内,越界快速失败(FR-004)。0 命中 → 可行动错误(逐项列出已搜索位置)。

### 3. Team Run Flow Obligation Set(团队运行义务集)

从 `templates/commands/team.md` 提取、由 run-team SKILL.md 承接的 run 语义程序性义务清单。真源迁移:落盘前 team.md,落盘后 run-team SKILL.md。逐条对映(义务 → 落点 → 强度)由 `contracts/run-team-parity.md` P-1…P-10 承载——本实体不复制其行,只声明集合身份:P-1…P-10 的并集 = 落盘时点 team.md 中 **run 语义的全部程序性义务**(主体 § Run Mode,含路由流中 run 直接承载的 team-not-found 义务),零丢失。

### 4. Probe Registry Object-row(skill-wrapup 注册行)

两新技能获得编译 Wrap-up 的注册事实。真源:`shared/definitions/probe-definitions.md` Object 表。

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| skill-run-skills-wrapup | skill-wrapup | skill:run-skills | wrap-up |
| skill-run-team-wrapup | skill-wrapup | skill:run-team | wrap-up |

验证:compile-embeds --check 零漂移;既有守卫 test_compile_embeds.py / test_registry_completeness.py 继续约束。

## 状态迁移

- **技能生命周期**(canonical 侧):authored(本特性实现)→ mirrored(sync-mirrors 落 .specify/skills)→ host-discovered(符号链接既有拓扑,零新机制)→ runnable(run-skills 解析可达)。无运行时状态机。
- **Feature 057 状态**:Draft → **Planned**(本计划落盘,本命令执行)→ Implemented(/speckit.implement 专属,Pre-Status-Flip Gate)。永不回退(VII 无回退门)。
