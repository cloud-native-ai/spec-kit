# Quickstart — 081 Stricter Acceptance & Artifact Review

Every scenario below is a **command a person can paste** plus the **status of that command in this stage**. The status discipline is owned by `/speckit.plan`'s Post-Generation Quality Gate: a command is either (a) executed in this phase with real output, or (b) pinned by a named contract test — and route (b) carries a **per-example** disclaimer that lists the premises the example rests on. There is no file-level disclaimer here: each block states its own status.

All commands run from the repository root `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`.

---

## S1 — Establish the test runner (executed)

```bash
.venv/bin/python -m pytest --version
.venv/bin/python -m pytest --collect-only -q | tail -1
git --version
```

**Executed 2026-11-03.** Measured output:

```
pytest 9.2.0
7016 tests collected in 1.03s
git version 2.54.0 (Apple Git-157)
```

These three lines are the RS-002 / RS-003 pins; `test-evidence/plan-runner-pins.txt` holds the full capture (interpreter 3.14.6, the six distributions installed to repair `.venv`, and the pip index used).

---

## S2 — Run the plan-stage deterministic gates (executed)

```bash
python3 scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md
python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/081-acceptance-hardening
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/081-acceptance-hardening --stage plan --repo .
```

**Executed 2026-11-03**; full transcript in `test-evidence/plan-gates.txt`. Expected results as measured: `status: ok` (five checks, 0 error / 0 warning); `status: ok` (six labels, 5 records); `decision=pass errors=0 advisories=58`. The 58 advisories are all `missing-path` findings naming the deliverables this plan is about to create — they are advisories by design and do not block (`--strict` would promote them).

---

## S3 — Mirror and per-tool-copy regeneration (executed, baseline)

```bash
python3 scripts/python/regen-command-copies.py --check
python3 scripts/python/sync-mirrors.py --check
```

**Executed 2026-11-03**: both exit `0` (six mirror pairs ok: templates 22 / skills-external 408 / skills-internal 136 / agents 3 / scripts 118 / shared 61). This is the *baseline* — it is why the close criterion for this feature can be stated as an absolute `exit 0` instead of "no new drift".

---

## S4 — Current line-registry behaviour before the change (executed; shows the gap)

```bash
export SPECIFY_LINE_REGISTRY_DIR=$PWD/.specify/.tmp/081/reg
python3 skills/external/sdd-loop-driver/scripts/line-registry.py \
  --action register --line-id 081-probe-line --run-id r20261103T000000Z-abcd \
  --driver-session probe --cli qodercli --project-dir "$PWD" --repo-root "$PWD"
python3 skills/external/sdd-loop-driver/scripts/line-registry.py \
  --action update --line-id 081-probe-line --state blocked
rm -rf "$SPECIFY_LINE_REGISTRY_DIR"
```

**Executed 2026-11-03.** The register call succeeds (`"state": "active"`); the update call fails with the seven-value domain, which is exactly the gap this feature closes:

```json
{"error": {"code": 2, "message": "invalid state: 'blocked' (expected one of ['active', 'closed', 'completed', 'orphaned', 'stale', 'stalled', 'waiting'])"}, "ok": false}
```

**After the change** the same call MUST succeed and MUST leave `merge_ready=false` with no lease and no `holder_line_id` (V-25 / I-2). That post-change expectation is **not** claimable yet — it is pinned by `tests/contract/test_line_state_blocked.py` (route (b) below).

---

## S5 — `specify init` precondition (executed; currently fails, and that is the point)

```bash
.venv/bin/specify init /tmp/demo-081 --ai claude --script sh --no-git --ignore-agent-tools
```

**Executed 2026-11-03**, output:

```
error Check for local templates: not found
Error: Local templates not found. GitHub download is no longer supported.
```

This is premise **EP-002 `falsified`** in `plan.md`, with `Decision: resolve-in-scope`: the fix is the repo-root fallback in `src/specify_cli/__init__.py` § `get_resource_path()` (T-005). **Post-change expectation** — exit `0`, and `<target>/.specify/` generated from the working tree:

