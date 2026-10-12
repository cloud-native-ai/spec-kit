# init 迁移计划 — profiles + xuanji-images(旧代 .specify → 分层运行时)

**制定**: 2026-10-12(spec-kit 框架仓,command-logic-as-classified-skills run 20261012T115331Z 收口后)· **执行**: 下次在两项目跑 `specify init` 时
**目标态**: `.specify/skills/` 外层平铺只剩 external 技能 + 用户自建技能;框架内部技能嵌套于 `.specify/skills/internal/<name>/`(15 个,带 `classification: internal`);命令模板为薄委派壳;状态面/工具记录在新址。
**权威依据**: `src/specify_cli/__init__.py`(`_OBSOLETE_SKILLS` :847 / `_FRAMEWORK_INTERNAL_SKILLS` :969 / `migrate_flat_internal_skills` :2014 / `remove_obsolete_assets` :1937 / init 升级链 :2390 起);`.specify/shared/definitions/tool-definitions.md` § Terminology;docs/git-workflow.md 状态面模型。

## 1. init 内置自动迁移(CLI 已承载,无需手工)

按 init 实际执行序:

1. **obsolete 清理**(`remove_obsolete_assets`,仅枚举清单,仅 `.specify/` 与活动工具命令目录):
   - draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml}(六引擎已并入 draw-diagram 内层)
   - git-{fleet,server-init,submodule-edit,workflow}(已并入 git-workspace)
   - 其余 23 项(manage-project / sdd-workflow / docx-utils 等,见 :847 清单)
2. **平铺内部技能迁移**(`migrate_flat_internal_skills`,必须在两层拷贝**之前**——CLI 已保证):15 个内部技能从 `.specify/skills/<name>/` 移入 `.specify/skills/internal/<name>/`;嵌套位已存在时平铺副本判 stale 删除;外部/用户技能永不触碰。
3. **两层技能带路径改写拷贝**(`copy_tree_with_rewrite`):`skills/external/<name>/ → .specify/skills/<name>/`(平铺)、`skills/internal/<name>/ → .specify/skills/internal/<name>/`(嵌套);源形态引用改写为运行时形态。
4. agents/、shared/、scripts/、memory/、templates/ 增量拷贝;instructions.md 再生成 + AGENTS.md/CLAUDE.md/QODER.md 等兼容符号链接;`.<agent>/skills → .specify/skills` 符号链接(qoder/claude/copilot)。
5. 拷贝为**加性合并**(dirs_exist_ok=True):同名框架文件被新版覆盖,用户内容永不删除。

## 2. init 不覆盖的 gap(手工步骤)

| # | Gap | 项目 | 处置 |
|---|-----|------|------|
| G1 | 旧状态面 `.specify/git-workflow.md`(新模型:状态在 `docs/git-workflow.md`) | **xuanji-images**(profiles 无此文件) | 优先:跑 `git-workspace` 技能 bootstrap(自带 legacy 探针,自动迁移到 docs/git-workflow.md);或手工 `git mv .specify/git-workflow.md docs/git-workflow.md` + 全仓引用更新。MUST NOT 双状态并存 |
| G2 | 旧工具记录 `.specify/tools/`(project/shell/system.json)+ `tools.md` 索引(新址 `.specify/memory/tools/` + guide) | **xuanji-images**(profiles 无) | 对照 `shared/definitions/tool-definitions.md` § Terminology 迁记录;旧 json 形态按 improve-tools 判定转换或归档 |
| G3 | 孤儿技能 `analysis-project`(不在 obsolete 清单、不在现役花名册) | **profiles** | 人工裁定:确认无引用后归档删除(它不在 _OBSOLETE_SKILLS,init 会当用户技能保留平铺) |
| G4 | `.<agent>/skills` 链接形态 | 两项目 | `.qoder/skills` 已是符号链接 ✓;执行时顺验 .claude/.github(claude/copilot 属 symlink assistants) |
| G5 | 多工具命令副本树陈旧(旧胖壳仍在前代副本目录) | 两项目 | 对每个在用工具各跑一次 `specify init --here --force --ai <tool>`(qoder/claude/copilot/opencode;加性、迁移幂等);或以主工具为准、其余树手工清旧壳 |
| G6 | 用户自建技能与本地修改 | **xuanji-images**:`xuanji-images-{add-image,build-k8s-images,install,setup-kdbg,setup-kind,rund}` 6 个 | 无需迁移(外层平铺形态不变);init 同名覆盖语义 → 第 0 步 pre-flight commit 是唯一回滚线 |
| G7 | git `dubious ownership` | **profiles** | 前置 `git config --global --add safe.directory /storage/project/profiles`(或以属主执行) |
| G8 | 遗留杂项 | 两项目 | profiles `.specify/docs`(旧工作区,人工定夺);旧 `instructions.md-<ts>` 备份、`skills.md`、`.specify/source.json` — 保留/由 init 自然刷新,无需动作 |

