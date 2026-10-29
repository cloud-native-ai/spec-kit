# Checklist Stage Checks — 077-doc-sdd-integration

**Stage**: checklist | **Date**: 2026-10-30 | **Branch**: `077-doc-sdd-integration` | **HEAD at run**: `af15468e` | **Working tree**: clean before this stage
**Companion artifact**: [`checklists/readiness-2026-10-30.md`](../checklists/readiness-2026-10-30.md)（40 项 / pass 21 / fail 19）
**Purpose**: 记录本阶段全部确定性读数与规格侧证据锚点的实测来源。除本文件与清单外，本阶段未修改任何文件。

## 1. Prerequisite（`check-prerequisites.sh --json`）

首次直跑失败（环境变量未设）：

```text
Error: CWS_LIB_BASH_HOME environment variable is not set.
Dependency check failed. Initializing dependencies are required.
```

显式设 `CWS_LIB_BASH_HOME=/Users/liuqiming.lqm/project/cloud-native-tools/cws-lib-bash` 后：

```json
{"REQUIREMENTS_DIR":"/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/077-doc-sdd-integration","REQUIREMENT_ID":"077","FEATURE_ID":"077","FEATURE_NAME":"项目文档的 SDD 接入（特性级类别与文档型阶段门禁）","AVAILABLE_DOCS":["research.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md"],"MODE":"C","WRITABLE":true}
```

rc=0。`REQUIREMENTS_DIR` 已解析为绝对路径。

## 2. Structure check（本阶段强制项）

命令：

```bash
python3 scripts/python/validate-requirements.py .specify/specs/077-doc-sdd-integration/requirements.md
```

逐字输出：

```text
file: .specify/specs/077-doc-sdd-integration/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 256 lines, 33 definition rows, 6 shared strings
0 error(s), 0 warning(s)
```

rc=0。五项命题全 pass。

## 3. Requirement counts（attributes used by the checklist）

```text
$ grep -cE '^- \*\*FR-[0-9]{3}\*\*:' requirements.md   → 25
$ grep -cE '^- \*\*SC-[0-9]{3}\*\*:' requirements.md   → 8
$ grep -cE '^### User Story' requirements.md            → 4
$ grep -cE '^\| .STR-[0-9]{3}.' requirements.md          → 6
```

## 4. Baseline probes（spec 侧「今天仍红」的起点）

### 4.1 `spec:` key on the existing engine

```bash
python3 scripts/python/flow-class-check.py --action lookup --unit-id "spec:077-doc-sdd-integration"
```

```text
invalid unit id 'spec:077-doc-sdd-integration': expected /speckit.<stem> or skill:<dir>
unit_id: spec:077-doc-sdd-integration
flow_class: execution
source: default
marker: null
basis: null
neutral: false
```

rc=2。与 `requirements.md` § 现状锚点、`quickstart.md` S1 的实测一致；`research.md` R-2 的键族尚不存在。

### 4.2 `--action structure` does not exist

```bash
python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/077-doc-sdd-integration
```

```text
doc-consistency-check.py: error: argument --action: invalid choice: 'structure' (choose from 'verify')
```

rc=2。`research.md` R-4 的「`--action` choices 从 `("verify",)` 扩为 `("verify","structure")`」与此对应。

### 4.3 Seven templates are unwired

```bash
for f in requirements clarify plan tasks checklist analyze implement docs humanize; do
  printf '%s=' "$f"; grep -c -E 'flow-class-check\.py' "templates/commands/$f.md"
done
```

```text
requirements=0
clarify=0
plan=0
tasks=0
checklist=0
analyze=0
implement=0
docs=1
humanize=0
```

七个阶段模板零命中；正控 `docs.md` 为 1。与 `research.md` R-7 和 `tasks.md § Measured Premises` 的同形读数一致。

### 4.4 No plan-side carrier for the four subsections

```bash
grep -n "Document Structure\|Chapter Tree\|Reader Baseline\|Evidence List\|Fact Owners" \
  templates/plan-template.md templates/commands/plan.md templates/commands/implement.md
```

无输出（零命中）。`tasks.md` 的源编辑面（T006 / T010 / T011 / T004 / T007 / T008 / T014 / T015 / T017–T020）也不含 `templates/plan-template.md`——CHK022 的实测依据。

### 4.5 The two "engine absent" constructions

```bash
python3 /nonexistent/flow-class-check.py --action lookup --unit-id "spec:077-doc-sdd-integration"; echo rc=$?
python3 scripts/python/flow-class-check.py --repo /nonexistent --action lookup --unit-id "spec:077-doc-sdd-integration"; echo rc=$?
```

