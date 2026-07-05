# Model Selection, Progress Ledger & File Handoffs

Reference detail for [../SKILL.md](../SKILL.md). Adapted from superpowers
(skills/subagent-driven-development). All working files for this draft skill
live under `draft/.sdd/` in the repo working tree.

---

## Model selection doctrine

Use the **least powerful model that can handle each role** to conserve cost and
increase speed. **Always specify the model explicitly when dispatching a
subagent** — an omitted model inherits your session's model, often the most
capable and most expensive, which silently defeats this whole doctrine.

### Roles

- **Mechanical implementation tasks** (isolated functions, clear specs, 1–2
  files): use a fast, cheap model. Most implementation tasks are mechanical
  when the plan is well-specified.
- **Integration and judgment tasks** (multi-file coordination, pattern
  matching, debugging): use a standard model.
- **Architecture and design tasks**: use the most capable available model. The
  final whole-branch review is one of these — dispatch it on the most capable
  available model, not the session default.
- **Review tasks**: choose the model with the same judgment, scaled to the
  diff's size, complexity, and risk. A small mechanical diff does not need the
  most capable model; a subtle concurrency change does.

### Turn count beats token price

Wall-clock and context cost scale with how many turns a subagent takes, and the
cheapest models routinely take 2–3× the turns on multi-step work — costing more
overall. Use a mid-tier model as the **floor** for reviewers and for
implementers working from prose descriptions. When the task's plan text
contains the complete code to write, the implementation is transcription plus
testing: use the cheapest tier for that implementer. Single-file mechanical
fixes also take the cheapest tier.

### Task complexity signals (implementation tasks)

| Signal | Model tier |
|--------|------------|
| Touches 1–2 files with a complete spec (or plan text contains the code) | cheapest |
| Touches multiple files with integration concerns | standard |
| Requires design judgment or broad codebase understanding | most capable |

### On the spec-kit Agent/Task tooling

