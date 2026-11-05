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
