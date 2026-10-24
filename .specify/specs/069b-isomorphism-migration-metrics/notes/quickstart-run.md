# Quickstart Run — 069b

**Owner**: T009（场景 1 / 场景 2）；场景 3–6 与 docs-sync 由各自任务行（T013 / T023 / T025）按同一形态追加。
**Run date**: 2026-10-25 · **Tree**: 场景 1 / 2 的工作树基于 `c38b44cc`，场景 3 / 4 / 5 基于 `ed713ede` 加 US3 改动，场景 6 基于 `efe63551` 加 US2 改动（`069b-isomorphism-migration-metrics`），各节输出均在提交前实跑取得。
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

## 场景 3 — 台账的双注入必须给出两种可区分的红（route b，T023 实跑）

**Owner**: T019（`coverage` / `red_kind` / 三个新 kind）、T023（本场景取证）
**Run**: 2026-10-25 · `~/tmp/069b-t023/` 下两个由真实 `templates/` + `skills/` + owner 复制的夹具根，各注入一处缺陷；
仓库本身零改动（`--repo` 指向副本）。

```bash
python3 scripts/python/flow-class-check.py --action check --repo . --format json         # 真实树
python3 scripts/python/flow-class-check.py --action check --repo ~/tmp/069b-t023/check-gap --format json
python3 scripts/python/flow-class-check.py --action check --repo ~/tmp/069b-t023/check-parse --format json
```

真实树（C-2 的六个伴生量 + `clean`）：

```json
{
  "action": "check", "units": 78,
  "coverage": {"ledger_rows": 78, "inventory_units": 78, "matched": 78,
               "gaps": 0, "parse_errors": 0, "floor": 39},
  "red_kind": "clean", "findings": [], "error": null
}
EXIT=0
```

文本面（空集旁同时打印两个反空真伴生量，MUST NOT 只打印「0 findings」）：

```text
flow-class check: 78 unit(s) scanned, 0 finding(s) [matched=78 inventory_units=78, clean]
coverage: ledger_rows=78 matched=78 inventory_units=78 gaps=0 parse_errors=0 floor=39
EXIT=0
```

| 注入 | `red_kind` | 退出码 | `coverage` | 代表 finding |
|------|-----------|--------|------------|--------------|
| A 删一行台账（`/speckit.agents`） | `gap` | 1 | `ledger_rows=77 matched=77 gaps=1 parse_errors=0 floor=39` | `missing` ×1 |
| B 表头保留、数据行全删（解析出 0 行而清单非空） | `parse-failure` | 1 | `ledger_rows=0 matched=0 gaps=78 parse_errors=1 floor=39` | `ledger-truncated` ×1 + `missing` ×78 |

**判据**：两次运行的 `red_kind` 不同（`gap` ≠ `parse-failure`）；「静默绿」（退出码 0）样本数 = 0；
A 的 77 行仍在解析侧下限 39 之上，因此 MUST NOT 报 `ledger-truncated`（C-1 / C-4）；
`gaps = missing + unknown` 与 `parse_errors = row-malformed + ledger-truncated` 在两个副本上都成立（C-2）。
钉住契约：C-1 / C-2 / C-3；SC-003。

---

## 场景 4 — 委托关系由模板解析，不由人工清单（route b，T023 实跑）

**Owner**: T020（`--action delegation`）、T023（本场景取证）
**Run**: 2026-10-25 · 真实树 + `~/tmp/069b-t023/deleg`（把 `skill:analyze-artifacts` 改成 `expression`）。

```bash
python3 scripts/python/flow-class-check.py --action delegation --repo . --format json
python3 scripts/python/flow-class-check.py --action delegation --repo ~/tmp/069b-t023/deleg --format json
```

真实树：

```text
commands_scanned=27  edges=41  findings=0
verdicts={'same-class': 35, 'neutral-exempt': 6}
crossing neutral edge = ('/speckit.docs', 'skill:memory-record', 'expression', 'execution')
EXIT=0
```

证伪副本（反类技能必须转红）：

```text
findings=[('delegation-mismatch', '/speckit.analyze')]
edge={'command': '/speckit.analyze', 'skill': 'skill:analyze-artifacts',
      'command_class': 'execution', 'skill_class': 'expression',
      'verdict': 'mismatch', 'source_line': 41}
EXIT=1
```

