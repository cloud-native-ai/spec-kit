# Quickstart Run — 062-humanize-command（T031）

**执行日期**: 2026-10-19（attempt 2，断点续跑）
**执行者**: `/speckit.implement` 阶段执行器
**分支**: `062-humanize-command`
**工作目录**: 仓库根 `/storage/project/cloud-native-ai/spec-kit`（以下命令均在此目录执行）
**环境**: Python 3.11.11 / pytest 8.4.2；`CWS_LIB_BASH_HOME=/storage/project/cloud-native-tools/cws-lib-bash` 可解析（tasks.md § Environment Prerequisites 的 restored 状态）

> Attempt 1 在 T031 中途因瞬时的 `UnsupportedFinishReasonError` 终止，非任务逻辑失败。本次按 quickstart.md 重新实跑 S1–S8 并复核 attempt 1 的部分运行结果：
> compile `0 written / 74 unchanged`、regen OK、`sync --only` 2 pairs ok —— 三项均被本次复跑重现（见 S7）。

---

## S1 — 按工具副本生成面

```bash
python3 scripts/python/regen-command-copies.py --check
```

```
OK: all per-tool command copies match the source templates.
```

**exit 0** —— 生成面零漂移；四个 `speckit.humanize.*` 副本在位且含生成警告头。

## S2 — 镜像对（相对判据 + 触碰对绝对判据）

```bash
python3 scripts/python/sync-mirrors.py --check
```

关键输出：

```
DIFF  .specify/shared/workflow/glossary.md
...
DIFF  .specify/shared/workflow/user-input-protocol.md
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

**exit 2**（存在既有漂移，符合预期；本特性判据为相对形式）。实测：

| 指标 | 值 |
|------|-----|
| 当前 DIFF 条数 | **205** |
| 冻结基线 DIFF 条数（`notes/baseline-mirror-check.txt`） | 209 |
| `comm -13`（NEW drift 名字） | **空（0）** |
| `comm -23`（本轮顺带修复） | 4：`.specify/scripts/python/probe-utils.py`、`.specify/shared/definitions/probe-definitions.md`、`.specify/skills/internal/run-skills/SKILL.md`、`.specify/skills/internal/run-team/SKILL.md` |
| 触碰对 `humanize` / `probe-definitions` 的 DIFF 行 | **零命中** |

触碰对字节一致（两条 `diff -q` 均 **exit 0**）：

```bash
diff -q skills/external/humanize/SKILL.md .specify/skills/humanize/SKILL.md   # exit 0
diff -q shared/definitions/probe-definitions.md .specify/shared/definitions/probe-definitions.md   # exit 0
```

## S3 — Wrap-up 编译面

```bash
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```

```
compile-embeds --check: 74 units, zero drift
```

**exit 0**。基线为「73/73 旧指纹漂移」；实现后 74 单元（新增 `skill:humanize`）全部为当前指纹，零漂移。`skill:humanize` 不出现在 drift 名单（grep 命中数 0）。

## S4 — 测试基线复核（名字级）

```bash
bash scripts/bash/run-tests.sh --names-out /tmp/quickstart-failed-tests.txt
```

```
=========== 64 failed, 3951 passed, 3 warnings in 132.99s (0:02:12) ============
# failed-name list written: /tmp/quickstart-failed-tests.txt (64 entries)
```

名字级对比（`LC_ALL=C`，冻结名单 `notes/baseline-failed-tests.txt` 71 条，未改写、未放宽）：

```
baseline=71 current=64
comm -13 baseline current  → 0 条（零新增失败）
comm -23 baseline current  → 7 条（既有欠账顺带转绿）
```

7 条顺带转绿节点：

```
tests/contract/test_compile_propagation_order.py::test_compiled_fingerprints_match_the_runtime_registry
tests/contract/test_execution_config_engine.py::TestErrorsAndWarnings::test_warning_surface_is_json_and_stderr
tests/contract/test_phase2_bindings.py::test_wrap_up_compile_unaffected_by_phase2_rows
tests/contract/test_probe_registry_umbrella.py::test_feedback_utils_probe_validate_still_green
tests/contract/test_run_skills_wiring.py::test_c1_run_skills_canonical_and_mirror_identical
tests/contract/test_run_skills_wiring.py::test_c7_run_team_canonical_and_mirror_identical
tests/contract/test_run_skills_wiring.py::test_c9_compile_embeds_zero_drift_73_units
```

说明：本次 run 为 `64 failed / 3951 passed`（T026 run #2 为 `65 failed / 3950 passed`）；判据始终是名字级 `comm -13` 为空，而非总数比较。名单文件留在 `/tmp`（运行记录，不提交），冻结基线文件未被触碰。

## S5 — 契约条款提取

```bash
python3 -c "
import sys; sys.path.insert(0,'.specify/scripts/python')
from clause_extract import extract_clauses
total=0
for f in ['command-surface.md','rewrite-behavior.md','tone-input-file.md']:
    p='.specify/specs/062-humanize-command/contracts/'+f
    cs=extract_clauses(p)
    total+=len(cs)
    print(f, len(cs), ','.join(cs) if cs else 'NONE')
