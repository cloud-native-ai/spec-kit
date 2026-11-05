# Quickstart — 082 机制/策略分离与技能引用归一化（可执行场景）

每个场景标注三件事：**执行口径**（本次 plan 运行实际跑过 = `run`；依赖尚未落地的产物 = `deferred`，并列出它依赖的前提）、**命令逐字**、**判据**。所有命令在仓根执行。

> 本文件属于 `/speckit.plan` 的 Post-Generation Quality Gate 的 execution-verify 范围：`run` 的场景含**实际输出**；`deferred` 的场景逐条列出它假设的 flags、ID 形态、文件位置与工具行为（见各场景末尾的 **Premises**），供 `/speckit.tasks` 与 `/speckit.implement` 重新测量而不是继承。

**场景总表（14 个；`run` 10 / `deferred` 6；S5 前后各半）**

| 场景 | 主题 | 口径 |
|---|---|---|
| S1 | 运行器与测试入口 | `run` |
| S2 | 定向集基线 | `run` |
| S3 | 镜像与命令副本基线（本轮复跑） | `run` |
| S4 | SC-003 封闭集预演 | `run` |
| S5 | 元技能形状与红线 | `run`（before）/ `deferred`（after） |
| S6 | SC-004 零写入模块 | `deferred` |
| S7 | SC-002 宿主实录 | `deferred` |
| S8 | SC-001 / SC-005 题集作答 | `deferred` |
| S9 | 阶段门（本轮复跑） | `run` |
| S10 | 归一化顺序探针的读数复核 | `run` |
| S11 | SC-006 矩阵首次全绿 | `deferred` |
| S12 | 安装态下源路径能否解析到镜像（EP-007(a)） | `deferred` |
| S13 | 五消费方的引用坐标实测 | `run` |
| S14 | 引用侧测试现状 | `run` |

## S1 — 运行器与测试入口（`run`）

```bash
.venv/bin/python --version && .venv/bin/python -m pytest --version
git --version
```

实测输出（本阶段）：

```
Python 3.14.6
pytest 9.2.0
git version 2.54.0 (Apple Git-157)
```

**判据**：三者与 `research.md` § R1 一致；不一致时本文件里的「基线 892 passed」不再可比（GM-08 的差集判据失效，须重测基线）。

**Premises**：`.venv/` 已就位；`PYTHONPATH` 未参与（下一条 S2 专门处理）。

## S2 — 定向集基线（`run`）

```bash
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  --names-out "$TMPDIR/mp-plan-probe/impact-names.txt" \
  tests/contract/test_merge_provenance_gate.py tests/contract/test_expression_compatibility.py \
  tests/contract/test_one_source_of_truth.py tests/contract/test_bilingual_expression.py \
  tests/contract/test_token_efficiency_gates.py tests/contract/test_feedback_skill_conformance.py \
  tests/contract/test_mirror_parity_suite.py tests/contract/test_glossary_mechanism.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_directory_governance.py \
  tests/contract/test_portable_skill_creation.py
```

实测输出：`892 passed in 16.66s`；`--names-out` 文件写入 0 条失败名（逐字见 `test-evidence/plan2026-11-05-baseline.txt`）。

**判据**：实现期以同一命令 + 11 个新模块 + 1 个测试辅助重跑，`实现后失败集 − 本基线失败集（空）` 必须为空（GM-08 的差集判据，MUST NOT 用绝对全绿）。

**Premises**：`run-tests.sh` 优先解析 `.venv/bin/python`（未改）；`env -u PYTHONPATH` 是必要的，否则 pytest 无法启动（`research.md` § R1 的逐字报错）；`$TMPDIR` 是本机受制裁的临时根，`--names-out` 的落点不进入仓内。

## S3 — 镜像与命令副本基线（`run`，本轮复跑）

```bash
python3 scripts/python/sync-mirrors.py --check; echo "rc=$?"
python3 scripts/python/regen-command-copies.py --check; echo "rc=$?"
```

实测输出（`sync-mirrors.py --check`，逐行）：

```
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (63 files)
rc=0
```

**判据**：实现关闭时两条 `--check` 仍 exit 0；**六对全 `ok` 且无新增漂移**。`shared/` 的文件数已从 62 变为 **63**（并发 owner 文档的镜像已生成，`cmp` 通过）——这是同步后的**新基线**，MUST NOT 被写死进任何断言。

