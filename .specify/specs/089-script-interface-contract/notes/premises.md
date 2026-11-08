# Generation-time premises — Feature 089 脚本接口契约

**Owner of this file**: the implement stage's Phase 1 (T001). It records the premises this feature's
rows were generated against, so a later reader can tell "the premise moved" from "the row is wrong".

**Authority**: the count table this file re-probes lives in `tasks.md` § "Premises measured at generation
time"; this file does not restate that table's derivations — it records the **implement-entry re-probe**
against it, plus the runtime-evidence landing points the implement stage writes into.

**Measured at**: 2026-11-06, implement entry, tree `/cws_data/cloud-native-ai/spec-kit` on branch
`089-script-interface-contract`, HEAD `9add95eb` (parent of this package's commits).

---

## 1. Runtime-evidence landing points (created by T001)

| Landing point | Purpose | Owner rows |
|---|---|---|
| `.specify/specs/089-script-interface-contract/notes/` | red-first evidence, premises, pre-change measurements, clause census | T001, T002, red-first rows |
| `.specify/specs/089-script-interface-contract/test-evidence/` (existing) | command captures: baselines, sandbox probes, SC readings, closure | T003, T005, every `SC-*` row |
| `.specify/specs/089-script-interface-contract/coverage-baseline.txt` (existing) | frozen contract-clause coverage baseline | T004 |
| `.specify/.tmp/` (git-ignored scratch) | probe sandboxes; never `/tmp` (this host mounts `/tmp` `noexec`) | T005, every sandbox row |

`.specify/.tmp/` is the only sanctioned scratch root this feature uses on the repository side; it is
declared in `.specify/.gitignore:30` (`.tmp/`), measured with `git check-ignore -v .specify/.tmp` →
`.specify/.gitignore:30:.tmp/	.specify/.tmp`, exit 0.

`/var/tmp` is used only where a **real git work tree** is required and the scratch must sit outside the
repository (the `git clone` variants in `quickstart.md`); it is a sanctioned temp root under
`shared/guidelines/temp-directory-discipline.md`.

## 2. Implement-entry re-probe of the generation-time premises

Every row below was re-measured at implement entry, not copied from `tasks.md`. Where a reading agrees
with `tasks.md` the row says `agrees`; any disagreement is an anomaly, and none was found.

| Premise | Implement-entry reading | Versus `tasks.md` |
|---|---|---|
| Tracked `*.sh` / `*.py` candidates | `git ls-files '*.sh' '*.py' \| wc -l` → **737** (71 sh + 666 py) | agrees |
| Ignored among the tracked set | `git check-ignore` over the 737 → **0** | agrees |
| Work-tree walk `*.sh` / `*.py` | `find . -path ./.git -prune -o \( -name '*.sh' -o -name '*.py' \) -print \| wc -l` → **737** | agrees (EP-001 holds: a coverage finding would mean a genuinely new file) |
| Candidate split by root | `tests/` 449 · `.specify/` 146 · `skills/` 87 · `scripts/` 51 · `src/` 3 · `install.sh` 1 | agrees |
| `scripts/bash/*.sh` | `git ls-files 'scripts/bash/*.sh' \| wc -l` → **14** (13 after excluding `common.sh`, the library) | agrees |
| `scripts/python/*.py` | `git ls-files 'scripts/python/*.py' \| wc -l` → **37** (36 after excluding the checker) | agrees |
| `skills/` script candidates | 71 `.py` + 16 `.sh` = **87** | agrees (the 60+13 / 11+3 layer split is not re-cut here) |
| `tests/` `.py` carrying a `__main__` block | per-file `grep -qE 'if __name__[[:space:]]*==[[:space:]]*["'\'']__main__["'\'']'` → **6**: `tests/contract/test_migration_distribution.py`, `tests/fixtures/cli_observation.py`, `tests/fixtures/client_project.py`, `tests/fixtures/humanize/diff_protected.py`, `tests/fixtures/review_git_repo.py`, `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` | agrees with the 6 (5 fixtures + 1 contract module); the naive `grep -qF 'if __name__ == "__main__":'` form would read 5 |
| Instructions size | `wc -c .specify/instructions.md` → **33 357 B** | agrees |
| Instructions budget constant | `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` → line 53, `INSTRUCTIONS_BUDGET_BYTES=34816` | agrees; headroom **1 459 B** |
| `-h` merged with `--help` | `grep -lE '\-\-help\|-h\|-h\|--help' scripts/bash/*.sh` → **7**: `check-prerequisites`, `create-new-plan`, `create-new-requirements`, `create-new-skill`, `create-new-tools`, `implement-plan`, `research-project` | agrees |
| New artifacts absent today | `shared/definitions/script-interface-definitions.md`, `scripts/python/script-interface-check.py`, `scripts/python/script_interface_cli.py`, `scripts/bash/script-interface.sh`, `tests/contract/test_script_interface_contract.py` — all five absent at implement entry | agrees |

## 3. Environment prerequisites (re-probed at implement entry, per `tasks.md` § Environment Prerequisites)

`tasks.md` forbids caching those verdicts across runs, so they were re-probed rather than read:

| Verdict | Implement-entry re-probe |
|---|---|
| `pytest` on `/usr/bin/python3` | `/usr/bin/python3 -m pytest --version` → **pytest 9.0.3**; interpreter **Python 3.11.0rc1** |
| `git` and `git worktree` | `git --version` → **2.34.1**; `git worktree list` → **one entry** (the plan-stage probe is gone) |
| System temp root execution | `mount \| grep -E ' /tmp '` → **`noexec`** — sandboxes MUST live under `.specify/.tmp/` or `/var/tmp` |
| `contract`-marked collection | proved by T003's full-suite run (see `test-evidence/baseline-full-suite-2026-11-06.txt`) |

## 4. What this file does not own

- The per-quantity re-derivation commands and the naive forms that disagree: `tasks.md` § "Premises
  measured at generation time" owns them, and this file cites that table rather than restating it.
- The pre-change readings this stage takes for the feature's own budgets: `notes/pre-change-measurements.md`
  (T002) owns those.