print('TOTAL', total)
"
```

```
command-surface.md 10 C-1,C-2,C-3,C-4,C-5,C-6,C-7,C-8,C-9,C-10
rewrite-behavior.md 14 C-11,C-12,C-13,C-14,C-15,C-16,C-17,C-18,C-19,C-20,C-21,C-22,C-23,C-35
tone-input-file.md 11 C-24,C-25,C-26,C-27,C-28,C-29,C-30,C-31,C-32,C-33,C-34
TOTAL 35
```

**exit 0**。

### S5b — FR 覆盖自检（修复记录）

**修复**: `clause_extract.clause_blocks()` 返回 `(clause_id, body)` 元组列表，不是字符串列表。attempt 1 的内联脚本直接 `'\\n'.join(clause_blocks(...))`，触发
`TypeError: sequence item 0: expected str instance, tuple found`。本次按返回类型解包后逐条款正文检索 FR 引用：

```bash
python3 -c "
import sys, re
sys.path.insert(0,'.specify/scripts/python')
from clause_extract import clause_blocks
contracts = ['command-surface.md','rewrite-behavior.md','tone-input-file.md']
expected = set(range(1,30))
covered = set()
for f in contracts:
    p = '.specify/specs/062-humanize-command/contracts/' + f
    ids=set()
    for cid, body in clause_blocks(p):
        for m in re.finditer(r'FR-0*(\d{1,3})', body):
            ids.add(int(m.group(1)))
    covered |= ids
    print(f, 'FR refs:', ','.join('FR-%03d'%i for i in sorted(ids)))
print('covered:', len(covered & expected), 'missing:', ','.join('FR-%03d'%i for i in sorted(expected-covered)) or 'NONE')
"
```

```
command-surface.md FR refs: FR-001,FR-002,FR-003,FR-006,FR-007,FR-015,FR-018,FR-020,FR-024,FR-025,FR-026,FR-027,FR-028,FR-029
rewrite-behavior.md FR refs: FR-002,FR-003,FR-004,FR-005,FR-006,FR-007,FR-008,FR-009,FR-010,FR-011,FR-012,FR-013,FR-021,FR-023,FR-026,FR-029
tone-input-file.md FR refs: FR-008,FR-014,FR-015,FR-016,FR-017,FR-018,FR-019,FR-020,FR-021,FR-022,FR-028
covered: 29 missing: NONE
```

**exit 0** —— FR-001..FR-029 全覆盖。

## S6 — 需求规格校验器

```bash
python3 .specify/scripts/python/validate-requirements.py .specify/specs/062-humanize-command/requirements.md
```

```
file: .specify/specs/062-humanize-command/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 265 lines, 40 definition rows, 4 shared strings
0 error(s), 0 warning(s)
```

**exit 0**。

## S7 — 传播次序端到端（注册 → 编译 → regen → sync）

### 步骤 2：编译（写）

```bash
python3 .specify/scripts/python/probe-utils.py --action compile-embeds
```

```
compiled 74 units: 0 written, 74 unchanged
```

**exit 0**（幂等：attempt 1 已写入，本次零变更）。

### 步骤 3：生成按工具副本

```bash
python3 scripts/python/regen-command-copies.py
```

```
Regenerated command copies for 4 tools.
```

**exit 0**。

### 步骤 4：特性限定镜像同步（仅 `--only`，未执行全局 sync）

```bash
python3 scripts/python/sync-mirrors.py --write --only skills/external/humanize --only shared/definitions/probe-definitions.md
```

```
scope --only: skills/external/humanize, shared/definitions/probe-definitions.md
ok    skills/external/ == .specify/skills/ (1 files)
ok    shared/ == .specify/shared/ (1 files)
```

**exit 0**。

### 步骤 5：复核

```bash
python3 scripts/python/regen-command-copies.py --check
# OK: all per-tool command copies match the source templates.        exit 0