> **Premises this example rests on (re-measure before using it)**: (1) the interpreter's sibling `specify` console script exists (`<dirname sys.executable>/specify`); (2) `get_resource_path()` has the repo-root fallback of T-005; (3) the target directory is writable and outside the repo; (4) `--ignore-agent-tools --no-git` are accepted flags (both verified in `specify init --help`). Route (b): pinned by `tests/integration/test_acceptance_smoke.py` (sub-check A), which asserts exit 0 and the presence of the generated `.specify/` tree — the example is not claimable as passing until that test exists.

---

## S6 — The closure check on the two fixtures (not yet executable; route (b))

```bash
python3 scripts/python/closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/positive --json
python3 scripts/python/closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/negative --json
```

**NOT executed — the script and fixtures do not exist yet.** Declared expected results (route (b), not a claim): the first exits `0` with `"verdict": "accept"`; the second exits `1` with `"verdict": "block"` and a reason set ⊆ the seven closed codes, containing `zero-final-path-pass`.

> **Premises**: (1) the fixture directories are declarative minimal file sets — `requirements.md`, `plan.md`, `tasks.md`, `verification.md`, a feature detail and a registry row (no real feature is referenced); (2) `--spec-dir` accepts a fixture path that is not under `.specify/specs/`; (3) the checker resolves the claimed status from the fixture's own detail/registry when `--feature-detail` is passed; (4) exit codes are `0/1/2` exactly as `contracts/closure-acceptance-check.contract.md` C-10 states. Route (b): pinned by `tests/contract/test_closure_acceptance_check.py` (positive + negative + ladder + premise + runtime-gap mutation cases).

---

## S7 — Read-only audit mode (not yet executable; route (b))

```bash
python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/080-humanize-run-output --audit-existing
git status --porcelain | wc -l
```

**NOT executed — the script does not exist yet.** Declared expectation: the audit lists the features that would become `Blocked` under the new rules, writes nothing, and exits `0`; the `git status --porcelain` line count is identical before and after.

> **Premises**: (1) `080-humanize-run-output` carries an `Implemented`-family claimed status for its bound Feature 062 (verify with `.specify/memory/features.md` before citing); (2) audit mode never writes, including no cache or lock file; (3) the audit's exit code reflects input validity only (C-10). Route (b): pinned by `tests/contract/test_closure_acceptance_check.py::test_audit_writes_nothing` (zero-write assertion against `git status --porcelain`) plus `tests/fixtures/acceptance-hardening/audit-history/`.

---

## S8 — The feature's own single smoke (not yet executable; route (b))

```bash
bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
```

**NOT executed — the test does not exist yet.** This is **the** smoke command this feature records in `verification.md` (`smoke_command`), and by FR-005 it must cover exactly three sub-checks: (A) `specify init` on a temp fixture, (B) the closure checker on the positive and negative fixtures, (C) `python3 scripts/python/regen-command-copies.py --check`. It must be runnable twice with the same exit code.

> **Premises**: (1) `scripts/bash/run-tests.sh` resolves `.venv/bin/python` (verified in S1 through `--collect-only`); (2) the test uses `tmp_path` for every fixture it creates, so nothing is written outside the pytest temp root except the deterministic evidence file `<spec-dir>/test-evidence/smoke-081.txt`; (3) no network is used; (4) the `specify` console script exists (S5 premise 1). Route (b): the smoke test pins itself — its three sub-checks are its own assertions, and the test's own existence is checked by the plan's `verification.md`-side record.

---

## S9 — Review three-call-site refusal (not yet executable; route (b))

```bash
# implement site
bash scripts/bash/run-tests.sh tests/contract/test_gate_wiring_081.py -q
# review site + ARC
bash scripts/bash/run-tests.sh tests/contract/test_acceptance_review_composition.py -q
# driver closure/merge site
bash scripts/bash/run-tests.sh tests/contract/test_line_state_blocked.py -q
```

**NOT executed — the tests do not exist yet.** Declared expectation: on the negative fixture, all three sites refuse (3/3) each with a named reason from the closed set, and the driver site leaves the line `blocked` rather than `completed`.

> **Premises**: (1) `integrate-lines.py` exposes the quality gate through its existing `--gate-cmd` hook (verified by reading the script's source, `research.md` § R6); (2) the three test modules will be created by this feature; (3) the composed review run's fourth unit exists (`skill:review-feature-quality`), which is what makes the review site's own refusal observable. Route (b): the three modules named in the commands.
