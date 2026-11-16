# Contract — `line-registration-scan.py` (read-only long-task scanner)

**Subject**: `scripts/python/line-registration-scan.py` (framework source; mirror `.specify/scripts/python/line-registration-scan.py`, generated — never hand-edited).
**Owners**: the mechanical criterion set is owned by this module's constants (A-15); the human criterion and its bounds are owned by `shared/guidelines/reporting-obligations.md` § 九. Shared literals are referenced as `[[STR-NNN]]`.

## C-01 — Surface

| Option | Repeatable | Meaning |
|--------|------------|---------|
| `--root <path>` | yes | scan root for this invocation; replaces the default set |
| `-h`, `--help` | — | print usage, exit 0 |

C-02 An undeclared option or a missing option value MUST exit `2` without scanning.
C-03 The script MUST be read-only: it writes no file, creates no directory, spawns no process and reaches no network.

## C-04 — Default roots

With no `--root`, the scanner MUST use `DEFAULT_SCAN_ROOTS` — the constant is the owner and this contract does not restate its members (declared live roots per A-21).

C-05 Each effective root MUST exist as a directory. A missing root, a non-directory root, or a root resolving outside the repository root is an input error: exit `2`, naming the root. A missing or empty root MUST NOT be rendered as a clean reading.
C-06 Every effective root MUST be printed in the reading, so a reader can tell which roots produced the verdict.

## C-07 — Judged file surface

A file is judged iff it is a regular file under an effective root, does not escape the repository root, and satisfies either: suffix `.sh` / `.bash` / `.py`, or a `#!` first line. Symlinks MUST be skipped and MUST NOT be followed. Non-matching files (including `.md`) MUST NOT enter judgement.

## C-08 — Criterion constants (the single machine owner)

The module carries exactly these module-level constants; tests import them and no other surface restates their members:

| Constant | Role |
|----------|------|
| `LONG_TASK_MARKERS` | content strings whose presence makes a judged file a long task (`[[STR-004]]`, `[[STR-005]]`) |
| `SELF_DECLARATION_MARKER` | a standalone comment line by which a file declares itself a long task (`[[STR-003]]`) |
| `COMPLIANT_INVOCATIONS` | invocation forms that discharge the duty: the `[[STR-001]]` wrapper form, and `[[STR-002]]` with action `register` / `update` / `deregister` |
| `DEFAULT_SCAN_ROOTS` | the declared live roots used when `--root` is absent |

C-09 Matching is case-sensitive literal containment; the scanner MUST NOT interpret the surrounding code, and MUST NOT add a second criterion outside these constants.

## C-10 — Verdict

A judged file is a **violation** when it hits `LONG_TASK_MARKERS` or carries `SELF_DECLARATION_MARKER`, and contains no member of `COMPLIANT_INVOCATIONS`. A hit with a compliant invocation is clean. The self-declaration marker declares a file a long task; it never exempts the file from registration.
C-11 A file with neither marker nor self-declaration is clean.

## C-12 — Owner skip

The scanner's own resolved path MUST be skipped when it falls inside a root, so the owner of the criterion is never judged as an executor. The skip MUST be printed as `owner-skipped: 1` (else `0`) and MUST NOT be counted as a clean hit in any other statistic.

## C-13 — Output

For every violation: `<path>:<line>: criterion=<content-marker|self-declaration>` followed by the matched text, one line per file. After the detail lines, one summary block:

```text
root: <path> (files: <n>)
...
scanned: <n> files
violations: <n>
owner-skipped: <0|1>
```

C-14 The reading MUST be deterministic for one tree: same roots, same content → same lines in the same order (lexicographic path order).

## C-15 — Exit status (closed set)

| Exit | Meaning |
|------|---------|
| `0` | no violation |
| `1` | at least one violation |
| `2` | input error (bad option, missing/non-directory/outside root) |

C-16 Exit `2` MUST take precedence over `0`/`1`: an input error is never reported as a reading.

## C-17 — Fixture use

The scanner MUST accept a fixture root inside the repository (the tests use `.specify/.tmp/line-registry-registration/`), and MUST behave identically there. No fixture-helper script exists; tests create and remove their own fixtures.

## Examples

**E-1 (not runnable in this planning run — the scanner does not exist yet).**
Premises: scanner implemented at C-01…; a fixture root created by the test; a script containing a `LONG_TASK_MARKERS` member and no compliant invocation.

```bash
python3 scripts/python/line-registration-scan.py --root .specify/.tmp/line-registry-registration
```

Expected: exit `1`; the fixture path appears with `criterion=content-marker`. Pinned by `tests/contract/test_line_registration_scan.py`.

**E-2 (not runnable in this planning run).** Premises: as E-1; the same fixture rewritten to keep its marker **and** invoke the wrapper, so a clean verdict can only come from compliant-invocation detection.

```bash
python3 scripts/python/line-registration-scan.py --root .specify/.tmp/line-registry-registration
```

Expected: exit `0`; `violations: 0`. Pinned by the same file (positive and negative legs both asserted).

**E-3 (not runnable in this planning run).** Premises: the declared live roots exist; the implementation is complete.

```bash
python3 scripts/python/line-registration-scan.py
```

Expected: exit `0`; the reading names each root, `violations: 0`, and `owner-skipped: 1`. The reading is written to `test-evidence/`; pinned by `tests/integration/test_line_registration_scan_live.py` plus the recorded reading.

**E-4 (recorded measurement, not a command example — 2026-11-16).** Each `LONG_TASK_MARKERS` member was searched across the three declared roots with a read-only grep at planning time: member 1 → 0 hits; member 2 → 4 hits, all `.md` under `skills/external/*/references/` and therefore excluded by C-07. The literals are owned by the constant and by `requirements.md` § Shared Strings, so they are not restated here.
