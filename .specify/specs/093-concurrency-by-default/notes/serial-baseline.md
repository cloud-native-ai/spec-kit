# Serial baseline — 091's own run record (T111, SC-006 comparison)

**Purpose**: the serial comparison row SC-006 requires, written from the existing record — **not**
re-measured in this feature. Every quantity 091 did not produce is marked `not_evaluated`.

| Quantity | Value | Source |
|----------|-------|--------|
| tasks | **62** | 091's own state spine `.specify/state/091-auto-git-closeout.md` line 57 (`implement U4: pass — 62/62 tasks`) and line 186 (`tasks: 62/62 rows checked`) |
| agents | **1** (single-agent fold) | 091's implement-stage record (`.specify/specs/091-auto-git-closeout/checkpoints/09-implement.md`; the whole run is one executor) |
| minutes | **116** | Cited from `requirements.md` § Overview / SC-006 / line 179 and `.specify/memory/features/093.md` line 5, which record the 091 measurement "62 任务、单代理、116 分钟"; the 091 spine in this tree does not itself carry the duration field, so the figure travels as the spec's dated citation of the 091 run and is **not** re-measured here |
| wall-clock per unit | `not_evaluated` | 091 did not produce per-unit durations |

**Concurrency side (this feature's own run)**: `effective: not_evaluated` with reason code
`mechanism-not-yet-landed` — see `notes/coordination-report.md`. The comparison is therefore a
citation pair, not a speedup claim: the serial baseline is 091's recorded fact; the concurrent
reading does not exist yet, and writing one from an estimate or from `0` is forbidden (SC-006,
FR-008).

**Reading chain**: `requirements.md` line 19 / line 179 / SC-006 (owner of the citation) →
`.specify/memory/features/093.md` line 5 → 091's state spine and checkpoint (owner of the task and
agent counts). No second copy of these numbers is introduced anywhere else.
