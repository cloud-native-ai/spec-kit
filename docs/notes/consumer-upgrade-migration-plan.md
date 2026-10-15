---
title: "客户项目旧 .specify 结构的迁移升级方案(技能两层重家后)"
created: 2026-10-11
expires: 2026-12-10
status: draft
target: "docs/tutorials/installation.md"
tags: [skill-layering, consumer-upgrade, migration, release]
---

# 客户 `.specify` 迁移与升级方案(技能内外分层发布)

> 依据:skill-layer 重构(commits `1adfa49a` + `766088f2`,已推 gitee/github/gitlab)后的机制审计 + **真实旧消费者升级仿真**(独立 venv + 新 wheel,命令见 §7)。

## 0. 结论摘要

- **仓内机制:零功能断点** —— 引擎 `--check` 0/0、门控 23、全量 3523P/1F(唯一 c7 为既有窗口项,见 register)、守卫两条带红绿。
- **消费者升级面:一处真断点** —— 旧项目中 15 个平铺 internal 框架技能在升级后**原样残留**(发现的可见面违背"内部技能不可见"判据);根因是升级**时序**缺陷。修复为 3 项小改(F1–F3)。
- 其余消费者面(重生成命令、退役清理、符号链接、用户技能红线、脚本/探针)经仿真**全部正常**。

## 1. 实证仿真(核心证据)

基线:真实旧消费者(由已发布的 0.0.22 安装:`/tmp/sk-consumer-probe`,35 个平铺技能 = 17 外部 + 15 内部框架名 + 3 退役名 + 用户技能)。用**本仓重构后 wheel** 在独立 venv 执行 `specify init . --force --ai qoder`:

| 面 | 升级后实测 | 判定 |
|----|-----------|------|
| 退役技能清理 | `removed 4 obsolete framework asset(s)`(git-fleet/server-init/submodule-edit/workflow) | ✅ |
| 命令副本 | 重生成,含 10 处 `.specify/skills/internal/…` 运行时形 | ✅ |
| 符号链接 | `.github/skills`、`.qoder/skills` → `.specify/skills` | ✅ |
| 用户自建技能 | 原样未动(红线守住) | ✅ |
| 内部层新装 | `.specify/skills/internal/` 15 个,内容为新版 | ✅ |
| **平铺内部副本** | **`migrated 0 … kept 15 (nested target exists)` — 15 个旧内容副本残留,发现面可见** | ❌ **断点** |
| 幂等 | 二次 `init` 无进一步变化(不恶化,但残留不消) | 中性 |
| 脚本/探针 | `create-new-tools.sh` runtime-first 候选梯;探针按名引用 | ✅ |

判定脚本(复算):`ls .specify/skills/*/ -d | wc -l` = 34(应为 19 = 17 外部 + `internal` + 用户 1);`test -d .specify/skills/create-agent` = true(应为 false)。

## 2. 断点根因

`src/specify_cli/__init__.py` 的升级序列为:**先**两层拷贝(内部层落 `internal/<name>`),**后** `migrate_flat_internal_skills`(位于 structural-cleanup 段)——迁移执行时"嵌套目标已存在",按既有语义走 `kept` 分支(保留平铺、不覆盖)。真实升级路径因此**永远命中 kept**;C2b 的函数级迁移测试是手工构造"无 nested"起点,故未暴露该顺序缺陷。

## 3. 修复设计(发布必做)

> **实现状态(2026-10-11):F1/F2/F3 已落地并经 S2 独立验证**(S1 交接门 PASS;验证报告:`.specify/teams/.work/post-refactor-mechanism-integrity/S2/verification.md`)。三场景一句话:
> - **A 修复轮**:真升级 `migrated 15` —— 平铺内部名清零、`internal/` 15 个齐、用户技能字节一致、副本引用重写为运行时形(哈希三角见 S2 报告 §2);
> - **B 对照轮**:HEAD(修复前)wheel 复现缺陷 `migrated 0; kept 15 (nested target exists)`,15 个平铺内部名全残留(红侧对照);
> - **C 双存分支**:真引擎触发 F2,`migrated 14; removed 1 stale flat duplicate(s)`,平铺旧副本被移除、nested 内容不被覆盖。
>
> 引擎文件还原 md5 `46cd0bbf0799ad64e87233f321a1b7c8` 经 S2 复核字节一致;F3 红先行证据在 `S1/manifest.md`。以下设计原文保留为历史。

- **F1 时序重排(核心,单点)**:把 `migrate_flat_internal_skills` 调用**提前到内部层拷贝之前**(拷贝仍负责刷新内容;迁移只负责归位)。预期:真升级日志变为 `migrated 15 … kept 0`。幂等、新装零影响。
- **F2 双存语义强化(推荐,防御)**:`kept` 分支对名单内框架名改为**移除平铺旧副本**(计数 `removed_stale`)。理由:名单门=框架所有(用户技能永不入名单,红线不受影响);"双存"状态在新语义下不可能由正常升级产生,保留只会喂养隐形性违背。同步修订 `tests/contract/test_flat_internal_skill_migration.py` 的 both-exist 用例期望。
- **F3 端态回归测试(必做)**:新增升级仿真级契约测试——伪 resource 树 + 伪旧装(平铺 15 内部名 + 用户技能)→ 跑两层拷贝 + 清理/迁移 → 断言端态:平铺内部名 = 0、nested = 15、用户技能在、副本引用 = 运行时形。本 note §1 的仿真结果即其**红先行样本**(先红后绿)。

## 4. 消费者升级操作(草案,将并入 `docs/tutorials/installation.md` 升级节)

