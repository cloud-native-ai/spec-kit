# Quickstart — 069a 分类本体、台账与文档型门禁

**Phase 1 output**（`/speckit.plan`，2026-10-24）。6 个场景按「先能证明基线 → 再证明新机制 → 最后证明兼容」排列。
每个命令示例标注核验路由：**(a)** = 本阶段已对真实工具执行，输出已贴；**(b)** = 由契约测试钉住有效性（实现落地时按断言核验），并逐例列出**前提**（premises）供 `/speckit.tasks` 与 `/speckit.implement` 重测而非继承。

**本阶段不实现任何运行时行为**：两个引擎（`flow-class-check.py`、`doc-consistency-check.py`）与四个接线点均尚不存在，场景 1–2 与 4 的 route (b) 示例即为待实现面。

---

## 场景 0 — 现状基线（route a，全部实跑）

```bash
# (a) 流程单元规模——台账的分母
ls templates/commands/*.md | wc -l          # → 27
ls -d skills/external/*/ | wc -l            # → 14
ls -d skills/internal/*/ | wc -l            # → 37
# 两层技能无同名冲突（空输出 = 无冲突）
comm -12 <(ls -d skills/external/*/ | xargs -n1 basename | sort) \
         <(ls -d skills/internal/*/ | xargs -n1 basename | sort)

# (a) 镜像基线（编辑前）
python3 scripts/python/sync-mirrors.py --check
#   → OK: all per-tool command copies match the source templates.
#     ok templates/ == .specify/templates/ (22 files)
#     ok skills/external/ == .specify/skills/ (396 files)
#     ok skills/internal/ == .specify/skills/internal/ (136 files)
#     ok agents/ == .specify/agents/templates/ (3 files)
#     ok scripts/ == .specify/scripts/ (109 files)
#     ok shared/ == .specify/shared/ (51 files)   (exit 0)

# (a) 结构面基线——**非零**，故判据只能写「零新增」
python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root . > /tmp/xj-docs-validate.json
#   → exit 0；violations=3（broken-link 2 + note-frontmatter 1）

# (a) 需求面基线
python3 scripts/python/validate-requirements.py .specify/specs/069a-flow-classification-docs-gates/requirements.md
#   → status: ok / id-contiguous, doc-order, ref-resolvable, marker-count, dup-id 全 pass
#     267 lines, 35 definition rows, 4 shared strings, 0 error(s), 0 warning(s) (exit 0)

# (a) 测试基线（名字级）
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/069a-flow-classification-docs-gates --stage requirements
#   → decision=pass errors=0 advisories=0 (fr=27 sc=8)
#     注：advisories=0 是 requirements 阶段（设计产物落盘前）的值；设计产物落盘后同命令复测为
#     79 条 missing-path advisory（全部指向尚待创建的新文件），decision 仍为 pass（2026-10-24 checklist 阶段复测）

/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --collect-only -q tests
#   → 5361 tests collected in 1.52s (exit 0)
```

**证明点**：台账分母（78）、镜像全绿、结构面 3 条既有违规、需求面全绿、测试采集面可用——实现期的四条判据都有可比较的分母。

**前提（premises）**：① pytest 不在本仓 `.venv`（实测 `No module named pytest`），本机唯一可用解释器是 `profiles/.venv`；
② `create-new-plan.sh` 需要 `CWS_LIB_BASH_HOME`（未导出时直接 `Dependency check failed`），且它按 `069-*` 前缀解析目录，**不会**命中 `069a-*`（见场景 5）。

---

## 场景 1 — 查表与缺口（route b：`tests/contract/test_flow_class_ledger.py` 钉住）

