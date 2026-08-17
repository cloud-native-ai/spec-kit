# Implementation Plan: init 落章机制——以 commit id 为唯一标识的框架来源回溯(Framework Source Stamp)

**Branch**: `043-init-commit-stamp` | **Date**: 2026-08-17 | **Spec**: [requirements.md](requirements.md)  
**Requirement → Feature**: `043-init-commit-stamp` → Feature 045 Framework Source Provenance  
**Input**: Specification from `.specify/specs/043-init-commit-stamp/requirements.md`

## Summary

`specify init` 在目标项目落一份**框架来源标识**(默认 `.specify/source.json`,STR-001):记录产出本次脚手架的框架源码 **git commit id(完整 40-hex,唯一标识,不用正式版本号)** + 框架名(`spec-kit`,STR-003)+ UTC 时间戳;持有目标项目的人凭 id 在框架仓 `git show <commit>` 反向定位精确代码切片。技术路线:**单一 commit 探测函数 + 构建期嵌入 + init 末尾薄写入**——`src/specify_cli/__init__.py` 新增唯一权威的 `_probe_head_commit(start_dir)`(git 探测文法仅此一份)与 `resolve_source_commit()`(解析顺序 **checkout git 探测 > 构建期嵌入值 > unavailable 哨兵**,STR-002);新增仓根 `hatch_build.py` 自定义构建钩子(hatchling custom hook,经 importlib 复用同一探测函数)在构建时把源 commit 写入 `src/specify_cli/_source_commit.json`(随 wheel/sdist 分发,.gitignore);init() 在 "Project ready." 前调用 `write_source_stamp(project_path)` 落章——刷新即覆写、写入失败黄色告警不阻塞 init。三态语义(有效 commit / 显式 unavailable+原因 / 文件缺失=来源未知),零臆造。

## Technical Context

**Language/Version**: Python ≥ 3.8(CLI 现行约束,`pyproject.toml`);构建钩子为仓根 Python 文件  
**Primary Dependencies**: 零新增——typer/rich 既有;hatchling 为既有 build-backend(custom build hook 经 `[tool.hatch.build.hooks.custom]` 启用,hook 在构建隔离环境内运行,仅用 stdlib)  
**Storage**: 文件系统——目标项目 `.specify/source.json`(JSON,UTF-8,indent 2);构建嵌入值 `src/specify_cli/_source_commit.json`(随包分发,.gitignore)  
**Testing**: pytest——契约 `tests/contract/test_source_stamp.py` + `tests/contract/test_build_hook.py`,集成 `tests/integration/test_init_source_stamp.py`(沿 `tests/script_api.py` 的 `RUNNER.invoke(app, ["init", ...])` 与 conftest 最小资源夹具模式);实现前冻结基线(name 级)  
**Target Platform**: 跨平台 CLI(Linux/macOS/Windows);git 探测经 `subprocess.run(["git", ...], timeout=…)` 失败即降级,git 不存在不影响 init  
**Project Type**: CLI 工具 + 模板框架(single;本需求全部落在 CLI 包与构建链,不触模板/skills 面)  
**Performance Goals**: init 末尾一次文件写 + 至多一次有界 git 子进程调用(< 5s timeout);无性能敏感面  
**Constraints**: ① commit id 是唯一标识,pyproject `version` 不作标识键(FR-002);② 落章永不阻塞 init(失败=黄色告警,FR-005);③ `pyproject.toml` 在仓写门禁 confirm 名单——implement 期编辑需用户确认;④ 资源访问沿 `MODULE_DIR = Path(__file__).parent` 既有模式(L60),不引入 importlib.resources 新文法;⑤ 时间戳复用既有 `_utc_compact_stamp()`(L476,ISO-8601 basic 形如 `20260817T075305Z`)  
**Scale/Scope**: 改动面 = 1 个 CLI 模块文件(新增 3 函数 + init 内 1 调用点)、1 个新仓根构建钩子文件、pyproject 增 hook 声明与 .gitignore 一行、3 个新测试文件、1 处用户文档;无镜像面、无模板面

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划逐条由 requirements(3 US/8 FR/5 SC)推导;contracts ×3 与 data-model 逐 FR 对应 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 045(clarify 裁定新建,与 024 正交轴双向交叉引用);feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | 用户意图(目标项目可反查框架来源切片)编码为落章文件+回溯闭环,零新语法/零交互面 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 3 份 contracts 先行;实现前定稿契约断言(三态/覆写/非阻塞/嵌入),测试任务先于实现任务 |
| V | AI Agent Integration Standards | ✅ Pass | 全部判定确定性下沉 CLI 函数与构建钩子(程序优先);无 agent 判断面 |
| VI | Continuous Quality & Observability | ✅ Pass | 落章文件即来源可观测面;写入失败有告警留痕(yellow warning 沿 init 既有模式) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本文件为 plan 阶段产物;澄清 4 条已入 Clarifications,无 NEEDS CLARIFICATION 残留 |
| VIII | Code as the Single Source of Truth | ✅ Pass | git 探测文法唯一权威在 `_probe_head_commit`(构建钩子经 importlib 复用同一函数,零第二套);现状锚点以源码实测为准 |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 新增 1 个构建钩子 + 1 个嵌入文件 + 3 个运行时函数——均为 FR-004(分发形态可得)的必要最小落点 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 用户文档落 `docs/tutorials/installation.md`;嵌入文件命名 `_source_commit.json`(下划线前缀=包私有数据,不入保留名注册表) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制落在框架源(CLI+构建链);本仓自身 `.specify/` 将在下一次 init 刷新时获得落章(FR-007 存量路径);不为本需求强行重跑 init |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 时间戳复用 `_utc_compact_stamp`;git 探测单源复用(构建期/运行期/测试);测试夹具沿 conftest 既有最小资源模式 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 补齐 use→反馈→iterate 环的"use 端可观测":目标项目首次可回答"我用的框架是哪个切片" |