**Premises**：`scripts/python/` 下这两个引擎存在且未改；`.specify/` 镜像当前与源逐字节相等（上面逐行证明）；`shared/` 计数是**实测值**而非期望值，只作为本次运行的读数。

## S4 — SC-003 封闭集预演（`run`）

把 `data-model.md` § GM-03 的补集断言写成一次性的只读探针（仓外运行，不进入交付面），逻辑是：取基线路径集 → 减去允许差异集 → 逐字节比较补集内每个文件。

```bash
BASE=3ffeb26e
python3 - "$BASE" <<'PY'
import subprocess, sys
base = sys.argv[1]
paths = subprocess.run(["git","ls-tree","-r","--name-only",base,"--","skills/","templates/commands/"],
                       capture_output=True, text=True, check=True).stdout.split()
allowed = {  # data-model.md § GM-03 第 1–8 行（比较单元内的允许差异路径）
 "skills/external/create-skills/SKILL.md",
 "skills/external/create-skills/references/mechanism-policy-check.md",
 "skills/external/improve-skills/SKILL.md",
 "skills/external/improve-skills/references/loop-playbook.md",
 "skills/external/merge-skills/SKILL.md",
 "skills/external/merge-skills/references/provenance-record.md",
 "skills/external/coaching-skills/SKILL.md",
 "skills/internal/run-skills/SKILL.md",
}
comp = [p for p in paths if p not in allowed]
bad = 0
for p in comp:
    blob = subprocess.run(["git","cat-file","blob","%s:%s" % (base, p)], capture_output=True).stdout
    try:
        cur = open(p, "rb").read()
    except OSError:
        bad += 1; continue
    if blob != cur:
        bad += 1
print("compared=%d complement=%d allowed_in_unit=%d frozen_mismatches=%d"
      % (len(paths), len(comp), len(allowed & set(paths)), bad))
PY
```

实测输出（改动前）：

```
compared=575 complement=570 allowed_in_unit=5 frozen_mismatches=0
```

**读法**：`allowed_in_unit=5` 表示允许集 8 条里已在基线**路径集**中存在的条数（`mechanism-policy-check.md` 是新增文件，必然不在基线；`coaching-skills` 与 `run-skills` 两份今天与基线逐字节相同，仍在路径集内）。实现后允许集里 8 条路径全部**存在且内容改变**，守卫的判据是 `frozen_mismatches` 仍为 0 且分母仍为 575。**判据**：`compared` 必须为 575（分母非零），`frozen_mismatches` 为 0；`allowed_in_unit` 只作为读数披露，MUST NOT 被写成断言常量。

**Premises**：基线提交 `3ffeb26e` 在本仓可达（`git cat-file -e 3ffeb26e^{commit}`）；比较单元 = `skills/` + `templates/commands/`（不含 `.specify/` 镜像与 `__pycache__`）；`git cat-file blob` 可用（RS-003）。

## S5 — 元技能形状与红线的 before/after（before = `run`，after = `deferred`）

```bash
for n in create-skills improve-skills merge-skills; do
  python3 skills/external/improve-skills/scripts/skill-shape.py "skills/external/$n/SKILL.md"; echo "$n shape rc=$?"
  python3 skills/external/improve-skills/scripts/redline-check.py "skills/external/$n/SKILL.md"; echo "$n redline rc=$?"
done
```

实测（**改动前**）：

| 文件 | `skill-shape.py` rc | `redline-check.py` rc / verdict |
|---|---|---|
| `create-skills` | 10（可控 ≈ 5354 / 5000） | 0 / `PASS — no red line triggered` |
| `improve-skills` | 10（可控 ≈ 5584 / 5000） | 0 / `PASS — no red line triggered` |
| `merge-skills` | 10（可控 ≈ 5096 / 5000） | 0 / `PASS — no red line triggered` |

**判据（before 半）**：三份 `skill-shape.py` 均 rc **10**（改动前就已超预算，属 `improve-skills` Hard Constraint 3 情形 (a) 的基线）；三份 `redline-check.py` 均 rc **0**。

**判据（after 半，`deferred`）**：实现后 MUST 为每个被改文件记录 `est_tokens_controllable` 的 **before / after 两数与 delta**；`redline-check.py` MUST 仍为 rc 0（转红则按 red-lines 处置，MUST NOT 静默例外）。coaching-skills 与 run-skills 同批记录（对照：shape rc 0 / redline rc 0）。

