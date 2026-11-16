# Quickstart — turning a batch script into a registered long task

**Goal**: make a long-running script visible to `/speckit.status` by wrapping it with `[[STR-001]]`, prove the scanner has teeth, and prove the digest reading. Every example below states whether it is runnable in this planning run; the executable ones were run on 2026-11-16 and their output is pasted.

**Prerequisite for S-1…S-6**: the implementation has landed `scripts/bash/line-run.sh` and `scripts/python/line-registration-scan.py` (and the text edits). Before that, those examples are **not runnable** and are pinned by the named tests instead.

**Isolation**: every scenario keeps its registry under the sanctioned, git-ignored root `.specify/.tmp/line-registry-registration/` (`.specify/.gitignore` matches `.tmp/`). No scenario touches the operator's environment registry, and no scenario uses bare `/tmp`.

```bash
REG=.specify/.tmp/line-registry-registration/registry
mkdir -p "$REG"
```

---

## S-1 — Wrap the script (the normal path)

1. Change the invocation from `bash batch.sh` to:

   ```bash
   SPECIFY_LINE_REGISTRY_DIR="$REG" \
   scripts/bash/line-run.sh --line-id batch-apply --run-id r20261116T090000Z-a001 -- bash batch.sh
   ```

2. While it runs, from the same repository:

   ```bash
   SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
   ```

3. After it ends, read the entry:

   ```bash
   python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['state'])" "$REG/batch-apply-r20261116T090000Z-a001.json"
   ```

**Expected**: the digest lists the line while the script runs; the entry reads `closed` afterwards; the wrapper exits with the script's status.

**Status**: not runnable in this planning run (wrapper absent). Premises: the wrapper implements C-01…C-19 of `contracts/line-run.contract.md`; cwd is a git repository; the engine is at declared candidate 1 of A-17. Pinned by `tests/integration/test_line_run_behavior.py`; the digest commands themselves were executed in S-7.

**Teardown**: `rm -rf .specify/.tmp/line-registry-registration`.

---

## S-2 — Failure path

```bash
SPECIFY_LINE_REGISTRY_DIR="$REG" \
scripts/bash/line-run.sh --line-id demo-fail --run-id r20261116T090000Z-a002 -- bash -c 'exit 7'
```

**Expected**: exit `7`; entry `demo-fail-r20261116T090000Z-a002` is `closed` with `last_event=failed`.

**Status**: not runnable in this planning run. Premises: as S-1. Pinned by `tests/integration/test_line_run_behavior.py`.

---

## S-3 — The wrapper is killed (residue stays visible)

1. Start a long child:

   ```bash
   SPECIFY_LINE_REGISTRY_DIR="$REG" \
   scripts/bash/line-run.sh --line-id demo-kill --run-id r20261116T090000Z-a003 -- sleep 60 &
   ```

2. Kill the wrapper (not the child):

   ```bash
   kill -9 %1
   ```

3. Read the entry and the digest:

   ```bash
   python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['state'])" "$REG/demo-kill-r20261116T090000Z-a003.json"
   SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
   ```

**Expected**: entry state `active` (not deleted, not `closed`); the digest lists it and shows its age. Once it ages past the digest's own stale bound it is marked stale by the digest — this feature adds no cleanup.

**Status**: not runnable in this planning run (wrapper absent). Premises: as S-1; `kill -9` targets the wrapper process; the child may need `kill` too. Pinned by `tests/integration/test_line_run_behavior.py`.

**Teardown**: kill the leftover `sleep`, then `rm -rf .specify/.tmp/line-registry-registration`.

---

## S-4 — Prove the scanner has teeth

1. Create a violating fixture (its content carries a `LONG_TASK_MARKERS` member and no compliant invocation — the member is read from the constant, never typed here):

   ```bash
   python3 - <<'PY'
   import importlib.util, pathlib
   spec = importlib.util.spec_from_file_location("scan", "scripts/python/line-registration-scan.py")
   m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
   root = pathlib.Path(".specify/.tmp/line-registry-registration"); root.mkdir(parents=True, exist_ok=True)
   (root / "fixture.sh").write_text("#!/usr/bin/env bash\n" + m.LONG_TASK_MARKERS[0] + " -auto-approve\n", encoding="utf-8")
   PY
   python3 scripts/python/line-registration-scan.py --root .specify/.tmp/line-registry-registration
   ```

   **Expected**: exit `1`; one violation line naming the fixture and `criterion=content-marker`.

