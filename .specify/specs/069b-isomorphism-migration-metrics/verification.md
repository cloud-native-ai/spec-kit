# Verification Log — 069b-isomorphism-migration-metrics

**Run**: 2026-10-25 · branch `069b-isomorphism-migration-metrics` · run-start HEAD `5d5331b9`
**Scope of this run**: Polish 阶段 T024–T029（镜像与命令副本、文档同步评估、全量回归、SC 证据、特性登记、终局门禁）＋ T014–T018 复选框回填（产物已存在且 78 支全绿，只补状态位）＋ 一处跨切片一致性修正（墙钟起点仪器，见 §跨切片一致性修正）
**Review-fix (2026-10-25, F1/F4/F5)**: 映射强制声明改为引用级可证伪（`gate:<算子 id>`）、SC-005 测量面从 13 文件恢复到「四棵树 + 本轮 owner」、「刷新载荷冒烟」补入 SC-002。逐项证据见 §Review-fix F1/F4/F5。
**Review-fix (2026-10-25, F2/F3/F6 + P2 F7–F12)**: 跨切片改动显式登记（tasks/plan 同步更正「零改动」表述）、父状态按 Pre-Status-Flip 门推进 `Planned → Implemented`、三项基线按「仪器-对象缺口」如实降级（不记 0）、P2 六项逐条处置。逐项证据见 §Review-fix F2/F3/F6/P2。
**Owner of the record shape**: `.specify/templates/verification-log-template.md`（`SC-NNN_status=` 词表：pass \| fail \| partial \| deferred \| unknown）
**Owner of the failing-test names and count**: `notes/test-baseline-contract.txt`（本文件只记 `comm -13` 的结果，不复述数字为「当前实测」）

**Command convention**: 引擎一律 `python3 scripts/python/<engine>.py` 与 `python3 .specify/scripts/python/<engine>.py`（镜像等价）；pytest 一律 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（本仓 `.venv` 无 pytest，见 tasks.md § Environment Prerequisites）。

```text
baseline_commit=4710676297dcdbcaabb72f6dc7882abfae906006
baseline_date=2026-10-25
baseline_branch=069b-isomorphism-migration-metrics
implementation_date=2026-10-25
post_change_commit=<pin: 本文件落地提交的 SHA，由紧随的仅改本行的 pin 提交回填>
post_change_commit_pin=single-line follow-up commit; this run's log is landed by the commit named in post_change_commit
deferred_tasks=
```

`deferred_tasks=` 为空：29 个任务行全部 `[X]`，无 `[~]`。SC-004 记 `unknown` 是**测量样本不足**（两名独立判定者未执行），不是任务推迟；`not-evaluated` 只出现在该条的 value/note 行，不占状态位。

---

## §T024 — 镜像同步与逐对核验

```bash
$ python3 scripts/python/sync-mirrors.py --write --only shared --only scripts
scope --only: shared, scripts
DIFF  .specify/scripts/python/flow-class-check.py
sync  scripts/ -> .specify/scripts/ (1 files)
DIFF  .specify/shared/definitions/flow-class-definitions.md
sync  shared/ -> .specify/shared/ (1 files)
EXIT=0
```

```bash
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (396 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (112 files)
ok    shared/ == .specify/shared/ (55 files)
EXIT=0
```

```bash
$ cmp shared/definitions/flow-class-definitions.md .specify/shared/definitions/flow-class-definitions.md && echo "owner mirror identical"
owner mirror identical
$ cmp scripts/python/flow-class-check.py .specify/scripts/python/flow-class-check.py && echo "engine mirror identical"
engine mirror identical
```

```bash
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
EXIT=0
```

**判读**：相对 T001 基线（`notes/pre-change-measurements.md` § 1：六对全 `ok`、`scripts/` 112 / `shared/` 55）**零新增差异**；`templates/commands/` 零改动（命令副本 `OK` 即证）。069b 的两处新载荷（owner 文档的两章节 + 台账版本声明、引擎的三动作与 `check` 扩展）已投影到 `.specify/` 镜像，没有手改镜像。

**同批的第二次投影**：本轮的跨切片一致性修正改动了 `shared/workflow/expression-gates.md`，按同一机制再次 `--only shared` 投影（见 §跨切片一致性修正），最终 `--check` 仍为上面的六对全 `ok`。

**证据指针**：本节三段命令与输出；`notes/pre-change-measurements.md` § 1。

---

## §跨切片一致性修正 — 墙钟起点仪器（`git log -1` → `git log --diff-filter=A`）

**缺陷**：`shared/workflow/expression-gates.md` § 三项基线把 `requirements→analyze 墙钟` 的起点写成 `git log -1 --format=%cs -- <requirements.md>`，而 069b 契约 `contracts/measurement-instruments.md` C-1 要求首次提交且实测证明 `git log -1` **取最近一次触及**（2026-10-25 对 069b `requirements.md` 返回 `2026-10-25`，真实首次提交是 `f0df3d0b 2026-10-24`），二者矛盾。069a 的 C-9 已声明「仪器口径与 `not-evaluated` 降级的规范条款归 069b」，故该修正属 069b 权限内的一致化，不是改写 069a 判据。

**改动（三处，最小面）**

| 文件 | 改动 |
|------|------|
| `shared/workflow/expression-gates.md` | § 三项基线表格行改为 `git log --diff-filter=A --format='%h %as' -- <requirements.md>` 的首次提交 author date；冻结点条目补一句「起点 MUST 用 `--diff-filter=A` 取新增提交；MUST NOT 用 `git log -1`」 |
| `.specify/shared/workflow/expression-gates.md` | 镜像同步（`sync-mirrors.py --write --only shared`），`cmp` 同字节 |
| `tests/contract/test_expression_gates_doc.py` | C-9 的机械断言从字面 `git log -1 --format=%cs` 改为 `--diff-filter=A`（同一判据的仪器编码，判据语义「首次提交」不变；断言消息注明 069b C-1 为仪器 owner） |