**Premises（after 半）**：实现期的被改文件集与 GM-03 第 1–8 行一致；`skill-shape.py` 的预算为 5000 可控 tokens 且 `--help` 可查；`redline-check.py` 的位置参数是 `skill_md` 路径；脚本位于 `skills/external/improve-skills/scripts/`（不在 `.specify/scripts/python/`）。

## S6 — 消费侧「策略缺失 → 零写入」（`deferred`，实现期）

```bash
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  tests/contract/test_mechanism_policy_missing_policy.py
```

**判据**：测试在 `tmp_path` 内造「假技能 + 假运行目录」，先取路径集 + sha256 快照，再走 owner § Consumption Contract 的检查（缺策略分支），断言快照逐文件相等（零写入），随后补齐策略重跑，断言产物哈希等于基线产物哈希。

**Premises**：`tests/contract/test_mechanism_policy_missing_policy.py` 由实现期创建（`data-model.md` E-5、`contracts/guard-and-measurement.contract.md` GM-05）；`tmp_path` 由 pytest 提供（既有 `tests/conftest.py`）；被检对象是 **owner 契约文本 + 文件系统快照**，不是 AI 行为；模块在 owner 文档落地前以「artifact missing」红（GM-01 的红先行形态）。

## S7 — SC-002 的宿主实录（`deferred`，实现期，证据而非测试）

**命令形态**：在一个受支持宿主上对同一技能草稿跑一次 `create-skills`（或 `improve-skills`），改动前 / 改动后各一次；命令由宿主自身的加载方式决定，本文件不预设 CLI flag。

**判据**：误置样本 ×2（策略误置：正文含一个绝对路径；机制误置：一段判定规则住在用户目录说明里）+ 正确分层样本 ×2；改动后 2/2 被点名（文件 + 位置）、2/2 零误报；改动前同流程对正确样本同样零误报。记录落 `test-evidence/sc-002-<date>.txt`，含宿主名 + 版本原文、输入草稿路径、输出原文、逐样本 verdict 表。

**Premises**：宿主取自 `docs/reference/cli/supported-agent-tools.md` 的 roster（`AGENT_CONFIG` 为准；RS-005）；`create-skills` § 6 的判定行已落地（SW-01）；样本草稿放在受制裁的临时根（`.specify/.tmp/` 或 `tmp_path`），MUST NOT 落到仓内未登记目录；`test-evidence/sc-002-*.txt` 的命名形态 `<date>` = `YYYY-MM-DD`。

## S8 — SC-001 / SC-005 的题集与作答（`deferred`，实现期）

**判据**：owner § Worked Examples 的题集 ≥ 12 条（`data-model.md` E-7 / V-21）；两位 fresh-context 只读判定者**仅凭 owner 文档**作答，一致率 100%（SC-001）；一位未参与本特性的读者作答，正确数 = 题集全集（SC-005）。记录落 `test-evidence/sc-001-<date>.txt` 与 `test-evidence/sc-005-<date>.txt`。

**Premises**：`shared/definitions/mechanism-policy-definitions.md` 与附录题集已创建；判定者不能读到 `requirements.md` / `plan.md` / `data-model.md`（只读 owner，否则分母被污染）；题集的 `basis` 列可被 `test_mechanism_policy_decidability.py` 解析；两份记录共用**同一份**题集分母，MUST NOT 另起一份。

## S9 — 阶段门（`run`，本轮复跑）

```bash
python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/082-mechanism-policy-separation --stage plan --repo .
python3 scripts/python/validate-requirements.py \
  .specify/specs/082-mechanism-policy-separation/requirements.md
python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan \
  --requirements .specify/specs/082-mechanism-policy-separation/requirements.md
python3 .specify/skills/sdd-loop-driver/scripts/overlap-check.py \
  --spec-dir .specify/specs/082-mechanism-policy-separation --repo .
```

实测（本轮逐字见 `test-evidence/plan-scope-update-gates.txt`）：