1. 升级命令(对既有项目,保持本地内容):`specify init . --force --ai <tool>`(幂等;用户内容与 memory 存量不被覆盖)。
2. 升级后核对(一键):见 §5 片段——① 无平铺内部名残留;② `.specify/skills/internal/` 15 个可解析;③ 用户技能原样;④ 建议重跑 `/speckit.instructions`(刷新指令面与 `skills.md` 说明文档)。
3. 回滚:升级仅增改框架文件 + 回收框架残留;用户内容不动,git 基线可回退。**注意**:旧版工具目录里残留的旧命令副本会在升级时被重生成覆盖(预期行为)。

## 5. 验证片段(附给 release notes)

```bash
# 升级后自检:应输出 OK(平铺内部名应为 0;nested 应为 15)
INT="collect-evidence create-agent create-team create-tools improve-agent improve-team improve-tools memory-recall memory-record self-improvement summarize-project archive-session code-review manage-agents study-project"
bad=0; for n in $INT; do [ -e ".specify/skills/$n" ] && { echo "STALE-FLAT: $n"; bad=1; }; [ -f ".specify/skills/internal/$n/SKILL.md" ] || { echo "MISSING-NESTED: $n"; bad=1; }; done
[ "$bad" = 0 ] && echo OK || echo "NEEDS-ATTENTION"
```

## 6. 机制审计矩阵(仓内 + 消费者)

| 机制面 | 仓内 | 消费者(升级后) |
|--------|------|----------------|
| sync-mirrors / regen 引擎 | ✅ 0/0 | n/a(不随行) |
| 门控扫描(≤23 预算) | ✅ 23 | n/a |
| CLI 升级路径(拷贝/迁移/清理) | ✅(F1–F3 已落地,经 S2 独立验证) | ❌ 平铺残留(F1 修) |
| 命令副本(四/各工具) | ✅ 运行时形 | ✅ 重生成 |
| 技能发现(一层扫描) | ✅ 守卫两条+红绿 | ✅(F1 修复后与仓内一致) |
| 部署脚本(bash) | ✅ runtime-first 梯 | ✅ |
| 探针注册(feedback/history) | ✅ 按名引用 | ✅ |
| 渲染 agents | ✅ | ✅ init 重渲("rendered 2") |
| `.specify/skills.md`/instructions | ✅ 已更新 | ⚠️ create-if-absent:老文件保留 → 建议重跑 /speckit.instructions |
| 退役清理(_OBSOLETE_*) | ✅ | ✅ removed 4 |
| register/goal/teams 记录面 | ✅(c7 行 open 见 register) | n/a |

## 7. 复现(仿真脚本)

```bash
# 1) 基线旧消费者(已存在:/tmp/sk-consumer-probe,0.0.22 平铺安装)
# 2) 构建本仓 wheel 并装独立 venv:
pip wheel --no-deps --no-build-isolation --wheel-dir /tmp/sim-wheel .
python3 -m venv --system-site-packages /tmp/sim-venv && /tmp/sim-venv/bin/pip install -q --no-deps --force-reinstall /tmp/sim-wheel/*.whl
# 3) 升级仿真(含用户技能红线用例):
cp -r /tmp/sk-consumer-probe /tmp/upgrade-sim && mkdir -p /tmp/upgrade-sim/.specify/skills/my-own-skill && printf -- "---\nname: my-own-skill\n---\n" > /tmp/upgrade-sim/.specify/skills/my-own-skill/SKILL.md
cd /tmp/upgrade-sim && /tmp/sim-venv/bin/specify init . --ai qoder --force --no-git --ignore-agent-tools
```

## 8. 边界与遗留

- 本方案**未含**发布工程项:版本号升位(当前仍 0.0.22)、release notes 正文、`_source_commit.json` 校验说明——随发布流程落。
- c7 窗口项、暂存泄漏治理:见 `.specify/memory/register.md` c7 行(另案,不阻塞本方案)。
- `kept` 计数语义若保留(F2 未采纳时),须在 release notes 明示"平铺内部残留属已知项 + 手工回收命令",**不推荐**。(F2 已采纳,本条条件不再成立,留作历史。)

## 9. 发布清单(草稿)

> 状态:成稿待发布流程消费;本节为占位清单,不自动触发任何动作。

- **版本升位**:0.0.22 → 0.0.23(`pyproject.toml` `version`;2026-10-11 实测当前 0.0.22)。
- **release notes 要点**:
  1. 升级命令:`specify init . --force --ai <tool>`(幂等;用户内容与 memory 存量不被覆盖,见 §4);
  2. 自检片段:§5 一键脚本(期望输出 `OK`:平铺内部名 0 / `internal/` 15 个齐 / 用户技能原样);
  3. 建议:升级后重跑 `/speckit.instructions` 刷新指令面(`skills.md`/`tools.md` 为 create-if-absent 语义,老文件不会自动刷新,见 §6 对应行)。
- **提交/推送步骤(占位,发布时执行)**:① 提交引擎与测试改动(F1/F2 落 `src/specify_cli/__init__.py`;F3 落 `tests/contract/test_upgrade_end_state.py` + `tests/contract/test_flat_internal_skill_migration.py` 用例修订);② 版本升位提交;③ 构建与发布(`pip wheel` 构建;uv tool / pipx 安装渠道);④ 分支与推送依 `docs/git-workflow.md` 管理块(git-utils 技能 scope)。
- **已知遗留**:
  - c7 窗口项(中立性预算红,另案、不阻塞发布):见 `.specify/memory/register.md` c7 行——待 053 流程的刻意重锚/复核裁定;
  - 并发会话的 merge-skills 批次(`skills/external/merge-skills/**` + 其 `.specify/skills/` 镜像 + evidence 归档)独立归其所属流程,不并入本发布批次;
  - `_source_commit.json` 校验说明(§8 边界项)仍待随发布流程落。
