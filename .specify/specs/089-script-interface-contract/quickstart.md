# Quickstart — Feature 089 脚本接口契约 (Script Interface Contract)

Nine scenarios, one per implementation slice. Each states its **premises** (what must already be true), the
**command**, and the **expected observation**. Scenarios marked *executable now* were run during the plan stage
against `/cws_data/cloud-native-ai/spec-kit` or a scratch copy; the rest name the slice at which they become
executable and the artifact that will hold the capture.

Vocabulary, at first use:

- **candidate** — a file this feature is allowed to judge: a `*.sh` or `*.py` path that `git ls-files` reports and
  `.gitignore` does not exclude (C-1).
- **applicable** — a candidate whose file, executed, *is the program* (it has an entry-point behaviour). Only an
  applicable file must answer `--help` / `--version` (C-3).
- **exempt** — a candidate that is a library, an imported-only module, or a declared exception; a projected
  mirror inherits its source's class and is judged on that source (C-6).
  An exempt file is not a free pass: it must carry a `basis` and an `evidence` string (C-18).
- **declared exception** — a row on the owner page's `## Declared Exceptions` chapter naming one skill directory and
  the clause it cannot satisfy (E-5).

All commands assume the repository root. `SPECKIT_PYTHON=/usr/bin/python3` is pinned because the `PATH` `python3`
has no `pytest` (Risk 10).

---

## S-0 — Baseline (executable now)

**Premises**: git work tree at the feature branch; nothing written outside `.specify/specs/089-script-interface-contract/`
and a scratch copy.

```bash
cd /cws_data/cloud-native-ai/spec-kit
SPECKIT_PYTHON=/usr/bin/python3
git ls-files '*.sh' '*.py' | wc -l
git ls-files '*.sh' '*.py' | while read -r f; do git check-ignore -q "$f" || echo "$f"; done | wc -l
/usr/bin/python3 -c 'import pytest; print(pytest.__version__)'
sha256sum scripts/bash/generate-instructions.sh
git status --porcelain -- .specify/instructions.md
```

**Expected**: both counts equal (737 at plan time; the screen's coverage assertion is that these two numbers agree,
not that they equal a constant — C-2). `pytest.__version__` prints `9.0.3`. The last line prints nothing.

**Capture**: `test-evidence/plan-baseline.txt`.

---

## S-1 — The owner page exists and the checker can read it (after S1)

**Premises**: `shared/definitions/script-interface-definitions.md` landed, its `.specify/shared/` mirror is clean,
and `shared/definitions/framework-map.md` registers it.

```bash
SPECKIT_PYTHON=/usr/bin/python3
/usr/bin/python3 scripts/python/sync-mirrors.py --check; echo "exit=$?"
grep -c '^## Declared Exceptions$' shared/definitions/script-interface-definitions.md
```

**Expected**: `exit=0`; the chapter heading appears exactly once. A reader of the page learns the five owned items
from its first screen, without following a pointer (C-23).

**Capture**: stdout of both, into `test-evidence/S-1-owner-page.txt`.

---

## S-2 — The checker runs, and its degraded paths are loud (after S2)

**Premises**: `scripts/python/script-interface-check.py` exists and its mirror is projected (C-33).

```bash
SPECKIT_PYTHON=/usr/bin/python3
mkdir -p .specify/.tmp
/usr/bin/python3 scripts/python/script-interface-check.py --json > .specify/.tmp/sic.json; echo "exit=$?"
/usr/bin/python3 scripts/python/script-interface-check.py --emit-rule > .specify/.tmp/sic-rule.json
/usr/bin/python3 scripts/python/script-interface-check.py --no-such-flag; echo "exit=$?"
/usr/bin/python3 -c 'import json;d=json.load(open(".specify/.tmp/sic.json"));print(d["schema"],d["candidates"],d["applicable"],d["exempt"],d["violations"])'
```

**Expected**: the first run exits `0` or `1` (never `2` on a healthy tree) and the payload prints
`script-interface-check/1` plus four integers whose `applicable + exempt == candidates`. `--emit-rule` prints a JSON
object with the eight keys of C-21. The unknown flag exits `2`. The engine obeys the contract it checks.

Two degraded paths, each *declared* rather than discovered (C-13):

```bash
# probe-unavailable: no interpreter that can run the candidate
/usr/bin/python3 scripts/python/script-interface-check.py --json --sandbox /nonexistent 2>&1 | tail -1; echo "exit=$?"
# candidate-not-collected: a tracked-looking file outside the two sources
```

**Expected**: each names its finding and exits `1`; no path silently degrades to "pass".

**Capture**: `.specify/.tmp/sic.json`, `.specify/.tmp/sic-rule.json` → `test-evidence/S-2-checker.txt`.

---

## S-3 — The contract test is red without its subject (after S3)

**Premises**: `tests/contract/test_script_interface_contract.py` landed with `pytestmark = pytest.mark.contract`.

```bash
SPECKIT_PYTHON=/usr/bin/python3
/usr/bin/python3 -m pytest -m contract tests/contract/test_script_interface_contract.py -q
```