```bash
$ git diff --stat shared/workflow/expression-gates.md
 shared/workflow/expression-gates.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_expression_gates_doc.py -q -p no:cacheprovider
..................                                                       [100%]
18 passed in 0.42s
EXIT=0
```

**未动的面**（可用 `git diff` 证）：六面表、调用点表、阻断级别与证据语法逐字未变；§ 阶段算子表的**算子文本 / 对应面 / 阻断级别**逐字未变。diff 只落在「三项基线」的表行与其后的冻结点条目（`33c47fd5`），以及 § 阶段算子表新增的 `算子 id` 列（`d8fc2bf9`，review-fix F1 为把 `已强制` 做成引用级可证伪而加）。069a 的其他判据（C-1…C-8、C-10…C-15）与断言**语义**均未改写。

**落地提交与登记（review-fix F2）**：本修正实际横跨两个提交——`33c47fd5`（`wall_clock` 起点仪器 + `tests/contract/test_expression_gates_doc.py` 的断言仪器重编码）、`d8fc2bf9`（同一 owner 的 `算子 id` 列 + 该列驱动的引用级断言）。旧记录把跨切片改动只写在 `verification.md` 与提交消息里，于是 `tasks.md` / `plan.md` 的「禁改面 / 本切片零改动 / 唯一 A-1」与树不一致；现已在两处登记（`tasks.md` § 跨切片一致性修正登记；`plan.md` § Constraint correction 与 § Mirror addendum），069a 的**规格目录**仍零改动。派发前提只给了一个提交号 `d8fc2bf9`，实测补全为上述两个：墙钟起点修正落在 `33c47fd5`，`d8fc2bf9` 是 `算子 id` 列与其断言。

**证据指针**：本节 `git diff --stat` 与 18 passed 实跑；`notes/expression-baseline.md` 表内 `wall_clock` 行已按同一仪器记录；`tasks.md` § 跨切片一致性修正登记（逐项授权与提交）。

---

## §T025 — 文档同步评估与结构面复核

按 `.specify/shared/workflow/docs-step.md` § Evaluation procedure 执行，完整评估记录（逐篇判定表与两段真实输出）落在 **`notes/quickstart-run.md` § docs-sync**。

**结论：`无需记录`。** 判定摘要：

- `docs/reference/commands/docs.md` 第 56 行的分类指针（069a 落盘）只声明「阶段 1 之前做一次类别读取并执行文档型算子」并把 owner 指到 `flow-class-definitions.md` / `expression-gates.md`；069b 改的是这两个 owner 的内部结构（映射、边界、台账版本、引擎动作），指针仍解析、未复述判据 → 无需改动。
- `docs/reference/commands/humanize.md`：069b 零改动 `templates/commands/` 与 `skills/`（命令副本 `--check` 仍 `OK`），该页行为契约不变 → 无需改动。
- `docs/concepts/*`：无流程分类 / 门禁主题页（全目录检索仅命中 `overview.md` 的一张文件计数表，与分类无关）→ 无需改动。
- 三个新引擎动作与 069a 的 `lookup` / `check` 一样不进入项目文档面（`grep -rn 'flow-class-check' docs/` 零命中，仓库无脚本参考面）→ 不为此新建文档面。

**结构面零新增**（T001 基线：`violations = 3`，`broken-link` 2 + `note-frontmatter` 1）：

```bash
$ python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .
{
  "violations": [
    { "kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/unit/test_qoder_support_matrix.py" },
    { "kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/integration/test_qoder_refresh.py" },
    { "kind": "note-frontmatter", "path": "docs/notes/type-follows-stage-misclassification.md", "detail": "missing: " }
  ]
}
EXIT=0
```

同计数、同 kind 集合、同路径。判据是「零新增」，不是「转绿」——三条既有违规原样保留，未顺手修复。

**证据指针**：`notes/quickstart-run.md` § docs-sync；本节 validate 输出。

---

## §T026 — 全量回归与红先证据完整性

```bash
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
    bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-after.txt \
    tests/contract tests/unit -q --tb=no -p no:cacheprovider
33 failed, 5219 passed, 5 skipped, 4 warnings in 344.09s (0:05:44)
EXIT=1
# failed-name list written: /Users/liuqiming.lqm/tmp/069b-names-after.txt (33 entries)

# 终态复跑（tasks 复选框、verification.md、features 落盘之后，同一判据）
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
    bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-final.txt \
    tests/contract tests/unit -q --tb=no -p no:cacheprovider
33 failed, 5219 passed, 5 skipped, 4 warnings in 334.34s (0:05:34)
EXIT=1
# failed-name list written: /Users/liuqiming.lqm/tmp/069b-names-final.txt (33 entries)
```

两次运行的失败名单逐名相同（`comm -13` 与 `comm -23` 均为空），故下列比对以终态复跑的 `~/tmp/069b-names-final.txt` 为准，判读同前。

失败名单与冻结基线做**名字级**比对（判据是名字不是条数）：

