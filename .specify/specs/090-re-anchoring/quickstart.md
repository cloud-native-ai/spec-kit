# Quickstart — Feature 090 Re-Anchoring（不忘初心 · 温故而知新）

Seven scenarios. Each states its **premises** (what must already be true), the **commands**, and the **expected
observation**. Scenarios marked *executable now* were run during the plan stage against
`/cws_data/cloud-native-ai/spec-kit`; scenarios marked *after tasks* name the artifact that will hold the capture.

Vocabulary, at first use:

- **方向锚 (direction anchor)** — the entry-time record every agent keeps: a **task anchor** (goal, non-goals,
  acceptance authority, stage plan, decision gates) plus a **rule anchor** (the operating rules in force).
- **core step** — one of four events that triggers an audit: stage U4, package boundary, checkpoint, subagent return.
- **reload tier** — `T0` (anchor digest, ≈1 KB, every core step) / `T1` (rule digest, ≈5 KB, stage boundaries and after
  a compaction) / `T2` (full manual, only when a dispatch form is unclear or a stall is handled).
- **verdict** — exactly one of `on-track` / `correction-applied` / `decision-needed`; only the last is surfaced.

All commands assume the repository root. `SPECKIT_PYTHON=/usr/bin/python3` is pinned because the `PATH` `python3`
resolves to a virtualenv **without** pytest (measured 2026-11-09: `No module named pytest`).

---

## S-0 — Baseline (executable now)

**Premises**: a clean-enough tree; the pre-existing contract-suite red set is present (it predates this feature).

```bash
cd /cws_data/cloud-native-ai/spec-kit
SPECKIT_PYTHON=/usr/bin/python3
$SPECKIT_PYTHON --version
$SPECKIT_PYTHON -m pytest --version
$SPECKIT_PYTHON -m pytest tests/contract/test_reanchoring_contract.py \
  tests/contract/test_sdd_loop_driver_reanchor.py \
  tests/contract/test_constitution_double_landing.py -q
```

**Expected**: `Python 3.11.0rc1`; `pytest 9.0.3`; the three modules pass. The measured reading on 2026-11-09 was
`27 passed` for those three modules (`2 failed, 129 passed` when `test_fast_fail_discipline.py` is added — its two
failures are the pre-existing entries in `research.md` R6).

**Capture**: `test-evidence/plan-contract-baseline-raw.txt` (full-suite run,
`49 failed, 6368 passed, 2 skipped in 486.38s`) and `test-evidence/plan-guards.txt` (the four-module run,
`2 failed, 129 passed in 1.88s`, whose two failures are the pre-existing entries in `research.md` R6).

---

## S-1 — The five faces exist and point at one owner (executable now)

**Premises**: the pre-landed tree is present (EP-002).

```bash
SPECKIT_PYTHON=/usr/bin/python3
$SPECKIT_PYTHON - <<'PY'
import pathlib
owner = pathlib.Path('shared/definitions/re-anchoring-definitions.md').read_text(encoding='utf-8')
toks = ("不忘初心","温故而知新","规则锚","T0","T1","T2","on-track","correction-applied","decision-needed")
print("owner_missing:", [t for t in toks if t not in owner])
for rel in (".specify/memory/constitution.md","templates/constitution-template.md"):
    print(rel, "Re-Anchoring (不忘初心 · 温故而知新)" in pathlib.Path(rel).read_text(encoding='utf-8'))
for rel in ("templates/instructions-template.md",".specify/instructions.md"):
    t = pathlib.Path(rel).read_text(encoding='utf-8')
    print(rel, "## Re-Anchoring (不忘初心 · 温故而知新)" in t, "re-anchoring-definitions.md" in t)
PY
```

**Expected** (measured 2026-11-09): `owner_missing: []`; all four surfaces print `True True`.
The same reading is available as `test-evidence/`-style evidence through
`tests/contract/test_reanchoring_contract.py` (4 assertions, part of the 27-pass module set in S-0).

---

## S-2 — The mirrors are byte-identical (executable now)

**Premises**: none beyond S-1. This is the mirror half of the feature's guarantee.

