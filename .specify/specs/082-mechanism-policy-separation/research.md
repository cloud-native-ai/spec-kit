# Research — 082 机制/策略分离（Phase 0 实测与设计探针）

**结论先行**：R1–R7 全部是 2026-11-05 在本仓的实测，没有一条从记忆或上一阶段的散文继承；R8 是两处**可判定的语义测试运行**（不是断言），R9 是 decision-tension 的门槛判定。

## R1 — 运行器与依赖实测（EP-001 的证据）

| 项 | 实测 |
|---|---|
| 默认 `python3` | `Python 3.9.6`（`/usr/bin` 侧），其 `pytest 8.4.2` |
| `scripts/bash/run-tests.sh` 解析到的解释器 | `.venv/bin/python` → `Python 3.14.6`；`pytest 9.2.0` |
| `git` | `git version 2.54.0 (Apple Git-157)` |
| `pyproject.toml` | `requires-python = ">=3.8"`（本特性不新增 pin） |

**发现（环境侧，非缺陷）**：本机 shell 的 `PYTHONPATH` 指向一套内部 lib 目录（`cloud-native-tools/cws-lib-python/{src,lib}`），其中携带 `platformdirs 4.10.0`，而 `.venv` 安装的是 `platformdirs 4.14.3`；`site-packages/platformdirs/` 目录已不在，但其 `dist-info` 仍声明 `pytest11` 入口点 `platformdirs.pytest_plugin`。结果是**只要 `PYTHONPATH` 在，`.venv/bin/python -m pytest` 在启动前就报**：

```
Error while loading plugin "pytest11".
ModuleNotFoundError: No module named 'platformdirs.pytest_plugin'
```

处置：测试必须用 `env -u PYTHONPATH bash scripts/bash/run-tests.sh …` 运行（见 R2 与 `test-evidence/plan2026-11-05-baseline.txt` 的逐字命令）。**这不改变仓内任何文件**，也不改变 RS-002 的行为；它是一条记录下来的运行前提，写进 EP-001 的证据列。`run-tests.sh` 的解析顺序（`SPECKIT_PYTHON` → `.venv/bin/python` → `python3`）未改，本特性 MUST NOT 因这条环境事实修改脚本。

## R2 — 定向集基线（GM-08 的实现期基准）

命令（逐字，见 `test-evidence/plan2026-11-05-baseline.txt`）：

```
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  --names-out <tmp>/impact-names.txt \
  tests/contract/test_merge_provenance_gate.py tests/contract/test_expression_compatibility.py \
  tests/contract/test_one_source_of_truth.py tests/contract/test_bilingual_expression.py \
  tests/contract/test_token_efficiency_gates.py tests/contract/test_feedback_skill_conformance.py \
  tests/contract/test_mirror_parity_suite.py tests/contract/test_glossary_mechanism.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_directory_governance.py \
  tests/contract/test_portable_skill_creation.py
```

结果：`892 passed in 16.66s`，失败名集空。

另一组（写入/路径前置检查）追加 `tests/contract/test_baseline_preflight_contract.py tests/contract/test_specify_script_paths.py` → `16 passed`。

全量套件在**污染环境**（`PYTHONPATH` 在）下跑过一次作为对照：`25 failed, 7148 passed, 7 skipped`；这 25 条里 4 条 `test_wp_mutation_drills.py` 相关失败经定位属环境/并发副作用，因此**全量结果不作为本特性的基线**，只作为「绝对全绿判据不可用」的证据（GM-08 的差集判据由此而来）。

## R3 — 允许差异集会撞上哪些既有冻结

本特性改五个技能文件，其中三个在既有冻结哈希清单里（`tests/contract/test_expression_compatibility.py` 读取 `.specify/specs/069*/notes/pre-change-file-hashes.txt`，含 `skills/external/{create-skills,improve-skills,merge-skills}/SKILL.md`）：

- 该模块以 `ALLOWED_POST_BASELINE_CHANGES` 登记表处理「合法改动」：每条登记带 `reason` + `markers`（改动后文件必须包含的字面）。**实测**：`test_c5_non_wiring_files_keep_their_frozen_hashes` 通过，说明登记机制是活的，且 `WIRING_SKILLS` 当前恰为 `create-docs` / `humanize` 两个，不覆盖三个元技能。
- 结论：实现期 MUST 在 `ALLOWED_POST_BASELINE_CHANGES` 追加三行（每个被改元技能一行），`markers` 取该技能新判定里**唯一**的字面（如 owner 路径或判定 id），MUST NOT 放宽哈希清单本身。
- `tests/contract/test_mirror_parity_suite.py`、`test_skill_layer_visibility_guards.py`、`test_feedback_skill_conformance.py` 的基线全绿（R2 内），实现期只需保证镜像同步后仍绿。