```bash
$ grep -v '^#' .specify/specs/069b-isomorphism-migration-metrics/notes/test-baseline-contract.txt \
    | sed '/^$/d' | sort > ~/tmp/069b-baseline-names.txt
$ sort ~/tmp/069b-names-final.txt > ~/tmp/069b-final-sorted.txt
$ comm -13 ~/tmp/069b-baseline-names.txt ~/tmp/069b-final-sorted.txt   # NEW failing node ids
（空输出；0 行）
$ comm -23 ~/tmp/069b-baseline-names.txt ~/tmp/069b-final-sorted.txt   # 基线内已转绿
（空输出；0 行）
$ wc -l < ~/tmp/069b-baseline-names.txt
33
```

**判读**：**NEW = 0**（`comm -13` 空）；预期内的既有红 33 条与冻结名单逐名相同，零条被顺手修掉、零条被掩盖。`pytest` 退出码 1 是既有红的正常反映（判据是名字级 `comm -13`，不是退出码 0）。通过数相对基线增加 128（= 069b 的 8 个新测试文件：US1 34 + US2 16 + US3 78），即新增测试全绿。

**红先证据完整性**（8 支测试各一条红跑 + 一条转绿，落点 `notes/red-first-evidence.md`）：

| 测试文件 | 红跑 | 转绿 |
|----------|------|------|
| `tests/unit/test_isomorphism_checker.py` | R1 | G1 |
| `tests/contract/test_isomorphism_map.py` | R2（合并红跑 R3） | G1 |
| `tests/contract/test_migration_distribution.py` | R4 | G5 |
| `tests/contract/test_ledger_reconciliation.py` | R5 | G6 |
| `tests/contract/test_delegation_classes.py` | R6 | G6 |
| `tests/contract/test_expression_faces.py` | R7 | G6 |
| `tests/contract/test_measurement_instruments.py` | R8 | G6 |
| `tests/unit/test_reconciler_extensions.py` | R9 | G6 |

缺项 = 0，无需补齐。US3 五支在收口轮复跑仍为 `78 passed`（`/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_ledger_reconciliation.py tests/contract/test_delegation_classes.py tests/contract/test_expression_faces.py tests/contract/test_measurement_instruments.py tests/unit/test_reconciler_extensions.py -q -p no:cacheprovider` → `78 passed in 7.55s`）。

**证据指针**：本节命令与两段 `comm` 输出；`notes/test-baseline-contract.txt`（名单 owner）；`notes/red-first-evidence.md` R1–R9 / G1–G6。

---

## §T027 — SC 证据矩阵

映射按 `tasks.md` § Requirement Coverage Map（SC-001 ← T006/T007/T009/T027；SC-002 ← T012/T013；SC-003 ← T019/T023；SC-004 ← T019/T027；SC-005 ← T021/T023）。状态取值只从 owner 模板的封闭集取；未测量的量显式降级，不记 0、不记达成。

- **SC-001** — 状态 **pass**（**引用级**）。真实树 `--action isomorphism --repo . --format json` 返回 `stages = 8`、`gates = 6`、`findings = []`、exit 0；8 个 `已强制` 行各带解析到该 `(stage, face)` 的 blocking `gate:<算子 id>` 引用（引用取自门禁 owner § 阶段算子表的 `算子 id` 列），逐行核对记录见 `notes/quickstart-run.md` § 场景 1；四类不可同构边界 a–d 各一次且 `门禁处理` 各绑 ≥1 个封闭 face id（契约测试覆盖）。失真可机械发现：引用级 5 种（`gate-ref-missing` / `gate-ref-unknown` / `gate-ref-malformed` / `gate-ref-not-blocking` / `gate-ref-mismatch`）＋ 行级/边界级 8 种（`annotation-false-enforced` / `annotation-false-unenforced` / `slogan-row` / `boundary-missing` / `boundary-unbound` / `boundary-malformed` / `medium-axis-in-map` / `code-operator-in-expression-gates`）各自转红、退出码 1。**不声称**：24 格自由文本的语义真实性（那一层归评审面 C-10）。未标注行 = 0、引用级失真行 = 0。
- **SC-002** — 状态 **pass**。三个事先冻结的客户快照（`notes/migration-samples.md`）各跑刷新前后两遍，失败 nodeid 名集 `comm -13` **均为空**：xuanji-agent（`3f68b62`，before ∅ / after ∅，250 passed）、xuanji-cli（`a0c476d`，before = after = 2 nodeid，`go test -json`）、xuanji-function（`a2fad18`，before = after = 12 nodeid）。**刷新载荷冒烟**（review-fix F5）在同三个快照上补测：安装后的 `.specify/scripts/python/flow-class-check.py --action lookup` 对 `/speckit.docs`（expression / reader-oracle）与 `/speckit.implement`（execution / mixed-oracle）均 exit 0 且 `source=ledger`；`--action check` / `--action isomorphism` 在客户根均 exit 2 + `framework-source-required`——载荷可执行、作用域守卫生效，不是只有文件在场。原始项目与其工作树零修改（`git archive` 只读，刷新前后脏文件数 195/548/28 不变）；刷新由本切片源码 wheel + `specify init` 完成，未用人工拷贝。逐项记录见 `notes/quickstart-run.md` § 6.3 / § 6.3b 与 `notes/migration-samples.md` § 刷新载荷冒烟。
- **SC-003** — 状态 **pass**。对台账做两种注入（临时副本，不改仓库）：A 删一行（`/speckit.agents`）→ `red_kind = gap`、exit 1、`ledger_rows=77 gaps=1 parse_errors=0`；B 破坏表形（表头保留、数据行全删）→ `red_kind = parse-failure`、exit 1、`ledger_rows=0 parse_errors=1` + `ledger-truncated`。两红**可区分**（`gap` ≠ `parse-failure`），静默绿样本数 = 0（真实树 `red_kind = clean`、exit 0 是唯一绿样本）。另在复制根上验证 `LEDGER_FLOOR = 39` 的反空真：77 行仍判 `gap`、MUST NOT 触发 `ledger-truncated`。逐项记录见 `notes/quickstart-run.md` § 场景 3。
- **SC-004** — 状态 **unknown**。**机器侧已测**：台账 `basis = mixed-oracle` 行 **8 行全部 `flow_class = execution`**（命令侧 `/speckit.constitution`、`/speckit.implement`、`/speckit.instructions`、`/speckit.interview`；技能侧 `skill:implement-feature`、`skill:manage-constitution`、`skill:manage-instructions`、`skill:run-interview`），`mixed-oracle-class` 反例注入（`basis = mixed-oracle` 且 `flow_class = expression`）转红（`tests/contract/test_ledger_reconciliation.py::test_mixed_oracle_expression_row_is_rejected`），择优样本数 = 0。**未测**：两名判定者（不同的人 / 不同的会话 / 判定时互不可见、结论分别落盘后比对）的独立归类演练**本次未执行**——本 run 是单代理 headless 收口，无第二名独立判定者，一致率无可测量的分母，故不记 100%、不记达成。
  - 样本清单与两类覆盖：**「既被人读又被脚本解析」**类取 `/speckit.instructions`（指令文本由读者判、符号链接由脚本判）与 `skill:manage-instructions`（同源技能）；**「须生成并编译」**类取 `/speckit.implement` 与 `skill:implement-feature`（台账 notes 原文为「代码须运行、规格回填须读者核」——执行侧 oracle 落在运行生成的产物上；owner 文档里字面的「须生成并编译 SDK 的 OpenAPI 契约」是边界例，不是台账单元）。机器侧落类分布 = 8/8 `execution`，0 条 `expression`。
  - **执行载体缺口（review-fix F10）**：本条的人工半在 `plan.md` / `tasks.md` 里**没有执行载体**——没有一行任务派发第二名互相隔离的判定者，也没有带 owner 的 `deferred` 条目。因此单代理收口下它只能落 `unknown`：不是「测了但没测准」，而是**从未安排测量**。解除条件与 owner 见 §Residual MEDIUM-1；机制修复归 review REC-069b-04（plan 期必须为需要多判定者的 SC 指定载体，否则不得进入 implement）。
