# Feature Detail: 脚本接口契约（Script Interface Contract）

**Feature ID**: 089
**Name**: 脚本接口契约（Script Interface Contract）
**Description**: 新增一条框架级通用治理规则：所有可直接执行的 `*.sh` / `*.py` 脚本 MUST 支持 `-h`/`--help` 与 `--version`，两者零副作用且判定先于主动作；未识别的选项 MUST 以非零退出码报错并给出用法，MUST NOT 被静默忽略后继续执行主动作；被 `source` / `import` 的纯库文件按机械判据豁免。规则落在五处（宪法模板、指令模板、本仓宪法、`manage-constitution` 的 MUST include 清单、镜像与双落地守卫计数 pin），并把本仓现存适用脚本补齐到契约。
**Status**: Implemented
**Created**: 2026-11-06 (renumbered 086 → 089 on 2026-11-09 to avoid the remote 086 collision; content unchanged)
**Last Updated**: 2026-11-06（tasks + checklist 阶段完成：`tasks.md` 87 行依赖任务、`validate-tasks.py` PASS（0 error / 62 warning）、`decomposition-check.py --mode tasks` = `proceed`（31 FR / 87 行，ceiling 120/160）、`account-clause-coverage.py --freeze` 落 `coverage-baseline.txt`（claimed clauses 38 / FR universe 31 / 573 冻结名，0 超基线）；两份 checklist：`checklists/requirements.md`（需求质量；checker 380 行 / 43 定义行 / 0 error）与 `checklists/contract-integrity-2026-11-06.md`（契约决策逻辑审计，C-1…C-38）；关键裁定：判据按运行语义（T-001）、镜像声明式投射替代逐字节相等（T-002）、宪法以 MINOR 增量随本特性落地（T-003）；`scripts/python/` 实测更正为 37 文件；状态保持 Planned。此前的 plan 阶段记录：`plan.md` + `research.md` R1–R13 + `data-model.md`（8 实体 / 22 规则）+ `contracts/` ×4（38 条款）+ `quickstart.md` S-0…S-8 + `feature-ref.md`；宪法动态检查 19/19 Pass；`pre-analyze-check.py --stage plan` `decision=pass`；`decomposition-check.py --mode plan` `proceed`；`validate-decision-tensions.py` 0 error / 3 记录）

## Overview

用户执行 `generate-instructions.sh --help` 想看接口，而该脚本没有参数解析：`--help` 被当作普通参数忽略，脚本继续执行其主动作（reconcile），向 `.specify/instructions.md` 追加了 11 个缺失的模板章节（+70 行 / 0 行删除）。这是一次**只读意图被解释为写入意图**的事故。

根因不是单个脚本的疏漏，而是框架里从来没有一条规则要求「可执行脚本必须声明自己的接口」。失效分三层：接口不可发现（没有 `--help` / `--version`）、未知参数被静默吞掉（`--help` 不是被拒绝而是被执行）、帮助路径本身没有被约束为零副作用。缺少第三层时，即使补上 `--help`，帮助信息与写盘仍可能同时发生。

本特性把规则本身作为交付物，并把本仓作为规则的第一批被检查对象：只写规则文字不补齐现存脚本，规则从第一天起就是假的。

## Latest Review

尚未进入 review。clarify 阶段（2026-11-06，模式 A）产出：9 条裁定、31 FR / 12 SC（10 `final` + 2 `supporting`）/ 7 用户故事 / 10 Assumptions；`validate-requirements.py` `status: ok`（374 行、43 定义行、0 error / 0 warning）；flow-class lookup 仍由声明行解析为 `execution`（exit 0）。

**clarify 的九条裁定（一句话各）**：

1. **候选面**＝`git ls-files` 减去 `.gitignore` 忽略者，另加一条覆盖断言（工作树里有文件既不在候选集也不在忽略集即报错）；`tests/` / `scripts/` / `skills/**` / `.specify/scripts/` / `src/` 全部逐文件判定，不做目录级豁免（FR-024）。
2. **bash 判据**从「有无顶层执行语句」改为「按脚本运行时守卫块之后的代码会不会执行」，`common.sh` 因此落在豁免侧（FR-025）。
3. **python 判据**从「有无 `__main__` 块」改为「入口载体执行时是否真的做事」；`tests/**` 与 `conftest.py` 不得因目录名豁免（FR-026）。
4. **owner 文档**落 `shared/definitions/script-interface-definitions.md`（判据表归 definitions，纪律归 guidelines）（A3）。
5. **`--version`** 输出单行 `<script-name> <framework-version>`，版本运行时读 `pyproject.toml`，脚本内零字面版本号（A4）。
6. **检查接线**＝新增 `scripts/python/script-interface-check.py` + 新增 `tests/contract/test_script_interface_contract.py`，不接 driver 门禁（FR-031）。
7. **已声明例外**登记在 owner 文档的 `## Declared Exceptions` 章节，检查器逐条复算判据、复算不成立即报错（FR-027 判据 + Key Entities 登记载体）。
8. **零副作用取证**在受测仓库之外的副本树上做前后快照比对；标志判定前置到所有写型副作用之前，bash 用 `"$@"` 扫描守卫块且在 source 共享库之前（FR-029）。
9. **`-h` 冲突**实测为零（本仓无脚本把 `-h` 用作其他含义），该 Edge Case 只作规则文本边界保留。

