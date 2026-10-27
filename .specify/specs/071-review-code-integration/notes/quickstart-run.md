# Quickstart Run — Feature 071 (implement, T034)

**Captured**: 2026-10-27, at HEAD `f02d9a0b887418753f4f05127519cebfe96fbf58` (implement part 7a), on a tree whose only untracked files were this run's own evidence captures. Every command below was run through the **installed mirror path** `.specify/skills/internal/code-review/scripts/git-delta-review.sh`, not the framework source `skills/internal/...` — the two files are byte-identical for this run (`sha256 ec0e0f49…c3c92fa`, `test-evidence/quickstart-mirror-identity.txt`), so what follows is evidence about the projection the commands actually consume.

**Status vocabulary used here** (no other status is claimed for any scenario):

| Status | Meaning |
|--------|---------|
| `EXECUTED` | the scenario's own commands were run; the pasted output and exit code are the real ones |
| `EXECUTED — premise corrected` | the scenario was run, its written premise did not hold on this repository, and the corrected form was run and recorded; the failing premise is stated |
| `PARTIALLY EXECUTED` | the deterministic part of the scenario was run; the part that needs a prompt executor is named and marked blocked, never reported as passed |

No scenario is reported as passed because a contract test says it should pass. Where a test pins the same behaviour, it is cited as a second witness, not as a substitute for a run.

**Environment**: `Python 3.11.11`, `pytest 8.4.2`, `GNU bash 4.4.20(1)-release`, `git 2.43.5`; `delta` is installed at `/home/agent/.cargo/bin/delta` and stdout is **not** a TTY in this stage's shell — the two facts Scenario D turns on.

**Docs↔template isomorphism (the first half of T034)**

```text
$ python3 -m pytest -q tests/contract/test_review_docs_isomorphism.py
.........                                                                [100%]
9 passed in 0.06s
exit=0
```

Green before any scenario ran; `test-evidence/quickstart-T034-isomorphism.txt`.

## Scenario summary