- **SC-005** — 状态 **pass**（测量面已按 review-fix F4 恢复）。`--action faces --repo . --format json` 返回 `faces = 6`、`findings = []`、exit 0——六面表恰好 6 行、face id 唯一、每行一个 `owner_pointer` 格（`+` 连接仍算一个绑定）、9 条真实指针路径在源码根或 `.specify/` 镜像可解析、`§` 锚均有匹配标题（`notes/quickstart-run.md` § 场景 5）。判据正文不搬家：`doc-consistency-check.py --action verify --faces duplicate --owner-path shared/definitions/flow-class-definitions.md --path shared --path templates/commands --path skills --path docs --spec-dir .specify/specs/069b-isomorphism-migration-metrics` 在**声明主体面（533 个文件）**上 `faces.duplicate = pass`、`findings = []`；比较侧是分类 owner 单文件（`scope.owners` 自证）。命令模板 / 技能 / 文档树里的副本注入各一条均转红（`tests/contract/test_expression_faces.py`）。旧口径「owner + spec artifacts 13 文件」已废弃——它看不见模板、技能与文档里的副本。

```text
SC-001_status=pass
SC-001_value=stages=8 gates=6 findings=0 exit=0; 8/8 rows cite a resolving blocking gate:<算子 id> at their own (stage, face) (reference-level); 4/4 boundaries bound to face ids; 5 reference-level + 8 row/boundary-level injections each turn red (exit 1)
SC-001_note=the falsifiable unit is the gate citation, not the free-text semantics — whether a cell *means* its gate stays with the review face (C-10); distortion detection proven by mutation, not by self-report

SC-002_status=pass
SC-002_value=3 pre-frozen snapshots (xuanji-agent 3f68b62 / xuanji-cli a0c476d / xuanji-function a2fad18); comm -13 empty for all three; refreshed-payload smoke on all three: lookup /speckit.docs + /speckit.implement exit 0 with source=ledger, check/isomorphism exit 2 framework-source-required; originals untouched (git archive)
SC-002_note=refreshed with this slice's wheel + specify init, never by manual copy; name-level, not count-level; the payload smoke is a second, independent evidence line (product suite never loads specify)

SC-003_status=pass
SC-003_value=injection A -> red_kind=gap exit 1 (rows=77 gaps=1); injection B -> red_kind=parse-failure exit 1 (rows=0 parse_errors=1); silent-green samples=0
SC-003_note=the two reds are distinguishable; 77 rows stays above the derived floor 39 and never trips ledger-truncated

SC-004_status=unknown
SC-004_value=8 ledger rows with basis=mixed-oracle, 8/8 flow_class=execution, 0 selective picks; mixed-oracle-class counter-injection turns red; two-judge independent classification NOT executed
SC-004_note=machine half measured; the 100% inter-judge agreement is not-evaluated because this run is a single agent (no second, mutually-blind judge), so achievement is not claimed; the status is unknown, not deferred (the sample exists, the second judge does not)

SC-005_status=pass
SC-005_value=faces=6 findings=0 exit=0; duplicate face pass with findings=0 over 533 files (shared/ + templates/commands/ + skills/ + docs/ + spec) against the classification owner as the sole comparison side; 9 owner paths resolve; copies injected into templates/commands, skills and docs each turn red
SC-005_note=criterion text stays in its owner; the old 13-file scope (owner + spec artifacts) is retired — it could not see template/skill/docs copies; expression-gates.md is no longer the comparison side but remains a subject
```