**Gates Status**: ⚠ 唯一 Partial 为原则 IX,属"新增最小确定性机制面"既定例外类别(同 042 先例),已列 Complexity Tracking 并给出被拒的更简替代;其余 12 项 Pass。

**Re-check after Phase 1**: 2026-08-17 — Phase 1 工件(data-model.md、contracts ×3、quickstart.md、feature-ref.md)落地后复核:IX 维持 Partial(钩子为 FR-004 契约钉死的必要面),其余不变;无新增 Fail/Partial。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/043-init-commit-stamp/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── source-stamp-resolution.contract.md
│   ├── source-stamp-write.contract.md
│   └── build-embedding.contract.md
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/          # requirements 校验清单(已存在)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings inlined below (internal investigation only, < 50 lines).

### Source Code (repository root)

```text
src/specify_cli/__init__.py          # +_probe_head_commit(唯一 git 探测文法)+resolve_source_commit(三态解析)+write_source_stamp(落章/覆写/非阻塞);init() 末尾 1 调用点
hatch_build.py                       # 新仓根 hatchling custom build hook:构建期经 importlib 复用探测函数,写 src/specify_cli/_source_commit.json
pyproject.toml                       # +[tool.hatch.build.hooks.custom] 声明(confirm 门文件)
.gitignore                           # +src/specify_cli/_source_commit.json(构建产物不入库)
docs/tutorials/installation.md       # 用户文档:「来源标识(source stamp)」小节(cat source.json → git show 回溯)
tests/contract/test_source_stamp.py  # 解析/写入契约(三态/40-hex/覆写零残留/哨兵+原因/写入失败告警)
tests/contract/test_build_hook.py    # 构建钩子契约(嵌入文件内容/unavailable 降级/复用同一探测函数)
tests/integration/test_init_source_stamp.py  # init 端到端(RUNNER.invoke + conftest 最小资源夹具;落章存在/刷新)
```

**Structure Decision**: 扩展既有"单模块 CLI + hatchling 打包"形态:不新增顶层目录(钩子文件挂仓根为 hatch 惯例),零模板/镜像面改动;运行时资源访问沿 `MODULE_DIR` 既有模式,嵌入文件与模板同路 Force-include 语义(位于包目录即随 wheel 分发)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