**判读**：41 条边全部由命令模板文本解析（同一模板内同名去重），35 条同类、6 条类中立豁免；
6 条豁免中只有 `docs → memory-record` 两侧类别不同，因此「豁免先于同类判断」这一裁决顺序被真实样本覆盖（C-8）；
类中立清单取自 owner § 类中立清单，引擎内无清单副本（C-10）；真实树零人工 command→skill 表（C-9）。
钉住契约：C-8 / C-9 / C-10；FR-012。

---

## 场景 5 — 六面 owner 指针 6/6 且判据不搬家（route b，T023 实跑）

**Owner**: T021（`--action faces`）、T023（本场景取证）
**Run**: 2026-10-25 · 真实树 + 只读复核 `doc-consistency-check.py` 的 duplicate 面。

```bash
python3 scripts/python/flow-class-check.py --action faces --repo . --format json
python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate \
  --path shared/definitions/flow-class-definitions.md \
  --spec-dir .specify/specs/069b-isomorphism-migration-metrics --format json
```

```json
{
  "action": "faces",
  "checked_at": "2026-10-24T17:52:28Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "faces": 6,
  "findings": [],
  "error": null
}
EXIT=0
```

duplicate 面（主体集 = 分类 owner + 本 spec 的 formal artifacts；S3 比较集是 9 条 owner 路径，含
`shared/workflow/expression-gates.md` 本身）：

```text
{"action": "verify", "scope": {"paths": ["…/shared/definitions/flow-class-definitions.md"], "files_scanned": 13},
 "faces": {"duplicate": "pass"}, "findings": [], "count_check": {"status": "not-run", …}, "degradations": []}
EXIT=0
```

**判读**：§ 六面 恰好 6 行、face id 唯一、每行一个 `owner_pointer` 格（`+` 连接仍算一个绑定）；
9 条真实指针路径在源码根或 `.specify/` 镜像可解析，`§` 锚在目标文件有匹配标题；
六面之外零第二绑定表（C-12），判据正文副本计数为 0（C-13）。
钉住契约：C-11 / C-12 / C-13；SC-005。

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
| 3 | xuanji-function | `a2fad18` | `<proj>/.venv/bin/python -m pytest -q --tb=no -rfE -p no:cacheprovider`（前置：`CWS_LIB_PYTHON_HOME` 指向 `cws-lib-python`，PYTHONPATH 只加其 `src`；见 `migration-samples.md` 第二条更正） | 12 nodeid | 12 nodeid | 空 | 零新增 |

逐项目 nodeid 名集（`comm -13` 的输入）：

- **xuanji-agent**：before = ∅，after = ∅ → `comm -13` 输出 0 行。套件输出 `250 passed in 3.44s`（before）/ `250 passed in 2.97s`（after）。
- **xuanji-cli**：before 与 after 都是同一集合 `xuanji-cli/cmd/xuanji-cli::TestLoginDefaultIsBucSilentChain` +
  `xuanji-cli/cmd/xuanji-cli::package`（`go test -json` 的两个 fail 事件：一个测试、一个包级失败）→ `comm -13` 输出 0 行。
- **xuanji-function**：before 与 after 都是同一 12 个 nodeid（2 个 `FAILED` + 10 个 `ERROR`；10 条 MySQL fixture
  error + 2 条既有失败）→ `comm -13` 输出 0 行；套件输出 `2 failed, 165 passed, 1 skipped, 10 errors`
  （before 2.04s / after 2.09s）。套件 MUST 用项目自己的 cws-lib 环境启动（`CWS_LIB_PYTHON_HOME` + 只取
  `cws-lib-python/src`，**不取 `lib`**——其 vendored `platformdirs` 缺 `pytest_plugin.py`，会遮住 pytest 9.x 的插件入口），
  否则以 `ModuleNotFoundError: cws_common` 拒绝启动；环境细节见 `migration-samples.md` 的 2026-10-25 第二条更正。

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
- **xuanji-function 需要项目自己的环境入口**：冻结的 `.venv/bin/python -m pytest -q` 只有在
  `CWS_LIB_PYTHON_HOME` 指向本机 `cws-lib-python` 且 PYTHONPATH 只取 `src`（不取 `lib`）时才能启动；
  这是套件通道的环境事实，不改冻结样本、不记 `not-evaluated`，也不以人工拷贝冒充刷新。
  SC-002 的机器侧结论因此是 **3 个 measured（`comm -13` 均为空）**。