### quickstart 七场景完成情况（`notes/quickstart-run.md`）

| # | 场景 | 状态 | 小节指针 |
|---|------|------|----------|
| 1 | 逐行核对同构映射 | 完成 | `notes/quickstart-run.md` § 场景 1 |
| 2 | 标注失真必须转红 | 完成 | § 场景 2 |
| 3 | 台账双注入两种可区分的红 | 完成 | § 场景 3 |
| 4 | 委托关系由模板解析 | 完成 | § 场景 4 |
| 5 | 六面 owner 指针 6/6 且判据不搬家 | 完成 | § 场景 5 |
| 6 | 迁移与分发（未刷新零调用点 / 刷新同包原子 / 三快照零新增） | 完成 | § 场景 6（含 6.1–6.4） |
| 7 | 三项基线只用既有仪器 | 完成 | § 场景 7（指针段）→ 实跑记录归 `notes/expression-baseline.md` § 复核 |

场景 7 的**值与仪器归 `notes/expression-baseline.md`**（本文件与 `quickstart-run.md` 只留指针，不复述数值）：四条来源命令全部 exit 0 可重跑；三项量的 verdict 均为 `not-evaluated`，但**原因不同且都不记 0**——`confirmations` 两个分项是实测 0（降幅不可定义）、`gate_calls` 是仪器看不见对象（通道数 `unit_id` 记录，门禁是脚本）、`wall_clock` 是终点记录在本切片从未生成（review-fix F6 已把该运行缺口登记在 `notes/expression-baseline.md` § 仪器-对象缺口）。docs-sync 评估另见 § T025 与 `quickstart-run.md` § docs-sync。

**证据指针**：本节各 SC 行的命令与 `notes/quickstart-run.md` 小节；机器侧 `flow-class-check.py` 三种动作的 JSON 输出；`tests/contract/test_ledger_reconciliation.py` 的 `mixed-oracle` 两用例。

---

## §T028 — 特性登记核对与补齐

**核对结果（三点）**

1. `features/069.md` § Related Specifications **原先缺**本切片的 tasks 指针与任务规模 → 本轮补一行 `Slice 069b Tasks（2026-10-25）`：`tasks.md` 任务行合计 **29**（Setup 3 / US1 6 / US2 4 / US3 10 / Polish 6）、全部 `[X]`、零 `[~]`，并指向同目录 `verification.md`（SC 状态分布 pass 4 / unknown 1）。
2. `features/069.md` § Status Tracking **已有**「切片 069b tasks（2026-10-25）」行（tasks 阶段回填，29 与 Tests Mode ON 均在），本轮**追加**「切片 069b implement（2026-10-25）」行记录收口证据（29/29 `[X]`、SC 分布、零 NEW、镜像、覆盖、结构面）。
3. § Slice-aware status 原文「069b = plan 已落盘……tasks / implement 未开始」已过期 → 改为「069b = Implemented」并保留父级索引状态列的处置说明（A-P1）。

**索引行（`features.md`）—— 收口时的处置与 review-fix F3 的更正**

- 收口时只改 069 行的 **Last Updated** 单元格，**Status 列保持 `Planned`**，理由写的是「`tasks.md` T028 明文『状态列 MUST 保持 `Planned`……`Implemented` 转移属 `/speckit.implement`／评审 owner』，本 run 按派发不进入 review」。
- **该理由不成立，已更正（review-fix F3）**：T028 那句话自相矛盾——本 run **就是**落实 implement 收口的那一趟；`shared/workflow/feature-integration.md` 的 Pre-Status-Flip 四项逐条全过（`tasks.md` 零 `[ ]` = 29/29 `[X]`、`deferred_tasks=` 空、5 条 SC 状态行齐备、无未处置 `[~]`），owner 协议要求推进。故索引行 069 的 Status 改为 `Implemented`（069a / 069b 均 Implemented），`features/069.md` 的 Status 同步改为 `Implemented`，其 § Slice-aware status 首条改写为「索引状态列 = `Implemented`」。
- **未主张的两级**：`Ready for Review`（状态机定义 = 全部 deferred 解决或豁免**且** review 证据产出）未写——review 报告已产出，但其 P0/P1 处置尚未闭合；`Completed`（人工验收）同样未写。
- **索引单元格按 F11 收敛**：069 行 Last Updated 原为逐次追加的长叙事（切分后单元格实测 2 959 字符），现改写为一行 `2026-10-25 (slice: 069b Implemented; 069a Implemented) — 详情见 .specify/memory/features/069.md`，叙事留在 `features/069.md` § Status Tracking；索引文件头 `Last Updated` 同步为 2026-10-25。未新增 Feature 行、未回填他特性登记。

**判读**：至此索引与详情文件不再互相矛盾，也没有虚报完成度——停在 `Implemented`，不写 `Ready for Review` / `Completed`。

**证据指针**：`.specify/memory/features/069.md`（§ Related Specifications 的 069b Tasks 行、§ Status Tracking 的 implement 行、§ Slice-aware status）；`.specify/memory/features.md` 069 行 Last Updated 单元格。

---

## §T029 — 终局门禁复跑

以下四段为收口时的真实输出（2026-10-25，工作树 = 本切片的全部改动落盘后、提交前）。

**GATE-1 `validate-tasks.py`**

```bash
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/069b-isomorphism-migration-metrics/tasks.md
PASS: .specify/specs/069b-isomorphism-migration-metrics/tasks.md — 0 error(s), 0 warning(s)
EXIT=0
```

**GATE-2 `pre-analyze-check.py --stage tasks`**

