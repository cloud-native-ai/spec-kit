# Research — 082 机制/策略分离（Phase 0 实测与设计探针）

**结论先行**：R1–R9 是第一个能力（机制/策略分离）的证据，R10–R15 是第二个能力（技能引用归一化）的证据；全部是 2026-11-05 在本仓的实测，没有一条从记忆或上一阶段的散文继承。R8 是两处**可判定的语义测试运行**（不是断言），R9 与 R15 是 decision-tension 的门槛判定，R10 是**程序输出**而非阅读。

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

## R10 — 归一化顺序的探针读数（第二能力的起点，FR-021/FR-030 的证据）

**这不是一次阅读，是一次程序输出**。本阶段对 clarify 裁决 (1) 主张的「现行顺序无法产生三值输出」做了可复算的复现：探针按 owner 文档**今天写明的步骤**（其 steps 1–5）对 14 行 fixture 逐行分类。

| 项 | 值 |
|---|---|
| fixture | `test-evidence/clarify-scope-update-fixture.json`，id `FIXTURE-PROBE-01`，14 行 |
| 逐字捕获 | `test-evidence/clarify-scope-update-fixture-probe.txt` |
| owner 文档被读时的 sha256 前缀 | `28432cd08257`（**只读**，本次运行未写入） |
| 读数 | `rows=14 current_unique_outcome_classes=2 (NAME,PATH) closed_three_way=False disagreements=none` |

**发现（三条，各对应 FR-030 / SC-006 的一个缺口）**：

1. **结果类只有两个**（NAME、PATH）——FAILURE 在现行过程中**不可表达**；失败由位置阶梯与信任边界两份别的文档在下游决定，这正是 FR-030 禁止的「第四种结果」。
2. **R05 vs R06 同一命令名分属两类**：`speckit.skills` → NAME，`speckit.skills/SKILL.md` → PATH。这是「通道判定先于剥离」的直接后果（plan.md § D12 residue 表第 1 行）。
3. **R14 `my-draft.md` → NAME `"my-draft.md"`**，而 `run-skills` 明说名字可省略扩展名——同一输入的两种合法读法，属 § D12 residue 表第 3 行，归属 requirements 已裁的扩展名条款，不是类错误。

**结论**：TARGET 顺序（判别 → 去空白/包裹引号 → 剥 `skill:` 与一段 `@`/`/` 前缀 → 剥 `SKILL.md`/尾 `/` → 通道判定 → 三值）**不是偏好，是被这两个可复算读数逼出来的**；13 行现有期望与 TARGET 的差集即为 implement 期断言集的第一批行（SC-006 要求 ≥ 12 行，fixture 给 14 行）。探针脚本本身在仓外（scratch），**不进入交付面**——被提交的是 fixture 与逐字捕获，复算因此可做（同 fixture + 同顺序 = 同表）。

## R11 — 消费方引用坐标的实测（SR-05 / GR-08 的分母）

clarify 裁决 ②（source-canonical）要改的是「引用串的写法」，因此分母必须是**当前存在的引用串**，不是「大概有几处」。全仓检索 `skill-reference-definitions`（排除 `.git`）后按坐标去重：

| 文件（源树） | 行 | 引用串里的路径口径 |
|---|---|---|
| `skills/external/create-skills/SKILL.md` | 35 | `.specify/shared/definitions/…`（镜像） |
| `skills/external/improve-skills/SKILL.md` | 20 | 镜像 |
| `skills/external/merge-skills/SKILL.md` | 27 | 镜像 |
| `skills/external/coaching-skills/SKILL.md` | 26 | 镜像 |
| `skills/external/coaching-skills/SKILL.md` | 48 | 镜像 |
| `skills/external/coaching-skills/SKILL.md` | 67 | 镜像（§ Nested） |
| `skills/internal/run-skills/SKILL.md` | 16 | 镜像 |
| `skills/internal/run-skills/SKILL.md` | 24 | 镜像 |

**合计 8 处引用串，全部是镜像路径**，分布在 5 份源 `SKILL.md`；镜像侧（`.specify/skills/…`）同样 8 处，但镜像由 `sync-mirrors.py` 生成（`--check` 本阶段复跑 rc=0），**改源即改镜像，不得手改镜像**（FR-028）。`coaching-skills` 的 § Nested 行（67）是同一替换的一次，不是额外规则——它仍在「8 处」之内。

**结论**：SR-05 / GR-08 的验收可逐坐标核对（8 行，行号会因编辑漂移，因此契约写的是**文件 + 引用串内容**而不是行号）；本阶段**不触碰**这五份未提交文件（派发边界），执行留 implement（plan.md § D11 已披露 test-vs-run 的落差）。

## R12 — 第二能力的测试载体：零命中（SC-006…SC-009 的现状）

```
grep -rl 'skill-reference' tests/   →  0 files
```

`tests/fixtures/` 下现有 12 个 fixture 目录（`acceptance-hardening/`、`bilingual/`、`coaching/`、`docs_command/`、`expression_line/`、`flow_class/`、`humanize/`、`sanitize/`、`sdd_loop_efficiency/`、`skill-layout/`、`teams/`、`todo-workspaces/`），**没有一个承载引用归一化矩阵**；`tests/contract/` 下与技能相关的既有测试（如 `test_run_skills_wiring.py`、`test_skill_layer_visibility_guards.py`、`test_expression_compatibility.py`）都不加载此类 fixture。