## 3. 执行序(每项目)

0. **前检**:`specify --version` 确认 CLI 携带两层技能源(wheel 内 `skills/{internal,external}/` 存在);git 工作区干净(不净先提交);profiles 加 safe.directory(G7)。
1. **备份**:pre-flight commit(消息如 `chore: pre-init-migration snapshot`)+ 记录 `git rev-parse HEAD`。
2. **逐工具 init**(G5):`specify init --here --force --ai <tool>`,每工具一次;init 输出的 migration/remove 计数记入执行记录。
3. **手工 gap**:G1 → G2 → G3(按项目差异表)。
3b. **sanitize 收尾(2026-10-12 起内置)**:跑 `/speckit.sanitize` —— 引擎已内置迁移残留检测(检测规则契约 §4a C-22/23/24):旧代技能目录(legacy 名集,归档处置)、旧代 `.specify/git-workflow.md` 状态文件(新状态面存在时)、旧 `.specify/tools/` 记录目录、内部分层的平铺重复;符号链接形态检查已扩至 `.qoder/skills`/`.claude/skills`(C-10)。归档类处置经确认计划批量执行;G3(孤儿技能裁定)仍需人工——`analysis-project` 不在 legacy 名集。
4. **验证清单**(全过才算完成):
   - 形态:`ls .specify/skills/` ⇒ 外层 = external 10 + internal/ 目录(+ 用户技能);`ls .specify/skills/internal/` = 15;obsolete 项不存在;
   - 标注:抽查 3 个内部技能 frontmatter 有 `classification: internal`;
   - 命令壳:任取 3 个 `speckit.*.md` 副本 = AUTO-GENERATED 头 + 生命周期节 + 薄委派块(非旧胖壳);
   - 链接:`.<agent>/skills`、AGENTS.md/CLAUDE.md/QODER.md 符号链接 `readlink` 正常;
   - 冒烟:任跑一条 `/speckit.*` 命令,确认其委派技能路径(`.specify/skills/internal/<name>/SKILL.md`)可解析;
   - xuanji 专项:git-workspace bootstrap 后 `docs/git-workflow.md` 存在且 `.specify/git-workflow.md` 已迁;memory/tools 新址生效。
5. **收尾**:git 提交迁移结果;source.json 已由 init 刷新(核对 commit 戳)。

## 4. 回滚

init 删除面仅 `_OBSOLETE_*` 枚举清单;其余加性。回滚 = `git reset --hard <pre-flight HEAD>`(仅当无后续有效工作);手工 gap 步骤各自可逆(git mv / 归档而非删除)。

## 5. 两项目差异速查

| | profiles | xuanji-images |
|---|---|---|
| 安装版本 | c2251c88 @ 2026-10-09 | 695d76d0 @ 2026-10-09(更早) |
| 平铺技能 | 37(含 1 孤儿 analysis-project) | 36 + 6 用户技能 |
| G1 git-workflow 状态面 | 无 | **有** |
| G2 tools 旧址 | 无 | **有** |
| G7 git 属主 | **有**(dubious ownership) | 无 |
