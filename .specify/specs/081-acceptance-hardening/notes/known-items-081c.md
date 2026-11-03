# Known Items — Feature 081, slice 081c

**What this file is**: findings recorded during 081c that are not fixed in this slice. A known item is
owned later; it is not an acceptance claim and not a substitute for its own severity.

| # | Finding | Disposition | Owner / mechanism |
|---|---------|-------------|-------------------|
| F15 | `this-slice` carriers do not survive their own slice's archive | **recorded; per-slice re-point is the interim rule** | `plan.md` § Inherited Blockers resolves a `task:<T-ID>+test:<path>` carrier against the **live** `tasks.md`. When 081b closed, its `tasks.md` became `tasks-081b.md`, so IB-006's `task:T005` and IB-004's `test:`-only later-slice carrier no longer described the live file. The 081c tasks stage re-pointed both to live rows (IB-004 → `task:T004+…`, IB-006 → `task:T012+…`) and measured the gate green. The mechanism has no archive notion; two principled fixes are possible — carriers name an explicit slice id resolved against `tasks-<slice>.md`, or a `resolved-in-earlier-slice` reading is introduced (the backward twin of `inherited-later`). Choosing either revises C-17's semantics, so it is **not** decided in 081c. Until then, every slice's tasks stage re-points the live rows and records the re-point. |

## Why this does not block the slice

The carrier's obligation is "the measurement is taken over by a mandatory row of the slice being
judged". Re-pointing preserves exactly that obligation and is measured by the gate; the underlying
schema question is about **which slice** a carrier may name, not about whether the measurement runs.
The 081c gate and closure payload are the evidence that the interim rule holds for this slice.
