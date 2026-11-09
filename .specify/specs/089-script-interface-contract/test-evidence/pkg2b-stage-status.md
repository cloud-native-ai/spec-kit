# Package 2b stage status — 089-script-interface-contract (T020–T029, US4 landings)

**Scope**: Phase 3 US4's **implementation band** (T020–T029). Ten rows: five landings, one
reconcile, one mirror re-projection, two success-criterion proofs and one policy record.
**Tree**: `/cws_data/cloud-native-ai/spec-kit`, branch `089-script-interface-contract`,
parent `b33751cc`.
**Run**: 2026-11-06, implement stage, package 2b of ~6.
**Commit**: `efa3a270` — the five landings and their pins move together (DoD-6).

---

## 1. Per-task completion

| Task | Status | Landing point (repo-relative) | Evidence |
|---|---|---|---|
| T020 | done | `templates/constitution-template.md` — `### XIX. Script Interface Contract (Declared, Zero-Side-Effect)`, 5 MUST bullets, `Rationale:`, pointer to `.specify/shared/definitions/script-interface-definitions.md`, scope stated in the rule | `test_c24_*` green (2 rows) |
| T021 | done | `skills/internal/manage-constitution/SKILL.md` — `- **MUST include**` entry 11 → 12, owner path + referenced-not-restated | `test_c26_*` green |
| T022 | done | `templates/instructions-template.md` — ambient `## Script Interface Contract` (2 sentences + owner path) | `test_c27_ambient_section_shape[template]` green |
| T023 | done | `.specify/memory/constitution.md` — principle XX, Sync Impact Report at top, `1.16.0 → 1.17.0`, `Last Amended` 2026-11-06, one edit | `test_c25_*` green (2 rows) |
| T024 | done | `.specify/instructions.md` — one `## Script Interface Contract` section, produced by `generate-instructions.sh` on a **cloned scratch tree** | `test-evidence/T024-instructions-reconcile.txt` |
| T025 | done | `.specify/templates/*` (2), `.specify/skills/internal/manage-constitution/SKILL.md`, `.specify/shared/definitions/script-interface-definitions.md` | `sync-mirrors.py --check` → exit 0, six pairs ok |
| T026 | done | `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` → `TPL_EXPECTED = 33`, `LIVE_EXPECTED = 34` | row green; 33/34 measured |
| T027 | done | clean downstream project built from this working tree | `test-evidence/SC-004-downstream.txt` |
| T028 | done | `git show efa3a270` — version line, Sync Impact Report, Last Amended in one commit | `test-evidence/SC-005-constitution-diff.txt` |
| T029 | done (Phase 3 half) | owner-page label set / matching unit / class vocabulary, as the input T082 compares against | `test-evidence/T029-owner-page-emit-rule.txt` |

**T019 stays OPEN** on purpose: its `[blockedBy: T018,T065]` names a Phase 4 row, so its green
point is Phase 4 by the tasks file's own declaration, not this package's choice. Its red reading
is unchanged and correct: `scripts/python/script-interface-check.py` does not exist until T032/T045.

## 2. Red → green readings (measured this package)

| Command | Before (b33751cc) | After |
|---|---|---|
| `pytest tests/contract/test_script_interface_contract.py tests/contract/test_constitution_double_landing.py -q` | **18 failed, 17 passed** | **1 failed, 34 passed** |
| `pytest tests/contract/test_script_interface_contract.py -q` | 11 failed, 3 passed | **1 failed, 13 passed** |
| `pytest tests/contract/test_constitution_double_landing.py -q` | 7 failed, 14 passed | **21 passed** |
| `pytest tests/contract/test_fast_fail_discipline.py -q` | 1 failed (baseline), 103 passed | **1 failed (same row), 103 passed** |
| `sync-mirrors.py --check` | exit 0 | **exit 0**, six pairs ok |
| `validate-tasks.py tasks.md` | `PASS (with warnings)`, 0 error, 62 warning | **unchanged** (0 error, 62 warning) |
| `grep -cE '^- \[[ >]\]' tasks.md` | 68 | **59** (nine rows closed, T019 deliberately left open) |

The one residual red in the new file is `test_c30_owner_table_and_checker_payload_agree_row_for_row`
(T019, Phase 4). The one residual red in the sibling file is `test_g9_total_equals_frozen_baseline`,
which is **already in `baseline-failed.txt`** — it was red at implement entry, before this feature
touched anything.

## 3. Count pins — the four values, recorded separately (SC-006 source)

| Pin | Value | Where measured |
|---|---|---|
| template principles | **19** | `grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md` |
| live principles | **20** | same, `.specify/memory/constitution.md` |
| generator MUST-include entries | **12** | sub-entry count in the `- **MUST include**` block |
| double-landing watchlist | **7** | `DOUBLE_LANDING_WATCHLIST` length |

Set-containment direction, recorded separately from the counts (SC-006(b)): every watchlist title
is present in the template roster AND in the generator's entry list — asserted by
`test_c7_watchlist_principles_land_on_both_sides`, which is green. The counts and the containment
are two different readings and are not merged into one sentence.

## 4. Corrections repaired in passing (disclosed)

