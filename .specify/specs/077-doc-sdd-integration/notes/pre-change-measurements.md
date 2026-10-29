# Pre-Change Measurements — Feature 077（2026-10-30）

本文件冻结 `tasks.md` § Measured Premises 的实测值与命令，并在本段起点（HEAD `e14408f7`，分支 `077-doc-sdd-integration`）复测一遍。

**读法**：`tasks.md` 记的是生成时（HEAD `06c31b1d`）的读数，本文件记的是本段起点的复测值。两者不一致时**不视为 premise 失效**——判据是「同一命令在今天的树上仍能复现同一结论」；出现漂移的行在表末单独登记原因，且不改变任何一条任务的验收条件。

解释器：`python3` = 系统解释器 3.14.6（引擎只用标准库）；pytest 与分发脚本用 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`。
工作目录：仓库根。

## A. 规格与契约面

| Premise | Re-derivation command | tasks.md 记录（@`06c31b1d`） | 本段复测（@`e14408f7`） |
|---------|-----------------------|------------------------------|--------------------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/077-doc-sdd-integration/requirements.md` | `25` | `25` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/077-doc-sdd-integration/requirements.md` | `8` | `8` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/077-doc-sdd-integration/requirements.md` | `4` | `4` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/077-doc-sdd-integration/requirements.md` | `6` | `6` |
| 契约文件数 | `ls .specify/specs/077-doc-sdd-integration/contracts/*.md \| wc -l` | `6` | `6` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/077-doc-sdd-integration/contracts/*.md \| grep -c '^  C-'` | `77`（13 + 12 + 13 + 19 + 11 + 9） | `77` |
| 条款计数陷阱形（*提及*数，不是定义数） | `grep -oh 'C-[0-9]\{2,3\}' .specify/specs/077-doc-sdd-integration/contracts/*.md \| wc -l` | `85` | `99` |
| 命令模板数 / 技能数 | `ls templates/commands/*.md \| wc -l`；`ls skills/external/*/SKILL.md skills/internal/*/SKILL.md \| wc -l` | `27` / `52` | `27` / `52` |
| 任务行数 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/077-doc-sdd-integration/tasks.md` | `28` | `28` |
| 任务标识的*提及*数（不是行数） | `grep -oE 'T[0-9]{3}' .specify/specs/077-doc-sdd-integration/tasks.md \| wc -l` | 「远大于 28」 | `197` |

**漂移登记 1（条款提及数 85 → 99）**：两轮 analyze 修复轮在契约之间新增了互引（条款正文引用其它条款 id），使*提及*数上升；**定义数仍为 77**。本行的判据是「提及数 ≠ 定义数」，该结论不变；`account-clause-coverage.py` 计的是定义数，不受影响。

## B. 引擎与模板现状（本特性要改的两处红）

| Premise | Re-derivation command | 本段复测（@`e14408f7`） |
|---------|-----------------------|--------------------------|
| 七模板三类 token 命中数 | `for f in requirements clarify plan tasks checklist analyze implement; do printf '%s=%s ' "$f" "$(grep -c -E 'flow_class\|flow-class\|expression' templates/commands/$f.md)"; done` | 七项各 `0`；正控 `docs=3`、`humanize=2` |
| `spec:` 键现状 | `python3 scripts/python/flow-class-check.py --action lookup --unit-id "spec:077-doc-sdd-integration"` | stderr `invalid unit id 'spec:077-doc-sdd-integration': expected /speckit.<stem> or skill:<dir>`；记录 `flow_class: execution` / `source: default` / `marker: null` / `basis: null` / `neutral: false`；退出码 **2** |
| `--action structure` 现状 | `python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/077-doc-sdd-integration` | `doc-consistency-check.py: error: argument --action: invalid choice: 'structure' (choose from 'verify')`；退出码 **2** |
| 台账现状 | `python3 scripts/python/flow-class-check.py --action check` | `79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]`；`coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39`；退出码 **0** |

## C. 分发基线

| Premise | Re-derivation command | 本段复测（@`e14408f7`） |
|---------|-----------------------|--------------------------|
| 镜像六对 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --check` | 六对全 `ok`（templates 22 / skills-external 406 / skills-internal 136 / agents 3 / scripts 117 / shared 60）；退出码 **0** |
| 命令副本 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.`；退出码 **0** |

## D. 七模板与基线提交逐字节相同（T009 / T010 的剥离判据起点）

命令：`for f in requirements clarify plan tasks checklist analyze implement; do git show "c1cd4600:templates/commands/$f.md" | shasum -a 256; done`

```text
requirements 31d0e1b43079a35f87c35029053ecee8557b75a282a5949079e2f90c6701a82b
clarify      baf687495d7f5bee1befbb61941aa348085148fe047c15360222e0ecab95cb92
plan         1833be4a713f7b9cc80f6953303428469e095f9f3efb9472dff225ec835f485c
tasks        205fa17fe0050ad1002f344783bb4239a5c70ef12144745e6883b45997d0c93d
checklist    54ca213e7c102af6eb8c173854863c1d19de34364001df31825fb7ccea387d8e
analyze      31dc261d9bf76243e4a50af62909dbb0c07fd7aa555ebf6acc0970c2eff8151b
implement    86974490811efa04008f955a44b60e2e739a36ea2bd83b6fe90e1af4c4d2eda9
```

同字节复算：`git hash-object templates/commands/<f>.md` 与 `git rev-parse c1cd4600:templates/commands/<f>.md` 对七个模板全部 `SAME`（接线尚未发生，剥离判据有可复算的起点）。

## E. 树面缺席项（本段要新建的路径）

| 检查 | 命令 | 实测 |
|------|------|------|
| 五个新测试文件不在树 | `ls tests/unit/test_flow_class_spec_key.py tests/contract/test_flow_class_spec_declaration.py tests/contract/test_stage_class_wiring.py tests/contract/test_document_structure_gate.py tests/contract/test_docs_gate_driver.py` | 五行 `No such file or directory` |
| `notes/` 证据槽不在树 | `ls -d .specify/specs/077-doc-sdd-integration/notes` | `No such file or directory`（T001 创建） |

## F. 测试预算起点（本段不重跑）

- 实现起点全量基线已由前一段落下：`.specify/specs/077-doc-sdd-integration/baseline-failed.txt`（39 条既有失败名，逐名与 076 closure 相同）；汇总 `6593 passed / 39 failed / 7 skipped`。
- 本段只用定向集（两个新测试文件 + 邻近引擎测试），**禁止全量**；39 条既有失败不得修、不得掩、不得算回归。
- plan 期定向基线：`test-evidence/plan-targeted-tests-baseline.txt` 末行 `1015 passed in 27.64s`（14 个既有测试文件）。