## R4 — 元技能的可插入点（逐文件实测）

| 文件 | 现状相关段落 | 本特性的插入点 | 依据 |
|---|---|---|---|
| `skills/external/create-skills/SKILL.md`（248 行） | § 3 已有 `${SKILL_HOME}` / `${SKILL_WORKDIR}` 约定（第 67–70 行）；§ 6 Validate 是 checklist（第 151–167 行）；无任何「技能 ↔ 运行环境」判定 | § 6 清单末尾新增一条 checklist 项 | A9 的现状读数在该文件层面成立 |
| `skills/external/improve-skills/SKILL.md`（156 行） | § 2 调研实现（第 39–42 行）；§ 5 有「Keep SKILL.md a contract」「Codify deterministic logic」（第 59–60 行），判的是技能**内部**；§ 3 冻结候选清单 | § 2 末尾调研问题 + § 3 候选类别 `policy source missing or ambiguous` | A9：现有两条相邻规则判的是「SKILL.md vs references/scripts」，不是「技能 vs 运行环境」 |
| `skills/external/merge-skills/SKILL.md`（165 行） | § 5 no-loss gate（第 74–87 行）、§ 8 验证（第 110–119 行） | § 5 之后一步前置判断 + § 8 一条验证项 | requirements § Clarifications 对 merge-skills 的取证 |
| `skills/external/coaching-skills/SKILL.md`（253 行） | `§ Compare` / `§ Improvement Plan` 产出观察与计划 | **不动**；排除理由只写进 owner 成员表 | C1 逐字谓词 |
| `skills/internal/run-skills/SKILL.md` | 目标技能按其自身流程执行 | **不动**；同上 | C1 |
| `templates/commands/skills.md`（73 行） | `### Routing` 表把 create / merge / coach 意图转发给元技能 | **不动**；命令面接线位声明在 owner 成员表 | C1 / A7 |

**`skill-shape.py` 实测（改动前基线，三份全部已超预算）**：

| 文件 | `skill-shape.py` exit | 可控正文 tokens / 预算 |
|---|---|---|
| `skills/external/create-skills/SKILL.md` | `10`（slim-recommended） | ≈ 5354 / 5000 |
| `skills/external/improve-skills/SKILL.md` | `10` | ≈ 5584 / 5000（已扣除契约强制块 466：`Agent-Specific Configuration`） |
| `skills/external/merge-skills/SKILL.md` | `10` | ≈ 5096 / 5000 |

**后果（写进 EP-004）**：`improve-skills` Hard Constraint 3 要求被改的 `SKILL.md` 在 `skill-shape.py` 下 exit `0`，**否则** loop report 必须带一条**记录的例外**：① 合格情形（契约强制内联段落，或改动前就已 exit `10` 的基线），② 改动前后 `est_tokens_controllable` 两个数与差值。三份文件**改动前已全部 exit `10`**，即情形 ① 的第二支成立，本特性无需先修体积；但实现期 MUST 为**每个被改文件**记录 before/after 两个数与它们的 delta，且新增文本 MUST 保持「一行判定 + 路径引用」形态（MUST NOT 因此把 body 再增长为手册）。这是既有债务的披露，不是本特性引入的缺陷。

## R5 — 镜像与命令副本基线

`python3 scripts/python/sync-mirrors.py --check` → exit 0，六对全部 `ok`：`templates/` 22、`skills/external/` 409、`skills/internal/` 138、`agents/` 3、`scripts/` 119、`shared/` 62。

**推论**：本特性新增一个 `shared/definitions/` 文档后，`shared/` 对会从 62 → 63；这不是漂移，是同步后的新基线。MUST NOT 把这个数字写死在任何断言里（既有测试不钉这个计数，已验证 R2 全绿）。

## R6 — 封闭集的规模（SC-003 的分母，实测）

`git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/` → **575** 个文件（`skills/` 548 + `templates/commands/` 27）；工作树同区 `git status --porcelain` 为空、`git diff --stat aaee504c..HEAD -- skills/ templates/ commands/` 为空。

**因此** SC-003 的守卫必须报出 `compared=575` 形态的计数；一个把范围写错（例如漏了 `templates/commands/`）的守卫会静默比较更少的文件而仍绿（R2 的 `test_c5_non_wiring_files_keep_their_frozen_hashes` 就是因为钉了 74/25/49 三个计数才抓得住漏项）。