1. **C-29's banned-literal scan matched bare words, and bare words collide with pre-existing
   prose.** Package 2a surfaced this (`ANOMALY A-1` there). Repaired as the brief directs, and
   the repair is **bounded**: the scan now matches the **complete label form** (the label plus its
   value, e.g. `` `usage` 标签 ``) and the classification-steps heading; the owner page gained
   exactly one paragraph stating that unit ("the unit of restatement is the complete label, not
   the word") and the guard **reads the form template back out of the page** instead of typing it.
   Why the bare word was wrong, measured: `templates/constitution-template.md` carries
   `Presenting options that are incomplete or incorrect` (principle XI, about decision quality) and
   `templates/instructions-template.md` carries `token usage efficiency` (Token Efficiency
   Discipline) — neither restates the owner page, so a bare-word scan reported two leaks that were
   not leaks. The page is still the single owner of what "restating a label" means.
2. **Four stale pins in `test_fast_fail_discipline.py` measured the surfaces this commit writes.**
   `test_x5` (version → 1.17.0), `test_x15` (watchlist length 6 → 7), `test_x18` (gate-row
   enumeration 19/18 → 20/19) and `test_a7` (instructions sections 32/33 → 33/34, the row T026
   names). `test_x5`/`test_x15`/`test_x18` went red **because of this package's landing** and would
   have been new failures; each is a pin over an artifact that changed, so raising it in the same
   commit is the tasks file's own stale-pin rule, not a scope expansion.
3. **The owner page's label paragraph needed a machine-readable form for the matching unit.**
   The inserted paragraph uses the literal `` `{0}` 标签 `` so the guard can read the template and
   instantiate it per label; a prose description would have left the guard inventing the form.
4. **One evidence-file measurement was wrong on first write and was corrected.** The T029 record
   first probed for `判为豁免`, which does not occur because the page writes the two arms of the
   same sentence as `即判适用, 不出现即判豁免`; the record now shows the measured string. Corrected
   rather than left standing, because an evidence file whose reading is false is a false reading.

## 5. Anomalies surfaced (not repaired in this package)

- `ANOMALY B-1` — **the T027 brief's premise is factually wrong about one of the two files it
  names.** The brief says SC-004 is proved by asserting that "the generated constitution carries
  the principle title and the generated `instructions.md` carries the ambient heading". Measured on
  a clean `specify init` (see `SC-004-downstream.txt`): **neither file exists in a fresh downstream
  project**. `specify init` copies `.specify/templates/constitution-template.md` and seeds
  `.specify/memory/constitution.md` with a placeholder ("This file is a placeholder for the project
  constitution … use `/speckit.constitution`"); it does not run the instructions generator, so
  `.specify/instructions.md` is absent until `/speckit.instructions` runs. The row is closed on the
  reading the criterion can actually be held to — the two **generated surfaces** a clean project
  receives carry the principle title and the ambient heading, byte-identical to the framework
  source — and the divergence is disclosed rather than silently reinterpreted. Deciding whether
  SC-004 should instead require `/speckit.constitution` + `/speckit.instructions` to run inside the
  proof is a change to `requirements.md`, which is not this package's write territory.
- `ANOMALY B-2` — **`generate-instructions.sh` aborts in a non-git downstream tree, before any
  instructions reconcile.** Measured: `bash .specify/scripts/bash/generate-instructions.sh` in the
  clean `/var/tmp` project exits 1 with `touch: cannot touch '//.gitignore': Permission denied`,
  at line 65, before the reconcile. Cause is measured and pre-existing: `scripts/bash/common.sh:5`
  sources `${CWS_LIB_BASH_HOME}/bin/cws_bash_env` on this host, whose `git_repo_root()` falls back
  to a path derived from the **library's** own location and returns `/` in a non-git directory, so
  `$REPO_ROOT/.gitignore` resolves to `//.gitignore`. This is the M-1 entry already in
  `.specify/memory/feedback/backlog.md` (2026-10-15). It is outside this package's territory (the
  file is T057's, and the helper is not even a shipped file) and it does not affect T024, where the
  clone **is** a git work tree. Surfaced, not repaired.
- `ANOMALY B-3` — **the sentence in commit `efa3a270`'s body that describes which rows stay red is
  wrong, and the commit is not reworded.** That paragraph claims the C-29 whitelist half stays red;
  in fact C-29 is fully green after the correction in § 4.1, and the only red rows are T019's
  `test_c30_*` and the baseline `test_g9`. Rewriting a commit message means rewriting history, which
  is a decision, not a correction; this record is the authoritative reading, and the tasks file's
  T019 row carries the same statement.

## 6. Assumptions taken (unattended run — recorded, not asked)

1. **The scrub tree for T027 is built from this working tree, not from the released package.** The
   installed `specify-cli` at `/cws_data/profiles/.venv` dates from 2026-08-06 and carries the
   pre-amendment templates, so proving SC-004 with it would have been a blind check (the compared
   baseline would not be the artifact under test). An isolated venv was built and this tree
   installed into it editable; the CLI that ran every leg is that venv's.
2. **`/var/tmp` was used, not `/tmp`,** because the Environment Prerequisites record `/tmp` as
   `noexec` on this host. All scratch lives under `/var/tmp/086-t024` and `/var/tmp/086-sc004`.
3. **T029 is closed as its Phase 3 half.** The row's text says "record … as the Phase 3 half of
   that assertion"; the assertion itself is T082's, in Phase 9. Closing it here records the input
   T082 compares against and claims nothing about the equality already holding.
4. **The T024 generator ran once, and the clone was staged for it.** The clone was copied from
   this working tree (which already carried the hand-inserted live section), so its
   `.specify/instructions.md` was reverted to its committed, pre-amendment state before the run —
   otherwise the reconcile would have found every section already present and proved nothing.
   The revert, the run and the before/after readings are all in the evidence file; no second run
   was made and none is claimed.