```bash
cd /cws_data/cloud-native-ai/spec-kit
for pair in \
  "shared/definitions/re-anchoring-definitions.md .specify/shared/definitions/re-anchoring-definitions.md" \
  "shared/definitions/agent-definitions.md .specify/shared/definitions/agent-definitions.md" \
  "templates/constitution-template.md .specify/templates/constitution-template.md" \
  "templates/instructions-template.md .specify/templates/instructions-template.md" \
  "skills/internal/manage-constitution/SKILL.md .specify/skills/internal/manage-constitution/SKILL.md" \
  "skills/external/sdd-loop-driver/references/checkpoint-protocol.md .specify/skills/sdd-loop-driver/references/checkpoint-protocol.md"; do
  set -- $pair; diff -q "$1" "$2" >/dev/null && echo "IDENTICAL $1" || echo "DRIFT $1"
done
```

**Expected** (measured 2026-11-09): six `IDENTICAL` lines, zero `DRIFT`.

---

## S-3 — The checkpoint protocol carries the rule-first audit (executable now)

**Premises**: the driver skill is present.

```bash
cd /cws_data/cloud-native-ai/spec-kit
grep -c '^### 5\. Direction audit$' skills/external/sdd-loop-driver/references/checkpoint-protocol.md
grep -c 'primary object is the RULES' skills/external/sdd-loop-driver/references/checkpoint-protocol.md
grep -c '^\- Q1 rules:' skills/external/sdd-loop-driver/references/checkpoint-protocol.md
```

**Expected** (measured 2026-11-09): `1`, `1`, `1`. Each pattern matches only the protocol's own prose and its minimal
shape; none can match the unrelated `Q1`/`Q2` quarter labels in the humanize fixtures.

---

## S-4 — A goal-first rewrite does NOT red today (executable now — this is the gap)

**Premises**: a scratch copy of the protocol (never edit the tracked file for this scenario).

```bash
cd /cws_data/cloud-native-ai/spec-kit
cp skills/external/sdd-loop-driver/references/checkpoint-protocol.md /var/tmp/proto-scratch.md
python3 - <<'PY'
import pathlib, re
p = pathlib.Path('/var/tmp/proto-scratch.md')
t = p.read_text(encoding='utf-8')
t = t.replace('1. Which rules govern this step', '1. Which goal governs this step', 1)
p.write_text(t, encoding='utf-8')
print('rewrote:', 'Which goal governs this step' in t)
PY
rm -f /var/tmp/proto-scratch.md
```

**Expected**: the scratch copy can be made goal-first with no test noticing — **that is the finding**, recorded as
`contracts/guard-tests.contract.md` C-7. The scenario's purpose is to keep the gap visible and to be re-run as the
**red control** once the ordering assertion lands (`S-6`).

---

## S-5 — The governance counting pins are consistent with the artifacts (executable now)

**Premises**: nothing; the pins and the artifacts are both in the tree.

```bash
cd /cws_data/cloud-native-ai/spec-kit
SPECKIT_PYTHON=/usr/bin/python3
grep -E '^(TEMPLATE_COUNT|LIVE_COUNT|COMMAND_COUNT) = ' tests/contract/test_constitution_double_landing.py
grep -cE '^### [IVXLC]+\. ' templates/constitution-template.md
grep -cE '^### [IVXLC]+\. ' .specify/memory/constitution.md
$SPECKIT_PYTHON -m pytest tests/contract/test_constitution_double_landing.py -q
```

**Expected** (measured 2026-11-09): the three pins print `21`, `22`, `14`; the two roster counts print `21` and `22`;
the module passes. `test_fast_fail_discipline.py::test_x13` derives the same three values independently, so an
agreement between the printed literals and the printed roster counts is the proposition, not the literal itself.

---

## S-6 — The ordering guard reds on a goal-first protocol (after tasks)

**Premises**: the task that lands `contracts/guard-tests.contract.md` C-7 has been implemented; a scratch copy of the
repository is available (`/var/tmp` is used because `/tmp` is `noexec` on this host).

```bash
cd /var/tmp && rm -rf qs090 && cp -a /cws_data/cloud-native-ai/spec-kit qs090 && cd qs090
python3 - <<'PY'
import pathlib
p = pathlib.Path('skills/external/sdd-loop-driver/references/checkpoint-protocol.md')
t = p.read_text(encoding='utf-8')
p.write_text(t.replace('1. Which rules govern this step', '1. Which goal governs this step', 1), encoding='utf-8')
PY
/usr/bin/python3 -m pytest tests/contract/test_sdd_loop_driver_reanchor.py -q
echo "exit=$?"
cd /var/tmp && rm -rf qs090
```

**Expected after the task lands**: the mutated copy fails and the unmutated copy passes; that pair is the red control
the clause requires. **Before** the task lands this scenario is not executable — it is stated so that the task's
acceptance is a measured pair rather than a claim.
