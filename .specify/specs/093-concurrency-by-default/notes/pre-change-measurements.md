# Pre-change measurements — 093-concurrency-by-default (WP1-facts entry)

Measured 2026-11-09 in this worktree (`093-clarify`, branch `093-concurrency-by-default`) before any
fact file of this feature was written. Command/output pairs are captured verbatim in
`test-evidence/wp1-t003-enumeration-probes.txt`; this page records the numbers and the two readings
the tasks artifact calls the "trap form".

## 1. Enumeration roots (T003)

| Probe | Reading |
|---|---|
| `ls -d skills/internal/*/ \| wc -l` | 38 |
| `ls -d skills/external/*/ \| wc -l` | 16 |
| `ls templates/commands/*.md \| wc -l` | 29 |
| `ls agents/*.md \| wc -l` | 17 |
| `ls -d .specify/teams/*/ \| wc -l` | 12 |
| `ls -d .specify/anchoring/*/ \| wc -l` | 6 |
| **enumerable bodies (sum of the five roots, `skills` counted as its two layers)** | **118** (38 + 16 + 29 + 17 + 12 + 6) |

**Trap form** — `ls -d .specify/skills/*/ | wc -l` reads **17**, not 16: the flat runtime layer holds
the 16 external skill projections **plus** the nested `internal/` directory. Counting the projection
tree therefore either double-counts the external skills (17 against the 16 real external roots) or, read
as "16 flat external projections", silently drops `internal/`. The five roots are the patterns in
`shared/declarations/facts/executor-enumeration-roots.yaml`; the projection tree is never a root.

Drift against `tasks.md` T003's frozen text: the row records the trap-form reading as **16**. The
measured reading today is **17** total entries (16 flat external + `internal/`) — the row's number is
the external-projection slice, this page records the raw command reading. No behaviour depends on the
number: the facts carry patterns, never counts (R-6).

## 2. Declaration layer baseline (feeds T005)

| Probe | Reading |
|---|---|
| `declaration_reader.py --action list --repo .` → `contract` keys | **9** |
| same → `facts` entries | **24** (the tasks/research text records 23; the tree has one more fact today — the 092 review-surface fact landed after that measurement) |
| same → `exclusions` rows | 73 |
| `declaration_reader.py --action get --fact concurrency-class` | exit **1**, `no declaration for fact 'concurrency-class'` |

Drift disclosure: `tasks.md` T005 says "measured baseline 2026-11-09: `facts` **23** entries". Today's
same-command reading is **24**. The pre-change reading recorded here is the measured one; the row's
count is stale by one and is not used as an assertion anywhere (the tests assert slug membership, not
a total).

## 3. Clause space baseline (feeds T006)

`grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing contract files:
18 (declaration-facts) + 22 (judgement-engine) + 22 (executor-obligations) + 18 (high-order-executors)
+ 14 (existing-semantics-disposal) = **94**. The count matches the plan's figure.