```text
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=9 waived=0
summary: {"errors": 0, "advisories": 9, "waived": 0, "fr": 14, "sc": 5, "tasks": 29, "clauses": 0, "files": 12}
EXIT=0
```

**advisory 逐条裁定（9 条，全部 `missing-path`）**：

| # | 指向 | 裁定 |
|---|------|------|
| 1–8 | `shared/definitions/isomorphism-map.md`（plan :293、tasks :70/:160/:296、research :23、checklist :75/:142×2） | **不处置，属预期残留**：该路径是 research R1 明确被否决的备选（第二份分类 owner），tasks.md § Path Conventions 明写「MUST NOT 创建」「不靠创建文件消除 advisory」 |
| 9 | `tests/test_adapter_contract.py`（checklist :128） | **不处置，属作用域误报**：该路径相对于**客户快照**（`xuanji-agent/tests/test_adapter_contract.py` 实测存在），不是本仓路径；pre-analyze 按本仓根解析才报缺失 |

**GATE-3 `decomposition-check.py --mode tasks`**

```json
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 14, "task_count": 29, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": []}
EXIT=0
```

**GATE-4 `account-clause-coverage.py`**

```text
$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics
claimed clauses (this feature): 51
baseline: .specify/specs/069b-isomorphism-migration-metrics/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 14 / FR claimed: 14 / FR uncovered: 0
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 14 of 14 FRs cited from citation groups
  [clause-unparsable] warn (87) — 87 files yield no clause id under the owner's forms; 0 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] pass (0) — baseline holds 495 names; 495 uncovered items are baseline-internal and do not block
0 error(s), 0 warning(s)
status: ok
EXIT=0
```

（`clause-unparsable` 的 `warn (87)` 是**常驻基线状态**：87 个文件不声明任何可解析条款形态，按 owner 判据「解析疑问，不读作零且已覆盖」；它不因本切片变化，也不是 error。）

**零新增命令 / 零新增门禁面**

```bash
$ ls templates/commands/*.md | wc -l
27
$ git diff --stat HEAD -- templates/commands
（空）
$ git diff -U0 shared/workflow/expression-gates.md | grep '^@@'
@@ -103 +103 @@
@@ -105 +105 @@
$ grep -rn -- '--action isomorphism\|--action delegation\|--action faces' \
    templates/ skills/ .claude/commands .github/prompts .opencode/command .qoder/commands
（无输出）
```

**判读**：命令模板 27 个文件与基线一致；`expression-gates.md` 的改动只有两处 hunk（`103` 基线表行、`105` 冻结点条目），**六面表与调用点表零改动**；四个动作（含新增三个）在任何命令模板、技能与全部命令副本中零命中——它们不是调用点。零新增 `/speckit.*` 命令、零新增门禁面。

**证据指针**：本节四段门禁输出 + 结构面三段命令；`notes/pre-change-measurements.md` § 2（结构面基线 3 条）。

### review-fix 后门禁复跑（2026-10-25，工作树 = review-fix F2/F3/F6 + P2 的全部落盘后、提交前）

上四段是**收口时**的真实输出；review-fix 之后条款数与命令口径有变（F5 追加 C-12、F2 改了 tasks 的禁改面表述），
故在同一台机器上复跑一遍。判据不变，数字以本小节为准：

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/069b-isomorphism-migration-metrics/requirements.md
file: .specify/specs/069b-isomorphism-migration-metrics/requirements.md
status: ok
  [id-contiguous] pass (0)   [doc-order] pass (0)   [ref-resolvable] pass (0)
  [marker-count] pass (0)    [dup-id] pass (0)
scanned: 284 lines, 19 definition rows, 3 shared strings
0 error(s), 0 warning(s)
EXIT=0

$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/069-execution-expression-sdd/requirements.md
status: ok
scanned: 356 lines, 54 definition rows, 4 shared strings
0 error(s), 0 warning(s)
EXIT=0

$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/069b-isomorphism-migration-metrics/tasks.md
PASS: .specify/specs/069b-isomorphism-migration-metrics/tasks.md — 0 error(s), 0 warning(s)
EXIT=0

$ python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
    --spec-dir .specify/specs/069b-isomorphism-migration-metrics --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=9 waived=0
{"summary": {"errors": 0, "advisories": 9, "waived": 0, "fr": 14, "sc": 5, "tasks": 29, "clauses": 0, "files": 12}}
EXIT=0

