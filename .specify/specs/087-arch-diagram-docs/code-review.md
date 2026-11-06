# Code Review Report — Round 2 (087-arch-diagram-docs)

| 属性 | 值 |
|------|-----|
| **轮次** | Round 2 — review-repair 复核 |
| **基准** | `24cb4edcc53db3cfc86f574e5e6d627c78b2ca08` (`24cb4edc`) |
| **目标** | `b06c93a7678b432a2c7649a1c9df21575124a081` (`b06c93a7`) |
| **本轮增量** | `37d93787..b06c93a7`（5 个提交：4 个 review 工件提交 + 1 个修复提交） |
| **基准来源** | `feature-first-commit`（round-1 base，未变） |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-06T10:36:30Z` |
| **Round-2 evidence** | `.specify/specs/087-arch-diagram-docs/test-evidence/review-round2.txt` |

## Round 2 verdict

**Gate: `allow`.** Round-1's 2 `blocking` and 6 `important` entries are closed in substance; the only
current entries are two `suggestion`s (F26/F27 below). The gate is read by
`git-delta-review.sh report --summary --file code-review.md`: `blocking=0`, `important=0`,
`suggestion=2`, exit 0.

| Round-1 entry | Severity | Disposition |
|---------------|----------|-------------|
| `docs-utils.py:402` — suffix list misses D1/D2 faces (F5) | blocking | **closed** — `DIAGRAM_SUFFIXES` carries `.html`, `.pdf`, `.drawio`, `.excalidraw`; `test_c010_html_face_is_recognised` is on disk and red against `37d93787`'s engine |
| `docs-utils.py:656` — source-only reference reported `satisfied` (F4) | blocking | **closed** — tier 9 requires `_has_rendered_face`; `test_c007_source_only_reference_is_not_satisfied` red-then-green |
| `docs-utils.py:429` — fenced-block removal shifts line numbers (F23) | important | **closed** — `_blank_fenced_blocks` preserves line counts; `test_c005_fenced_block_does_not_shift_the_line` |
| `docs-utils.py:791` — global `--root` check changes existing actions (F21) | important | **closed** — check scoped to `obligation`; `validate --root /nonexistent` exits 0, `obligation` exits 2 |
| `docs-utils.py:520/604` — 3.9+ APIs against a 3.8 floor (F22) | important | **closed** — slice/`relative_to` forms; `removeprefix`/`is_relative_to` appear only in explanatory comments |
| `test_docs_obligation_scenarios.py:539` — SC-001 reference assertion too loose (F24) | suggestion | **closed** — the assertion resolves the link target and requires a `rendered[].path` member |
| `create-docs/SKILL.md:61-69` + `improve-docs/SKILL.md:57` — spec-local contract links (F6, two entries) | important | **closed in substance** — no `../../specs/087-.../contracts/` link remains; the schema/reason table now ships in `references/diagram-obligation.md`; the remaining dead links are F26 (suggestion) |
| `build_fixtures.py:295` — `--check` not byte-exact, unknown flags rebuild (F25) | important | **closed** — byte comparison; `--help` exits 2; the probe left `git status` empty |

### 🟢 [SUGGESTION] skills/external/create-docs/SKILL.md (Line 61)

> Two spec-local links remain in the shipped skill: [`contracts/diagram-obligation.contract.md`](contracts/diagram-obligation.contract.md) at line 61 and [`quickstart.md`](quickstart.md) at line 75; `skills/external/improve-docs/SKILL.md:119` also cites `quickstart.md` S3. Neither resolves in a client project (the skill ships as `.specify/skills/create-docs/`). The primary F6 harm is fixed — the record schema, verdict/reason table and exemption schema now live in the shipped reference — so this is a suggestion, not a repeat of the important entry. Line 61 is also pinned by `test_c007_baseline_single_owner`, so removing it needs a test change. Fix: cite the contract by its framework-repository path in prose and replace the `quickstart.md` links with `references/diagram-obligation.md` pointers. (F26)

<sub>10:36:30</sub>

### 🟢 [SUGGESTION] skills/external/create-docs/references/diagram-obligation.md (Line 3)

> Dual ownership: the spec contract (`contracts/diagram-obligation.contract.md:4-10`) declares itself owner of the closed verdict/reason sets, the precedence and the two record schemas; the shipped reference (`references/diagram-obligation.md:3-6`) declares itself owner of "the two record formats and the verdict vocabulary". The precedence tables differ in granularity (contract `C-016` 9 rows; reference § 7 8 rows, two pairs merged), and the reference header says "six-value verdict set" while § 4 lists five. The two copies currently agree on the five verdicts and reason pairs, so this is a drift risk rather than a live wrong reading. Fix: demote the contract to the dated design record (or point its vocabulary at the shipped reference), align the precedence table, and correct the "six-value" sentence. (F27)

<sub>10:36:30</sub>

**Round-2 scope note.** The delta `37d93787..b06c93a7` contains 32 paths: the 7 code/test files re-judged
above, spec artifacts and review evidence, generated mirrors, and one fixture record. The round-1
coverage receipt (177 changed / 11 judged / 166 skipped / 0 gap at head `37d93787`) remains the dated
coverage record; this round did not re-run a receipt over the full feature delta and does not restate
its four counts. No full test suite was run; the targeted readings are in `test-evidence/review-round2.txt`.

---

# Round 1 code record — dated record (head 37d93787, 2026-11-06)

> Preserved as the round-1 record. Its seven finding headings are demoted to `####` and marked
> `resolved` so the round-2 gate reads only the current entries; the opinion bodies are unchanged.

# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `line/087-arch-diagram-docs` |
| **基准** | `24cb4edcc53db3cfc86f574e5e6d627c78b2ca08` (`24cb4edc`) |
| **目标** | `37d937872613f97c5141bfb36e8bbc17e678dd1c` (`37d93787`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-06T10:04:29Z` |

## 变更概览

```
 .claude/commands/speckit.docs.md                   |    3 +-
 .github/prompts/speckit.docs.prompt.md             |    3 +-
 .opencode/command/speckit.docs.md                  |    3 +-
 .qoder/commands/speckit.docs.md                    |    3 +-
 .specify/memory/features.md                        |    3 +-
 .specify/memory/features/087.md                    |   70 ++
 .specify/memory/register.md                        |    3 +
 .specify/skills/create-docs/SKILL.md               |   35 +-
 .specify/skills/create-docs/scripts/docs-utils.py  |  386 ++++++-
 .specify/skills/improve-docs/SKILL.md              |   14 +
 .../087-arch-diagram-docs/baseline-failed.txt      |   26 +
 .../checklists/requirements-quality.md             |  175 +++
 .../checklists/requirements.md                     |   53 +
 .../checkpoints/01-requirements.md                 |   44 +
 .../checkpoints/02-clarify.md                      |   47 +
 .../087-arch-diagram-docs/checkpoints/03-plan.md   |   55 +
 .../087-arch-diagram-docs/checkpoints/04-tasks.md  |   47 +
 .../checkpoints/05-checklist.md                    |   44 +
 .../checkpoints/06-analyze.md                      |   49 +
 .../checkpoints/07-implement.md                    |   45 +
 .../contracts/diagram-obligation.contract.md       |  363 +++++++
 .../contracts/flow-obligations.contract.md         |  142 +++
 .../087-arch-diagram-docs/coverage-baseline.txt    |  575 ++++++++++
 .specify/specs/087-arch-diagram-docs/data-model.md |  190 ++++
 .../specs/087-arch-diagram-docs/feature-ref.md     |   77 ++
 .../goal/087-arch-diagram-docs/goal.md             |   28 +
 .../notes/pre-change-measurements.md               |  218 ++++
 .../087-arch-diagram-docs/notes/quickstart-run.md  |  338 ++++++
 .../notes/red-first-evidence.md                    |  424 ++++++++
 .specify/specs/087-arch-diagram-docs/plan.md       |  577 ++++++++++
 .specify/specs/087-arch-diagram-docs/quickstart.md |  333 ++++++
 .../specs/087-arch-diagram-docs/requirements.md    |  313 ++++++
 .specify/specs/087-arch-diagram-docs/research.md   |  164 +++
 .specify/specs/087-arch-diagram-docs/tasks.md      |  334 ++++++
 .../team/087-arch-diagram-docs/team.md             |  177 ++++
 .../test-evidence/analyze-repair-round1.md         |  169 +++
 .../test-evidence/analyze-report-round1.md         |   56 +
 .../test-evidence/analyze-stage-status.jsonl       |    1 +
 .../test-evidence/checklist-stage-status.jsonl     |    1 +
 .../test-evidence/clarify-stage-status.jsonl       |    1 +
 .../test-evidence/coverage-baseline-pointer.txt    |   25 +
 .../test-evidence/implement-part1.txt              |  156 +++
 .../test-evidence/implement-part2.txt              |  188 ++++
 .../test-evidence/implement-part3.txt              |   92 ++
 .../test-evidence/implement-part4.txt              |  123 +++
 .../test-evidence/implement-part5.txt              |  122 +++
 .../test-evidence/implement-stage-status.jsonl     |    1 +
 .../test-evidence/plan-stage-status.jsonl          |    1 +
 .../test-evidence/plan-stage-status.md             |  121 +++
 .../test-evidence/plan-verifier-attempt1.md        |   41 +
 .../test-evidence/plan-verifier-attempt2.md        |   33 +
 .../test-evidence/plan-verifier-attempt3.md        |   34 +
 .../test-evidence/requirements-loop-state.json     |  192 ++++
 .../test-evidence/tasks-stage-status.jsonl         |    1 +
 docs/concepts/documentation-model.md               |   17 +
 skills/external/create-docs/SKILL.md               |   35 +-
 skills/external/create-docs/scripts/docs-utils.py  |  386 ++++++-
 skills/external/improve-docs/SKILL.md              |   14 +
 templates/commands/docs.md                         |    3 +-
 tests/contract/test_expression_compatibility.py    |   20 +
 tests/fixtures/docs-obligation/build_fixtures.py   |  299 ++++++
 tests/fixtures/docs-obligation/clean/README.md     |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../docs-obligation/clean/docs/assets/widget.mmd   |    3 +
 .../docs-obligation/clean/docs/assets/widget.png   |    1 +
 .../docs-obligation/clean/docs/assets/widget.svg   |    3 +
 .../clean/docs/concepts/widget-overview.md         |   10 +
 .../docs-obligation/clean/docs/contribute/index.md |    3 +
 .../docs-obligation/clean/docs/decisions/index.md  |    3 +
 .../docs-obligation/clean/docs/reference/index.md  |    3 +
 .../docs-obligation/clean/docs/tasks/index.md      |    3 +
 .../docs-obligation/clean/docs/tutorials/index.md  |    3 +
 tests/fixtures/docs-obligation/conftest.py         |   95 ++
 .../docs-obligation/deleted-rendered/README.md     |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../deleted-rendered/docs/assets/widget.mmd        |    3 +
 .../docs/concepts/widget-overview.md               |   10 +
 .../deleted-rendered/docs/contribute/index.md      |    3 +
 .../deleted-rendered/docs/decisions/index.md       |    3 +
 .../deleted-rendered/docs/reference/index.md       |    3 +
 .../deleted-rendered/docs/tasks/index.md           |    3 +
 .../deleted-rendered/docs/tutorials/index.md       |    3 +
 .../fixtures/docs-obligation/exempt-bad/README.md  |    3 +
 .../exemptions/concepts/widget-overview.md         |    7 +
 .../exempt-bad/docs/concepts/widget-overview.md    |    8 +
 .../exempt-bad/docs/contribute/index.md            |    3 +
 .../exempt-bad/docs/decisions/index.md             |    3 +
 .../exempt-bad/docs/reference/index.md             |    3 +
 .../docs-obligation/exempt-bad/docs/tasks/index.md |    3 +
 .../exempt-bad/docs/tutorials/index.md             |    3 +
 tests/fixtures/docs-obligation/exempt-ok/README.md |    3 +
 .../exemptions/concepts/widget-overview.md         |    8 +
 .../exempt-ok/docs/concepts/widget-overview.md     |    8 +
 .../exempt-ok/docs/contribute/index.md             |    3 +
 .../exempt-ok/docs/decisions/index.md              |    3 +
 .../exempt-ok/docs/reference/index.md              |    3 +
 .../docs-obligation/exempt-ok/docs/tasks/index.md  |    3 +
 .../exempt-ok/docs/tutorials/index.md              |    3 +
 .../docs-obligation/exempt-superseded/README.md    |    3 +
 .../exemptions/concepts/widget-overview.md         |    8 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../exempt-superseded/docs/assets/widget.mmd       |    3 +
 .../exempt-superseded/docs/assets/widget.png       |    1 +
 .../exempt-superseded/docs/assets/widget.svg       |    3 +
 .../docs/concepts/widget-overview.md               |   10 +
 .../exempt-superseded/docs/contribute/index.md     |    3 +
 .../exempt-superseded/docs/decisions/index.md      |    3 +
 .../exempt-superseded/docs/reference/index.md      |    3 +
 .../exempt-superseded/docs/tasks/index.md          |    3 +
 .../exempt-superseded/docs/tutorials/index.md      |    3 +
 .../fixtures/docs-obligation/no-diagram/README.md  |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../no-diagram/docs/assets/widget.mmd              |    3 +
 .../no-diagram/docs/assets/widget.png              |    1 +
 .../no-diagram/docs/assets/widget.svg              |    3 +
 .../no-diagram/docs/concepts/widget-overview.md    |    8 +
 .../no-diagram/docs/contribute/index.md            |    3 +
 .../no-diagram/docs/decisions/index.md             |    3 +
 .../no-diagram/docs/reference/index.md             |    3 +
 .../docs-obligation/no-diagram/docs/tasks/index.md |    3 +
 .../no-diagram/docs/tutorials/index.md             |    3 +
 tests/fixtures/docs-obligation/no-trace/README.md  |    3 +
 .../no-trace/docs/assets/widget.mmd                |    3 +
 .../no-trace/docs/assets/widget.png                |    1 +
 .../no-trace/docs/assets/widget.svg                |    3 +
 .../no-trace/docs/concepts/widget-overview.md      |   10 +
 .../no-trace/docs/contribute/index.md              |    3 +
 .../no-trace/docs/decisions/index.md               |    3 +
 .../no-trace/docs/reference/index.md               |    3 +
 .../docs-obligation/no-trace/docs/tasks/index.md   |    3 +
 .../no-trace/docs/tutorials/index.md               |    3 +
 .../docs-obligation/orphan-rendered/README.md      |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   22 +
 .../orphan-rendered/docs/assets/widget.mmd         |    3 +
 .../docs/concepts/widget-overview.md               |   10 +
 .../orphan-rendered/docs/contribute/index.md       |    3 +
 .../orphan-rendered/docs/decisions/index.md        |    3 +
 .../orphan-rendered/docs/reference/index.md        |    3 +
 .../orphan-rendered/docs/tasks/index.md            |    3 +
 .../orphan-rendered/docs/tutorials/index.md        |    3 +
 .../docs-obligation/orphan-source/README.md        |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../orphan-source/docs/assets/widget.png           |    1 +
 .../orphan-source/docs/assets/widget.svg           |    3 +
 .../orphan-source/docs/concepts/widget-overview.md |   10 +
 .../orphan-source/docs/contribute/index.md         |    3 +
 .../orphan-source/docs/decisions/index.md          |    3 +
 .../orphan-source/docs/reference/index.md          |    3 +
 .../orphan-source/docs/tasks/index.md              |    3 +
 .../orphan-source/docs/tutorials/index.md          |    3 +
 .../docs-obligation/stale-source/README.md         |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   27 +
 .../stale-source/docs/assets/widget.mmd            |    3 +
 .../stale-source/docs/assets/widget.png            |    1 +
 .../stale-source/docs/assets/widget.svg            |    3 +
 .../stale-source/docs/concepts/widget-overview.md  |   10 +
 .../stale-source/docs/contribute/index.md          |    3 +
 .../stale-source/docs/decisions/index.md           |    3 +
 .../stale-source/docs/reference/index.md           |    3 +
 .../stale-source/docs/tasks/index.md               |    3 +
 .../stale-source/docs/tutorials/index.md           |    3 +
 .../docs-obligation/trace-incomplete/README.md     |    3 +
 .../20261106T090000Z-0870a1b2-diagram-trace.json   |   22 +
 .../trace-incomplete/docs/assets/widget.mmd        |    3 +
 .../trace-incomplete/docs/assets/widget.png        |    1 +
 .../trace-incomplete/docs/assets/widget.svg        |    3 +
 .../docs/concepts/widget-overview.md               |   10 +
 .../trace-incomplete/docs/contribute/index.md      |    3 +
 .../trace-incomplete/docs/decisions/index.md       |    3 +
 .../trace-incomplete/docs/reference/index.md       |    3 +
 .../trace-incomplete/docs/tasks/index.md           |    3 +
 .../trace-incomplete/docs/tutorials/index.md       |    3 +
 tests/integration/test_docs_command_scenarios.py   |  847 +++++++++++++++
 .../integration/test_docs_obligation_scenarios.py  |  990 +++++++++++++++++
 tests/unit/test_docs_obligation_reuse.py           |  473 +++++++++
 tests/unit/test_docs_utils_carriers.py             |  121 +++
 tests/unit/test_docs_utils_obligation.py           | 1118 ++++++++++++++++++++
 177 files changed, 11696 insertions(+), 24 deletions(-)
```

---

## Review 意见


#### R1 [BLOCKING — resolved in b06c93a7] skills/external/create-docs/scripts/docs-utils.py (Line 402)

> The recognisable-diagram suffix list is a second, incomplete copy of draw-diagram's delivery table. DIAGRAM_SUFFIXES omits the D1-mandatory .html face and the D2 .drawio/.excalidraw sources and .pdf render; a conformant document that links widget.html, widget.drawio or widget.pdf is judged missing/no-diagram-reference. Probes on copies of tests/fixtures/docs-obligation/clean/ reproduced all three false reds. Fix: derive the suffix set from skills/external/draw-diagram/references/delivery-contract.md (or add .html/.pdf/.drawio/.excalidraw) and add fixtures.

<sub>18:06:25</sub>


#### R1 [BLOCKING — resolved in b06c93a7] skills/external/create-docs/scripts/docs-utils.py (Line 656)

> Tier 9 returns satisfied when the document's only reference points at the editable SOURCE (widget.mmd) and both faces exist. C-007 condition 2 requires the reference target to be a rendered[].path. Probe: clean/ copy, document changed from ../assets/widget.svg to ../assets/widget.mmd, engine returns satisfied/reference-resolves. The SC-001 assertion (tests/integration/test_docs_obligation_scenarios.py:539) only checks '../assets/' and '](', so it cannot catch this. Fix: require the resolved target to be one of the entry's rendered[].path before tier 9, and add a negative fixture.

<sub>18:06:25</sub>


#### R1 [IMPORTANT — resolved in b06c93a7] skills/external/create-docs/scripts/docs-utils.py (Line 429)

> Fenced-code removal uses re.sub(r'\`\`\`.*?\`\`\`', '', text, flags=re.S), which deletes the block's newlines and shifts every later line number. A document with a 5-line fenced block before its diagram link (link on line 9) reports line=5. C-005 requires line to be the reference's line. Fix: replace each fenced block with the same number of newlines (or blank lines) so line numbering is preserved.

<sub>18:06:25</sub>


#### R1 [IMPORTANT — resolved in b06c93a7] skills/external/create-docs/scripts/docs-utils.py (Line 791)

> The new global 'if args.action != obligation and not root.is_dir(): return 2' changes every existing action's behaviour on a missing root. Base 24cb4edc: validate/scan/stats exited 0 with an empty JSON payload; new: exit 2. C-015 says validate's exit-code semantics are unchanged, and no task row asks for this change. Fix: scope the check to obligation (as the branch already does) or record and test the behaviour change explicitly.

<sub>18:06:25</sub>


#### R1 [IMPORTANT — resolved in b06c93a7] skills/external/create-docs/scripts/docs-utils.py (Line 520)

> str.removeprefix (line 520) and Path.is_relative_to (line 604) are Python 3.9+ APIs. pyproject.toml declares requires-python >=3.8 and RS-001 promises the new scripts/tests run on >=3.8; on a 3.8 interpreter the new action raises AttributeError. Fix: use startswith/slicing and a try/relative_to or string-prefix check, or raise the declared floor and record the change.

<sub>18:06:25</sub>


#### R1 [SUGGESTION — resolved in b06c93a7] tests/integration/test_docs_obligation_scenarios.py (Line 539)

> SC-001's 'reference' assertion accepts any '../assets/' link (it never checks the target is a rendered face). It would pass a document that links widget.mmd, which is the behaviour the second blocking finding describes. Tighten the assertion to the trace record's rendered[].path(s).

<sub>18:06:25</sub>




#### R1 [IMPORTANT — resolved in b06c93a7] skills/external/create-docs/SKILL.md (Line 61)

> The shipped skill links the obligation to ../../specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md (lines 61-63, 69). The runtime mirror is .specify/skills/create-docs/SKILL.md, so that relative link resolves to .specify/specs/087-arch-diagram-docs/... — the authoring repository's development spec, which no client project receives. In a consuming project the trace-record schema, carrier table and exemption schema the skill names are unreachable (dead link), and the skill cannot be followed by the book. Fix: move the normative schema/table to a shipped reference under skills/external/create-docs/references/ (or inline the record schema in the skill) and keep the spec contract as the dated record.

<sub>18:06:49</sub>


#### R1 [IMPORTANT — resolved in b06c93a7] skills/external/improve-docs/SKILL.md (Line 57)

> Same portability defect as the create-docs pointer: the content-improvement flow sends a client reader to ../../specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md for the verdict vocabulary and reason table, but the shipped mirror is .specify/skills/improve-docs/SKILL.md and the linked spec is not part of any client runtime. The skill quotes none of the vocabulary, so the client has no reachable owner. Fix: cite a shipped reference (or the checker's own --help/payload) rather than the authoring spec.

<sub>18:06:49</sub>




#### R1 [IMPORTANT — resolved in b06c93a7] tests/fixtures/docs-obligation/build_fixtures.py (Line 295)

> The builder's __main__ treats every argument except --check as 'rebuild': a plain '--help' invocation ran build_all() and rewrote tests/fixtures/docs-obligation/orphan-rendered/.../20261106T090000Z-0870a1b2-diagram-trace.json (added the PNG face and two sha256 values). check() only verifies path presence/absence, so it still printed OK — the 'repository copy == registered composition' invariant does not cover record bytes. This review's accidental run changed that file and it was restored to HEAD before this record was refreshed; the defect remains. Fix: make check() byte-compare each fixture against the builder's deterministic output (or a committed hash manifest), and make unknown flags exit 2 instead of rebuilding.

<sub>18:10:45</sub>




> **未提交范围（未评审）**: 38 个未提交路径未计入本次评审对象（.specify/memory/session/20261105T033022Z-run-determination-speckit-plan-r20261105t033022z-e4a7.md, .specify/memory/session/20261105T034532Z-run-determination-speckit-clarify-r20261105t033420z-082a.md, .specify/memory/session/20261105T041200Z-run-determination-speckit-plan-r20261105t033420z-082a.md, .specify/memory/session/20261105T080146Z-run-determination-speckit-clarify-r20261105t074027z-084a.md, .specify/memory/session/20261105T082004Z-run-determination-speckit-plan-r20261105t074027z-084a.md, .specify/specs/087-arch-diagram-docs/review.md, .specify/memory/exec-quant/records/20261106T062113898880Z-a68a0a47.json, .specify/memory/exec-quant/records/20261106T062441209619Z-e4551090.json, .specify/memory/exec-quant/records/20261106T063211225381Z-2a39a615.json, .specify/memory/exec-quant/records/20261106T065148971561Z-fc6d0104.json, .specify/memory/exec-quant/records/20261106T071003204813Z-7fd2cdda.json, .specify/memory/exec-quant/records/20261106T071931265894Z-116ca453.json, .specify/memory/exec-quant/records/20261106T073734709560Z-15db8345.json, .specify/memory/exec-quant/records/20261106T074249931669Z-675f14de.json, .specify/memory/exec-quant/records/20261106T075307371543Z-8a090e14.json, .specify/memory/exec-quant/records/20261106T093826265649Z-d6ce4f86.json, .specify/memory/feedback/20261106T062117Z-speckit-requirements.md, .specify/memory/feedback/20261106T062127Z-speckit-requirements.md, .specify/memory/feedback/20261106T062443Z-skill-create-requirements.md, .specify/memory/feedback/20261106T062511Z-skill-create-requirements.md, .specify/memory/feedback/20261106T063214Z-speckit-clarify.md, .specify/memory/feedback/20261106T065222Z-speckit-plan.md, .specify/memory/feedback/20261106T071005Z-speckit-plan.md, .specify/memory/feedback/20261106T071933Z-speckit-plan.md, .specify/memory/feedback/20261106T073737Z-speckit-tasks.md, .specify/memory/feedback/20261106T073834Z-speckit-tasks.md, .specify/memory/feedback/20261106T074249Z-speckit-checklist.md, .specify/memory/feedback/20261106T074439Z-speckit-checklist.md, .specify/memory/feedback/20261106T075313Z-speckit-analyze.md, .specify/memory/feedback/20261106T093856Z-speckit-implement.md, .specify/memory/feedback/20261106T093919Z-speckit-implement.md, .specify/memory/session/20261106T062111Z-run-determination-speckit-requirements-087-req-20261106t0621.md, .specify/memory/session/20261106T063159Z-run-determination-speckit-clarify-clarify-087-20261106t0632z.md, .specify/memory/session/20261106T063208Z-run-determination-speckit-clarify-clarify-087-20261106t0632z.md, .specify/memory/session/20261106T065146Z-run-determination-speckit-plan-plan-087-20261106t0640z.md, .specify/memory/session/20261106T093805Z-run-determination-speckit-implement-r20261106t093725z-087e.md, .specify/memory/session/20261106T093813Z-run-determination-speckit-implement-r20261106t093905z-087e.md, .specify/memory/session/20261106T093821Z-run-determination-speckit-implement-r20261106t093940z-087e.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=24cb4edcc53db3cfc86f574e5e6d627c78b2ca08
head=37d937872613f97c5141bfb36e8bbc17e678dd1c
base_source=feature-first-commit
renderer=text
changed_files=177
judged_files=11
skipped_files=166
gap_files=0
lines_added=11696
lines_deleted=24
file.001.path=.claude/commands/speckit.docs.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.github/prompts/speckit.docs.prompt.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.opencode/command/speckit.docs.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.qoder/commands/speckit.docs.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/memory/features.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/memory/features/087.md
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/memory/register.md
file.007.verdict=skipped
file.007.reason=non-code-file
file.008.path=.specify/skills/create-docs/SKILL.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.specify/skills/create-docs/scripts/docs-utils.py
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.specify/skills/improve-docs/SKILL.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/specs/087-arch-diagram-docs/baseline-failed.txt
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/specs/087-arch-diagram-docs/checklists/requirements-quality.md
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/specs/087-arch-diagram-docs/checklists/requirements.md
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/specs/087-arch-diagram-docs/checkpoints/01-requirements.md
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/specs/087-arch-diagram-docs/checkpoints/02-clarify.md
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/specs/087-arch-diagram-docs/checkpoints/03-plan.md
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/specs/087-arch-diagram-docs/checkpoints/04-tasks.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/specs/087-arch-diagram-docs/checkpoints/05-checklist.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/specs/087-arch-diagram-docs/checkpoints/06-analyze.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/specs/087-arch-diagram-docs/checkpoints/07-implement.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/specs/087-arch-diagram-docs/contracts/flow-obligations.contract.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/specs/087-arch-diagram-docs/coverage-baseline.txt
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/specs/087-arch-diagram-docs/data-model.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/specs/087-arch-diagram-docs/feature-ref.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/specs/087-arch-diagram-docs/notes/pre-change-measurements.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/specs/087-arch-diagram-docs/notes/quickstart-run.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/specs/087-arch-diagram-docs/notes/red-first-evidence.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/specs/087-arch-diagram-docs/plan.md
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/specs/087-arch-diagram-docs/quickstart.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/specs/087-arch-diagram-docs/requirements.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/specs/087-arch-diagram-docs/research.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/specs/087-arch-diagram-docs/tasks.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/specs/087-arch-diagram-docs/team/087-arch-diagram-docs/team.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/specs/087-arch-diagram-docs/test-evidence/analyze-repair-round1.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/specs/087-arch-diagram-docs/test-evidence/analyze-report-round1.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/087-arch-diagram-docs/test-evidence/analyze-stage-status.jsonl
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/087-arch-diagram-docs/test-evidence/checklist-stage-status.jsonl
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/087-arch-diagram-docs/test-evidence/clarify-stage-status.jsonl
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/087-arch-diagram-docs/test-evidence/coverage-baseline-pointer.txt
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-part1.txt
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-part2.txt
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-part3.txt
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-part4.txt
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-part5.txt
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/087-arch-diagram-docs/test-evidence/implement-stage-status.jsonl
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/087-arch-diagram-docs/test-evidence/plan-stage-status.jsonl
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/087-arch-diagram-docs/test-evidence/plan-stage-status.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/087-arch-diagram-docs/test-evidence/plan-verifier-attempt1.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/087-arch-diagram-docs/test-evidence/plan-verifier-attempt2.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/087-arch-diagram-docs/test-evidence/plan-verifier-attempt3.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/087-arch-diagram-docs/test-evidence/requirements-loop-state.json
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/087-arch-diagram-docs/test-evidence/tasks-stage-status.jsonl
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=docs/concepts/documentation-model.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=skills/external/create-docs/SKILL.md
file.056.verdict=reviewed
file.057.path=skills/external/create-docs/scripts/docs-utils.py
file.057.verdict=reviewed
file.058.path=skills/external/improve-docs/SKILL.md
file.058.verdict=reviewed
file.059.path=templates/commands/docs.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=tests/contract/test_expression_compatibility.py
file.060.verdict=reviewed
file.061.path=tests/fixtures/docs-obligation/build_fixtures.py
file.061.verdict=reviewed
file.062.path=tests/fixtures/docs-obligation/clean/README.md
file.062.verdict=skipped
file.062.reason=generated
file.063.path=tests/fixtures/docs-obligation/clean/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.063.verdict=skipped
file.063.reason=generated
file.064.path=tests/fixtures/docs-obligation/clean/docs/assets/widget.mmd
file.064.verdict=skipped
file.064.reason=generated
file.065.path=tests/fixtures/docs-obligation/clean/docs/assets/widget.png
file.065.verdict=skipped
file.065.reason=generated
file.066.path=tests/fixtures/docs-obligation/clean/docs/assets/widget.svg
file.066.verdict=skipped
file.066.reason=generated
file.067.path=tests/fixtures/docs-obligation/clean/docs/concepts/widget-overview.md
file.067.verdict=skipped
file.067.reason=generated
file.068.path=tests/fixtures/docs-obligation/clean/docs/contribute/index.md
file.068.verdict=skipped
file.068.reason=generated
file.069.path=tests/fixtures/docs-obligation/clean/docs/decisions/index.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=tests/fixtures/docs-obligation/clean/docs/reference/index.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=tests/fixtures/docs-obligation/clean/docs/tasks/index.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=tests/fixtures/docs-obligation/clean/docs/tutorials/index.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=tests/fixtures/docs-obligation/conftest.py
file.073.verdict=reviewed
file.074.path=tests/fixtures/docs-obligation/deleted-rendered/README.md
file.074.verdict=skipped
file.074.reason=generated
file.075.path=tests/fixtures/docs-obligation/deleted-rendered/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.075.verdict=skipped
file.075.reason=generated
file.076.path=tests/fixtures/docs-obligation/deleted-rendered/docs/assets/widget.mmd
file.076.verdict=skipped
file.076.reason=generated
file.077.path=tests/fixtures/docs-obligation/deleted-rendered/docs/concepts/widget-overview.md
file.077.verdict=skipped
file.077.reason=generated
file.078.path=tests/fixtures/docs-obligation/deleted-rendered/docs/contribute/index.md
file.078.verdict=skipped
file.078.reason=generated
file.079.path=tests/fixtures/docs-obligation/deleted-rendered/docs/decisions/index.md
file.079.verdict=skipped
file.079.reason=generated
file.080.path=tests/fixtures/docs-obligation/deleted-rendered/docs/reference/index.md
file.080.verdict=skipped
file.080.reason=generated
file.081.path=tests/fixtures/docs-obligation/deleted-rendered/docs/tasks/index.md
file.081.verdict=skipped
file.081.reason=generated
file.082.path=tests/fixtures/docs-obligation/deleted-rendered/docs/tutorials/index.md
file.082.verdict=skipped
file.082.reason=generated
file.083.path=tests/fixtures/docs-obligation/exempt-bad/README.md
file.083.verdict=skipped
file.083.reason=generated
file.084.path=tests/fixtures/docs-obligation/exempt-bad/docs/.speckit/exemptions/concepts/widget-overview.md
file.084.verdict=skipped
file.084.reason=generated
file.085.path=tests/fixtures/docs-obligation/exempt-bad/docs/concepts/widget-overview.md
file.085.verdict=skipped
file.085.reason=generated
file.086.path=tests/fixtures/docs-obligation/exempt-bad/docs/contribute/index.md
file.086.verdict=skipped
file.086.reason=generated
file.087.path=tests/fixtures/docs-obligation/exempt-bad/docs/decisions/index.md
file.087.verdict=skipped
file.087.reason=generated
file.088.path=tests/fixtures/docs-obligation/exempt-bad/docs/reference/index.md
file.088.verdict=skipped
file.088.reason=generated
file.089.path=tests/fixtures/docs-obligation/exempt-bad/docs/tasks/index.md
file.089.verdict=skipped
file.089.reason=generated
file.090.path=tests/fixtures/docs-obligation/exempt-bad/docs/tutorials/index.md
file.090.verdict=skipped
file.090.reason=generated
file.091.path=tests/fixtures/docs-obligation/exempt-ok/README.md
file.091.verdict=skipped
file.091.reason=generated
file.092.path=tests/fixtures/docs-obligation/exempt-ok/docs/.speckit/exemptions/concepts/widget-overview.md
file.092.verdict=skipped
file.092.reason=generated
file.093.path=tests/fixtures/docs-obligation/exempt-ok/docs/concepts/widget-overview.md
file.093.verdict=skipped
file.093.reason=generated
file.094.path=tests/fixtures/docs-obligation/exempt-ok/docs/contribute/index.md
file.094.verdict=skipped
file.094.reason=generated
file.095.path=tests/fixtures/docs-obligation/exempt-ok/docs/decisions/index.md
file.095.verdict=skipped
file.095.reason=generated
file.096.path=tests/fixtures/docs-obligation/exempt-ok/docs/reference/index.md
file.096.verdict=skipped
file.096.reason=generated
file.097.path=tests/fixtures/docs-obligation/exempt-ok/docs/tasks/index.md
file.097.verdict=skipped
file.097.reason=generated
file.098.path=tests/fixtures/docs-obligation/exempt-ok/docs/tutorials/index.md
file.098.verdict=skipped
file.098.reason=generated
file.099.path=tests/fixtures/docs-obligation/exempt-superseded/README.md
file.099.verdict=skipped
file.099.reason=generated
file.100.path=tests/fixtures/docs-obligation/exempt-superseded/docs/.speckit/exemptions/concepts/widget-overview.md
file.100.verdict=skipped
file.100.reason=generated
file.101.path=tests/fixtures/docs-obligation/exempt-superseded/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.101.verdict=skipped
file.101.reason=generated
file.102.path=tests/fixtures/docs-obligation/exempt-superseded/docs/assets/widget.mmd
file.102.verdict=skipped
file.102.reason=generated
file.103.path=tests/fixtures/docs-obligation/exempt-superseded/docs/assets/widget.png
file.103.verdict=skipped
file.103.reason=generated
file.104.path=tests/fixtures/docs-obligation/exempt-superseded/docs/assets/widget.svg
file.104.verdict=skipped
file.104.reason=generated
file.105.path=tests/fixtures/docs-obligation/exempt-superseded/docs/concepts/widget-overview.md
file.105.verdict=skipped
file.105.reason=generated
file.106.path=tests/fixtures/docs-obligation/exempt-superseded/docs/contribute/index.md
file.106.verdict=skipped
file.106.reason=generated
file.107.path=tests/fixtures/docs-obligation/exempt-superseded/docs/decisions/index.md
file.107.verdict=skipped
file.107.reason=generated
file.108.path=tests/fixtures/docs-obligation/exempt-superseded/docs/reference/index.md
file.108.verdict=skipped
file.108.reason=generated
file.109.path=tests/fixtures/docs-obligation/exempt-superseded/docs/tasks/index.md
file.109.verdict=skipped
file.109.reason=generated
file.110.path=tests/fixtures/docs-obligation/exempt-superseded/docs/tutorials/index.md
file.110.verdict=skipped
file.110.reason=generated
file.111.path=tests/fixtures/docs-obligation/no-diagram/README.md
file.111.verdict=skipped
file.111.reason=generated
file.112.path=tests/fixtures/docs-obligation/no-diagram/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.112.verdict=skipped
file.112.reason=generated
file.113.path=tests/fixtures/docs-obligation/no-diagram/docs/assets/widget.mmd
file.113.verdict=skipped
file.113.reason=generated
file.114.path=tests/fixtures/docs-obligation/no-diagram/docs/assets/widget.png
file.114.verdict=skipped
file.114.reason=generated
file.115.path=tests/fixtures/docs-obligation/no-diagram/docs/assets/widget.svg
file.115.verdict=skipped
file.115.reason=generated
file.116.path=tests/fixtures/docs-obligation/no-diagram/docs/concepts/widget-overview.md
file.116.verdict=skipped
file.116.reason=generated
file.117.path=tests/fixtures/docs-obligation/no-diagram/docs/contribute/index.md
file.117.verdict=skipped
file.117.reason=generated
file.118.path=tests/fixtures/docs-obligation/no-diagram/docs/decisions/index.md
file.118.verdict=skipped
file.118.reason=generated
file.119.path=tests/fixtures/docs-obligation/no-diagram/docs/reference/index.md
file.119.verdict=skipped
file.119.reason=generated
file.120.path=tests/fixtures/docs-obligation/no-diagram/docs/tasks/index.md
file.120.verdict=skipped
file.120.reason=generated
file.121.path=tests/fixtures/docs-obligation/no-diagram/docs/tutorials/index.md
file.121.verdict=skipped
file.121.reason=generated
file.122.path=tests/fixtures/docs-obligation/no-trace/README.md
file.122.verdict=skipped
file.122.reason=generated
file.123.path=tests/fixtures/docs-obligation/no-trace/docs/assets/widget.mmd
file.123.verdict=skipped
file.123.reason=generated
file.124.path=tests/fixtures/docs-obligation/no-trace/docs/assets/widget.png
file.124.verdict=skipped
file.124.reason=generated
file.125.path=tests/fixtures/docs-obligation/no-trace/docs/assets/widget.svg
file.125.verdict=skipped
file.125.reason=generated
file.126.path=tests/fixtures/docs-obligation/no-trace/docs/concepts/widget-overview.md
file.126.verdict=skipped
file.126.reason=generated
file.127.path=tests/fixtures/docs-obligation/no-trace/docs/contribute/index.md
file.127.verdict=skipped
file.127.reason=generated
file.128.path=tests/fixtures/docs-obligation/no-trace/docs/decisions/index.md
file.128.verdict=skipped
file.128.reason=generated
file.129.path=tests/fixtures/docs-obligation/no-trace/docs/reference/index.md
file.129.verdict=skipped
file.129.reason=generated
file.130.path=tests/fixtures/docs-obligation/no-trace/docs/tasks/index.md
file.130.verdict=skipped
file.130.reason=generated
file.131.path=tests/fixtures/docs-obligation/no-trace/docs/tutorials/index.md
file.131.verdict=skipped
file.131.reason=generated
file.132.path=tests/fixtures/docs-obligation/orphan-rendered/README.md
file.132.verdict=skipped
file.132.reason=generated
file.133.path=tests/fixtures/docs-obligation/orphan-rendered/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.133.verdict=skipped
file.133.reason=generated
file.134.path=tests/fixtures/docs-obligation/orphan-rendered/docs/assets/widget.mmd
file.134.verdict=skipped
file.134.reason=generated
file.135.path=tests/fixtures/docs-obligation/orphan-rendered/docs/concepts/widget-overview.md
file.135.verdict=skipped
file.135.reason=generated
file.136.path=tests/fixtures/docs-obligation/orphan-rendered/docs/contribute/index.md
file.136.verdict=skipped
file.136.reason=generated
file.137.path=tests/fixtures/docs-obligation/orphan-rendered/docs/decisions/index.md
file.137.verdict=skipped
file.137.reason=generated
file.138.path=tests/fixtures/docs-obligation/orphan-rendered/docs/reference/index.md
file.138.verdict=skipped
file.138.reason=generated
file.139.path=tests/fixtures/docs-obligation/orphan-rendered/docs/tasks/index.md
file.139.verdict=skipped
file.139.reason=generated
file.140.path=tests/fixtures/docs-obligation/orphan-rendered/docs/tutorials/index.md
file.140.verdict=skipped
file.140.reason=generated
file.141.path=tests/fixtures/docs-obligation/orphan-source/README.md
file.141.verdict=skipped
file.141.reason=generated
file.142.path=tests/fixtures/docs-obligation/orphan-source/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.142.verdict=skipped
file.142.reason=generated
file.143.path=tests/fixtures/docs-obligation/orphan-source/docs/assets/widget.png
file.143.verdict=skipped
file.143.reason=generated
file.144.path=tests/fixtures/docs-obligation/orphan-source/docs/assets/widget.svg
file.144.verdict=skipped
file.144.reason=generated
file.145.path=tests/fixtures/docs-obligation/orphan-source/docs/concepts/widget-overview.md
file.145.verdict=skipped
file.145.reason=generated
file.146.path=tests/fixtures/docs-obligation/orphan-source/docs/contribute/index.md
file.146.verdict=skipped
file.146.reason=generated
file.147.path=tests/fixtures/docs-obligation/orphan-source/docs/decisions/index.md
file.147.verdict=skipped
file.147.reason=generated
file.148.path=tests/fixtures/docs-obligation/orphan-source/docs/reference/index.md
file.148.verdict=skipped
file.148.reason=generated
file.149.path=tests/fixtures/docs-obligation/orphan-source/docs/tasks/index.md
file.149.verdict=skipped
file.149.reason=generated
file.150.path=tests/fixtures/docs-obligation/orphan-source/docs/tutorials/index.md
file.150.verdict=skipped
file.150.reason=generated
file.151.path=tests/fixtures/docs-obligation/stale-source/README.md
file.151.verdict=skipped
file.151.reason=generated
file.152.path=tests/fixtures/docs-obligation/stale-source/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.152.verdict=skipped
file.152.reason=generated
file.153.path=tests/fixtures/docs-obligation/stale-source/docs/assets/widget.mmd
file.153.verdict=skipped
file.153.reason=generated
file.154.path=tests/fixtures/docs-obligation/stale-source/docs/assets/widget.png
file.154.verdict=skipped
file.154.reason=generated
file.155.path=tests/fixtures/docs-obligation/stale-source/docs/assets/widget.svg
file.155.verdict=skipped
file.155.reason=generated
file.156.path=tests/fixtures/docs-obligation/stale-source/docs/concepts/widget-overview.md
file.156.verdict=skipped
file.156.reason=generated
file.157.path=tests/fixtures/docs-obligation/stale-source/docs/contribute/index.md
file.157.verdict=skipped
file.157.reason=generated
file.158.path=tests/fixtures/docs-obligation/stale-source/docs/decisions/index.md
file.158.verdict=skipped
file.158.reason=generated
file.159.path=tests/fixtures/docs-obligation/stale-source/docs/reference/index.md
file.159.verdict=skipped
file.159.reason=generated
file.160.path=tests/fixtures/docs-obligation/stale-source/docs/tasks/index.md
file.160.verdict=skipped
file.160.reason=generated
file.161.path=tests/fixtures/docs-obligation/stale-source/docs/tutorials/index.md
file.161.verdict=skipped
file.161.reason=generated
file.162.path=tests/fixtures/docs-obligation/trace-incomplete/README.md
file.162.verdict=skipped
file.162.reason=generated
file.163.path=tests/fixtures/docs-obligation/trace-incomplete/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json
file.163.verdict=skipped
file.163.reason=generated
file.164.path=tests/fixtures/docs-obligation/trace-incomplete/docs/assets/widget.mmd
file.164.verdict=skipped
file.164.reason=generated
file.165.path=tests/fixtures/docs-obligation/trace-incomplete/docs/assets/widget.png
file.165.verdict=skipped
file.165.reason=generated
file.166.path=tests/fixtures/docs-obligation/trace-incomplete/docs/assets/widget.svg
file.166.verdict=skipped
file.166.reason=generated
file.167.path=tests/fixtures/docs-obligation/trace-incomplete/docs/concepts/widget-overview.md
file.167.verdict=skipped
file.167.reason=generated
file.168.path=tests/fixtures/docs-obligation/trace-incomplete/docs/contribute/index.md
file.168.verdict=skipped
file.168.reason=generated
file.169.path=tests/fixtures/docs-obligation/trace-incomplete/docs/decisions/index.md
file.169.verdict=skipped
file.169.reason=generated
file.170.path=tests/fixtures/docs-obligation/trace-incomplete/docs/reference/index.md
file.170.verdict=skipped
file.170.reason=generated
file.171.path=tests/fixtures/docs-obligation/trace-incomplete/docs/tasks/index.md
file.171.verdict=skipped
file.171.reason=generated
file.172.path=tests/fixtures/docs-obligation/trace-incomplete/docs/tutorials/index.md
file.172.verdict=skipped
file.172.reason=generated
file.173.path=tests/integration/test_docs_command_scenarios.py
file.173.verdict=reviewed
file.174.path=tests/integration/test_docs_obligation_scenarios.py
file.174.verdict=reviewed
file.175.path=tests/unit/test_docs_obligation_reuse.py
file.175.verdict=reviewed
file.176.path=tests/unit/test_docs_utils_carriers.py
file.176.verdict=reviewed
file.177.path=tests/unit/test_docs_utils_obligation.py
file.177.verdict=reviewed
<!-- coverage-receipt:end -->