| Scenario | Subject | Status |
|----------|---------|--------|
| A | base resolution tiers | `EXECUTED` |
| B | a run producing both conclusions | `PARTIALLY EXECUTED` — deterministic substratum run; prompt-level carriers blocked |
| C | a feature with no code paths in its delta | `EXECUTED` |
| D | no renderer on the host | `EXECUTED` |
| E | gap drill (red first, then green) | `EXECUTED — premise corrected` (the record's range must be supplied to `receipt`) |
| F | focused review of an oversized diff | `EXECUTED — premise corrected` (the written selector matches nothing here) |
| G | the gate verdict, from the explicit record only | `EXECUTED` |
| H | where a finding may and may not go | `PARTIALLY EXECUTED` — written duties verified; the `/speckit.feedback` run itself blocked |

## A — base resolution

```text
$ git log --diff-filter=A --format='%H %ad %s' --date=short -- .specify/specs/071-review-code-integration/requirements.md
8d18265baf9d1aa8c4580339946411ddb082735f 2026-10-27 docs(071-review-code-integration): land the review × code-review composition requirements
$ git rev-parse 8d18265b^
e57052efa1c16871da4e24a56eabf7402b6fd87e                                   exit 0
$ git symbolic-ref refs/remotes/origin/HEAD
fatal: ref refs/remotes/origin/HEAD is not a symbolic ref                   exit 128
$ git remote -v
origin  git@github.com:github/spec-kit.git (fetch/push)   # the UPSTREAM project, plus gitee/github/gitlab mirrors of this work
$ git merge-base main HEAD
926836e0fc931bfdbd531f45b0b27e3715e84a0c                                   exit 0
$ bash .specify/skills/internal/code-review/scripts/git-delta-review.sh base \
    --spec .specify/specs/071-review-code-integration
base=e57052efa1c16871da4e24a56eabf7402b6fd87e
head=f02d9a0b887418753f4f05127519cebfe96fbf58
base_source=feature-first-commit                                            exit 0
$ … base --spec … --json
{"base":"e57052efa1c16871da4e24a56eabf7402b6fd87e","head":"f02d9a0b887418753f4f05127519cebfe96fbf58","base_source":"feature-first-commit"}
```

Matches the quickstart's expected value exactly (`base_source=feature-first-commit`, `base=e57052ef…`, `head` = run-start `HEAD`), and reproduces the documented reason the tier order exists: `refs/remotes/origin/HEAD` is not a symbolic ref here, `origin` is the upstream project, and `main`'s merge base (`926836e0`) is far behind the feature slice.

## B — a run producing both conclusions

`/speckit.review` is a prompt, not a program: in this stage nothing executes prompts, so the two carriers it is judged on (`review.md` § 2.1 and the feature detail's `## Latest Review` entry) **cannot be produced here**. That half is **blocked**, not passed; `tests/contract/test_review_code_composition.py` pins the text that would drive it.

What was run is the deterministic substratum the command delegates to — the four-step non-interactive path (C-17), all through the mirror:

```text
$ … triage --spec .specify/specs/071-review-code-integration
base=e57052efa1c16871da4e24a56eabf7402b6fd87e
head=f02d9a0b887418753f4f05127519cebfe96fbf58
base_source=feature-first-commit
changed_files=127
triage=run
basis=code path in the committed delta: .specify/skills/internal/code-review/scripts/git-delta-review.sh skills/internal/code-review/scripts/git-delta-review.sh tests/contract/… (10 code paths)   exit 0

$ … start --spec .specify/specs/071-review-code-integration
✓ 代码段记录已创建: .specify/specs/071-review-code-integration/code-review.md
record=.specify/specs/071-review-code-integration/code-review.md
archive=none
renderer=text                                                               exit 0

$ … note --review-file <record> -s suggestion -f templates/commands/review.md -c "…"   exit 0
$ … note --review-file <record> -s important -f skills/internal/code-review/scripts/git-delta-review.sh -l 700 -c "…"   exit 0

$ … receipt --review-file <record> --spec .specify/specs/071-review-code-integration
changed_files=127  judged_files=127  skipped_files=0  gap_files=0
lines_added=18075  lines_deleted=159
blocking_entries=0  verdict=pass
uncommitted_scope=5
record=.specify/specs/071-review-code-integration/code-review.md            exit 0
```

Two facts worth carrying forward: the **uncommitted-scope disclosure** fired with the real count (`uncommitted_scope=5`) and a `> **未提交范围（未评审）**…` line inside the record (C-44, FR-005); and a second `receipt` call over the same repository state produced a **byte-identical block** (`diff` of the two extracted blocks, 267 lines, `rc=0` — `test-evidence/quickstart-BE-receipt-determinism.txt`), which is C-33 in observable form.

The `--code-paths` override was exercised live in both directions: `--code-paths '*.md'` → `triage=run` with the 58 documentation/artifact paths as the basis; `--code-paths '*.nomatch'` → `triage=not-applicable` with `basis=no code deliverable…` (`test-evidence/quickstart-B-codepaths-md.txt`, `quickstart-C-codepaths-none.txt`).

Rotation (the second run of the same feature) is recorded in G below.

## C — a feature with no code paths in its delta

Both branches of the triage rule were produced from real ranges:

```text
$ … triage --since 8d18265b^ --head 8d18265b          # that commit touched 11 spec/memory/evidence files, no code path
changed_files=11
triage=not-applicable
basis=no code deliverable: the committed delta contains no code path         exit 0

$ … triage --since HEAD --head HEAD                    # empty delta
base=head=f02d9a0b…  changed_files=0
triage=not-applicable
basis=no committed code delta                                                exit 0
```

No record is created for a non-`run` triage value:

```text
$ … start --spec .specify/specs/071-review-code-integration --triage not-applicable
refused: triage=not-applicable
no record is created for a triage value other than run (C-11 / data-model V29)   exit 2
$ ls .specify/specs/071-review-code-integration/code-review.md
ls: cannot access '…/code-review.md': No such file or directory
```

The process-report half of C (the reason and verdict carried in `review.md` § 2.1, the feature detail entry repeating it) is **blocked** for the same reason as B.

## D — no renderer on the host

```text
$ DELTA_BIN=/nonexistent-delta bash …/git-delta-review.sh receipt \
    --review-file <record> --renderer text --spec .specify/specs/071-review-code-integration
renderer=text  changed_files=127  judged_files=127  gap_files=0  verdict=pass      exit 0
$ grep -n "渲染模式" <record>        → | **渲染模式** | `renderer: text` |
$ grep -cE "已完成可视化评审|rendered review complete|visual review performed|side-by-side review done" <record>   → 0
```

The no-TTY case — the one that actually happens — was also run, with the renderer **present**:

```text
$ command -v delta                      → /home/agent/.cargo/bin/delta
$ [[ -t 1 ]] && echo tty || echo no-tty → no-tty
$ … receipt --review-file <record> --spec …      → renderer=text … verdict=pass    exit 0
```

An available renderer produced no rendered-mode claim: the record kept `renderer: text` and the four forbidden literals of SC-003 stayed at zero hits. Both runs are `test-evidence/quickstart-D-no-renderer.txt` and `quickstart-D-nontty.txt`.

## E — gap drill (premise corrected, then run)

**The written command does not do what the quickstart expects on this repository.** Run literally, `receipt --review-file <record>` has no `--spec`/`--since`, so the base falls through the feature tier to the **trunk merge-base** (`926836e0…`, `base_source=trunk-merge-base`) — a range dominated by unrelated work — and inside it sits a binary asset:

```text
$ … receipt --review-file .specify/specs/071-review-code-integration/code-review.md
行数无法测量 (binary): .specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png
不可量测的数字字段意味着不写块 (C-41 / V16)                                  exit 2
```

That is the script behaving as `coverage-receipt.md` C-41 requires (an unmeasurable quantity means no block and exit `2`, never `0`), but it means the receipt must be given **the same range the record was created with**. The corrected form — the composed four-step path, where step 1 `base --spec` already resolved `e57052ef…` and the caller passes it through — is what was drilled below.

```text
$ … receipt --review-file <record> --spec .specify/specs/071-review-code-integration    # first write
changed_files=127  judged_files=127  skipped_files=0  gap_files=0  verdict=pass        exit 0
# remove the file.001.path / .verdict pair by hand, then re-run
changed_files=127  judged_files=126  skipped_files=0  gap_files=1  verdict=not-evaluated  exit 1
# restore the removed pair from the backup, then re-run
changed_files=127  judged_files=127  skipped_files=0  gap_files=0  verdict=pass        exit 0
# replace the reason with a value outside the closed five-value set
$ … receipt --review-file <record> --spec … --skip-with-reason ".specify/**" --reason "free text reason outside the closed set"
changed_files=127  judged_files=22  skipped_files=0  gap_files=105  verdict=not-evaluated  exit 1
```

The two cannot-evaluate cases of the same alphabet:

```text
$ … receipt --review-file .specify/.tmp/quickstart-071/missing.md --spec …
✗ 记录不存在: … (先跑 start 创建/轮转记录)                                    exit 2
$ … receipt --review-file <record> --since deadbeefdeadbeef
base_source=not-evaluated
reason=显式基准不可解析: deadbeefdeadbeef
resolve_command=git log --diff-filter=A --format=%H -- <spec-dir>/requirements.md ; git rev-parse HEAD ; git merge-base <trunk> HEAD   exit 2
```

So the closed alphabet `0` / `1` / `2` was observed with one meaning each, red-then-green included, and no block was written on the `2` path (`test-evidence/quickstart-E-*.txt`).

**Premise corrected, disclosed rather than patched**: `quickstart.md`'s D/E/F command lines omit `--spec`; `skills/internal/code-review/SKILL.md` step 4 likewise shows only `receipt --review-file <record>`. On a repository whose trunk has diverged from the feature slice, that form judges a different range than the record header carries (and here cannot evaluate at all). No artifact was edited for it — `quickstart.md` is plan-owned, and which surface should carry the range (the documented invocation, or the script inheriting `base`/`head` from the record header) is a choice between two readings that this stage does not own. Recorded as an observation for the driver.

## F — focused review of an oversized diff (premise corrected, then run)

The written selector matches nothing in this feature's delta, so the literal command cannot demonstrate a skip:

```text
$ … receipt --review-file <record> --spec … --skip-with-reason "src/legacy/**" --reason size-guard-focus-not-reviewed
changed_files=127  judged_files=127  skipped_files=0  gap_files=0  verdict=pass          exit 0
```

With a selector that matches real changed paths, the focus semantics appear exactly as specified:

```text
$ … receipt … --skip-with-reason "docs/**" --reason size-guard-focus-not-reviewed
changed_files=127  judged_files=126  skipped_files=1   gap_files=0  verdict=not-evaluated  exit 0
$ … receipt … --skip-with-reason ".specify/**" --reason size-guard-focus-not-reviewed
changed_files=127  judged_files=21   skipped_files=106 gap_files=0  verdict=not-evaluated  exit 0
```

A legal skip is a legal verdict (exit `0`, not a gap) but never coverage credit: the segment verdict left `pass` and became `not-evaluated` (C-37 / A-13), and the block carried `file.110.verdict=skipped` with `file.110.reason=size-guard-focus-not-reviewed`. `src/legacy/**` is not a path this repository has, which is the whole of the premise failure.

## G — the gate verdict, from the explicit record only

```text
$ … note --review-file <record> -s blocking -f skills/internal/code-review/scripts/git-delta-review.sh -l 1011 -c "… (drill only)"   exit 0
$ … report --summary --file <record>
  🔴 [blocking] 1 … record=<record>  blocking_entries=1  gate=deny
  ✗ 合入门禁: 存在 1 条 [blocking] — 必须解决后方可合入                     exit 1
```

The second half is the same command after the code segment was re-run, which produces a **new record** rather than "clearing" anything:

```text
$ … start --spec .specify/specs/071-review-code-integration          # second run of the feature
record=…/code-review.md  archive=.specify/specs/071-review-code-integration/code-review-20261027T084638Z.md   exit 0
$ … receipt --review-file <record> --spec …    → changed 127 / judged 127 / skipped 0 / gap 0, blocking_entries=0, verdict=pass   exit 0
$ … report --summary --file <record>           → blocking_entries=0  gate=allow  ✓ 满足收敛条件                                     exit 0
```

Both halves read the current record only; nothing was resolved in place (`test-evidence/quickstart-G-*.txt`, `quickstart-B-second-run.txt`).

## H — where a finding may and may not go

The `/speckit.feedback` run itself is **blocked**: it is a prompt, and this stage executes no prompts. Its written duties were verified deterministically instead:

- the classification duty is on both surfaces C-57 names — `templates/commands/review.md:117` ("Only framework friction may be posted… a code defect … MUST NOT be posted as a feedback entry") and `skills/internal/code-review/SKILL.md:96-97` (the Chinese counterpart, with the `code-review.md` retention rule);
- all three units are already registered in the probe registry, so no wrap-up recompilation is needed — `speckit-review-wrapup` (line 78), `skill-code-review-wrapup` (line 87), `skill-review-sdd-process-wrapup` (line 174) of `.specify/shared/definitions/probe-definitions.md`;
- the store named on both surfaces is project-local (`scope: local`, `.specify/memory/feedback/`), unbounded-auto-transmission is forbidden by the surrounding text, and this feature added no second destination.

The two constructed samples — a framework-friction entry judged legal, a code defect judged a violation — are pinned by `tests/contract/test_review_feedback_boundary.py`, which is green in this part's closure run (T036). That is a second witness, not a run of the scenario.

## Teardown

The drill writes into the feature directory by design (`<spec>/code-review.md` plus its rotation archive). Everything it created was removed once the evidence above was captured:

```text
$ rm -f .specify/specs/071-review-code-integration/code-review.md \
        .specify/specs/071-review-code-integration/code-review-20261027T084638Z.md
$ ls .specify/specs/071-review-code-integration/ | grep -c code-review   → 0
```

Scratch (record backups, extracted blocks) lived under `.specify/.tmp/quickstart-071/`, which `.specify/.gitignore` matches; it is not archived. What remains in `git status` after teardown is this run's evidence captures and this note — no `code-review*.md`, no block left behind in any committed artifact.

## What this run does not prove

- The prompt-level halves of B, C and H (`review.md` § 2.1, the feature detail entry, the `/speckit.feedback` run) — blocked, as stated, with the pinning tests named.
- Anything about the receipt's behaviour on a repository whose trunk equals the feature slice: the `--spec`-less form was observed failing here and was not re-observed succeeding elsewhere.
- The `lines_added`/`lines_deleted` values are measurements of one range on one day (18075 / 159 over `e57052ef..f02d9a0b`); they move with the range and are not a baseline.