## R7 — 可用的确定性载体（决定「零新脚本」是否成立）

| 判定 | 确定性载体 | 结论 |
|---|---|---|
| owner 文档形态（章节、字面、双语） | pytest 契约测试（`tests/contract/`，stdlib + pytest 即可） | 不需要脚本 |
| 一源（owner 之外零复制） | 同上：分词/子串扫描在测试里完成 | 不需要脚本 |
| 元技能接线的存在/位置/唯一性 | 同上：按文件读行、定位章节、数判定条数 | 不需要脚本 |
| 封闭集逐字节（SC-003） | `git ls-tree` / `git cat-file` / `git diff --name-status` + `Path.read_bytes()` | 不需要脚本（git 是运行时栈 RS-003） |
| 零写入（SC-004 主面） | `tmp_path` 快照（路径集 + sha256）在测试里比较 | 不需要脚本 |
| 题集可解析（SC-001/SC-005 分母） | 同上：解析 owner 附录表格 | 不需要脚本 |
| 语义判定（这条内容归哪一层） | **只有模型/人** | 因此落 SC-001 双判定者与 SC-002 流程实录，MUST NOT 正则化 |
| 技能形状/红线 | 既有 `${SKILL_HOME}/scripts/{skill-shape,redline-check}.py` | 复用 |

**结论**：A6 / C8 的「不预设脚本」在本阶段被证实**可兑现**——所有可判定的部分都有既有载体（pytest + git + 两个既有技能脚本），不可判定的部分本来就不该变成 Gates（`contracts/guard-and-measurement.contract.md` GM-02）。这是 D2 的证据，不是偏好。

## R8 — 两处语义测试的**可判定性实测**（SC-001 的预演）

本阶段对 owner 文档要写的两类条目做了两轮「同判据、不同读法」的自查（同一 agent 两遍，**证据等级弱于**双独立判定者，仅用于确认判据无歧义）：

| 样本 | 读法 A | 读法 B | 是否一致 |
|---|---|---|---|
| 技能正文写 `输出到 /Users/<me>/out/` | 策略（环境绑定） | 策略（换环境要改） | 一致 |
| `references/runbook.md` 里的「先校验再写入再报告」三步 | 机制（步骤顺序） | 机制 | 一致 |
| `.specify/state/<line>.md` 的写入路径 | 策略（根） | 策略 | 一致 |
| 同一句里的「写状态到 `.specify/state/`」 | 拆开判：动作规则机制、根策略 | 同 | 一致（拆法是 requirements Edge Case 已定的） |
| 脚本 `coverage_probe.py --emit-baseline <path>` | 逻辑机制 / 参数策略 | 同 | 一致 |
| 双语标题 `机制/策略分离(Mechanism–Policy Separation)` | 不构成内容（语言不参与判定） | 同 | 一致 |

**发现**：唯一需要「拆开判」的形态是第 4 条，requirements § Edge Cases 已经给出拆法，因此 owner 只需**指向**该拆法而不需新增规则（OD-03）。SC-001 的 100% 一致率要求因此是可达的，但**真正的分母**由 owner 附录题集（E-7，≥ 12 条）在 implement 期给出——本阶段的 6 条自查不进入 SC-001 的分母。

## R9 — Decision Tension 门槛判定

按 `.specify/shared/guidelines/decision-tension.md` § 承重门槛：
- **不可逆**：写入 `ALLOWED_POST_BASELINE_CHANGES` 与新增 owner 文档都是可回滚的文本改动 → 不成立。
- **跨团队**：本特性改变的是**元技能作者/改进流程的判定义务**，而这三个元技能是框架分发给所有下游项目的能力；下游作者的行为会因此改变 → **成立**。
- **高爆炸半径**：误置判定误报会让每个下游项目的技能创建流程多一条强制改正 → **成立**。
- **触及宪法 MUST**：直接触及 Principle XIV（一源）、XVII（目录治理）、XI（两顶帽子）→ **成立**。

`plan.md` § Decision Tensions 因此写 **T-001 … T-003** 三条记录（载体、接线形态、零脚本+零命令面）。

## 未决与交下一阶段

- 三个「分母待定」项（SC-001 题集 / SC-002 样本集 / SC-005 读者样本）在本阶段被**落成 owner 附录的封闭题集**（E-7）——分母不再是「待定」，而是「由 owner 附录给出，数量 ≥ 12，implement 期冻结」。requirements checklist 记录的缺口由此关闭。
- `improve-skills` 的 `skill-shape.py` 结果只能在实现后测（现在测的是改动前），因此 EP-003 状态记 `unverified` 并写明由哪个任务闭合。