2. Rewrite the **same** fixture so it keeps the marker **and** goes through the wrapper, then rescan — this exercises compliant-invocation detection, not merely the absence of a marker:

   ```bash
   python3 - <<'PY'
   import importlib.util, pathlib
   spec = importlib.util.spec_from_file_location("scan", "scripts/python/line-registration-scan.py")
   m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
   root = pathlib.Path(".specify/.tmp/line-registry-registration")
   text = ("#!/usr/bin/env bash\n"
           "scripts/bash/line-run.sh --line-id f --run-id r20261116T090000Z-a0ff -- "
           + m.LONG_TASK_MARKERS[0] + "\n")
   (root / "fixture.sh").write_text(text, encoding="utf-8")
   PY
   python3 scripts/python/line-registration-scan.py --root .specify/.tmp/line-registry-registration
   ```

   **Expected**: exit `0`; `violations: 0` — the file still contains the marker, so only the compliant invocation can explain the clean verdict.

**Status**: not runnable in this planning run (scanner absent). Premises: the scanner implements `contracts/line-registration-scan.contract.md`; the marker literal is read from the module constant; the fixture root is git-ignored. Pinned by `tests/contract/test_line_registration_scan.py` (both legs).

**Teardown**: `rm -rf .specify/.tmp/line-registry-registration`.

---

## S-5 — The live repository reads clean

```bash
python3 scripts/python/line-registration-scan.py
```

**Expected**: exit `0`; the reading names `scripts/bash/`, `scripts/python/`, `skills/`, reports `violations: 0` and `owner-skipped: 1`. The implementation run saves this reading under `test-evidence/`.

**Status**: not runnable in this planning run (scanner absent). Premises: the declared roots exist; the `.md` files under `skills/external/*/references/` are excluded by the file-surface rule (C-07). The planning-time measurement over the same roots is recorded in `research.md` § Baseline measurements.

---

## S-6 — Check the wiring surfaces

```bash
grep -n "Single source" templates/commands/status.md
grep -n "line-run.sh" templates/instructions-template.md .specify/instructions.md
grep -n "line-registry.py" skills/internal/run-team/SKILL.md
```

**Expected**: one hit each for the first two patterns in their files; three hits (register / update / close) for the engine path in run-team, plus the `line_id` mention in §7.

**Status**: not runnable in this planning run (the texts are not edited yet; the pre-edit baseline is `0` hits for all four counts, measured in `contracts/wiring-surfaces.contract.md` E-2). Pinned by `tests/contract/test_line_registration_wiring.py`.

---

## S-7 — Registry/digest lifecycle (executable now)

This scenario uses only the existing engine and digest; it is the behavioural backbone the wrapper rides on.

```bash
REG=.specify/.tmp/line-registry-registration/registry
mkdir -p "$REG"
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action register \
  --line-id probe-line-20261116 --run-id r20261116T090000Z-abcd \
  --project-dir "$PWD" --repo-root "$PWD" --state active
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action deregister \
  --line-id probe-line-20261116 --reason completed
SPECIFY_LINE_REGISTRY_DIR="$REG" python3 scripts/python/status-digest.py --action digest --workspace "$PWD"
rm -rf .specify/.tmp/line-registry-registration
```

**Measured on 2026-11-16 with the commands above**:

| Step | Output (excerpt) | Exit |
|------|------------------|------|
| empty registry digest | `nothing-running` | `3` |
| register | JSON entry with `"state": "active"`, `"last_event": "registered"` | `0` |
| digest while active | table row naming `probe-line-20261116`, state `活跃` (active) | `0` |
| deregister | JSON entry with `"state": "closed"`, `"last_event": "completed"`, `run_history` entry `outcome=completed` | `0` |
| digest after close | `nothing-running` | `3` |

**Teardown**: the last line above removes the whole scratch root — executed in the same round; the directory is gone.

**What this proves for the feature**: the digest lists an `active` line, hides a `closed` one, and renders `[[STR-006]]` for an empty set; those are the readings the wrapper's scenarios assert.

---

## Example status matrix

| Scenario | Runnable in this planning run | Evidence route |
|----------|-------------------------------|----------------|
| S-1, S-2, S-3 | no (wrapper absent) | pinned by `tests/integration/test_line_run_behavior.py` |
| S-4 | no (scanner absent) | pinned by `tests/contract/test_line_registration_scan.py` |
| S-5 | no (scanner absent) | pinned by `tests/integration/test_line_registration_scan_live.py`; its reading is recorded in `test-evidence/` at implementation time |
| S-6 | no (texts not edited) | pinned by `tests/contract/test_line_registration_wiring.py` |
| S-7 | **yes — executed** | output pasted above; safe to repeat (`$REG` is scratch and torn down) |

## Running the tests that guard this document

```bash
bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py tests/contract/test_line_registration_scan.py tests/contract/test_line_registration_wiring.py -q
bash scripts/bash/run-tests.sh tests/integration/test_line_run_behavior.py tests/integration/test_line_registration_scan_live.py -q
```

**Status**: not runnable in this planning run (the test files do not exist yet). Premises: the unique runner entry is `scripts/bash/run-tests.sh`; paths are forwarded to pytest; each test isolates its registry. Pinned by the test files themselves at implementation time.
