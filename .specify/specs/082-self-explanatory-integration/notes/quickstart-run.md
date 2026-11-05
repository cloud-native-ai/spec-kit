# T024 — live instructions reconcile (idempotency capture)

- date: 2026-11-05T05:59:49Z
- command: `bash scripts/bash/generate-instructions.sh`
- rc: 0
- live size: 33357 B; budget constant: 34816; expected verdict: within

```text
[2026-11-05 13:59:48][529137][INFO]Generating tool JSON manifests...
[2026-11-05 13:59:49][529137][INFO]Backing up existing instructions to .specify/instructions.md-2026-11-05-135949
[2026-11-05 13:59:49][529137][INFO]Existing instructions kept as the refresh base (not overwritten).
[2026-11-05 13:59:49][529137][INFO]Section reconcile: live instructions already carry all template sections.
[2026-11-05 13:59:49][529137][INFO]The /speckit.instructions command reconciles each section against current
[2026-11-05 13:59:49][529137][INFO]project state and the latest template, and can recover content dropped by
[2026-11-05 13:59:49][529137][INFO]older versions from the .specify/instructions.md-* backup history.
[2026-11-05 13:59:49][529137][INFO]Instructions size: 33357 B (budget 34816 B, 1459 B headroom). Section table, largest first:
| section                                         | live B | tmpl B | delta | placeholder | project-owned |
|-------------------------------------------------|--------|--------|-------|-------------|---------------|
| Documentation Map                               | 4980   | 2726   | +2254 | yes         | no            |
| Fast Fail Discipline                            | 1993   | 1993   | 0     | no          | no            |
| Tech Stack & Resources                          | 1717   | 514    | +1203 | yes         | no            |
| Progress Reporting Discipline                   | 1481   | 1481   | 0     | no          | no            |
| User-Facing Comprehension                       | 1353   | 1353   | 0     | no          | no            |
| Run Determination                               | 1351   | 1351   | 0     | no          | no            |
| Concurrent Development Safety (并发开发安全)          | 1337   | 1337   | 0     | no          | no            |
| Two Hats: Framework Source vs Client Runtime    | 1315   | 1315   | 0     | no          | no            |
| Ask, Record, Repeat                             | 1281   | 1281   | 0     | no          | no            |
| Proactive Flow Trigger                          | 1129   | 1129   | 0     | no          | no            |
| SDD Routing Decision (SDD 分流裁决)                 | 1124   | 1124   | 0     | no          | no            |
| Suggested Tooling Scope (High-Level)            | 1002   | 1002   | 0     | no          | no            |
| Task Complexity Rubric                          | 996    | 996    | 0     | no          | no            |
| One Source Of Truth                             | 967    | 967    | 0     | no          | no            |
| Fact, Correctness & Logic Checks (Input Sanity) | 955    | 955    | 0     | no          | no            |
| Single-Run Evidence Discipline                  | 901    | 901    | 0     | no          | no            |
| Token Efficiency Discipline                     | 880    | 880    | 0     | no          | no            |
| ID Register (编号登记)                              | 814    | 814    | 0     | no          | no            |
| Dogfooding Practice                             | 810    | 810    | 0     | no          | no            |
| Recurring Operational Lessons                   | 646    | 0      | +646  | no          | yes           |
| Root-Cause Problem Solving                      | 637    | 637    | 0     | no          | no            |
| Self-Explanatory Structure (不言自明)               | 618    | 618    | 0     | no          | no            |
| Git Workflow                                    | 576    | 576    | 0     | no          | no            |
| Spec Kit Framework Map                          | 551    | 551    | 0     | no          | no            |
| Spec Kit Runtime & Symlink Model                | 541    | 541    | 0     | no          | no            |
| Grounded Naming                                 | 518    | 518    | 0     | no          | no            |
| Skills & Tools                                  | 467    | 468    | -1    | no          | no            |
| Closed-Set Claims (封闭清单声明)                      | 456    | 456    | 0     | no          | no            |
| Project Overview                                | 436    | 236    | +200  | yes         | no            |
| Temporary Directory Discipline                  | 415    | 415    | 0     | no          | no            |
| AI Tool Compatibility                           | 374    | 228    | +146  | no          | no            |
| Bilingual Expression (双语表述)                     | 372    | 372    | 0     | no          | no            |
| Knowledge Recording & Promotion                 | 364    | 364    | 0     | no          | no            |
[2026-11-05 13:59:49][529137][INFO]Ensured project glossary at .specify/memory/glossary.md (non-destructive)
[2026-11-05 13:59:49][529137][INFO]Updating symlinks for AI tools...
success Instructions generated/updated at .specify/instructions.md
```

