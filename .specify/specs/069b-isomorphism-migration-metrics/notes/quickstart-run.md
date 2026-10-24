# Quickstart Run — 069b

**Owner**: T009（场景 1 / 场景 2）；场景 3–6 与 docs-sync 由各自任务行（T013 / T023 / T025）按同一形态追加。
**Run date**: 2026-10-25 · **Tree**: 场景 1 / 2 的工作树基于 `c38b44cc`，场景 6 基于 `efe63551` 加 US2 改动（`069b-isomorphism-migration-metrics`），各节输出均在提交前实跑取得。
**Interpreter**: pytest 仅 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest` 可用；引擎用系统 `python3`。

---

## 场景 1 — 逐行核对同构映射（route b）

命令与真实输出（`stages = 8`、`gates = 6`、`findings = []`、退出码 0）：

```
$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json
{
  "action": "isomorphism",
  "checked_at": "2026-10-24T17:17:24Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "stages": 8,
  "gates": 6,
  "findings": [],
  "error": null
}
EXIT=0
```

```
$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format text
flow-class isomorphism: 8 stage row(s), 6 gate face(s), 0 finding(s)
EXIT=0
```

**逐行核对记录**（8 行 × `强制状态` 真实性；blocking 行取自 `shared/workflow/expression-gates.md` § 阶段算子表，16 行 / 6 面）：

| 阶段 | 强制状态 | 强制门禁 | 该阶段存在的 blocking 算子行（对应面） |
| --- | --- | --- | --- |
| requirements | 已强制 | `requirements-clarity`、`evidence-asof` | requirements-clarity、evidence-asof |
| clarify | 已强制 | `requirements-clarity`、`reader-purpose` | requirements-clarity、reader-purpose |
| plan | 已强制 | `fact-consistency`、`structure-links-build` | fact-consistency、structure-links-build |
| tasks | 已强制 | `fact-consistency`、`evidence-asof` | fact-consistency、evidence-asof |
| checklist | 已强制 | `reader-purpose`、`fact-consistency` | reader-purpose、fact-consistency |
| analyze | 已强制 | `fact-consistency`、`review` | fact-consistency、review |
| implement | 已强制 | `structure-links-build` | structure-links-build（`reader-purpose` 在本阶段只有 advisory，未被点名） |
| review | 已强制 | `review`、`fact-consistency` | review、fact-consistency |

核对结论：8 行全部 `已强制`，每行点名的每个 `(阶段, face)` 在该阶段都有一行 `阻断级别 = blocking` 的算子行；未出现「借别阶段 blocking 背书」的行；`已声明未强制` 在本版不出现（8 个阶段都有 blocking 算子，标成未强制反而是失真）。

---

## 场景 2 — 标注失真必须转红（route b）

注入在 `tmp_path` 的 owner 副本上进行（复制真实 owner / gate owner / 名册，MUST NOT 把仓库改坏再改回），每项由一支契约测试断言「引擎退出码 1 且 finding kind 命中」。

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_isomorphism_map.py \
    -q -p no:cacheprovider -k injected
8 passed, 15 deselected
EXIT=0
```

| 注入 | 期望 kind | 执行测试（nodeid 后缀） | 结果 |
|------|-----------|--------------------------|------|
| `implement` 行 `强制门禁 = reader-purpose`（该阶段只有 advisory） | `annotation-false-enforced` | `test_injected_false_enforced_turns_red` | passed |
| `requirements` 行改 `已声明未强制`（该阶段有 blocking） | `annotation-false-unenforced` | `test_injected_false_unenforced_turns_red` | passed |
| `plan` 行同时清空 `强制门禁` 与 `强制状态` | `slogan-row` | `test_injected_slogan_row_turns_red` | passed |
| 删掉边界 (c) | `boundary-missing` | `test_injected_boundary_missing_turns_red` | passed |
| 边界 (c) `门禁处理` 不写 face id | `boundary-unbound` | `test_injected_boundary_unbound_turns_red` | passed |
| 边界 (b) `为什么不能互换` 置空 | `boundary-malformed` | `test_injected_boundary_malformed_turns_red` | passed |
| `tasks` 行结构格加入「按扩展名判定」 | `medium-axis-in-map` | `test_injected_medium_axis_phrase_turns_red` | passed |
| 阶段算子表追加一行 `pytest -q tests/` | `code-operator-in-expression-gates` | `test_injected_code_operator_turns_red` | passed |

