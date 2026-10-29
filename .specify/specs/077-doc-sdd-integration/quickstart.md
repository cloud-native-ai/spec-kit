# Quickstart: 项目文档的 SDD 接入

**Feature**: 077-doc-sdd-integration
**Spec**: [requirements.md](requirements.md) · **Plan**: [plan.md](plan.md)
**Note**: 每个可执行示例都标注了 **Premises**（该示例所依赖的、本阶段无法执行验证的假设：flags、ID 形态、
文件位置、工具行为）与 **Pinned by**（把「实施后的期望结果」钉住的契约测试）。带「实测」标记的输出是本次
规划会话真实跑出来的；其余示例当前**尚不可执行**，其期望结果只由 `Pinned by` 指名的测试负责，
本文件不替它们背书。

前置（所有示例共用）：仓库根 = `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`，
解释器 = `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`。

## S1 — 解析一条特性线的类别（今天：红；实施后：绿）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/flow-class-check.py \
  --action lookup --unit-id "spec:077-doc-sdd-integration"
```

**实测（2026-10-30，实施前）**：

```text
invalid unit id 'spec:077-doc-sdd-integration': expected /speckit.<stem> or skill:<dir>
unit_id: spec:077-doc-sdd-integration
flow_class: execution
source: default
marker: null
basis: null
neutral: false
# exit 2
```

**实施后期望**：退出码 0，`source: declaration`，`flow_class` 等于本线声明行的取值，`marker: null`，`basis: null`。

**Premises**：键文法 `^spec:[a-z0-9][a-z0-9-]*$`；解析位置 `<repo>/.specify/specs/<name>/requirements.md`；
本线声明行为 `**Flow Class**: execution`（A6）。
**Pinned by**：`tests/unit/test_flow_class_spec_key.py`。

## S2 — 三例判定：已声明 / 未声明 / 取值越界

三例都用临时仓库树 + `--repo`，不往真实 `.specify/specs/` 写夹具。**临时树必须自带 owner 文档**：
解析入口先解析 owner（`shared/definitions/flow-class-definitions.md`，相对 `--repo`），树里没有它时三例
会一起降到退出码 2（`owner-unavailable`）——那是「机制缺席」的形态，不是本场景要判的三态。

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
TMP=$(mktemp -d)                       # 临时根，用完即删
mkdir -p "$TMP/.specify/specs/fx-declared" "$TMP/.specify/specs/fx-absent" "$TMP/.specify/specs/fx-bad"
mkdir -p "$TMP/shared/definitions"     # ← 补 owner：缺这行三例会同时降级
cp shared/definitions/flow-class-definitions.md "$TMP/shared/definitions/"

printf '# fx\n\n**Flow Class**: expression\n' > "$TMP/.specify/specs/fx-declared/requirements.md"
printf '# fx\n'                                > "$TMP/.specify/specs/fx-absent/requirements.md"
printf '# fx\n\n**Flow Class**: expressive\n'  > "$TMP/.specify/specs/fx-bad/requirements.md"

for name in fx-declared fx-absent fx-bad; do
  /Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/flow-class-check.py \
    --repo "$TMP" --action lookup --unit-id "spec:$name"; echo "exit=$?"
done
rm -rf "$TMP"
```

**实施后期望**（2026-10-30 实跑）：`fx-declared` → `expression` / `source: declaration` / exit 0；
`fx-absent` → `execution` / `source: default` / `marker: <069 默认标记>` / `error.label: declaration-absent`（advisory）/ exit 0
（这一行是「任何无该字段的线」——引擎不区分存量/新增——不阻断；它与「机制降级」的差别在 `error.label` 上可见）；
`fx-bad` → `flow_class: null` / `source: declaration` / stderr 一行 `<code>: <path>:<line> carries 'expressive', …` /
**exit 1**（不是 2）。三例各答不同，且 `fx-absent` 与降级形态的标签不同。

**裸树形态（不补 owner）**：三例一起返回 `flow_class: execution` / `source: default` / `marker: null` /
`error.label: owner-unavailable`（stderr 点名 owner 文档不存在）/ exit 2——这是 FR-009 / C-012 的降级分支，
**不是**本场景的三态判定；默认类别在场而 `owner-unavailable` 在 `error.label`，因此它不会被读成「作者未声明」。
「退出码 2 不带任何类别值」的现成样例是另一条路径：spec 目录或 `requirements.md` 不存在（`flow_class: null`，C-003）。

**Premises**：`--repo` 接受任意目录作为仓库根；**该根下必须有 `shared/definitions/flow-class-definitions.md`**
（或 `.specify/shared/…` 的同名副本），否则解析在 owner 一步就降级；三份夹具的 `requirements.md` 只需头部区即可解析；
`fx-bad` 的 `expressive` 落在封闭集之外。
**Pinned by**：`tests/unit/test_flow_class_spec_key.py`（退出码、记录与退出码 2 的标签）、
`tests/contract/test_flow_class_spec_declaration.py`（四个声明码）、
`tests/integration/test_expression_line_pilot.py`（把同样的「临时树 + 真实 owner」构造搬成夹具，八条阶段算子实跑）。