$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics
uncovered beyond baseline: 0
FR universe: 14 / FR claimed: 14 / FR uncovered: 0
companion: claimed clauses 52, scanned files 184, clause universe 1035, FR universe 14
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 14 of 14 FRs cited from citation groups
  [clause-unparsable] warn (87) — 常驻基线（解析疑问，不读作零且已覆盖）
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s)
status: ok
EXIT=0
```

**判读**：`tasks` 仍 29 行（review-fix 未新增任务行，见 `tasks.md` § 跨切片一致性修正登记）；**advisory 仍 9 条**，即
原先逐条裁定的 8 条被否决备选路径 + 1 条客户快照相对路径，没有新增；条款覆盖从 51 → 52（F5 的 C-12 认领到 T029），
**0 beyond baseline**——A 组追加 C-12 时未同步认领分区，曾使该门禁报 `1 beyond baseline`（status `uncovered`），
本组的登记修正把它拉回 `ok`；这不是放宽判据。需求侧的两个 `validate-requirements.py`（父 / 069b）均为 `ok`。

---

## §Review-fix F2/F3/F6 + P2（2026-10-25）

**口径**：本节只记**规格 / 登记 / 记录面**的修正；代码面归 review-fix A（见 §Review-fix F1/F4/F5）。每条给「处置形态 → 证据指针」。

| Finding | 严重级 | 处置 | 证据 |
|---------|-------:|------|------|
| F2 跨切片改动未登记，「唯一 A-1 / 零改动」与树不符 | P0 | **fixed** | `tasks.md` § 跨切片一致性修正登记（4 行 + 范围边界 + 为何不补任务行）；`tasks.md` § Path Conventions 的 `禁改面` 与 § Notes 两处旧表述就地更正（保留原文 + `~~删除线~~` + 更正句）；`plan.md` § Constraint correction 与 § Mirror addendum；本节 §跨切片一致性修正 补两个落地提交。**069a 判据正文零改动**（`git diff 33c47fd5^ -- .specify/specs/069a-flow-classification-docs-gates` 为空） |
| F3 Feature 069 停在 `Planned` 而 Pre-Status-Flip 四项全过 | P1 | **fixed** | `features.md` 069 行 Status = `Implemented`；`features/069.md` Status = `Implemented`、§ Slice-aware status 首条 = 索引状态列 `Implemented`、Status Tracking 新增「Implemented（切片 2/2）」；四项证据 = 本节 § DoD 的 DoD-1 / DoD-7 + `deferred_tasks=` 空 + `tasks.md` 零 `[~]`。**未写** `Ready for Review` / `Completed` |
| F6 `gate_calls` / `wall_clock` 结构性不可测，且归因写成「记录属别的切片」 | P1 | **fixed（记录面）** | `notes/expression-baseline.md`：`gate_calls` 的 `frozen_value` 由 `0` 改为 `not-evaluated` + 原因（契约 C-3 明禁「当作 0」）；新增 § 仪器-对象缺口（三条，各带处置）；`wall_clock` 的「5 条全属其他特性」归因删除，改写为「本切片 analyze 未产出运行判定记录」；`verification.md` §T027 指针段同口径。**不伪造 0**：`confirmations` 的 0 是实测值照记；`gate_calls` 通道里观察到的 0/1 只作「命令单元计数」写进实测明细，不作本量之值 |
| F7 `post_change_commit` 的值位是散文（shell 命令） | P2 | **fixed** | 头部 `post_change_commit=` 填本文件的落地提交 SHA；该值由紧随的一次「仅改这一行」的 pin 提交回填，`post_change_commit_pin` 记其性质 |
| F8 快照「跑测前提」三条为假，且更正只追加在表后 | P2 | **recorded** | `notes/migration-samples.md`：前提列改名「冻结原文，未经冒烟；实际可执行前提见 § 跑测机制更正」，表下新增《跑测前提》更正段（哪几行按原样启动不了、冻结的是样本不是运行环境契约），并声明该缺口归 REC-069b-10 |
| F9 CHK025 在切片收口时仍 `[ ]` 且无收口证据 | P2 | **recorded（转交）** | 清单 CHK025 disposition 由 `verify-in-implementation` 改判 **`out-of-slice`**，保持 `[ ]`，转交 `OI-069b-01`（`register.md`）；本节 §Checklist 收口对账 |
| F10 SC-004 需两名隔离判定者，plan 从未安排 | P2 | **recorded** | §T027 SC-004 新增「执行载体缺口」子条（说明 `unknown` 是「从未安排测量」而非测不准）；§Residual MEDIUM-1 保留解除条件；机制修复归 REC-069b-04 |
| F11 索引 Last Updated 单元格写成 2 959 字符的追加式叙事 | P2 | **fixed** | 见 §T028「索引单元格按 F11 收敛」：改为一行 `日期 (slice: 069b Implemented; 069a Implemented) — 详情见 .specify/memory/features/069.md` |
| F12 三个样本同组同作者，代表性未记录 | P2 | **recorded** | `notes/migration-samples.md` § 样本代表性：六维「已覆盖 / 未覆盖」表 + 读法（SC-002 只在该六个维度上成立）；样本本身未更换（换了就不是同一份冻结记录） |

**未处置残留（明确承认）**：F2 的机制修复（提交门按 `禁改面` 做 diff 校验）与 F6 的仪器插桩（门禁脚本在调用点写 exec-quant 形状记录）都是 **framework 改动**，按本次派发不在本组范围；已由 review REC-069b-05 / REC-069b-08 承载。本组只保证**记录与树一致、不虚报**。

## §Checklist 收口对账（review-fix F9）

实现收口时清单是 35 `[x]` / 1 `[ ]`，而唯一未闭合项的 disposition 写着 `verify-in-implementation`——实现期却从未核对它。对账结果与处置：

```text
$ grep -c '^- \[x\]' .specify/specs/069b-isomorphism-migration-metrics/checklists/isomorphism-migration-metrics.md
35
$ grep -c '^- \[ \]' .specify/specs/069b-isomorphism-migration-metrics/checklists/isomorphism-migration-metrics.md
1
```

- **CHK025（唯一 `[ ]`）→ 转交，不关闭**：它问「客户副本的漂移检查有没有 owner 与仪器」。框架源 ↔ 镜像有 `sync-mirrors.py --check`；客户副本由 `specify init` 整文件覆盖，且 C-4 禁止新增客户侧检查器——这是 **FR-008 的需求缺口**，实现期没有任何动作能关闭它，也没有证据可引用。故 disposition 改判 `out-of-slice`，登记 `OI-069b-01`，owner = 后续修订 FR-008 的特性（未立项），解除条件 = 指定 owner 与仪器或明确豁免。**保持 `[ ]`**。
- **CHK036 的两处前提已过期**：原文「Feature 保持 `Planned`」「069a 除 A-1 外零改动」在 F2 / F3 的修正后不成立，已在原行追加「状态更新」子句，不重写历史行。
- **汇总由标记派生**：35 + 1 = 36 = 清单项总数；`[x]` 数未变、`[ ]` 仍为 1——**没有把「转交」写成「关闭」**。

**证据指针**：清单 CHK025 / CHK036 行与 § Notes；`register.md` 的 `OI-069b-01` 行。

## §DoD 状态

| DoD 行 | 状态 | 证据 |
|--------|------|------|
| DoD-1 全部任务 `[X]` 且无 `[~]` | pass | `tasks.md` 29 行全 `[X]`；`deferred_tasks=` 空 |
| DoD-2 两个编辑面按契约交付 | pass | owner 8×3 + 四边界 + 台账版本（`test_isomorphism_map` 24 用例 / `test_ledger_reconciliation` 21 用例全绿）；引擎三动作 + `check` 扩展；`lookup` 与 069a 八 kind 零改动（G3 回归证据） |
| DoD-3 52 条款各认领一次 | pass | `account-clause-coverage.py`：claimed = 52、uncovered beyond baseline = 0（§ T029 的 review-fix 复跑）。plan 期的 51 条在 review-fix F5 追加 C-12 后升为 52 条，绿点归 T029（见 `tasks.md` § 跨切片一致性修正登记） |
| DoD-4 8 支新测试全绿且零新增失败 | pass | US1 34 + US2 16 + US3 78 全绿；`comm -13` 空（§ T026） |
| DoD-5 镜像与副本零漂移 | pass | 六对 `ok`、两个编辑面 `cmp` 同字节、命令副本 `OK`（§ T024） |
| DoD-6 零新命令 / 零新门禁面 / 零项目侧存储 / 零新采集器 | pass | `templates/commands/` 27 个文件；三个新动作在 `templates/` `skills/` 及全部命令副本中零命中；`expression-gates.md` 六面表与调用点表 `git diff` 零改动；`.specify/memory/` 零类别存储（`test_migration_distribution` 断言） |
| DoD-7 SC 状态行齐备 | pass | 5 条 bullet + 5 组 `SC-NNN_status=`；分布 = pass 4 / unknown 1（SC-004 带 not-evaluated + reason，未记达成；`not-evaluated` 未占状态位） |
| DoD-8 三快照 `comm -13` 为空 | pass | 三个快照均为空（§ T027 SC-002） |

---

## §Assumptions（本轮自行裁决）

- **A-P1（已废止 / superseded，2026-10-25 review-fix F3）父 Feature 状态列保持 `Planned`**：原理由「`tasks.md` T028 明文『状态列 MUST 保持 `Planned`……`Implemented` 转移属 `/speckit.implement`／评审 owner』，本 run 按派发不进入 review」**自相矛盾**——本 run 就是落实 implement 收口的那一趟，且 Pre-Status-Flip 四项全过，owner 协议要求推进。现已把索引行推进为 `Implemented`（见 §T028 与 `features/069.md` § Slice-aware status）。保留此条只为留痕：**当时停在 `Planned` 是欠报**，不是「更保守的正确值」。
- **A-P2 跨切片修正落在 owner + 其契约测试**：`tests/contract/test_expression_gates_doc.py` 的字面断言属 069b 的编辑面（`tests/contract/`），改的是同一判据的仪器编码，不是判据语义；069a 的 contracts 文档（`.specify/specs/069a-.../`，禁改面）保持原样，其 C-9 已把仪器口径委派给 069b。
- **A-P3 SC-004 的「须生成并编译」样本**：台账里没有字面写「编译」的单元，取 `/speckit.implement` 与 `skill:implement-feature`（notes 原文「代码须运行」= 执行侧 oracle 落在运行生成的产物上）。这是**样本措辞的近似**，已在 SC-004 行明写；该条状态本就是 `unknown`，不因此影响任何「达成」结论。

---

## §Residual（遗留问题，按严重度）

- **MEDIUM-1**：SC-004 的人工半（两名互相隔离判定者的独立归类）未执行——单代理收口无第二判定者，且 plan / tasks 从未为它安排执行载体（review-fix F10）。解除条件：由第二名判定者在隔离结论后逐条比对 8 个混合 oracle 单元与判据，统计一致率并落盘。机制修复归 review REC-069b-04。
- **MEDIUM-2（review-fix F6 登记）**：本切片 2026-10-25 的 analyze 轮未产出 `/speckit.analyze` 运行判定记录，故 `wall_clock` 只有起点、没有终点。这不是数据窗口的性质，而是运行缺口（那轮 analyze 是自跑，未走记录入口）。解除条件：该轮以 `/speckit.analyze` 入口重跑并落记录，或把 analyze 的收尾接上运行判定（框架改动，归 REC-069b-08）。
- **LOW-1**：`docs/` 没有脚本参考面（`flow-class-check.py` 的四个动作在项目文档中零记载，069a 的 `lookup`/`check` 亦然）。本轮按 docs-step 判「无需记录」——新增参考面属 `/speckit.docs` 的结构决策，不在实现收口内。
- **LOW-2（已解除，2026-10-25 review-fix F3）**：`features.md` 的 069 行状态列曾停在 `Planned`（A-P1）。现已按 Pre-Status-Flip 门推进为 `Implemented`，本条关闭。
- **LOW-3（transferred，2026-10-25 review-fix F9）**：客户侧分类副本的漂移检查缺 owner 与仪器（CHK025）。本切片判 `out-of-slice`，转交 `OI-069b-01`（`register.md`），owner = 后续修订 FR-008 的特性（未立项）。**未关闭**。