判读：每种注入各自转红、退出码 1；真实树同一命令退出码 0（场景 1），因此红不是环境噪声。

---

## 场景 6 — 迁移与分发（未刷新零调用点 / 刷新同包原子 / 三快照名字级零新增失败）

**Owner**: T011（四类载荷实测）、T012（三快照）、T013（未刷新形态复核）
**Run date**: 2026-10-25 · **Tree**: 工作树基于 `efe63551`（`069b-isomorphism-migration-metrics`）加本阶段改动（提交前实跑）。

### 6.1 未刷新形态：零调用点（只读复核）

```
$ git show f0df3d0b:templates/commands/docs.md | grep -cE -- "--action (check|delegation|faces|isomorphism)"
0
EXIT=1        # grep 无匹配，即 0 命中
$ git show f0df3d0b:templates/commands/humanize.md | grep -cE -- "--action (check|delegation|faces|isomorphism)"
0
EXIT=1
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
EXIT=0
```

当前树（即刷新源）同样是零调用点：`templates/commands/` 与 `skills/` 中引用 `flow-class-check.py` 的文件共 **2** 个
（`templates/commands/docs.md`、`skills/external/humanize/SKILL.md`），二者都只调 `--action lookup`；
四个动作（`check` / `delegation` / `faces` / `isomorphism`）的调用点数 = **0**。

```
$ grep -rn -- "flow-class-check.py" templates/commands/ skills/ | wc -l
2
$ grep -rnE -- "flow-class-check\.py.*--action (check|delegation|faces|isomorphism)" templates/commands/ skills/ | wc -l
0
```

判读：未刷新项目拿到的是旧命令副本与旧技能，它们不含新动作；本切片没有新增任何调用点（契约 C-1 / C-3）。

### 6.2 刷新后原子到位：四类载荷同一发行包

四条命令（2026-10-25 实跑；`tomllib` 用 profiles venv 解释器，系统 `python3` 是 3.9 无该模块）：

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python - <<'PY'
import tomllib
from pathlib import Path
cfg = tomllib.loads(Path("pyproject.toml").read_text())
fi = cfg["tool"]["hatch"]["build"]["targets"]["wheel"]["force-include"]
for k in ("shared", "scripts", "templates"):
    print(f'"{k}" = "{fi[k]}"')
PY
"shared" = "specify_cli/shared"
"scripts" = "specify_cli/scripts"
"templates" = "specify_cli/templates"
EXIT=0

$ grep -n 'shared_dest = project_path / "\.specify" / "shared"' src/specify_cli/__init__.py
2467:            shared_dest = project_path / ".specify" / "shared"
$ grep -n -A1 'resource_path / "shared"' src/specify_cli/__init__.py
2471:                resource_path / "shared",
2472-                shared_dest,

$ grep -n 'def _stage_skills\|"specify_cli/skills"\|_stage_skills(build_data)' src/hatch_build.py
42:def _stage_skills(build_data):
59:    build_data.setdefault("force_include", {})[str(staged)] = "specify_cli/skills"
78:        _stage_skills(build_data)
```

| 载荷 | 源 | 客户落点 | 实测证据 |
|------|----|----------|----------|
| 分类所有者（含映射与边界） | `shared/` | `.specify/shared/` | `"shared" = "specify_cli/shared"` + `src/specify_cli/__init__.py:2467` 的 shared 复制段 |
| 引擎 | `scripts/` | `.specify/scripts/` | `"scripts" = "specify_cli/scripts"` |
| 技能（本切片不改） | `skills/{external,internal}` | `.specify/skills/` | `src/hatch_build.py:42` 的 `_stage_skills` → `specify_cli/skills` |
| 命令副本（本切片不改） | `templates/commands/` | 每工具副本 | `"templates" = "specify_cli/templates"` + `regen-command-copies.py --check` = `OK` |

### 6.3 三个客户快照：名字级零新增失败

wheel 由本切片源码构建并暂存（预装 `specify` 的包内无 069a 载荷，不作刷新入口）：

```
$ python3 -m pip wheel . --no-deps -w ~/tmp/069b-wheel --trusted-host yum.tbsite.net
...
Successfully built specify-cli
Created wheel ... specify_cli-0.0.22-py3-none-any.whl
EXIT=0

$ python3 -m pip install --target ~/tmp/069b-pkg --no-deps --upgrade ~/tmp/069b-wheel/specify_cli-*.whl
Successfully installed specify-cli-0.0.22
EXIT=0