**结论**：SC-006 的「真实仓内位置」不能靠复用既有目录**宣称**满足——必须新增一个目录（plan.md § D13：`tests/fixtures/skill-reference/`，成为第 12 个既有 `tests/fixtures/` 兄弟目录，**不是新根**，FR-029/C4 不受影响）。同一读数也是 FR-027「核验/补齐」里最硬的一条缺口：现有实现**没有断言**。

## R13 — 五个消费方的接线落点（FR-026 的实现坐标）

逐份读工作树中的未提交实现，接线落点与「是否复制了语法」如下（读的是**当前状态**，不是承诺）：

| 消费方 | 接线落点 | 只声明自己参数？ |
|---|---|---|
| `run-skills` | § Input Contract（输入段）+ § 1 第 0 步（归一化先于位置阶梯） | 是（第 0 步只调 owner，不重述顺序） |
| `create-skills` | 输入解析段（skill name 定义行） | 是，且写明「新建时是**命名**而非解析」 |
| `improve-skills` | § Input Contract | 是 |
| `merge-skills` | § Input Contract | 是 |
| `coaching-skills` | § Inputs + § Nested | 是 |

**发现**：五份都**没有**复制接受形式清单或失败表，因此 FR-026 的「MUST NOT 复制」当前成立；但五份都引用**镜像**路径（R11），与 clarify 裁决 ② 冲突——这是 plan 必须落地、implement 执行的唯一实质缺口（SU-02 → SR-05 / GR-08 / T-004）。另一处需核验的落点漂移：`run-skills` 第 0 步把「剥前缀/后缀」自述了一遍（与 owner 的归一化顺序构成**第二份散文**），FR-026 允许它「声明自己的参数」，但不允许它成为第二 owner——implement 核验时 MUST 把该句收敛为「按 owner 归一化并披露」，否则 FR-019（唯一 owner）在文字层被破。

## R14 — 源路径 vs 镜像路径：取舍的可判别证据（T-004）

用一个**行为差**而不是偏好来判定：在框架源仓内，`skills/external/create-skills/` 与 `shared/definitions/` 的**相对拓扑**与安装后 `.specify/skills/…` 与 `.specify/shared/…` 的拓扑相同，因此「相对框架根解析」在两种模式下都成立；而绝对化的 `.specify/…` 在源树里指向一份**再生成副本**（本次并发实现两侧 `cmp` 相同，只因刚跑过 `sync-mirrors`）。

| 判别项 | 引用镜像路径 | 引用源路径 |
|---|---|---|
| 源仓内读到旧文的条件 | 改源后忘记重生成 → **会** | 不会 |
| standalone 部署（无 `.specify/`） | 路径不存在 | 相对框架根成立 |
| 与 SC-007 的分母冲突 | 有（把生成物当被引用坐标） | 无 |

**结论**：三条判别项一致指向源路径 → T-004 写入 plan（含 revision trigger：若某消费方确实需要「以安装根为锚的绝对坐标」，须由一次明确裁决引入，而不是让五份文件各写一种拼写）。本阶段该判定的**执行**受派发边界限制（不改那五份未提交文件），故 EP-007 记 `unverified` 并写明闭合任务。

## R15 — 第二能力的 Decision Tension 门槛

同一份承重门槛（`.specify/shared/guidelines/decision-tension.md` § 承重门槛）对第二个能力复判：

- **不可逆**：文本改动 + fixture 目录，可回滚 → 不成立。
- **跨团队**：五份消费方都是分发给下游项目的元技能，归一化是它们的公共前置 → **成立**。
- **高爆炸半径**：归一化错一个类，等于把用户的一条命令误当技能解析（或反之） → **成立**。
- **触及宪法 MUST**：Principle XIV（一源：引用文法唯一 owner）、XVII（目录治理：fixture 目录落位）、XI（两顶帽子：源 vs 镜像）→ **成立**。

三门槛成立 → 第二条记录 **T-004**（不新增记录数以外的张力：SU-03 的 `speckit.skills` 分类冲突由「先剥后判」闭合，属**纠正**而非判定，见 plan.md § Scope Update Record）。

## 未决与交下一阶段

- 三个「分母待定」项（SC-001 题集 / SC-002 样本集 / SC-005 读者样本）在本阶段被**落成 owner 附录的封闭题集**（E-7）——分母不再是「待定」，而是「由 owner 附录给出，数量 ≥ 12，implement 期冻结」。requirements checklist 记录的缺口由此关闭。
- `improve-skills` 的 `skill-shape.py` 结果只能在实现后测（现在测的是改动前），因此 EP-003 状态记 `unverified` 并写明由哪个任务闭合。
- 第二能力的**执行面**在本阶段只做到「读 + 判 + 记」，未落笔：R11 的 8 处引用串改写（SR-05 / GR-08）、R13 的 `run-skills` 第 0 步散文收敛、SC-006…SC-009 的断言（R12 的零命中）都归 implement，派发边界不允许本阶段改那五份未提交的并发实现文件。因此 EP-007 记 `unverified`，闭合点写在 `quickstart.md` § S11 / § S12。
- 探针（R10）的脚本留在仓外 scratch：本阶段**不新增门禁脚本**（D11 / FR-029）；被提交的是 fixture + 逐字捕获，复算靠「同 fixture + 同顺序 = 同表」。若 implement 要把同一张表变成可执行断言，那是 SC-006 的测试载体（`tests/contract/skill_reference_matrix.py` + 矩阵测试），不是新门禁。