---

## 场景 7 — 三项基线只用既有仪器（route a）

本场景的**值与仪器归 `notes/expression-baseline.md`**（三行表 + 四条来源命令 + 「不可计部分」都在该文件，本节不复述数值，只留指针与完成状态）：四条通道命令全部 exit 0 可重跑；`gate_calls` / `confirmations`（门控观察 + clarify 轮次两个分项）/ `wall_clock` 均按 `contracts/measurement-instruments.md` C-6 记 `not-evaluated` + reason——不记 0、不记达成。起点仪器为 `git log --diff-filter=A --format='%h %as' -- requirements.md`（`f0df3d0b 2026-10-24`）。

---

## docs-sync — 文档同步评估与结构面复核（T025）

评估程序按 `.specify/shared/workflow/docs-step.md` § Evaluation procedure 逐步执行；本节记录判定与两段真实输出。

### 本切片产生了什么（Assess）

- owner 文档 `shared/definitions/flow-class-definitions.md` 新增 `## 同构映射（8 阶段 × 3 面）`、`## 不可同构边界` 与 `## 逐流程台账` 的 `**台账版本**` 声明；
- 引擎 `scripts/python/flow-class-check.py` 新增 `isomorphism` / `delegation` / `faces` 三个只读动作，`check` 扩展 `coverage` / `red_kind` / 两个新 kind；
- 三个客户快照的迁移证据与本切片自身的度量基线（`notes/expression-baseline.md`）。

### 逐篇判定（Conclude）

| 页面 | 是否失真 | 判定 |
|------|----------|------|
| `docs/reference/commands/docs.md` | 否 | 该页第 56 行的指针（069a 落盘）只声明「命令在阶段 1 之前做一次类别读取并执行文档型门禁算子」，并把台账与算子集的 owner 指到 `flow-class-definitions.md` / `expression-gates.md`；069b 改的是这两个 owner 的内部结构（映射、边界、台账版本、引擎动作），指针仍解析、未复述任何判据 → 无需改动 |
| `docs/reference/commands/humanize.md` | 否 | 069b 未改命令模板与技能接线（`templates/commands/`、`skills/` 零改动，`regen-command-copies.py --check` 仍 `OK`），该页描述的行为契约不变 → 无需改动 |
| `docs/concepts/*` | 否 | 该目录无流程分类 / 门禁主题页（全目录检索 `flow.class|flow_class|类别|expression-gates|文档型|执行类|表达类` 仅命中 `overview.md` 的一张文件计数表，与分类无关）→ 无需改动 |
| `docs/reference/{agents,cli,skills,teams}` | 否 | 无 `flow-class-check.py` 的引擎参考面（`grep -rn 'flow-class-check' docs/` 零命中）；三个新动作与 069a 的 `lookup` / `check` 一样不进入项目文档面 → 无需改动（不为此新建文档面） |

**结论**：`无需记录` —— 本切片不新增用户可见命令、不改变任何命令的对外行为、不新增门禁面；映射与边界是框架治理结构，其唯一载体已是 owner 文档，项目文档只保留指针（069a 已落）。按 docs-step 的红线，不为「看起来有产出」而制造文档改动。

### 结构面复核（`violations` 计数与 kind 集合相对 T001 基线零新增）

```bash
$ python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .
exit 0
{
  "violations": [
    { "kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/unit/test_qoder_support_matrix.py" },
    { "kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/integration/test_qoder_refresh.py" },
    { "kind": "note-frontmatter", "path": "docs/notes/type-follows-stage-misclassification.md", "detail": "missing: " }
  ]
}
```

与 `notes/pre-change-measurements.md` § 2 基线（`violations = 3`：`broken-link` 2 + `note-frontmatter` 1）**同计数、同 kind 集合、同路径**。判据是「零新增」，不是「转绿」：三条既有违规原样保留，未顺手修复。