## Part 6 (T032) — pairwise byte comparison of the three new mirror pairs

Recorded verbatim, each command followed by its runtime exit code. `cmp` prints nothing and exits 0
when the two files are identical.

```console
$ cmp shared/definitions/self-explanatory-definitions.md \
      .specify/shared/definitions/self-explanatory-definitions.md
rc=0
$ cmp shared/guidelines/self-explanatory.md \
      .specify/shared/guidelines/self-explanatory.md
rc=0
$ cmp shared/workflow/best-practice-optimization.md \
      .specify/shared/workflow/best-practice-optimization.md
rc=0
```

All three exit codes are 0: the three source/mirror pairs are byte-identical.

Independently of `cmp`, the whole pair was compared file-by-file with `filecmp.cmp(..., shallow=False)`
(no mtime shortcut), which found `missing_in_dst: []`, `extra_in_dst: []`, `differing: []` across
65 source files and 65 mirror files — i.e. the three new documents are identical **and** nothing
else in the pair drifted.

## Part 6 (T029) — `specify init` from a venv built on this working tree

```console
$ python3 -m venv .venv                                          # temp dir, rc=0
$ .venv/bin/python -m pip install -e "$(git rev-parse --show-toplevel)"
Successfully installed specify-cli-0.0.22 … rc=0
$ .venv/bin/python -c "import specify_cli, os; print(os.path.dirname(specify_cli.__file__))"
/storage/project/cloud-native-ai/spec-kit/src/specify_cli

$ cd client && ../.venv/bin/specify init --here --ai claude --no-git --skip-tls \
      --ignore-agent-tools
   ok Using local templates: shared copied
Project ready.
rc=0

$ for p in .specify/shared/definitions/self-explanatory-definitions.md \
           .specify/shared/guidelines/self-explanatory.md \
           .specify/shared/workflow/best-practice-optimization.md; do
    test -f "$p" && echo "PRESENT $p $(wc -c <"$p") B" || echo "MISSING $p"
  done
PRESENT .specify/shared/definitions/self-explanatory-definitions.md 4553 B
PRESENT .specify/shared/guidelines/self-explanatory.md 6298 B
PRESENT .specify/shared/workflow/best-practice-optimization.md 4703 B
```

The client copies are 45 B / 27 B / 90 B longer than their sources: `copy_tree_with_rewrite` rewrites
source-form path prefixes (`shared/...` → `.specify/shared/...`) on the way, which is the expected
transformation, not corruption — the receiving project's references must point at its own runtime
tree. `.specify/shared/` in the client holds 65 files, matching the source tree.

`--ignore-agent-tools` was added to the dispatcher's flags because this host has no `claude` agent
CLI and `init` aborts on that check before reaching the copy step; without it the run would fail for
a reason unrelated to distribution. The three flags the brief mandates (`--here`, `--no-git`,
`--skip-tls`) are all present.

---

# Part 7 (T036) — the distribution probe, and why the complete judgement needs a local build

## T036-a — the ambient `specify init` probe (the reading the brief calls `partial`)

Executed 2026-11-05 in `~/tmp/082-part7/probe` (a sanctioned cross-repo temp root, outside git; see
`shared/guidelines/temp-directory-discipline.md` § 1).