```bash
# 已登记的流程单元：类别来自台账
python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs" --format json
#   → {"unit_id":"/speckit.docs","flow_class":"expression","source":"ledger",
#      "marker":null,"basis":"reader-oracle","neutral":false}   (exit 0)

# 未登记单元：默认类 + 固定标记（不得呈现为已判定）
python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.nonexistent" --format json
#   → {"unit_id":"/speckit.nonexistent","flow_class":"execution","source":"default",
#      "marker":"未声明·按默认","basis":null,"neutral":false}    (exit 0)

# 台账 ↔ 清单对账：零缺口
python3 scripts/python/flow-class-check.py --action check --format json
#   → {"action":"check","findings":[],"units":78,"checked_at":"..."}   (exit 0)

# 缺口演练：把一行从台账删掉后再跑（演练后还原）
python3 scripts/python/flow-class-check.py --action check --format json
#   → {"findings":[{"kind":"missing","unit_id":"skill:humanize"}], ...}   (exit 1)
```

**前提（逐例）**：① 动作名 `check` / `lookup` 与 `--unit-id` / `--repo` / `--format` 旗标（契约 `flow-class-ledger.md` C-13）；
② `lookup` 的 JSON 键集合（`data-model.md` E9；示例输出里的键名与取值是**输出样例**，属防漂移固定副本，规范字面量见 requirements §Shared Strings 的 `[[STR-003]]` / `[[STR-001]]` / `[[STR-002]]`）；
③ 默认标记字面量与 `requirements.md` § Shared Strings 的 `STR-004` 同值（测试固定副本）；
④ 台账行语法（契约 C-4）与反空真下限 27/51（契约 C-5）。四条全部由契约测试断言；演练用 `--repo` 指向临时夹具，不改本仓台账。

**分类正确性（route b：`tests/contract/test_flow_class_correctness.py` 钉住）**

```bash
# 固定 fixture：≥10 个流程单元（两类 ≥3 / 未声明 ≥1 / 类中立 ≥1 / 混合 oracle ≥1）
#   逐单元断言 lookup 的 flow_class / source / basis / marker 与 oracle 相符
#   → 断言全绿（不是"文件在场"这类结构断言）

# 变异断言：把 fixture 中一个单元的类别改错后重跑同一比对
#   → 比对 MUST 转红（证明该测试能证伪；改对后回绿）
```

**前提（逐例）**：① oracle 是测试内的固定期望表（与台账同源、独立书写，避免用被测实现生成期望）；
② 变异在临时副本上做，不改本仓台账；③ 该测试是 SC-001 的机械核验面，两人判定演练为并列人工证据。

---

## 场景 2 — 文档型门禁三面（route b：`tests/contract/test_doc_consistency_checker.py` 钉住）

```bash
# 读者 + 证据 + 副本 + 计数（四面的缺省组合）
python3 scripts/python/doc-consistency-check.py --action verify \
  --spec-dir .specify/specs/<doc-type-feature> \
  --path docs/concepts/<page>.md --format json
#   → {"faces":{"reader":"pass","evidence":"pass","duplicate":"pass","count":"delegated"},
#      "findings":[],"count_check":{"status":"delegated","reason":null}}   (exit 0)

# 注入 1：把一处引用改写成 owner 原文副本
#   → finding {face:"duplicate", rule:"duplicate-fact", path/counterpart 两侧定位}
# 注入 2：把一处 as-of 改成更早日期
#   → finding {face:"evidence", rule:"as-of-stale"}
# 注入 3：把一处派生计数改成手打且与定义数不符
#   → finding {face:"count", rule:"count-mismatch"}（经 pre-analyze-check 委派）
#   （任一注入存在时 exit 1）

# 计数面委派不可用时的降级（不得静默绿）
#   → {"count_check":{"status":"not-run","reason":"pre-analyze-check.py not found"}}  (exit 0 非 strict / 1 strict)
```

**前提（逐例）**：① 两面声明行形态 `**Readers**:` / `**Reading scenario**:`（契约 `expression-gate-operators.md` C-4）；
② 归一化与排除闭集（契约 `doc-consistency-checker.md` C-2/C-5）；③ 委派目标的调用形态与 finding 映射（C-6）；
④ `as-of` 的 git 时钟来源 `git log -1 --format=%cs -- <path>`（本仓实测可用，返回 `2026-10-24`）。
注入演练由夹具执行，不修改真实规格。

