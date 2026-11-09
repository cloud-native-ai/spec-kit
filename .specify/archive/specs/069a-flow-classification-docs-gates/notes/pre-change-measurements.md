# Pre-change measurements — 069a (Phase 1 Setup)

**Owner of this record**: `tasks.md` T001（改前基线捕获）。本文件只记录**编辑前**实测值；后续每个「相对基线零新增」判据都以本文件为对照物，不另写第二份基线清单。

- Capture date: 2026-10-24 21:23–21:29 +0800 / 2026-10-24T13:23–13:29Z (UTC)
- Branch: `069-execution-expression-sdd`
- `git rev-parse HEAD`: `01d1feaa08d4541be2b59af30aa8c2e87128e55a`（捕获于 2026-10-24T13:23:56Z）

逐项捕获时刻（命令按执行顺序；同一分钟内完成的项只记到分钟，不编造秒）：

| 项 | 时刻 (UTC) |
|----|-----------|
| HEAD / `git status --short` | 13:23:56Z / 13:24Z |
| `sync-mirrors.py --check`、`regen-command-copies.py --check` | 13:24Z |
| `docs-utils.py --action validate`、062/067/068 `shasum` | 13:24Z |
| 74 行哈希清单计算 | 13:24Z（写盘并回验 13:29Z） |
| `account-clause-coverage.py --freeze` | 13:24Z |
| 契约套件重采 | 13:24:41Z → 13:28:11Z（209.77 s） |

## 1. 工作树状态（`git status --short`，捕获时逐字）

```
 M .specify/memory/session/20261020T042213Z-run-determination-speckit-tasks-speckit-tasks-20261020t04215.md
 M .specify/memory/session/20261021T132909Z-run-determination-speckit-tasks-tasks-066a-20261021.md
?? .spec-kit/
?? .specify/memory/exec-quant/records/20261024T042048454345Z-aa788745.json
?? .specify/memory/exec-quant/records/20261024T043043138703Z-5d6b88ec.json
?? .specify/memory/exec-quant/records/20261024T122325278000Z-e9cba0a1.json
?? .specify/memory/exec-quant/records/20261024T124558229923Z-ebf6e230.json
?? .specify/memory/exec-quant/records/20261024T125553396297Z-3a2caefd.json
?? .specify/memory/feedback/20261024T042052Z-speckit-requirements.md
?? .specify/memory/feedback/20261024T043049Z-speckit-clarify.md
?? .specify/memory/feedback/20261024T122329Z-speckit-plan.md
?? .specify/memory/feedback/20261024T124602Z-speckit-tasks.md
?? .specify/memory/feedback/20261024T125558Z-speckit-checklist.md
?? .specify/memory/session/20261024T042034Z-run-determination-speckit-requirements-069-req-20261024t1220.md
?? .specify/memory/session/20261024T043030Z-run-determination-speckit-clarify-20261024t043100z-speckit-c.md
?? .specify/memory/session/20261024T122322Z-run-determination-speckit-plan-plan-069a-20261024.md
?? .specify/memory/session/20261024T124553Z-run-determination-speckit-tasks-tasks-069a-20261024t1245z.md
?? .specify/memory/session/20261024T125553Z-run-determination-speckit-checklist-checklist-069a-20261024t.md
```

判读：两条 `M` 与全部 `??` 均为运行期记录，与本切片无关；本节只作改前快照，不纳入提交、不还原。

## 2. 镜像面：`python3 scripts/python/sync-mirrors.py --check`

```
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (396 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (110 files)
ok    shared/ == .specify/shared/ (53 files)
```

exit 0。判据：**相对本基线零新增差异**（不是绝对全绿）。

## 3. 命令副本面：`python3 scripts/python/regen-command-copies.py --check`

```
OK: all per-tool command copies match the source templates.
```

exit 0。判据：重生成后 `--check` 为 `OK`。

## 4. 结构面：`python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .`

exit 0，`violations` = **3**，kind 集合 = `broken-link`(2) + `note-frontmatter`(1)：

```json
{
  "violations": [
    {"kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/unit/test_qoder_support_matrix.py"},
    {"kind": "broken-link", "path": "docs/concepts/overview.md", "detail": "../../tests/integration/test_qoder_refresh.py"},
    {"kind": "note-frontmatter", "path": "docs/notes/type-follows-stage-misclassification.md", "detail": "missing: "}
  ]
}
```

判据：`violations` 计数与 kind 集合**零新增**（基线非零，本切片不为它转绿）。

## 5. 前序规格哈希（`shasum -a 256`，SC-008 分母）

```
987b24ea1f98abb2a01d14779814eab28416f4ad1cbd81a36d51efb72d5f9da0  .specify/specs/062-humanize-command/requirements.md
29e26b701ebef9d80782b9a215ef97759290a384d898cb3320cfedde161fa0cd  .specify/specs/067-loop-efficiency-hardening/requirements.md
ec20d5e28bd0eb5e2afdbd851cb753ef6e1c37a1c24e66b196f9305f18b45af7  .specify/specs/068-exec-quant-feedback-channel/requirements.md
```

与 `tasks.md` § Measured Premises 冻结值逐字节一致。

## 6. 非接线文件哈希清单：`notes/pre-change-file-hashes.txt`

- 生成命令（仓库根执行，`LC_ALL=C sort` 固定顺序）：

  ```bash
  { for f in $(ls templates/commands/*.md | LC_ALL=C sort); do
      case "$(basename "$f")" in docs.md|humanize.md) continue;; esac
      shasum -a 256 "$f"; done
    for f in $(ls -d skills/external/*/ | sed 's#/$##' | LC_ALL=C sort; \
               ls -d skills/internal/*/ | sed 's#/$##' | LC_ALL=C sort); do
      case "$f" in skills/external/create-docs|skills/external/humanize) continue;; esac
      shasum -a 256 "$f/SKILL.md"; done; } > .specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt
  ```