## Key Changes

1. **规则 owner 文档**：`shared/definitions/script-interface-definitions.md` 持有契约的判据、必备内容、豁免判据、第三方判据与 `## Declared Exceptions` 登记章节；宪法与指令侧只放摘要 + 指针。
2. **框架模板双落地**：`templates/constitution-template.md` 新增一条原则；`templates/instructions-template.md` 新增一条常驻段落（摘要 + 指针），下游项目经 `specify init` 获得。
3. **本仓宪法同步**：`.specify/memory/constitution.md` 按本仓编号顺延新增原则，产出版本 MINOR 增量、Sync Impact Report 与 Last Amended 更新。
4. **生成器清单**：`skills/internal/manage-constitution/SKILL.md` 的 `MUST include` 清单新增条目，使 `/speckit.constitution` 在下游项目把该原则视为必须存在项。
5. **契约检查**：`scripts/python/script-interface-check.py` 做机械候选屏 + 逐脚本四项结论（适用性 / help / version / 未知选项拒绝）+ 违规计数；由 `tests/contract/test_script_interface_contract.py` 消费，接入既有 pytest 契约面，不新增独立门禁。
6. **现存脚本补齐**：`scripts/bash/*.sh`、`scripts/python/*.py`、`skills/**/scripts/` 下的适用脚本补齐 `-h`/`--help`、`--version`、未知选项拒绝与零副作用，既有选项语义、JSON 输出与退出码逐字不变。
7. **守卫 pin 更新**：双落地守卫的 TEMPLATE_COUNT / LIVE_COUNT / COMMAND_COUNT 与 watchlist，以及 `test_fast_fail_discipline.py` 的计数一致性断言。

## Implementation Notes

- **既有两个前提被实测更正**（记入 requirements § Assumptions A2）：
  - `refresh-tools.sh` **有** `--help` 分支（含 `usage()`），任务简报把它列为「无 help」与实测不符；实测无 help 的是 `collect-history.sh`、`common-todo.sh`、`common.sh`、`detect-feature-context.sh`、`generate-instructions.sh`、`run-tests.sh` 共 6 个。
  - `.specify/instructions.md` 的 git 历史里**不存在** +70 行 / 0 删除的提交（最近改动是 082 的 `02fd6db5`）；故事故未进入版本控制，SC-002 写成自包含的可复现实验而不是与事故 diff 比对。
- **候选面比脚本目录大两个数量级**：仓库内 `*.sh` 71 个、`*.py` 666 个（含 `tests/`）。这是 FR-002 要求机械候选屏而非手写清单的直接理由。
- **豁免不是白名单**：判定只回答「该文件是否有独立入口」，且用的是**运行语义**而不是源码字面（bash：按脚本跑时守卫块之后的代码会不会执行；python：入口载体执行时是否真的做事）；同时具备两种用途的文件判为适用。
- **两条 requirements 期读数在 clarify 被实测更正**（记入 requirements § A2 更正段）：`scripts/python/` 下真正实现 `--version` 的是 **0** 个而非 2 个（那两处 `--version` 是 `subprocess` 探测别程序的参数）；`refresh-tools.sh` 有 `usage()` 与 `*)` 调用但没有 `--help|-h` 分支。误读成因正是本特性要治的「grep 命中即认为实现」。
- **第三方脚本不改上游**：随技能分发的脚本以已声明例外形态出现，必须在检查输出中可见，不得用目录级排除静默绕过。
- **零副作用是判定顺序问题**：标志判定必须前置于任何可能写盘或索要确认的前置检查（含镜像 refresh、日志目录、工具 manifest），否则查接口本身会被要求确认；取证必须在仓库之外的副本树上做，否则临时文件会掩蔽或误报一次真实写入。

## Related Files

- 规格：`.specify/specs/089-script-interface-contract/requirements.md`
- 质量检查单：`.specify/specs/089-script-interface-contract/checklists/requirements.md`
- 阶段门禁证据：`.specify/specs/089-script-interface-contract/test-evidence/requirements-gates.txt`
- 事故脚本：`scripts/bash/generate-instructions.sh`


## Merge note (2026-11-09)

2026-11-09 用户指令合并到 master 并推送；T086 零新增门未复测为绿（上次全量 78 新增，随后 instructions/neutrality/merge_provenance/client_capture/trigger_promotion 等族修复已清掉 ≥28，未在合并前复跑）；review 阶段按用户指令跳过。