Spec Kit dispatches subagents through the generic Agent/Task tooling, which
takes a `model` parameter (e.g. `haiku` / `sonnet` / `opus` in Claude Code, or
your harness's equivalent tiers). Set it on **every** dispatch — implementer,
reviewer, and fix — mapping the role above to a concrete tier. If a project
uses the `.specify` agent triad, you may route the reviewer role through
`qa-engineer` and the implementer through `module-designer`; SDD does not
require it.

---

## Progress ledger

Conversation memory does not survive compaction. Controllers that lost their
place have re-dispatched entire completed task sequences — the single most
expensive failure observed. Track progress in a ledger **file**, not only in
todos.

- **Location:** `draft/.sdd/progress.md` (git-ignored scratch; see workspace
  helper below).
- **At skill start**, read it and resume:

  ```bash
  cat "$(git rev-parse --show-toplevel)/draft/.sdd/progress.md" 2>/dev/null || echo "(no ledger yet — first run)"
  ```

  Tasks listed there as complete are **DONE** — do not re-dispatch them; resume
  at the first task not marked complete.

- **When a task's review comes back clean**, append one line in the same message
  as your other bookkeeping:

  ```
  Task N: complete (commits <base7>..<head7>, review clean)
  ```

  Record deferred Minor findings under the task line so the final whole-branch
  review can triage them:

  ```
  Task N: complete (commits abc1234..def5678, review clean)
    minor: extract magic number 100 -> PROGRESS_INTERVAL (indexer.py:130)
  ```

- **The ledger is your recovery map:** the commits it names exist in git even
  when your context no longer remembers creating them. After compaction, trust
  the ledger and `git log` over your own recollection.
- `git clean -fdx` will destroy the ledger (it's git-ignored scratch); if that
  happens, recover from `git log`.

### Example ledger

```
# SDD progress — <plan file>
# branch: <branch>   started from: <merge-base7>

Task 1: complete (commits 0a1b2c3..4d5e6f7, review clean)
Task 2: complete (commits 4d5e6f7..89abcde, review clean)
  minor: help text missing --concurrency flag (cli.py:1-31)
Task 3: in progress
```

---

## File handoffs & context hygiene

Everything you paste into a dispatch prompt — and everything a subagent prints
back — stays resident in your context for the rest of the session and is re-read
on every later turn. Hand artifacts over as **files**:

- **Task brief:** before dispatching an implementer, extract the task's full
  text to `draft/.sdd/task-N-brief.md`. Your dispatch contains: (1) one line on
  where this task fits; (2) the brief path, introduced as "read this first — it
  is your requirements, with the exact values to use verbatim"; (3) interfaces
  and decisions from earlier tasks the brief cannot know; (4) your resolution of
  any ambiguity you noticed; (5) the report-file path and report contract.
  Exact values (numbers, magic strings, signatures, test cases) appear only in
  the brief.
- **Report file:** name it after the brief (`task-N-brief.md` →
  `task-N-report.md`). The implementer writes the full report there and returns
  only status, commits, a one-line test summary, and concerns.
- **Reviewer inputs:** the task reviewer gets three paths — the same brief file,
  the report file, and the review package — plus the global constraints that
  bind the task.
- **Fix dispatches** append their fix report (with test results) to the same
  report file and return a short summary; re-reviews read the updated file.

**Do not pre-judge for the reviewer.** Never instruct a reviewer to ignore or
not flag a specific issue, and never pre-rate a finding's severity ("treat as
Minor at most"). If you believe a finding would be a false positive, let the
reviewer raise it and adjudicate it in the review loop. A finding labeled
plan-mandated — or any finding conflicting with the plan's text — is the
human's decision: present the finding beside the plan text and ask which
governs.

---

## Helper concepts (adapted from superpowers `scripts/`)

Superpowers ships three small bash helpers. You do not need the scripts
verbatim — the concepts and the snippets below are enough. All resolve into
`draft/.sdd/` for this draft skill.

### `sdd-workspace` — resolve the scratch directory

Ensures the working-tree directory SDD uses for briefs, reports, review
packages, and the ledger. It lives in the **working tree** (not under `.git/`,
which the harness protects from agent writes) with a self-ignoring `.gitignore`
so it stays out of `git status` and out of accidental commits.

```bash
sdd_workspace() {
  root=$(git rev-parse --show-toplevel)
  dir="$root/draft/.sdd"
  mkdir -p "$dir"
  printf '*\n' > "$dir/.gitignore"
  printf '%s\n' "$dir"
}
```

### `task-brief PLAN_FILE N` — extract one task's text to a file

Pulls Task N's full text out of the plan into `draft/.sdd/task-N-brief.md`, so
the task text never passes through the controller's context and the implementer
reads it in one call. (The fence toggle keeps `## Task` headings inside code
blocks from being mistaken for task boundaries.)

```bash
task_brief() {
  plan=$1; n=$2
  out="$(sdd_workspace)/task-${n}-brief.md"
  awk -v n="$n" '
    /^```/ { infence = !infence }
    !infence && /^#+[ \t]+Task[ \t]+[0-9]+/ {
      intask = ($0 ~ ("^#+[ \t]+Task[ \t]+" n "([^0-9]|$)"))
    }
    intask { print }
  ' "$plan" > "$out"
  [ -s "$out" ] || { echo "task ${n} not found in ${plan}" >&2; return 3; }
  echo "wrote ${out}: $(wc -l < "$out" | tr -d ' ') lines"
}
```

### `review-package BASE HEAD` — one file with commits + stat + diff

Writes the commit list, `git diff --stat`, and the net diff with extended
context (`-U10`) to `draft/.sdd/review-<base7>..<head7>.diff`, named per range
so a re-review after fixes gets a distinct fresh file. Use the **recorded
per-task BASE**, never `HEAD~1` — `HEAD~1` silently drops all but the last
commit of a multi-commit task. For the final whole-branch review, use
`BASE = git merge-base <trunk> HEAD`.

```bash
review_package() {
  base=$1; head=$2
  git rev-parse --verify --quiet "$base" >/dev/null || { echo "bad BASE: $base" >&2; return 2; }
  git rev-parse --verify --quiet "$head" >/dev/null || { echo "bad HEAD: $head" >&2; return 2; }
  out="$(sdd_workspace)/review-$(git rev-parse --short "$base")..$(git rev-parse --short "$head").diff"
  {
    echo "# Review package: ${base}..${head}"; echo
    echo "## Commits";       git log --oneline "${base}..${head}"; echo
    echo "## Files changed"; git diff --stat   "${base}..${head}"; echo
    echo "## Diff";          git diff -U10     "${base}..${head}"
  } > "$out"
  echo "wrote ${out}: $(git rev-list --count "${base}..${head}") commit(s)"
}
```

The printed path is what you name in the reviewer dispatch. The output never
enters your own context; the reviewer sees the commit list, stat summary, and
full diff with context in one Read call.
