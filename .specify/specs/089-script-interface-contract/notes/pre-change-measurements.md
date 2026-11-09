# Pre-change measurements — Feature 089 脚本接口契约

**Owner of this file**: the implement stage's Phase 1 (T002). It freezes the readings the feature's own
budgets are judged against, **taken before any implementation row of this feature wrote a byte**.

Every row carries the exact command and the reading, both taken at the timestamp below. A later row that
claims "the section fits" or "the budget moved" is compared against THIS table, never against a number
recalled from `plan.md` or `tasks.md`.

**Measured at**: 2026-11-06, implement entry, tree `/cws_data/cloud-native-ai/spec-kit`, branch
`089-script-interface-contract`, HEAD `9add95eb` (working tree clean for every path named below).

---

## 1. Instructions size against its budget (Risk 7, T062's subject)

| Quantity | Command | Reading |
|---|---|---|
| Live instructions size | `wc -c .specify/instructions.md` | **33 357 B** |
| Budget constant | `grep -n 'INSTRUCTIONS_BUDGET_BYTES' scripts/bash/generate-instructions.sh` | line **53**: `INSTRUCTIONS_BUDGET_BYTES=34816` |
| Headroom | `34816 − 33357` | **1 459 B** |
| Template instructions size (the section is authored here first) | `wc -c templates/instructions-template.md` | **28 930 B** |
| Top-level `##` sections, template | `grep -c '^## ' templates/instructions-template.md` | **32** |
| Top-level `##` sections, live | `grep -c '^## ' .specify/instructions.md` | **33** |

The last two rows are the `test_a7` pins T026 moves (32 → 33, 33 → 34). They are measured here so T026's
edit is a comparison against a reading, not against a memory.

## 2. The `-h`-merged script list (Risk 6, T059's merge condition)

Command: `grep -lE '\-\-help\|-h|-h\|--help' scripts/bash/*.sh` — **7** files:

```
scripts/bash/check-prerequisites.sh
scripts/bash/create-new-plan.sh
scripts/bash/create-new-requirements.sh
scripts/bash/create-new-skill.sh
scripts/bash/create-new-tools.sh
scripts/bash/implement-plan.sh
scripts/bash/research-project.sh
```

These seven MUST get their guard merged into the existing `--help|-h` arm; a second `-h` branch is the
defect this reading prevents. `scripts/bash/common.sh` is **not** in the list: it carries no option
surface at all, which is why it is exempt by measurement rather than by name.

## 3. Candidate counts (the coverage assertion's pre-change state — C-1 / C-2)

| Quantity | Command | Reading |
|---|---|---|
| Tracked `*.sh` + `*.py` | `git ls-files '*.sh' '*.py' \| wc -l` | **737** (71 `.sh`, 666 `.py`) |
| Ignored among the tracked set | `git ls-files '*.sh' '*.py' \| while read -r f; do git check-ignore -q "$f" \&\& echo "$f"; done \| wc -l` | **0** |
| Work-tree walk | `find . -path ./.git -prune -o \( -name '*.sh' -o -name '*.py' \) -print \| wc -l` | **737** |
| Untracked-and-unignored (C-2's finding set today) | walk minus candidates | **0** |

The two sources coincide today. That coincidence is exactly why C-2's coverage assertion exists: a
screen whose source breaks would still be 737 candidates here and would go unnoticed.

## 4. The per-surface candidate counts the backfill rows consume

| Surface | Command | Reading | Backfill row |
|---|---|---|---|
| `scripts/bash/*.sh` | `git ls-files 'scripts/bash/*.sh' \| wc -l` | **14** (13 applicable candidates; `common.sh` exempt by measurement) | T059 |
| `scripts/python/*.py` | `git ls-files 'scripts/python/*.py' \| wc -l` | **37** (36 excluding the checker itself) | T060 |
| `skills/**` script candidates | `git ls-files 'skills/*' \| grep -cE '\.py$'` / `'\.sh$'` | **71** `.py` + **16** `.sh` = 87 | T061 |
| `skills/external/<name>/` script candidates | `git ls-files 'skills/external/*' \| grep -cE '\.(sh\|py)$'` | **73** | T061 / T069 |
| `tests/` `.py` carrying `__main__` | per-file `grep -qE 'if __name__[[:space:]]*==[[:space:]]*["'\'']__main__["'\'']'` | **6** (listed below) | T083 |

The six `tests/` modules: `tests/contract/test_migration_distribution.py`,
`tests/fixtures/cli_observation.py`, `tests/fixtures/client_project.py`,
`tests/fixtures/humanize/diff_protected.py`, `tests/fixtures/review_git_repo.py`,
`tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`.

## 5. The `classification:` roster (FR-027's only machine marker)

| Command | Reading |
|---|---|
| `grep -rh -m1 '^classification:' skills/external/*/SKILL.md \| sort \| uniq -c` | **16** × `classification: external` |
| `grep -rh -m1 '^classification:' skills/internal/*/SKILL.md \| sort \| uniq -c` | **38** × `classification: internal` |

Two of the 16 external skills (`coaching-skills`, `create-skills`) hold no `*.sh` / `*.py` (measured
2026-11-06, feature-ref F-5), so the 73 external script candidates all live under skills that this feature
will classify as third-party. `skills/external/*` script candidates carry `classification: external`, so
they are third-party by FR-027's two-condition test; the register stays empty unless a real exception is
found (T069 / SC-012 read the recomputation, never a claim).

## 6. Version source (C-8)

| Command | Reading |
|---|---|
| `grep -n '^version' pyproject.toml` | line 3: `version = "0.0.22"` |
| `grep -n '\^requires-python' pyproject.toml` | `requires-python = ">=3.8"` |
| Interpreter used by every test command here | `/usr/bin/python3 -m pytest --version` → pytest **9.0.3** on Python **3.11.0rc1** |

The literal `0.0.22` is recorded here as a **reading of the version file**, never as a value any script may
carry: C-8's repository-wide scan for a version-shaped literal inside a script body MUST return zero hits,
and `0.0.22` is the string that scan is calibrated against.

## 7. What this file does not own

- Clause coverage: T004's re-freeze comparison against `coverage-baseline.txt` owns that reading.
- Full-suite node ids: `test-evidence/baseline-failed.txt` (T003) owns that set.
- Sandbox cost: `test-evidence/T005-sandbox-probe.txt` (T005) owns that timing.

The raw capture of every command in this file is `test-evidence/T002-pre-change-measurements.txt`.