**Expected**: green on the compliant tree. Then, for **M-1**, in a scratch copy only:

```bash
scratch=$(mktemp -d -p /var/tmp) && cp -a /cws_data/cloud-native-ai/spec-kit "$scratch/repo"
# remove ONE compliant script's --help arm, then:
( cd "$scratch/repo" && /usr/bin/python3 scripts/python/script-interface-check.py; echo "exit=$?" )
```

**Expected**: exit `1` and the mutated path named on its own line. A test that stays green under M-1 is not a
contract test; the mutation legs M-1…M-6 are what make this file load-bearing (≥1 mutation assertion is the
requirement, six is the design).

---

## S-4 — Governance lands on all five surfaces at once (after S4)

**Premises**: the template principle, the live constitution principle, the instructions ambient section, the
`manage-constitution` mandate entry, and the two count pins are all in the same commit.

```bash
SPECKIT_PYTHON=/usr/bin/python3
/usr/bin/python3 -m pytest -m contract tests/contract/test_constitution_double_landing.py -q
/usr/bin/python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k test_a7
grep -n '^### ' .specify/memory/constitution.md | tail -2
head -3 .specify/memory/constitution.md
```

**Expected**: both tests green with the counts moved from the measured baseline (18/19/11, watchlist 6) to
(19/20/12, watchlist 7) for the double-landing pins, and from (32/33) to (33/34) for `test_a7`'s
`TPL_EXPECTED`/`LIVE_EXPECTED`. The last principle's numeral is the next Roman numeral in sequence (no gap, no
reuse). The header carries `1.17.0` and a fresh `Last Amended`.

**Trap**: raising a count is not the amendment — the double-landing test's `c10` mutation probe is what proves the
count still *catches* a missing landing. Do not edit the counts to make a red test green.

---

## S-5 — The incident script stops being an incident (after S5; the load-bearing scenario)

**Premises**: `scripts/bash/script-interface.sh` exists, its guard body is inlined into every applicable `.sh`, and
the mirror projection rule (C-33…C-38) is registered for the `scripts` pair.

```bash
SPECKIT_PYTHON=/usr/bin/python3
# Premise: the scratch tree MUST be able to exec (see the trap note below) and, for the
# status line, MUST be a real git work tree — `git clone` a local copy, do not `cp -a`.
scratch=$(mktemp -d -p /var/tmp)/repo
git clone -q --no-hardlinks /cws_data/cloud-native-ai/spec-kit "$scratch"
cd "$scratch"
before=$(sha256sum .specify/instructions.md | cut -d' ' -f1)
bash scripts/bash/generate-instructions.sh --help >/dev/null 2>&1; h=$?
after=$(sha256sum .specify/instructions.md | cut -d' ' -f1)
echo "help_exit=$h unchanged=$([ "$before" = "$after" ] && echo yes || echo no)"
git status --porcelain            # MUST print nothing
```

**Expected**: `help_exit=0 unchanged=yes` and `git status --porcelain` prints nothing. Measured during the plan
stage on a `git clone` of this repository at `23c7a83b`: `help_exit=0 unchanged=yes`, clean status.

**The escaped write is not where the hash guard looks — this is the trap that makes S-5 load-bearing.** Three
measured facts, on the same clone:

1. `generate-instructions.sh --help` today exits **0** and writes **nothing**, so a guard that only diffs
   `.specify/instructions.md` cannot tell "the guard works" from "the script was harmless". A probe with no
   discriminating control is not evidence.
2. The un-flagged run on a **healthy** file is also a no-op: `git status --porcelain` is empty after it, because the
   reconcile's inject/strip pass writes only on `missing or stripped`. Do not use a healthy tree as the red control.
3. The write that *does* escape lands on **`.gitignore`**, not on `.specify/instructions.md`:
   `gitignore_add_pattern ".specify/instructions.md-*"` (lines 216) and `".specify/tools/*.json"` (line 66) are
   reached unconditionally, so the incident surfaces as a `.gitignore` diff with the instructions file untouched.

**Therefore SC-002's snapshot pair MUST name both files** — `.specify/instructions.md` **and** `.gitignore` — and
the red control MUST be the damaged-file variant:

```bash
# red control: delete one template section from the clone, then run the UN-FLAGGED form
/usr/bin/python3 - <<'PY'
import re, pathlib
p = pathlib.Path('.specify/instructions.md'); t = p.read_text()
m = re.search(r'^## ', t, re.M); p.write_text(t[:m.start()] + t[t.index('\n## ', m.start()+1)+1:])
PY
before=$(sha256sum .specify/instructions.md | cut -d' ' -f1)
bash scripts/bash/generate-instructions.sh >/dev/null 2>&1
after=$(sha256sum .specify/instructions.md | cut -d' ' -f1)
echo "noflag_changed=$([ "$before" = "$after" ] && echo no || echo yes)"
```

**Measured expected** (run during this stage): `noflag_changed=yes`, and the log line
`Injected missing template section(s): Project Overview`. The guard's job is to make the **flagged** form leave
both files byte-identical; this control proves the un-flagged form would not.

**Two environment traps that will fake a pass or a fail:**

