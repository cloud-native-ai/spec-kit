# Quickstart Run — Feature 051 (User-Facing Comprehension)

**Run by**: T013 · **Date**: 2026-09-18 · **Scope**: scenarios **1** and **2** (the two US1
owns). Scenarios 3–6 belong to US2–US5 and are recorded by their own tasks.

Every expectation below is **observed output**, not a prediction. Where the quickstart states
a pre-change baseline, the post-change value is shown beside it.

---

## 场景 1 — 真源文档存在且镜像逐字节相等(US1 / SC-003)

```
$ ls -l shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md
  -rw------- 13110 shared/guidelines/user-facing-comprehension.md
  -rw------- 13110 .specify/shared/guidelines/user-facing-comprehension.md
$ cmp shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md && echo "BYTE-IDENTICAL"
  BYTE-IDENTICAL
$ ls -1 shared/guidelines/*.md | wc -l
  12
```

| Expectation | Observed | Verdict |
|---|---|---|
| both files exist | both present, 13110 bytes each | ✅ |
| `cmp` silent → `BYTE-IDENTICAL` | `BYTE-IDENTICAL` | ✅ |
| guideline count = **12** | **12** (pre-change baseline 11, +1 for this feature) | ✅ |

> Working-tree mode shows `-rw-------` for this file and 6 of its 11 siblings, while 3 show
> `-rw-r--r--`. This is a local umask artifact, **not** a repository defect: `git ls-files -s`
> records `100644` for every one of them (git tracks only the executable bit). No action.

---

## 场景 2 — 常驻章节抵达活动指令文件(US1 / FR-003 / FR-038)

```
$ grep -c '^## User-Facing Comprehension' templates/instructions-template.md \
      .specify/templates/instructions-template.md .specify/instructions.md
  templates/instructions-template.md:1
  .specify/templates/instructions-template.md:1
  .specify/instructions.md:1
$ grep -c '^## ' templates/instructions-template.md
  18
$ grep -c '^## ' .specify/instructions.md
  19
```

| Expectation | Observed | Verdict |
|---|---|---|
| three `grep -c` each = **1** | 1 / 1 / 1 | ✅ |
| template sections **17 → 18** | **18** | ✅ |
| live sections **18 → 19** | **19** (the extra one is the project-owned `## Recurring Operational Lessons`) | ✅ |

### Position window

`grep -n '^## ' templates/instructions-template.md` (excerpt):

```
    8:## Documentation Map
   25:## Proactive Flow Trigger
   35:## Fact, Correctness & Logic Checks (Input Sanity)
   50:## One Source Of Truth
   60:## Task Complexity Rubric
   66:## Token Efficiency Discipline
   74:## User-Facing Comprehension
   86:## Dogfooding Practice
```

| Expectation | Observed | Verdict |
|---|---|---|
| new section **after** `Token Efficiency Discipline` | 66 → **74** | ✅ |
| new section **before** `Dogfooding Practice` | **74** → 86 | ✅ |
| `Documentation Map` → `Proactive Flow Trigger` → `Fact, Correctness…` adjacency unchanged | 8 → 25 → 35, still consecutive, no insertion inside the window | ✅ |

The same order holds in the live file (`.specify/instructions.md`: 74 → **82** → 94), so the
additive reconcile injected the section at its **template-relative** position rather than
appending it at the end.

### Dangling-pointer traversal (FR-038 / SC-017)

```
$ grep -oE '\.specify/shared/guidelines/[a-z0-9-]+\.md' .specify/instructions.md | sort -u | while read -r p; do
    s="shared/guidelines/$(basename "$p")"
    [ -f "$s" ] && echo "ok   $s" || echo "MISSING  $s"
  done
  ok   shared/guidelines/ask-record-repeat.md
  ok   shared/guidelines/better-harness.md
  ok   shared/guidelines/confirmation-gates.md
  ok   shared/guidelines/dogfooding.md
  ok   shared/guidelines/one-source-of-truth.md
  ok   shared/guidelines/proactive-trigger.md
  ok   shared/guidelines/task-complexity-rubric.md
  ok   shared/guidelines/token-efficiency.md
  ok   shared/guidelines/user-facing-comprehension.md
```

| Expectation | Observed | Verdict |
|---|---|---|
| all `ok`, zero `MISSING` | **9 `ok`, 0 `MISSING`** | ✅ |
| pointer surface grows by 1 | pre-change **8** → post-change **9** (the new guideline) | ✅ |
| remainder unchanged | still the same **3** structurally unpointed guidelines | ✅ |

The traversal reaches **9** of the **12** guidelines now on disk. The 3 it cannot reach
(`checklist-methodology.md`, `requirements-guidelines.md`, `self-improvement.md`) have no
pointer on either instruction surface, so no pointer to them can dangle; they are accounted
for by `ambient-section.md` **C-11(b)**'s remainder assertion instead — remainder ⊆ those
three, in subset semantics, so deleting any existing pointer grows the remainder and fails
while adding one does not. That is what makes "all 12 accounted for" true in an implementable
form rather than by a traversal that structurally cannot reach them.

---

## Symlink aliases (T009's fourth verification)

All 8 remain symbolic links into `.specify/instructions.md` — none was replaced by a regular
file by the regeneration:

```
  AGENTS.md -> .specify/instructions.md            .github/copilot-instructions.md -> ../.specify/instructions.md
  CLAUDE.md -> .specify/instructions.md            .qoder/project_rules.md -> ../.specify/instructions.md
  QODER.md  -> .specify/instructions.md            .claude/project_rules.md -> ../.specify/instructions.md
  HERMES.md -> .specify/instructions.md            .opencode/instructions.md -> ../.specify/instructions.md
```

The new section therefore reaches all 8 agent surfaces through the symlink, with no separate
edit per tool.

---

## Regeneration side effects worth recording

`bash scripts/bash/generate-instructions.sh` reported
`Injected missing template section(s): User-Facing Comprehension` and, as designed, kept the
existing live file as the refresh base rather than overwriting it. It also wrote a dated
backup `.specify/instructions.md-2026-09-18-192435` and refreshed the tool JSON manifests.
The backup is the generator's own history mechanism (the log names it as the recovery source
for content dropped by older versions); it is not a feature artifact and is not staged.