python3 scripts/python/sync-mirrors.py --check | grep -E 'humanize|probe-definitions' || echo "touched pairs: zero DIFF"
# touched pairs: zero DIFF

python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
# compile-embeds --check: 74 units, zero drift                      exit 0
```

### 证据逐单元隔离

- **编译面**：当前 drift 单元集合为空；相对基线 73 单元 `comm -13` → **0** 个 NEW 归因；`skill:humanize` 不在 drift 名单。
- **镜像面**：只取两个触碰对——`humanize` 与 `probe-definitions` 均零 DIFF；新增对字节一致。
- **测试面**：只取 `comm -13`（S4）→ 0 条新增失败；不因既有欠账减少而放宽。

### 非计划改动复核：`.specify/scripts/python/probe-utils.py`

工作树中该文件的路径归一化（`.specify/scripts/` → `scripts/`）**是本特性编译管线所必需**，实测证明：

1. 逐文件暂存原工作树版本，单文件 `git checkout HEAD -- .specify/scripts/python/probe-utils.py`；
2. `probe-utils.py --action compile-embeds --check` → **exit 2**，`probe registry invalid`，逐条报 `object 'trigger-p1-feature-dir': unit 'scripts/python/trigger-utils.py' must be an engine script path (.specify/scripts/python/*.py ...)` 等（registry 已使用框架源面 `scripts/...`，运行时引擎为陈旧副本）；
3. 从备份逐文件恢复后 → **exit 0**，`compile-embeds --check: 74 units, zero drift`。

结论：保留该改动；它是**运行时镜像与框架源 `scripts/python/probe-utils.py` 的同步修复**（源侧在 HEAD 已是归一化语义，运行时副本陈旧），并已在 `verification.md` § Deviations 记录偏差与理由。修复后该镜像对不再出现在 S2 的 DIFF 名单。

## S8 — 改写行为评估（可复现性抽检）

完整 S8 行为评估已在 T008/T013/T016/T029 执行并落档于 `verification.md`（不因 attempt 中断而失效）。本次按 quickstart S8 的验证形态做确定性复跑抽检：

```bash
python3 tests/fixtures/humanize/diff_protected.py --selftest
# SELFTEST PASS（clean pair exit 0 / mutated pair exit 1）        exit 0

python3 tests/fixtures/humanize/diff_protected.py --input tests/fixtures/humanize/inline/s01-zh-report.md \
  --output .specify/specs/062-humanize-command/notes/e8-run/s01-rewritten.md
# RESULT: PASS (17 item lines)                                    exit 0

python3 tests/fixtures/humanize/diff_protected.py --input tests/fixtures/humanize/inline/s08-threat-inline.md \
  --output .specify/specs/062-humanize-command/notes/e8-run/s08-rewritten.md
# RESULT: PASS (16 item lines)                                    exit 0

python3 tests/fixtures/humanize/diff_protected.py --input tests/fixtures/humanize/inline/s10-long-multichapter.md \
  --output .specify/specs/062-humanize-command/notes/e8-run/s10-rewritten.md
# RESULT: PASS (148 item lines)                                   exit 0

python3 tests/fixtures/humanize/diff_protected.py --input tests/fixtures/humanize/tone/base-sample.md \
  --output .specify/specs/062-humanize-command/notes/e8-run/tone/T-audience.md \
  --annotations .specify/specs/062-humanize-command/notes/e8-run/tone/T-audience-annotations.json
# RESULT: PASS (16 item lines)                                    exit 0
```

抽检覆盖：内联（s01）、注入防线（s08）、长文档分段（s10）、受众适配 + 新增句蕴含标注（T-audience）。全部与 `verification.md` 已录结果一致。

## Teardown

- 管线无清理步骤；`sync-mirrors --write --only` 为幂等同步，无状态残留；`compile-embeds` 本次 `0 written`。
- 工作树条目数：管线前 **214** → 管线后 **214**（本 notes 文件为 T031 预期产物，另计）。
- `/tmp` 下的测试名单为运行记录，不进入提交；冻结基线 `notes/baseline-*.txt` 未被改写。

## Verdict

S1–S8 全部通过；零新增测试失败、零 NEW 镜像漂移、零编译漂移、35/35 条款与 29/29 FR 覆盖；非计划改动经必要性实测后保留并记录。**未发现异常。**