```console
$ mkdir -p ~/tmp/082-part7/probe && cd ~/tmp/082-part7/probe
$ specify init --here --ai claude --no-git --skip-tls --ignore-agent-tools   # exit 0
   ok Using local templates: shared copied
Project ready.
EXIT=0

$ ls -d .specify/shared
.specify/shared
$ find .specify/shared -maxdepth 2 -type d
.specify/shared
.specify/shared/definitions
.specify/shared/workflow
.specify/shared/constants
.specify/shared/guidelines
.specify/shared/patterns

$ for p in .specify/shared/definitions/self-explanatory-definitions.md \
           .specify/shared/guidelines/self-explanatory.md \
           .specify/shared/workflow/best-practice-optimization.md; do
    test -f "$p" && echo "PRESENT $p" || echo "ABSENT  $p"
  done
ABSENT  .specify/shared/definitions/self-explanatory-definitions.md
ABSENT  .specify/shared/guidelines/self-explanatory.md
ABSENT  .specify/shared/workflow/best-practice-optimization.md

$ find .specify/shared -type f | wc -l
59
```

**Reading.** The `.specify/shared/` landing directory itself is present (so T036's stop condition —
"if the landing directory is itself absent, stop and escalate" — does **not** fire), and the three
documents are absent. Absence has a measured cause, not a guessed one:

```console
$ python3 -c "import specify_cli,os;print(os.path.dirname(specify_cli.__file__))"
/usr/local/lib/python3.11/site-packages/specify_cli
$ python3 -c "print(open('/usr/local/lib/python3.11/site-packages/specify_cli/_source_commit.json').read())"
{ "commit": "26731b670a5d1f2c7e590729aa7ea947031975b9", "embedded_at": "20261029T093040Z" }
$ git log --oneline -1 26731b67
26731b67 refactor(specs): renumber 074-sdd-loop-efficiency to 075
$ git log --oneline 26731b67..HEAD | wc -l
271
$ git merge-base --is-ancestor e88cebc2 26731b67 && echo "release includes part 6" \
                                                      || echo "release PRECEDES the three documents"
release PRECEDES the three documents
```

The installed CLI is built from `26731b67` (2026-10-29), **271 commits behind** this checkout, and
that commit is an ancestor of the part-6 commit that introduced the three documents. Its packaged
`shared/` tree therefore cannot carry them, and the 59-file landing is consistent with the 62-file
`shared/` of that era minus files added later. This is not an exemption (T029 forbids reading the
stale install as evidence); it is the reason the probe's negative result is uninformative about
distribution.

## T036-b — the alternative reading: the same command against a build of THIS tree

The complete judgement needs a build whose resources carry the documents. Performed with an editable
install of the working tree (`pip install -e .` equivalent), in the same temp root:

```console
$ python3 -m venv ~/tmp/082-part7/venv                                   # rc=0
$ ~/tmp/082-part7/venv/bin/python -m pip install -e /storage/project/cloud-native-ai/spec-kit
… Successfully installed specify-cli-0.0.22                              # rc=0
$ ~/tmp/082-part7/venv/bin/python -c "from importlib.metadata import version; print(version('specify-cli'))"
0.0.22

$ mkdir -p ~/tmp/082-part7/client2 && cd ~/tmp/082-part7/client2
$ ~/tmp/082-part7/venv/bin/specify init --here --ai claude --no-git --skip-tls --ignore-agent-tools
   ok Using local templates: shared copied
   ok Using local templates: .claude/skills symlink ready
Project ready.
EXIT=0

$ for p in .specify/shared/definitions/self-explanatory-definitions.md \
           .specify/shared/guidelines/self-explanatory.md \
           .specify/shared/workflow/best-practice-optimization.md; do
    test -f "$p" && echo "PRESENT $p $(wc -c <"$p") B" || echo "ABSENT  $p"
  done
PRESENT .specify/shared/definitions/self-explanatory-definitions.md 4553 B
PRESENT .specify/shared/guidelines/self-explanatory.md 6298 B
PRESENT .specify/shared/workflow/best-practice-optimization.md 4703 B

$ find .specify/shared -type f | wc -l
65
```