```text
.../Python: can't open file '/nonexistent/flow-class-check.py': [Errno 2] No such file or directory
rc=2
repository root is not a directory: /nonexistent
rc=2
```

两种构造 rc 都是 2，但都不打印 `owner-unavailable`；SC-002 Source 只写「把引擎路径指向不存在的位置」，没有指定是哪一种——CHK009 的实测依据。

## 5. 069 is untouched

```bash
git diff --stat c1cd4600..HEAD -- \
  .specify/specs/069-execution-expression-sdd \
  .specify/memory/features/069.md \
  .specify/memory/features/069a.md \
  .specify/memory/features/069b.md
```

无输出（空 diff）。`features.md` 的 069 行状态为 `Implemented`（`grep -n "069" .specify/memory/features.md` 第 78 行）。

## 6. Invariant probes

### 6.1 Command inventory

```bash
ls templates/commands/*.md | wc -l
```

```text
27
```

与 `research.md` R-8 的「27 模板 / 52 技能」分母一致。

### 6.2 `--faces` stays four

`scripts/python/doc-consistency-check.py:42`：

```text
FACES = ("reader", "evidence", "duplicate", "count")
```

`scripts/python/doc-consistency-check.py:952`：

```text
parser.add_argument("--action", default="verify", choices=("verify",))
```

### 6.3 Confirmation-gate budget

```bash
python3 scripts/python/scan-confirmation-gates.py --summary
```

```text
blocking confirmation gates: 27
  destructive: 20
  governance_kept: 7
violations (reversible gates still blocking): 0
```

与 `research.md` R-12 的实测一致（27，零整数余量）。**无** 077 的 FR / SC / 契约 / 任务重跑此读数；既有守卫只覆盖四个具名面（`goal` / `instructions-template` / `feedback-step` 等）并把总量上限写成 `cap = baseline["total"] * 0.25`（`tests/contract/test_confirmation_gates_sweep.py:166`），+1 不会转红。CHK039 的依据。

### 6.4 Feature registry derived counts

```text
.specify/memory/features.md:86    → 25 FR / 8 SC / 4 user stories / 2 shared strings
.specify/memory/features/077.md:28 → 25 FR / 8 SC / 4 用户故事 / 2 Shared Strings
validate-requirements.py           → 6 shared strings
```

CHK040 的依据：登记面 2 vs 规格面 6，且 T024 不含计数校准步。

## 7. Checklist verdict derivation

| 分节 | 条目 | 判定依据（本文档中的实测/引文来源） |
|------|------|--------------------------------------|
| A 声明行 | CHK001–006 | §3 STR-001；`requirements.md` 第 6 行；E3 / C-003 / C-006 / FR-004 / FR-005 |
| B 解析引擎 | CHK007–011 | §4.1；C-002/C-004/C-006；E2 表 9 字段 vs「八项」；`action_lookup` 的 `UNIT_ID_RE` 先于 `parse_owner` |
| C 七模板 | CHK012–016 | §4.3；C-003/C-007；R-9；`tasks.md § Measured Premises` 七条 SHA-256 |
| D 文档结构 | CHK017–023 | §4.2、§4.4；STR-003…006；E6 码表；`--spec-dir` 单输入；Clarifications 第 5 条 |
| E 驱动槽位 | CHK024–031 | C-001/C-004/C-006/C-007 (driver)；FR-017 vs 算子表 implement 两行；E7 无哈希；E8 `rc`；`FACES` 四面 |
| F 回退 | CHK032–035 | FR-009 / FR-024；E3 的降级记录；E9 三元组 |
| G 不变量 | CHK036–040 | §5、§6.1–§6.4 |

## 8. Same-author disclosure

本 run 无断点，被评工件与评分者同一作者；执行环境未暴露子代理派发工具。按 `.specify/shared/workflow/objective-analysis-gate.md` §7，清单的每一行都带 `(detected: direct read, subagent unavailable)`；本文档的确定性读数（第 2–6 节）属 program validators / 测量步骤，不在该降级范围内。

## 9. Zero-modification attestation

本阶段只新建两个文件：

- `.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md`
- `.specify/specs/077-doc-sdd-integration/test-evidence/checklist-stage-checks.md`

`requirements.md` / `plan.md` / `data-model.md` / `contracts/` / `tasks.md` / `quickstart.md` / `research.md` / `feature-ref.md` 均未改动；无 `PLAN-EDIT` 声明。