## S3 — 文档结构门禁（今天：`--action structure` 不存在）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/doc-consistency-check.py \
  --action structure --spec-dir .specify/specs/077-doc-sdd-integration
```

**实测（2026-10-30，实施前）**：

```text
doc-consistency-check.py: error: argument --action: invalid choice: 'structure' (choose from 'verify')
# exit 2
```

**实施后期望**：本线类别为 `execution`，故输出 `status: not-applicable`、打印 `class=execution source=declaration`
与被检查文件数，**退出码 0**，且**不**出现 `0 violation(s) passed` 一类措辞。

只做 plan 侧时输出 MUST 另标 `two-way: not-run`（不给 `--path` 就没有落文可比，缺省形态 MUST NOT 被读作两向通过）。
两向比对的形态是同一个命令追加既有 `--path`（不新增参数）：

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/doc-consistency-check.py \
  --action structure --spec-dir .specify/specs/077-doc-sdd-integration \
  --path .specify/specs/077-doc-sdd-integration/plan.md
```

一条表达类夹具线的期望（四子节齐备 → 绿；缺 `### Chapter Tree` → 结构语法族的
`subsection-missing`，`name=` 点名缺失子节）由 `Pinned by` 的契约测试负责。

**Premises**：`--action` 的 choices 从 `("verify",)` 扩为 `("verify","structure")`；`--faces` 四面取值集不变；
`not-applicable` 的呈现形态（`class=` / `source=` / 伴生量）。
**Pinned by**：`tests/contract/test_document_structure_gate.py`。

## S4 — 七个阶段模板是否已接线（今天：全 0）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
for f in requirements clarify plan tasks checklist analyze implement; do
  printf '%s ' "$f"
  grep -c -E 'flow-class-check\.py' "templates/commands/$f.md"
done
```

**实测（2026-10-30，实施前）**：七个模板各 `0`（正控：`templates/commands/docs.md` 为 `1`）。

**实施后期望**：七个模板各 `1`（子节内恰一次 lookup）；`docs.md` / `humanize.md` 不变。

**Premises**：子节内只出现一次引擎路径；子节标题固定、独占一个块（供剥离守卫使用）。
**Pinned by**：`tests/contract/test_stage_class_wiring.py`。

## S5 — 分发面漂移检查（今天即可跑）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --check
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/regen-command-copies.py --check
```

**实测（2026-10-30，实施前）**：两条命令均退出码 0（六对 `ok`；per-tool 副本与源模板一致）。
原始输出见 `test-evidence/plan-sync-mirrors-baseline.txt` 与 `test-evidence/plan-regen-command-copies-baseline.txt`。

**实施后期望**：仍退出码 0——本次改动全部落框架源，副本由再生成机制产出，判据是「相对上述基线无新增漂移」。

**Premises**：per-tool 命令副本目录的存在性由 `regen-command-copies.py` 实测（注册表最多六个目标，本仓当前四个：
`.claude/` / `.github/` / `.qoder/` / `.opencode/`；`.codex/` 与 `.hermes/` 目录不存在，故不产出，也不算漂移）；
`templates/commands/**` 不进 templates 镜像对。
**Pinned by**：`tests/contract/test_mirror_parity_suite.py`（既有）与 `tests/contract/test_stage_class_wiring.py`
（副本携带接线子节）。

## S6 — 两槽位审计对 `docs-gate-full` 的接纳（今天：已用夹具实测）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
D=.specify/.tmp/sdd-loop/tmp/plan077
mkdir -p "$D"            # .specify/.gitignore 已忽略 .tmp/
# 夹具：两行 docs-gate-full 槽位（baseline + closure），见 test-evidence/plan-audit-test-budget-docs-gate-probe.txt
/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  skills/external/sdd-loop-driver/scripts/audit-test-budget.py \
  --spine "$D/spine.md" --spec-dir .specify/specs/077-doc-sdd-integration --stage-check closure
```

**实测（2026-10-30）**：`slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=6 environment_failures=0`，
槽位层面**零违规**；`status=fail` 全部来自夹具未提供六阶段 E3 证据（与槽位内容无关）。负控（追加第二个
`baseline` 行）转红，证明该探针不是空绿。**计数读法**：`passed` 只数**算子级** `pass`，`failed` 只数算子级 `fail` / `not-evaluated`，
两者之和等于算子级行数；`not-applicable` 只出现在 `G-implement-structure` 的 `build` **子行**并面级单列——
MUST NOT 用「算子总数 − (`passed` + `failed`)」反推它（子行与算子级行不是同一计量单位）。

**实施后期望**：审计行为**不变**——这是「槽位只换内容」的验收点。

**Premises**：`selection_basis` 不做枚举校验（只校验在场）；`passed` / `failed` 只校验可解析为整数；
closure 的 `baseline_compare` 接受 `comm -13` 形态。
**Pinned by**：`tests/contract/test_docs_gate_driver.py`。

## S7 — 清理

S2 的 `mktemp -d` 目录由脚本内 `rm -rf` 清除；S6 的夹具目录 `.specify/.tmp/sdd-loop/tmp/plan077` 在
收尾时删除（`.specify/.gitignore` 的 `.tmp/` 规则已覆盖，`git status --ignored` 不应把它当新增）。
本 quickstart 不在仓库内留下任何永久工件。