- 实测规模：**74 行** = 25 个非接线命令模板（27 个模板剔除 W1 `docs.md`、W2 `humanize.md`）+ 49 个非接线技能源（51 个技能剔除 W3 `skills/external/create-docs/SKILL.md`、W4 `skills/external/humanize/SKILL.md`）；每行 `sha256␠␠<仓库相对路径>`。
- 名单自检：`grep -c '^templates/commands/'` = 25、`grep -c '^skills/'` = 49、`grep -cE 'create-docs/SKILL.md|humanize/SKILL.md|templates/commands/(docs|humanize).md'` = 0。
- 清单自身指纹（写盘后 `shasum -a 256`）：`c88a4022a66629e4b18b0fdb2f48025b4568c10e4c04533869586cab367ab507`。
- 回验：把清单里的 74 个路径重新 `sha256` 后与清单逐行 diff，**空输出**（清单与当前树一致）。

## 7. 条款覆盖基线（T002）

- 命令：`python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069a-flow-classification-docs-gates --freeze > .specify/specs/069a-flow-classification-docs-gates/coverage-baseline.txt`，exit 0。
- 文件形态：**497 行** = 2 行头部 + **495** 行冻结 UNCOVERED 条款名。
- 头部两行：L1 是 `comm -13` 比对配方（含 `LC_ALL=C` 说明）；L2 为
  `# frozen-from: .specify/specs/*/contracts/* excluding 069a-flow-classification-docs-gates | … | base-sha: 01d1feaa08d4 | files: 176 (parsed 89 + named 87)`。
  两个标记实测：`frozen-from:` 命中 1 行、`excluding 069a-flow-classification-docs-gates` 命中 1 行（均在 L2；L1 是比对配方，故「头部两行」合计承载两标记）。
- 本切片条款泄漏核对（只看正文，`tail -n +3`）：`069a-flow-classification-docs-gates` 命中 **0**；四个契约文件名 `flow-class-ledger|expression-gate-operators|doc-consistency-checker|compatibility-distribution` 命中 **0**。→ 本切片 50 条款不在自己的豁免基线里，只能被认领。
- 口径唯一落点：该文件头部；不另写第二份清单。

## 8. 契约套件名字级基线（T003）

- 命令：`/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider`
- 起止：2026-10-24T13:24:41Z → 2026-10-24T13:28:11Z（209.77 s），exit 1（存在既有失败，符合基线预期）
- 结果行：`33 failed, 4177 passed, 5 skipped, 1 warning in 209.77s (0:03:29)`
- 冻结文件：`notes/test-baseline-contract.txt`（33 条 node id，`LC_ALL=C sort`）。
- 判据：**零新增失败 node id**（名字级 `comm -13`），不是「全绿」。

### 8.1 与生成时冻结名单的差值（31 → 33）

旧冻结名单（HEAD `756b1f31`，31 条）→ 本次（HEAD `01d1feaa`，33 条）：

- **NEW（有 2，均为 `inherited`）**：

  | node id | 实测失败面 | provenance | 分类 |
  |---------|-----------|------------|------|
  | `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` | `templates/instructions-template.md` 顶级 `## ` 段落 24 → **26**（断言硬 pin 24） | 上游提交 `5b13564b feat(guidelines): add temp-directory and knowledge-promotion disciplines` 新增 `## Temporary Directory Discipline` 与 `## Knowledge Recording & Promotion` 两段 | `inherited`（上游在本切片冻结后引入，非本切片改动；未修 pin） |
  | `tests/contract/test_shared_reference_rewrite.py::test_skills_use_installed_absolute_shared_form` | `skills/internal/{memory-recall,memory-record}/SKILL.md` 出现裸 `shared/guidelines/...` 引用 | 同一上游提交 `5b13564b` 在这两个技能新增 `shared/guidelines/knowledge-promotion.md` 裸路径引用 | `inherited` |

- **GONE（有 0）**：`comm -23 old new` 空输出——旧 31 条在新树全部仍失败。
- 归属判定依据：`git log --oneline 756b1f31..HEAD` 只含 069a 文档提交与上述上游提交 `5b13564b`；两个新失败都指向 `5b13564b` 触碰的 `templates/instructions-template.md` / `skills/internal/memory-*`，与本切片写目标（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`scripts/python/flow-class-*.py`、`templates/commands/{docs,humanize}.md`）无交集。
- 处置：按任务纪律**不修**这两个既有失败（不掩盖、不为基线转绿改无关测试），新名单以本次实测为准。

## 9. 与 `tasks.md` § Measured Premises 的偏差（继承前提重测）

| Premise | tasks.md 冻结值 | 本次实测 | 分类 / 依据 |
|---------|-----------------|----------|-------------|
| `sync-mirrors.py --check` 的 `scripts/` 文件数 | 109 | **110** | `inherited` — 上游 `5b13564b` 新增 `scripts/python/scan-temp-usage.py` |
| 同命令的 `shared/` 文件数 | 51 | **53** | `inherited` — 同提交新增 `shared/guidelines/temp-directory-discipline.md`、`shared/guidelines/knowledge-promotion.md` |
| 结构面 `violations` | 3（`broken-link` 2 + `note-frontmatter` 1） | 3（同 kind） | 一致 |
| 062/067/068 哈希 | `987b24ea…` / `29e26b70…` / `ec20d5e2…` | 逐字节一致 | 一致 |
| 契约失败名单 | 31 条 @ `756b1f31` | 33 条 @ `01d1feaa` | `inherited`，见 §8.1 |