**Reading.** The same command, differing only in which tree the entry point was built from, produces
all three documents and the full 65-file tree. The gap between T036-a and T036-b is exactly the
release gap — so the distribution **mechanism** is proven on this tree, and "the published wheel does
not carry the documents yet" is a release fact owned by the release, not by this repository.

**Conclusion recorded for T036.** The brief's alternative reading is confirmed, not merely repeated:
`specify init` distributes the three documents once the entry point is built from a tree that carries
them. Re-running T036-a after a release that includes `e88cebc2` (or later) is the only remaining step,
and it needs no change in this repository.

T036's row is closed with no code change: both readings are transcripts above.

## Part 7 (T037/T038) — mutation legs came from a temp copy, not the repository

The leg driver and both mutation transcripts live in `notes/red-first-evidence.md` § M-5 / M-6; the
scratch root `.specify/.tmp/082-part7/` was created only after `git check-ignore -q .specify/.tmp`
succeeded, and was removed before this part's commit. No repository file was the subject of a mutation.

## T047 — 名称一致性终检 (executed 2026-11-05, implement part 9)

Two greps over the four client-facing outputs. Both name the **bracketed** form exactly as the
ratified shared string `STR-003` writes it; neither is a substring proxy for "the principle exists".

```console
$ grep -cF 'Self-Explanatory Structure (不言自明)' templates/constitution-template.md \
      templates/instructions-template.md .specify/memory/constitution.md .specify/instructions.md
templates/constitution-template.md:1
templates/instructions-template.md:1
.specify/memory/constitution.md:2
.specify/instructions.md:1
RC=0
```

Each file carries at least one occurrence (`1 / 1 / 2 / 1`). The live constitution's `2` is the body
heading **plus** this amendment's Sync Impact Report line that names the principle it added — two
surfaces of the same one name, not two names.

```console
$ grep -cF '.specify/shared/definitions/self-explanatory-definitions.md' templates/constitution-template.md \
      templates/instructions-template.md .specify/memory/constitution.md .specify/instructions.md
templates/constitution-template.md:1
templates/instructions-template.md:1
.specify/memory/constitution.md:1
.specify/instructions.md:1
RC=0
```

Each client-facing output carries the **runtime** owner pointer exactly once. The pointer is the
`.specify/` form (what a client project actually has on disk, Assumption A3), not the framework-source
`shared/definitions/...` form — those two are different readers, and only the runtime form is
client-facing.

**Variant scan (the negative half of the claim).** The brief asks only for the two greps above, but a
name check that cannot fail on a competing form proves little, so the two variant shapes
`contracts/glossary-integration.contract.md#C-34` enumerates were searched for as well:

```console
$ grep -rnE 'Self-[Ee]xplanatory [Ss]tructures' --include='*.md' templates/ \
      .specify/instructions.md .specify/memory/constitution.md .specify/templates/
(no output)  RC=1

$ grep -c '望文生义' templates/constitution-template.md templates/instructions-template.md \
      .specify/memory/constitution.md .specify/instructions.md
templates/constitution-template.md:0
templates/instructions-template.md:0
.specify/memory/constitution.md:0
.specify/instructions.md:0
RC=1
```

The plural form `Self-explanatory Structures` appears nowhere (`RC=1` = no match); every occurrence in
the four outputs is the singular bracketed form. The retired Chinese name `望文生义` is absent from all
four client-facing outputs (`0` each), so no output treats it as a current name.

**Scope note.** T047's own claim is name consistency across the four outputs, and that is what the
command output above establishes. The *third-form* assertion with its guard (`STR-001` vs `STR-003`
shared portion, `望文生义`-as-current-name) is `C-34`'s and is **T053's**, not this row's; T053 is not
started here.

## Part 9 (T044-T047) — scratch root

The C-33 red-leg driver ran from `.specify/.tmp/082-part9/`, created only after
`git check-ignore -q .specify/.tmp` matched (`.specify/.gitignore:30 .tmp/`), and removed before this
part's commit. Every leg operated on copies; the real store's sha256 is asserted unchanged in the leg
driver's isolation check.