---

## 场景 3 — 三项基线的冻结（route a：三个来源命令已实跑；route b：记录形态）

```bash
# (a) 门禁调用次数来源：按时间窗取记录，再按声明的门禁单元集过滤
python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json | head -3
#   → [ { "kind": "speckit.exec-quant", "schema_version": 2,
#         "unit_id": "skill:git-utils", "collected_at": "2026-10-20T02:39:20Z", ... }, ... ]  (exit 0)

# (a) 单次运行判定与时间戳来源
python3 scripts/python/run-determination.py --action history --target /speckit.plan --limit 3 --json | head -8
#   → {"target":"/speckit.plan","counts":{"total":12,...},"records":[{...,"determined_at":"2026-10-21T13:02:41Z"}]}  (exit 0)

# (a) 墙钟起点：requirements 首次提交日期
git log -1 --format=%cs -- .specify/specs/069a-flow-classification-docs-gates/requirements.md
#   → 2026-10-24

# (b) 冻结记录（实现期写入该特性的 notes/，形态见 data-model.md E8）
# tests/contract/test_expression_gates_doc.py 断言：门禁 owner 含三项基线的来源表，
# 且缺 compared_at 的记录被列为不可验收。
```

**前提**：① `exec-quant` 的 `--since` 接受 ISO 日期（实测）；② `run-determination --action history` 必须给 `--target`（实测：缺参返回
`history is missing required arguments: --target`）；③ 三项量的仪器口径与 `not-evaluated` 降级的**规范条款**归 069b（父编号 041），本切片只用既有通道取数。

---

## 场景 4 — 兼容与分发（route a：基线；route b：接线的兼容语义）

```bash
# (a) 前序规格字节不变（SC-008 的分母，编辑前后必须相同）
shasum -a 256 .specify/specs/062-humanize-command/requirements.md \
              .specify/specs/067-loop-efficiency-hardening/requirements.md \
              .specify/specs/068-exec-quant-feedback-channel/requirements.md
#   → 987b24ea…f5f9da0  062
#     29e26b70…1a0cd   067
#     ec20d5e2…b45af7  068

# (a) 接线前基线：副本与模板一致
python3 scripts/python/regen-command-copies.py --check
#   → OK（exit 0）

# (b) 改完两个模板后**必须**重生成副本，再验零漂移
python3 scripts/python/regen-command-copies.py          # 生成 8 个副本（docs/humanize × 4 工具）
python3 scripts/python/regen-command-copies.py --check
#   判据：OK（判的是「生成物 = 源模板」，不是「模板未改」）

# (b) 镜像：源与镜像同字节（含两个技能的新增行）
python3 scripts/python/sync-mirrors.py --write --only shared --only scripts --only skills
python3 scripts/python/sync-mirrors.py --check

# (b) 接线本身（由 tests/contract/test_expression_gate_wiring.py 钉住；此处给人工复核形态）
grep -n "flow-class-check.py\|expression-gates.md\|flow-class-definitions.md" \
     templates/commands/docs.md
#   → docs 模板命中：lookup 调用 + 两个 owner 指针
grep -n "flow-class-definitions.md\|expression-gates.md" templates/commands/humanize.md
#   → 只命中两个 owner 指针
grep -n "flow-class-check.py\|--action lookup\|doc-consistency-check.py" templates/commands/humanize.md
#   → 空（humanize 命令保持 Simple：零脚本调用；类别读取在技能执行体）
grep -n "flow-class-check.py\|--action lookup" skills/external/humanize/SKILL.md
#   → 命中（该流程唯一的类别读取，位于 Stage 6）
grep -n "doc-consistency-check.py" templates/commands/docs.md
#   → docs 路径命中 doc 检查器；humanize 模板 MUST NOT 命中（最小集不套六面）
grep -c "SKILL.md" templates/commands/humanize.md
#   → 1（062 的单一委派断言；接线文字不得再提技能路径）
grep -rn "flow-class-check.py\|expression-gates.md\|doc-consistency-check.py" \
     templates/commands/*.md skills/*/*/SKILL.md | grep -v -e "commands/docs.md" -e "commands/humanize.md" \
     -e "create-docs/SKILL.md" -e "humanize/SKILL.md"
#   → 空（接线封闭集之外零调用点）
```