| 命令 | 读数 |
|---|---|
| `pre-analyze-check.py --stage plan` | `decision=pass errors=0 advisories=127 waived=0`（2026-11-05 repair pass 逐字复跑；`tasks.md` 落地后读数由 97 升至 127，增量全部是 `missing-path` advisory，指向本计划声明为 to-be-created 的路径） |
| `validate-requirements.py` | `status: ok`、`39 definition rows`、`0 error(s), 0 warning(s)`、六项检查全 `pass` |
| `decomposition-check.py --mode plan` | `{"decision": "proceed", "measured": {"fr_count": 30, "fr_ceiling": 60, "task_ceiling": 80}, "reasons": []}` |
| `overlap-check.py` | `overlaps=18 decision=overlap`（2026-11-05 复跑；`same-path` 18 条 = `shared/workflow/glossary.md` 3 条 + 五份 `SKILL.md` 15 条，全部是与既有特性（`059` / `062` / `063` / `078` / `029` / `044` / `051` / `057`）的**历史已完成重叠**，按状态脊 § Overlap adjudication 记录；逐条原文见 `test-evidence/analyze-repair-gates.txt`。两份新 owner 文档与三份 `references/` 无任何重叠） |

**判据**：门 1 `decision=pass` 且 `errors=0`（advisory 允许——**本轮读数 127 条**，全部是 `missing-path`，逐条指向本计划声明为 to-be-created 的产物或在 `checklists/requirements.md` 里的占位写法）；门 2 `status ok`；门 3 `decision=proceed` 且 `fr_count=30` / `fr_ceiling=60`；门 4 的 `overlap` 不得含 `shared/workflow/glossary.md` 以外的**新**交付路径（`skill-reference.contract.md` 的 SR 组不新增交付路径行）。

**Premises**：本仓 `.specify/skills/sdd-loop-driver/` 已安装（镜像自 `skills/external/sdd-loop-driver/`）；`validate-requirements.py` 的计数字面以那次运行为准（本文件不手抄 FR / SC 计数）；overlap 检查对**已完成的**历史特性的交付面也计入比较（081 复跑同样报 29 条），故 `clear` 在「新特性修改既有共享文件」这一常态下不可达。

## S10 — 归一化顺序探针的读数复核（`run`）

本阶段**不重跑探针代码**（clarify 期的一次性脚本不在仓内，也不许新增门禁脚本）；改为直接消费 clarify 已落盘的逐字输出，并与声明的六步顺序逐条对账：

```bash
sed -n '1,40p' .specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-fixture-probe.txt
python3 -c "import json;d=json.load(open('.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-fixture.json'));print(d['id'], len(d['rows']))"
```

实测（消费的既有读数，非本轮新跑）：

```
rows=14 current_unique_outcome_classes=2 (NAME,PATH) closed_three_way=False disagreements=none
FIXTURE-PROBE-01 14
```

**判据**：读数与 `research.md` § R10 一致——当前六步顺序只产生 NAME / PATH 两类，**无法产生 FR-030 的第三值（failure）**，且 `speckit.skills`（R05）与 `speckit.skills/SKILL.md`（R06）分属两类。这是 D12 与 GR-04 的反例证据，不是偏好。

**Premises**：`test-evidence/clarify-scope-update-fixture-probe.txt` 与 `.json` 已在 `518466db` 中提交（`git cat-file -e 518466db:.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-fixture.json`）；被复核的是**当时**的 owner 正文，实现期改写后该读数不再代表现状，须由 S11 的矩阵复算重新取证。

## S11 — SC-006 矩阵首次全绿（`deferred`，实现期，本轮新增）

```bash
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  tests/contract/test_skill_reference_matrix.py tests/contract/test_skill_reference_grammar.py \
  tests/contract/test_skill_reference_consumers.py tests/contract/test_skill_reference_command_surface.py \
  tests/contract/test_skill_reference_failures.py
```

**判据**：`tests/contract/skill_reference_matrix.py` 逐行复算 `tests/fixtures/skill-reference/normalization-matrix.json`，打印 `rows=N matched=N failed=0`；**分母 N ≥ 12**，任一行不匹配即失败（GM-13）；每行的 `expect.outcome` ∈ {`command-surface`, `skill`, `failure`} 且 `failure` 行的 `failure_class` ∈ E-10 四值；`surface` / `failure` 子段各自非空（SC-008 正例 ≥ 2 + 负例 ≥ 1；SC-009 四类各 ≥ 1）。逐字输出落 `test-evidence/sc-006-<date>.txt`。