## T049 — cost and structure final check (executed 2026-11-05, implement part 10a)

### The budget verdict, in the shape the generator actually emits it

`scripts/bash/generate-instructions.sh` computes the verdict token internally
(`"over" if size >= budget else "within"`, line 113) and **never prints that token**: both branches
branch on it and print a human sentence instead. So no `BUDGET: 33357 34816 within` line appears in
any output, and quoting one would be a fabricated transcript. The `within` verdict is carried by the
`info` line plus the positive headroom figure — the `over` branch has no counterpart (`warning` +
"over by N B" + a convergence prompt):

```console
$ bash scripts/bash/generate-instructions.sh
…
[2026-11-05 14:28:22][1886573][INFO]Section reconcile: live instructions already carry all template sections.
[2026-11-05 14:28:22][1886573][INFO]Instructions size: 33357 B (budget 34816 B, 1459 B headroom). Section table, largest first:
…
success Instructions generated/updated at .specify/instructions.md
RC=0
```

`Instructions size: … (budget 34816 B, 1459 B headroom)` — an `info` line with positive headroom and no
`warning` line = **`within`**. Cross-checked against the file on disk:

```console
$ wc -c .specify/instructions.md
33357 .specify/instructions.md

$ grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh \
      .specify/scripts/bash/generate-instructions.sh
scripts/bash/generate-instructions.sh:53:INSTRUCTIONS_BUDGET_BYTES=34816
.specify/scripts/bash/generate-instructions.sh:53:INSTRUCTIONS_BUDGET_BYTES=34816
```

`33357 < 34816` and `34816 − 33357 = 1459`, so the verdict is `within` on arithmetic the reader can
recompute. Source and mirror carry the same constant.

### The three-part record (plan T-001 / C-18)

This is the 旧值 → 新值 / 实测尺寸 / 理由 triple the task row requires. It is recorded here and in
this part's commit message; the constant's own owner is the comment above line 53 of the generator.

| part | value |
|------|-------|
| 旧值 → 新值 | `INSTRUCTIONS_BUDGET_BYTES` 32768 → **34816** (a 1024 multiple, +2048 B) |
| 本次实测尺寸 | live `.specify/instructions.md` = **33357 B** (was 32739 B before the section; the new `## Self-Explanatory Structure (不言自明)` section is 618 B) |
| 理由 | 新增 `## Self-Explanatory Structure (不言自明)` 小节（US2）使 live 文件越过旧值 32768；按 plan T-001 的「1024 的整数倍、且至少留 1024 B 余量」取最小值：34816 留下 1459 B 余量。33792 只留 435 B（< 1024 B）故不合规 — adjudicated 2026-11-05T05:52:03Z |

### The gate total, unchanged

```console
$ python3 scripts/python/scan-confirmation-gates.py --json
total= 27
by_class= {'governance_kept': 7, 'destructive': 20}
by_verdict= {'keep_gate': 27}
violations= []
RC_SCAN=0
```

`total = 27`, identical to the T002 baseline (`notes/pre-change-measurements.md` § T002) and to every
earlier part's reading — **zero new gate hits** from this feature. The `27`-vs-frozen-`23` mismatch in
`test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` is Feature 050's inherited
baseline (plan EP-003, `Decision: fallback`), not something this row introduced; the count it pins was
already 27 before part 1.

## T052 — structure final check and the Completion Gate rows (executed 2026-11-05, implement part 10a)

### `validate-tasks.py`

```console
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/082-self-explanatory-integration/tasks.md
PASS (with warnings): .specify/specs/082-self-explanatory-integration/tasks.md — 0 error(s), 34 warning(s)
RC=0
```

Exit 0. The 34 warnings are the three adjudicated classes the file already documents in
§ Adjudicated validator warnings (`green-cross-phase` / `green-clause-collision` /
`green-path-divergence`); every one is partitioned by story and none names a missing file. The warning
count moved 32 → 34 during the tasks stage's own U4 repair (`94e8c30d`), not in this part.

### GATE-1 — four guard classes green, no new failing node