本需求**零镜像面**:改动文件(CLI 模块、仓根钩子、pyproject、.gitignore、docs、tests)均无镜像或再生副本——`src/specify_cli` 不在 sync-mirrors 对内,docs 单份,tests 单份。唯一"生成物" `src/specify_cli/_source_commit.json` 是构建产物(.gitignore,不入库、不需镜像)。

## Phase 0: Research Review

无 standalone research.md——以下勘察结论全部来自仓内实测(Explore 子代理,2026-08-17),供 Phase 1 直接引用:

- **init() 形态**(`src/specify_cli/__init__.py` L2442–2764):Typer 命令,目标路径 `project_path`(`--here` 取 cwd,否则 `Path(project_name).resolve()`);模块级 Rich `console`(L2225);**warn-but-continue 先例**充分——`tracker.error("features-dir", …)` mkdir 失败不中止(L2654)、git 不可用 `tracker.skip`(L2673)、git init 失败黄色告警+手工指引(L2700–2710);收尾序:…"Project ready."(L2697)→ git 告警 → 安全注 → Next steps——**落章调用点定在 "Project ready." 打印之前**。
- **运行时资源先例**:全仓无 importlib.resources/pkg_resources;统一 `MODULE_DIR = Path(__file__).parent.resolve()`(L60)+ `get_resource_path()`(L1268)判 `(MODULE_DIR/"templates").exists()`;wheel 经 `[tool.hatch.build.targets.wheel]` force-include 把 memory/scripts/templates/skills/agents/shared 映入包目录(L28–34)——包目录内文件天然随 wheel 分发,**嵌入文件放 `MODULE_DIR/_source_commit.json` 完全沿此模式**。
- **构建链**:`[build-system] requires=["hatchling"]`(L18–20),**无既有 build hook**;**仓内无 CI**(`.github/` 无 workflows/)——构建为本地 `hatch build`/等价,checkout 内 commit 恒可得;FR-004 的"构建期嵌入"落点即 hatch custom hook。
- **测试先例**:`tests/script_api.py` `RUNNER.invoke(app, ["init", *args])`(typer.testing CliRunner);集成测试沿 `copy_local_templates(project_path, ai, "sh")` + `monkeypatch.setattr("specify_cli.get_resource_path", lambda: fixture_path)`(conftest 提供 qoder/claude 最小资源夹具)——本需求集成测试直接 `RUNNER.invoke(app, ["init", <tmp 项目名>, "--ai", "qoder", "--no-git", ...])` + monkeypatch 夹具,断言 `<项目>/.specify/source.json`。
- **时间戳**:`_utc_compact_stamp()`(L476)输出 `20260817T075305Z`(ISO-8601 basic)——FR-003 的 UTC ISO-8601 由它满足,复用零新文法。
- **版本面**:CLI 无 `__version__`、无 `--version`;`0.0.22` 仅存在于 pyproject——落章是首个自标识工件,与正式版本号零耦合(佐证 FR-002 可零冲突落地)。
- **裁决**:无 /speckit.interview 必要——剩余设计决策(嵌入文件名/解析顺序/调用点/文档落点)均由规格 + 仓内约束唯一推导,已在 contracts 定约。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 原则 IX(新增构建机制面):仓根 `hatch_build.py` + 包内嵌入文件 `_source_commit.json` | FR-004 要求已安装分发形态(wheel/sdist——主流安装路径)也能获得真实 commit;wheel 内无 git 仓,运行时探测在该形态结构性不可得,唯一出口是构建期嵌入 | (a) 仅 checkout 直测 → wheel 用户(主流)一律落 unavailable 哨章,落章对其无价值,FR-004 需降级为 best-effort,违背需求意图;(b) 运行时网络反查远端版本 → 违背离线约束与"不承诺网络能力"的 Out of Scope;(c) 手工在发版时改文件 → 人肉步骤必漂移(忘记即永远 unavailable),机制化正是本需求目的 |