$ test -f ~/tmp/069b-pkg/specify_cli/shared/definitions/flow-class-definitions.md \
    && test -f ~/tmp/069b-pkg/specify_cli/scripts/python/flow-class-check.py
EXIT=0        # 两个载荷均在包内
```

三个快照都用 `git -C <project> archive <HEAD> | tar -x -C ~/tmp/069b-snap-<n>` 建立（原始项目零修改），
原始项目脏文件数在跑测前后一致：`xuanji-agent 195` / `xuanji-cli 548` / `xuanji-function 28`。

| # | 项目 | 快照 HEAD | 套件命令（取自 `notes/migration-samples.md`） | 刷新前 | 刷新后 | `comm -13` | 结论 |
|---|------|-----------|-----------------------------------------------|--------|--------|-----------|------|
| 1 | xuanji-agent | `3f68b62` | `PYTHONPATH=<snap>/src <proj>/.venv/bin/python -m pytest tests/ -q --tb=no -rf -p no:cacheprovider` | 0 nodeid（250 passed） | 0 nodeid（250 passed） | 空 | 零新增 |
| 2 | xuanji-cli | `a0c476d` | `go test ./... -json` | 2 nodeid | 2 nodeid | 空 | 零新增 |
| 3 | xuanji-function | `a2fad18` | `<proj>/.venv/bin/python -m pytest -q --tb=no -rf -p no:cacheprovider` | 套件未启动（collection 7 errors） | 套件未启动（同左） | not-evaluated（本机缺 `cws-lib-python`：`CWS_LIB_PYTHON_HOME` 未设、`cws_py_test` 不存在；`import cws_common / asiops / cws_daemon` 均 `ModuleNotFoundError`） | not-evaluated |

逐项目 nodeid 名集（`comm -13` 的输入）：

- **xuanji-agent**：before = ∅，after = ∅ → `comm -13` 输出 0 行。套件输出 `250 passed in 3.44s`（before）/ `250 passed in 2.97s`（after）。
- **xuanji-cli**：before 与 after 都是同一集合 `xuanji-cli/cmd/xuanji-cli::TestLoginDefaultIsBucSilentChain` +
  `xuanji-cli/cmd/xuanji-cli::package`（`go test -json` 的两个 fail 事件：一个测试、一个包级失败）→ `comm -13` 输出 0 行。
- **xuanji-function**：刷新前后都以 `Interrupted: 7 errors during collection` 退出 2，**没有任何测试 nodeid**；
  按契约 C-8 记 `not-evaluated` + reason，**不记 0 新增失败**（套件入口依赖的 `cws-lib-python` 不在本机，
  冻结命令与项目自有 wrapper 都不可启动；不以人工 `cp` 或换套件冒充刷新）。

刷新执行（同一发行包；三项目都用其既有 AI 工具 `qoder`）：

```
$ cd ~/tmp/069b-snap-N \
    && PYTHONPATH=~/tmp/069b-pkg /Users/liuqiming.lqm/project/profiles/.venv/bin/specify init . \
       --here --force --ai qoder --no-git --ignore-agent-tools
...
Project ready.
EXIT=0
```

刷新后三快照的 `.specify/shared/definitions/flow-class-definitions.md` 与
`.specify/scripts/python/flow-class-check.py` 均在位（`test -f` 均退出 0）；
owner 内 `同构映射（8 阶段 × 3 面）` 命中 2（开篇 owns 项 + 章节标题），`069b 承接` 命中 0。

### 6.4 本阶段的裁定与假设（均按 tasks 原文裁决）

- **P4 只收敛被枚举的 10 处**：判据 `:35`（现 `:34`）1 处、台账说明 1 处、台账 `notes` 8 处，全部改为
  `contracts/ledger-reconciler.md` C-7。`:47` 的「规范条款归 069b」属 069a 的 § 判定依据表（判据正文），
  且 069b 已落盘，不再是悬空指针——按「不改 069a 判据正文」保留。
- **P2 的 `:19` 交接行**已由 US1 的 T006 删除，本阶段未再触碰。
- **xuanji-function 的 `not-evaluated` 是环境事实，不是零回归证据**：C-8 明确允许该降级，且禁止把
  「套件没跑起来」记成 0 新增失败；SC-002 的机器侧结论因此是 2 个 measured + 1 个 not-evaluated。