`tasks.md` § Completion Gate names three suites on the command line and speaks of "four guard classes";
the fourth is the mirror-parity suite named in `plan.md` EP-004. Both readings were measured.

```console
$ python3 -m pytest tests/contract/test_constitution_double_landing.py \
      tests/contract/test_instructions_section_propagation.py \
      tests/contract/test_glossary_mechanism.py -q
.....................................                                    [100%]
37 passed in 1.81s
RC=0
```

```console
# the fourth guard class (EP-004) plus the two baseline-red-adjacent suites, name-level comparison
$ python3 -m pytest tests/contract/test_constitution_double_landing.py \
      tests/contract/test_instructions_section_propagation.py \
      tests/contract/test_glossary_mechanism.py \
      tests/contract/test_mirror_parity_suite.py \
      tests/contract/test_proactive_trigger_section.py -q --tb=no
FAILED tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
1 failed, 821 passed in 6.80s
RC=1
```

The one failure is in `baseline-failed.txt` (`grep -c` → **1**), so the name-level comparison
`comm -13 baseline-failed.txt <current-names>` has **nothing left over**: zero new failing node ids.

```console
# the four guards' own modules (each feature's new carrier) — no failure at all
$ python3 -m pytest tests/contract/test_mirror_parity_suite.py \
      tests/contract/test_self_explanatory_constitution.py \
      tests/contract/test_self_explanatory_distribution.py \
      tests/contract/test_self_explanatory_glossary.py -q
798 passed in 9.08s
RC=0
```

**GATE-1 verdict: PASS** — guard classes green, `comm -13` empty.

### GATE-2 — every `plan.md` § Mirror Obligations row verified

```console
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
RC_SYNC=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
RC_REGEN=0
```

Six `cmp` byte comparisons for the six mirrored sources the table names:

```console
$ for p in shared/definitions/self-explanatory-definitions.md shared/guidelines/self-explanatory.md \
      shared/workflow/best-practice-optimization.md templates/constitution-template.md \
      templates/instructions-template.md scripts/bash/generate-instructions.sh; do
    cmp -s "$p" ".specify/$p" && echo "IDENTICAL $p" || echo "DIFFERS   $p"; done
IDENTICAL shared/definitions/self-explanatory-definitions.md
IDENTICAL shared/guidelines/self-explanatory.md
IDENTICAL shared/workflow/best-practice-optimization.md
IDENTICAL templates/constitution-template.md
IDENTICAL templates/instructions-template.md
IDENTICAL scripts/bash/generate-instructions.sh
```

All ten rows of the table resolve: the three `shared/` rows and the two `templates/` rows and the one
`scripts/` row are the six `ok`/`IDENTICAL` pairs above (`shared` at 65 files, matching the T005 and
T031 readings); the seventh row is covered by the `shared` pair; the eighth row (unedited
`templates/commands/`) is the `regen` `OK:` line plus an empty `git diff --stat -- templates/commands/`
(`RC=0`); rows nine and ten are `not applicable` by the table's own text (`docs/` has no mirror pair,
tests are not mirrored) and judge nothing here.

**GATE-2 verdict: PASS.**

### GATE-3 — no `[ ]` / `[>]` rows remain

```console
$ grep -cE '^- \[[ >]\]' .specify/specs/082-self-explanatory-integration/tasks.md
0
```

(Before this part's row closures the same command returned 6 — T048…T053. Its output after the
closures in this commit is `0`; the command is reproduced verbatim in
`test-evidence/implement-part-10a.md` with both readings.)

**GATE-3 verdict: PASS.**

### GATE-4 — deferred to part 10b, by the part brief

GATE-4 checks `verification.md`: every `**Path**: final` criterion carrying `SC-NNN_status=pass` plus
a `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=` triple. That file does not exist yet —
it is created by the implement wrap-up, which this part MUST NOT run. GATE-4 is therefore **not run and
its result is not asserted anywhere**. Writing a `verification.md` here (or a fail-invented GATE-4 line)
would manufacture exactly the evidence the row asks a later step to produce honestly.