**Simple 形态的既有回归（route a，本次实跑）**

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_humanize_command_surface.py -q -p no:cacheprovider
#   → 10 passed（2026-10-24；含 test_c01_thin_entry_shape / test_c02_single_skill_delegation）
#   模板当前形态实测：非表格行 40 条（上限 120）、无 ## Wrap-up、SKILL.md 唯一一处、零 flow-class-check 引用
```

**兼容语义（本场景要证明的命题）**

| 状态 | 构成 | 行为 |
|------|------|------|
| 未刷新项目 | 旧命令副本 + 旧技能；`.specify/shared/` 无两份 owner、`.specify/scripts/` 无两个引擎 | 副本不含 lookup → **零调用点**，行为与接线前逐字一致 |
| 已刷新项目 | 新副本 + 新技能 + 两份 owner + 两个引擎（同一发行包） | 两个入口在判定前各执行一次 lookup，接线生效 |
| 异常态（只拷了模板/只拷了脚本） | 调用点存在但目标缺失 | lookup 失败 → 默认类 + 固定标记（或 `owner-unavailable`），保持既有门禁、不中断、不静默切门禁集 |

**前提**：① 三个哈希是**当前**值，`tests/contract/test_expression_compatibility.py` 以同样方式重算并比对；
② `sync-mirrors.py --only` 是**可重复旗标**（`action="append"`，实测 `--only shared,scripts,skills` 作为单个前缀返回 exit 2 `--only prefix matches no mirror pair or regen surface`）；③ `.specify/` 侧不得手改；
④ 每工具命令副本是生成物——只改模板不重生成 = 假绿，由 `test_expression_gate_wiring.py` 的副本内容断言兜住。

---

## 场景 5 — 脚手架的正确用法（route a，含一次已披露的偏差）

```bash
# (a) 直接运行会解析到**父**规格目录（切片目录不在 069-* 的 glob 内）
CWS_LIB_BASH_HOME=<cws-lib-bash> bash .specify/scripts/bash/create-new-plan.sh --json
#   → Copied plan template to .../.specify/specs/069-execution-expression-sdd/plan.md
#     {"SPECS_DIR":".../069-execution-expression-sdd", ...}

# (a) 切片计划的正确做法：显式复制模板到切片目录
cp .specify/templates/plan-template.md .specify/specs/069a-flow-classification-docs-gates/plan.md
```

**前提/披露**：`common.sh` 的 `find_feature_dir_by_prefix` 只按数字前缀匹配，切片目录（`069a-*`）不在其中；
本运行两次触发该偏差（一次为脚手架、一次为复核该行为），两次生成的父目录 `plan.md` 均已删除——本运行未创建父规格计划。
`CWS_LIB_BASH_HOME` 未导出时脚本直接失败（实测 `Error: CWS_LIB_BASH_HOME environment variable is not set.`）。

---

## 场景 6 — 全量回归（route a：基线；route b：判据）

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider
#   (a) 基线（2026-10-24，编辑前）：4154 passed, 31 failed, 5 skipped in 201.91s
#       失败名单冻结在 notes/test-baseline-contract.txt
#   (b) 实现后判据：与基线名单比较，**零新增失败名字**
```

**前提**：既有 31 红属其他特性的登记债，本切片不修复也不掩盖；判据是名字级差值，不是绝对绿。
