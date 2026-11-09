# Contract: Script Interface Criteria

**Feature**: 089-script-interface-contract | **Contract file**: `contracts/script-interface-criteria.contract.md`
**Guard carrier**: `tests/contract/test_script_interface_contract.py` (decision clauses) + the owner page's
own guard (pointer/rule clauses)
**FR coverage**: each clause carries its own trailing citation group; that group, not this header, is the owner of the mapping

The contract's判据: what counts as a candidate, what separates an applicable script from an exempt library,
what an applicable script owes, and how a mirror copy is judged. Every clause is decidable by a program; the
owner page `shared/definitions/script-interface-definitions.md` states the same rule in human form, and C-21
(see `contracts/contract-checker-cli.contract.md`) asserts the two agree.

## C-1 — Candidate screen from two machine-readable sources

The candidate set MUST be derived as `git ls-files '*.sh' '*.py'` minus the paths `git check-ignore` reports as
ignored. No hand-written directory list, no per-directory exclusion. When git is unavailable the work-tree walk
becomes the candidate set and the report MUST say `source=walk-only`; it MUST NOT report an empty candidate set
as a pass.

(FR-002, FR-024)

## C-2 — Coverage assertion

The check MUST walk the whole work tree for `*.sh` / `*.py`. A file that is neither a candidate nor ignored MUST
produce `candidate-not-collected` naming the file and MUST exit 1. The assertion is the only thing standing
between "the screen's source is broken" and "everything passed".

(FR-024)

## C-3 — bash classification is a run, not a read

A `.sh` candidate MUST be classified applicable if and only if, run as a script (not sourced), the code placed
after its recognized-option trigger executes. The check MUST decide this by instrumenting that position in a
copy of the file and observing the marker. None of the following MAY be used as the criterion: the presence of
top-level statements, the shebang word (`bash` vs `sh`), or any self-description in the file.

(FR-003, FR-017, FR-025)

## C-4 — python classification is a run, not a block

A `.py` candidate MUST be classified applicable if and only if running it with a declared action produces an
effect outside the interpreter's own import machinery. The presence of `if __name__ == "__main__":` MUST NOT be
the criterion: a module that carries the block and is never run as a script does not act when executed, and a
module that acts on import is not exempt either.

(FR-026)

## C-5 — Both uses ⇒ applicable

A file that is both sourced/imported and executable as a script MUST be classified applicable. "It is also a
library" MUST NOT be accepted as grounds for exemption.

(FR-009)

## C-6 — Mirror copies

A `.specify/**` script copy with a same-path source MUST inherit that source's class and MUST be judged for the
flag surface it carries (source surface plus the declared projection). It MUST NOT be judged twice as if it were
an independent script, and it MUST NOT be exempted by being a copy.

A `.specify/**` script copy **without** a same-path source MUST be judged on its own run semantics, exactly like
any other candidate; its `basis` is `mirror-unpaired`, distinct from `projected-mirror`. Measured on this tree:
**73** of the 87 `.specify/skills/` script copies have no source at the literal `.specify/skills/<rest>` path
(the runtime skill directory names differ from `skills/external/<name>/` and `skills/internal/<name>/`), and 81
copies across all of `.specify/` are unpaired once the 8 fixture stubs under `.specify/specs/075-…/notes/` are
counted. The candidate set is therefore never de-duplicated by path — both sides of a projected pair stay
candidates — although the probe work may be de-duplicated by probing each distinct content once.

(FR-024, FR-030)

## C-7 — Mandatory help content, as four labels

An applicable script's `-h` and `--help` MUST both exit 0 and print: (a) the usage form, (b) the recognized
options, (c) whether the script has side effects and which, (d) the meaning of its exit codes. The check MUST
assert the four labels as four separate assertions, so a help text that mentions "usage" and nothing else cannot
satisfy the clause by substring accident. `-h` and `--help` MUST produce the same body.

(FR-003)

## C-8 — Version line and its single source

`--version` MUST exit 0 and print exactly one line `<script-name> <framework-version>`. `<framework-version>` MUST
be read from `pyproject.toml` at run time; the value read MUST equal the file's `version` field at that moment.
No script may carry a literal version string: the repository-wide scan for a version-shaped literal inside a
script body MUST return zero hits. The file is located by a bounded upward search from the script's own directory to the enclosing repository
root (the nearest ancestor containing `.git`), never beyond it; the resolved root's `pyproject.toml` is the only
version source. When no such root or no `pyproject.toml` is found the line MUST be `<script-name> unknown` and
the exit code MUST remain 0.

(FR-004)

## C-9 — Unrecognised options are rejected before the action

An undeclared token beginning with `-` MUST exit non-zero and MUST NOT reach the main action; its output MUST be
produced before any write. A recognized option present in the same invocation MUST NOT let an unrecognized one
through. A token after a bare `--` MUST NOT be treated as an unrecognized option. The rejection MUST apply when
the script otherwise accepts free-text positional arguments.

A wrapper that DECLARES `passthrough` forwards the unknown token to its downstream parser by its author's own
statement; that is declared behaviour, not a token "silently ignored and then acted on", so the second leg is
judged compliant with basis `passthrough`. A script that declares nothing and merely happens to exit 0 MUST stay
red.

(FR-006, FR-007)

## C-10 — Zero side effects, proved on a sandbox copy

Zero side effects MUST be judged on a copy of the repository created outside the measured tree. The snapshot pair
is: `git status --porcelain` output, `sha256` of every `*.sh` and `*.py` in the measured tree, and the file list
plus hashes under `.specify/`. The four runs (`-h`, `--help`, `--version`, one unrecognized option) MUST leave the
pair identical. Running the probes against the live tree MUST NOT be accepted as evidence, because the scripts'
own temporary directories would mask or counterfeit a real write.

(FR-005, FR-019, FR-029)

## C-11 — Help wins over any main action

When the consumer declares a write-triggering option, and that option is present together with a flag, the flag
MUST win: the process MUST exit before the main action, in either argument order. This clause is the memory of
the incident (`script.sh --help --write`).

The write-triggering option is the one the consumer DECLARES — a `writes=OPTION` on the guard's `define` call
(bash) or an option help line closing with `(triggers the write)` (python). A consumer that declares none has no
order to judge: the probe MUST report `not applicable` with basis `no-write-option`, never a violation. The
clause's precondition is absent rather than unmet, and inventing an option to test against would demand that
every script spell the engine's idea its own way.

(FR-005)

## C-12 — No silent omission

A candidate that is neither compliant nor exempt MUST be reported as a violation naming the missing limbs. The
report MUST NOT contain an "unevaluated" state that is counted as compliant.

(FR-010)

## C-13 — Degraded paths are red

Sandbox creation failure, probe timeout, a projection-rule mismatch, and an unreadable exception row MUST each be
a finding with a distinct name and exit 1. None of them MAY reduce to `violations=0`.

(FR-010)