**Premises**：五个 pytest 模块与 `skill_reference_matrix.py` 由实现期创建（`contracts/guard-and-measurement.contract.md` GM-11）；fixture 以 `test-evidence/clarify-scope-update-fixture.json` 的 14 行为**起点**扩展（不是另起一份）；`skill_reference_matrix.py` 是 **test-only** 辅助（MUST NOT 进入 `scripts/`、MUST NOT 成为门禁）；模块在 owner 定稿前以「artifact missing」红。

## S12 — 安装态下源路径能否解析到镜像（EP-007(a) 的唯一闭合点）（`deferred`，实现期，本轮新增）

```bash
# 在一次性安装副本上验证，不污染当前仓
python3 scripts/python/sync-mirrors.py --check; echo "sync rc=$?"
test -f .specify/shared/definitions/skill-reference-definitions.md && echo "mirror present"
cmp shared/definitions/skill-reference-definitions.md .specify/shared/definitions/skill-reference-definitions.md && echo "mirror byte-identical"
grep -rn "\.specify/shared/definitions/skill-reference-definitions.md" skills/ --include=SKILL.md | wc -l
```

**判据**：① `sync-mirrors.py --check` rc 0；② 镜像存在且与源 `cmp` 逐字节相同；③ 五份消费方 `SKILL.md` 中对 `.specify/shared/definitions/…` 的引用串计数 = **0**（SR-05 的断言面）；④ 另需一次**安装态**实跑（在 `specify init` 产出的临时项目里确认「以相对框架根解析」能命中镜像），其结果写入 `test-evidence/`，这是 EP-007(a) 从 `unverified` 变绿的唯一依据。

**Premises**：`.specify/shared/definitions/` 与 `shared/definitions/` 的相对拓扑在所有部署形态下相同（`research.md` § R14 的判别项表）；安装态样本在一个受制裁的临时根下生成（`$TMPDIR`，MUST NOT 落在仓内）；本阶段**没有**安装态样本，故本场景在本阶段记 `deferred` 而非 `run`——判据 ①②③ 可达、④ 不可达。

## S13 — 五消费方的引用坐标实测（`run`，本轮新增）

```bash
for f in skills/external/create-skills/SKILL.md skills/external/improve-skills/SKILL.md \
         skills/external/merge-skills/SKILL.md skills/external/coaching-skills/SKILL.md \
         skills/internal/run-skills/SKILL.md; do
  printf '%s\t' "$f"; grep -c 'skill-reference-definitions' "$f"
done
grep -rn 'skill-reference-definitions' skills/ --include='SKILL.md' | grep -c '\.specify/shared/definitions/'
cmp shared/definitions/skill-reference-definitions.md .specify/shared/definitions/skill-reference-definitions.md && echo "owner mirror in sync"
```

**判据**：逐文件计数之和 = **8**（`create-skills` 1 / `improve-skills` 1 / `merge-skills` 1 / `coaching-skills` 3 / `run-skills` 2），且其中**镜像路径**形式 = 8（今天全部是镜像路径）；`cmp` 一致说明这只是**引用坐标错**、内容未漂移。实现期的判据是镜像路径形式的计数 = **0**（SR-05 / GR-08）。

**Premises**：五份源 `SKILL.md` 在工作树中存在（并发实现已在工作树，A11 / FR-027）；行号会随编辑漂移，故判据用**文件 + 引用串内容**而不钉行号（`research.md` § R11）；`.specify/skills/` 侧的 8 处由 `sync-mirrors.py` 生成，改源即改镜像。

## S14 — 引用侧测试现状（`run`，本轮新增）

```bash
grep -rl 'skill-reference' tests/ | wc -l
ls tests/fixtures/ | wc -l
test -d tests/fixtures/skill-reference && echo "fixture dir present" || echo "fixture dir absent"
```

**判据**：`tests/` 对 `skill-reference` 的命中 = **0**（R12），`tests/fixtures/` 下现有 **12** 个按特性命名的夹具目录且**没有** `skill-reference/`——即引用侧测试**尚不存在**，SC-006…SC-009 是本计划的真正新增工作量，不是「核验已有测试」。

**Premises**：`tests/fixtures/` 的既有 12 个目录按特性命名（`acceptance-hardening/`、`bilingual/`、`coaching/`、`docs_command/`、`expression_line/`、`flow_class/`、`humanize/`、`sanitize/`、`sdd_loop_efficiency/`、`skill-layout/`、`teams/`、`todo-workspaces/`）；新增的 `tests/fixtures/skill-reference/` 是第 13 个（既有根下的新子目录，不是新根，D13 / FR-029）。
