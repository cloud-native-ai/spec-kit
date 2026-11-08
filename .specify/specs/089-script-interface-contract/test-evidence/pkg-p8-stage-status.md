# P8 stage status (test surface under the 2026-11-08 narrowing, 2026-11-08)

The ruling: **only functional, non-read-only scripts** must answer `--help` / `--version`. The
checker implements four bases for everything else — `pytest-module`, `optional-read-only`,
`out-of-scope`, `historical-record` — and files them in `exemptions[]` with the basis printed on the
row. The failures this stage repaired were all one defect: **fixtures that stood for REQUIRED
scripts carried no write-triggering declaration**, so the checker filed them read-only and the
clauses that measure them went quiet (a green that says nothing, and a red that never fires).

No implementation, no `scripts/`, no `shared/`, no `templates/`, no constitution was changed by this
stage — only `tests/contract/test_script_interface_contract.py`.

## Per-fixture reading: required vs optional

All readings taken from the checker's own `--json` payload, current tree, after the edits.

| fixture | declaration carried | classified | filed as | used by |
|---|---|---|---|---|
| `_strict_bash` (bash, C-9-strict) | `--out PATH  where to write (triggers the write)` on a printed usage line | **required**, `applicable=true` | `violation_rows: []`, `exemptions: []` | `_compliant_tree` → C-17 green leg, C-19 green leg, T079 control |
| `_strict_python` (python, C-9-strict) | same annotation inside the printed `USAGE` text | **required**, `applicable=true` | green, `exemptions: []` | `_compliant_tree` → python half |
| `_flapless_bash` (new, C-17/C-19 red legs) | keeps `--out … (triggers the write)`, deletes every flag limb | **required**, `applicable=true` | `violations=1`, missing `help, version, unknown-rejected`; exit 1 | C-17 red leg, C-19 red leg |
| `_strict_bash` + `-h\|--help` arm deleted (T079 mutant) | declaration inherited → still required | **required** | exit 1, `scripts/keepme.sh` named | T079 |
| `_verbatim_required` (new, C-30 acting leg) | `--out PATH  where to write (triggers the write)` | **required**, `applicable=true` | `violations=1` naming `skills/external/vendor/scripts/verbatim.sh`; exit 1 | C-30 unregistered, acting leg |
| `_external_skill` default body (bare `echo`) | none | read-only | `exemptions[] basis="optional-read-only"` | C-30 unregistered, read-only leg |
| `good_bash` / `good_python` (`_probe_tree`) | already carried the annotation | required | unchanged | C-5/C-9/C-10/C-11 (were green, stay green) |

## Per-test repair

| test | repair kind | what changed |
|---|---|---|
| `test_c17_the_exit_code_is_derived_from_the_report` | required (add write option) | the inline `main(){ echo hi; }` red control replaced by `_flapless_bash`, which keeps the write DECLARATION and drops only the flag limbs |
| `test_c19_the_human_face_prints_violations_and_always_the_summary` | required (add write option) | same red control substitution (`silent.sh`) |
| `test_t079_a_deleted_help_arm_goes_red_and_names_the_script` | required (add write option) | `_strict_bash`'s usage body now annotates `--out` with `(triggers the write)`; the mutation is unchanged |
| `test_c30_an_unregistered_third_party_script_is_an_ordinary_candidate` | required + optional legs | split into two legs: an ACTING third-party script (declaration present) must be a named violation — registration is the only credential; a read-only third-party script is filed `optional-read-only`, never `declared-exception`. `_external_skill` gained a `body=` parameter |
| `test_c30_owner_table_and_checker_payload_agree_row_for_row` | column mapping | the comparison now derives each JSON key from the page's column heading (`unsatisfied clause` → `unsatisfied_clause`) and compares all four columns, so the two registered document-utils rows compare row-for-row instead of tripping on the key spelling |
| `test_c25` / `test_c35` / `test_c33` | **not repaired — carried, see ANOMALY** | out of this stage's territory (constitution text, mirror sync) |

Note on the fixture-intent rule: the write DECLARATION is what keeps a fixture in the required set.
Deleting it along with the surface (`_flapless_bash` v1) makes the checker re-file the file as
`optional-read-only`, and the "must go red" assertions become unmeasurable — the same false green in
a new place. The declaration therefore stays; only the flag limbs go.

## Readings

| check | command | result |
|---|---|---|
| target suites | `/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py tests/unit/test_script_interface_cli.py` | **120 passed, 3 failed** (all three carried; see ANOMALY) |
| unit suite alone | `/usr/bin/python3 -m pytest -q tests/unit/test_script_interface_cli.py` | 30 passed |
| contract suite alone | `/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py` | 90 passed, 3 failed |
| before this stage | same contract suite | 85 passed, 8 failed |
| closed this stage | — | C-17, C-19, T079, C-30 (×2) — the five the brief named |
| safety snapshot | `python3 scripts/python/workspace-guard.py --snapshot /var/tmp/086-p8.json --repo .` | `recorded`, taken before any probe |
| safety check | `python3 scripts/python/workspace-guard.py --check /var/tmp/086-p8.json --repo .` | `clean` |

## Carried failures (pre-existing, outside this stage's territory)

| test | cause | why not repaired here |
|---|---|---|
| `test_c25_live_constitution_carries_the_principle` | `.specify/memory/constitution.md` §XX gained a sixth bullet — `- A pytest module, a pure library, and a read-only script are outside the REQUIRED set …` — which carries no `MUST`, so the sibling guard's limb (c) fails. The TEMPLATE roster (`templates/constitution-template.md` §XIX) does NOT carry that bullet, so the two rosters have diverged in content, not only in numeral. | repairing it means editing the constitution: either deleting the bullet or re-wording it as a `MUST NOT` and re-running the amendment (version bump + Sync Impact Report). Both are constitutional choices the brief forbids this stage from making. |
| `test_c35_the_check_asserts_the_projection_and_names_its_kind` | `sync-mirrors.py --check` reports `DIFF .specify/templates/instructions-template.md`: the source `templates/instructions-template.md` was narrowed (ambient sentence) while its mirror was not re-projected. | fixing it is `sync-mirrors.py --write`, which rewrites `.specify/` (forbidden here) and absorbs the drift as a mirror projection; the direction of the narrowing (source vs runtime) is the owner's call. |
| `test_c33_no_mirror_is_hand_edited_and_c38_each_carries_one_marker` | same single drift as C-35 (`"DIFF" in proc.stdout`). | same as C-35. |

All three were failing when this stage began and are unaffected by anything changed here.