- `/tmp` is mounted `noexec` on this host, so any scratch tree under `/tmp` fails at the first nested
  `scripts/bash/refresh-tools.sh` invocation with `Permission denied` and **exit 126** — that is the mount, not the
  script. Use a directory under `/var/tmp` (or `$HOME`) and verify with `mount | grep ' /var/tmp '`.
- A tree populated by `tar`/`cp` from `git ls-files` is **not** a git work tree, so `git status --porcelain` prints
  `fatal: not a git repository` and every "did it write?" reading becomes meaningless. Clone, or run
  `git init && git add -A` first.

**Never run the un-flagged form on the live tree.** It writes `.specify/instructions.md` by design.

---

## S-6 — Python answers, and the version has exactly one source (after S6)

**Premises**: `scripts/python/script_interface_cli.py` exists; `VersionAction` is registered on the top parser *and*
every subparser; both `argparse`-free readers (`clause_extract.py`, `gate-check.py`) gained a pre-parse guard.

```bash
SPECKIT_PYTHON=/usr/bin/python3
/usr/bin/python3 scripts/python/sync-mirrors.py --version; echo "exit=$?"
/usr/bin/python3 scripts/python/goal-utils.py --version; echo "exit=$?"       # required subparsers
scratch=$(mktemp -d -p /var/tmp) && cp -a /cws_data/cloud-native-ai/spec-kit "$scratch/repo"
sed -i 's/^version = .*/version = "9.9.9"/' "$scratch/repo/pyproject.toml"
( cd "$scratch/repo" && /usr/bin/python3 scripts/python/sync-mirrors.py --version )
```

**Expected**: `sync-mirrors.py <version>` exit 0; `goal-utils.py <version>` exit 0; the copy prints
`sync-mirrors.py 9.9.9`, proving the value is read at run time and not baked in. A repository-wide scan for a
version-shaped literal inside a script body returns zero hits (C-8).

**Measured today (the red baseline this scenario must flip)**: `goal-utils.py --version` exits **2** with
`error: the following arguments are required: action` — the required-subparsers trap (Risk 5). Two python scripts
carry **no `argparse`** and read `sys.argv` directly — `clause_extract.py`, `gate-check.py` — while three more
(`validate-decision-tensions.py`, `validate-falsification-quartet.py`, `validate-requirements.py`) import
`argparse` and hand `sys.argv[1:]` to `parse_args`. `clause_extract.py --help` today exits **2** printing
`--help: not a file`: it read read-only intent as an action (Risk 9). A guard that only wraps `argparse` users
therefore leaves the two `argparse`-free readers uncovered, while the three `argparse` users still need the action
registered on the top parser *and* every subparser; `validate-decision-tensions.py` is also the validator this
feature's own `T-001…T-003` records are checked with.

---

## S-7 — The instructions budget (after S7)

**Premises**: the ambient section text is final.

```bash
SPECKIT_PYTHON=/usr/bin/python3
wc -c .specify/instructions.md
grep -n 'INSTRUCTIONS_BUDGET_BYTES' scripts/bash/generate-instructions.sh
```

**Expected**: the file's size ≤ the constant. At plan time the file is 33 357 B against 34 816 B, so the section
must fit in 1 459 B or the constant moves by the smallest multiple of 1024 keeping ≥ 1024 B of headroom (Risk 7).
The commit body records old value / new value / measured size / reason.

---

## S-8 — Closure (after S8)

**Premises**: S0–S7 done.

```bash
SPECKIT_PYTHON=/usr/bin/python3
/usr/bin/python3 scripts/python/script-interface-check.py --json > .specify/specs/089-script-interface-contract/test-evidence/closure-check.json
/usr/bin/python3 -m pytest -m contract -q
/usr/bin/python3 scripts/python/sync-mirrors.py --check; echo "exit=$?"
cd .specify/specs/089-script-interface-contract && /usr/bin/python3 ../../skills/sdd-loop-driver/scripts/audit-test-budget.py --spec . 2>/dev/null; echo "exit=$?"
```

**Expected**: `violations=0` with every exempt row carrying `basis` + `evidence`; the contract suite green; the
mirror check `exit=0`; exactly the **two** budget slots recorded (`baseline`, `closure`) and no third.

---

## What this quickstart deliberately does not do

- It does not hand-verify files one at a time. 737 candidates are judged by the engine; a human reads the report,
  not the corpus. Any scenario here whose "expected" is a list of paths longer than a screen is a design smell.
- It does not exempt `tests/` as a directory. 449 of the 737 candidates live there (447 `.py` + 2 `.sh`); 441
  `.py` have no `__main__` and are exempt by `no-entry-point`, while the 6 modules that do carry one (5 under
  `tests/fixtures/` plus `tests/contract/test_migration_distribution.py`) and `conftest.py` are judged by what
  they do when run (R7).
- It does not edit `.specify/` mirrors. Every mirror is produced by `sync-mirrors.py` from its source, except the
  two declared projection kinds (`python-version-bridge`, `bash-version-guard`) whose projection is a named function
  checked by `--check-projection` (C-33).
