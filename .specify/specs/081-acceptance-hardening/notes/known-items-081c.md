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

## Post-r2 M/L cleanup (2026-11-03)

The r2 gate passed with zero open C/H. The six new r2 M/L rows and the round-1 M rows with a
one-line fix were repaired in the same pass: R2-F-10 (leg (d) now names the derivation owner and
asserts no restatement), R2-F-11 (leg (k) names the countable dimension headings), R2-F-12 (the two
surviving sole-ownership sentences qualified), R2-F-13 (the content-definition vs field-declaration
split stated), R2-F-14 (legs j/k pointed from the traceability cells), R2-F-15 (DoD-6 names both
census pins), R2-F-16 (the 56-advisory reading marked dated, 69 recorded), F-11 (extractor narrowed
in T009), F-12 (`SEGMENTS` four-concept update in T010), F-13 (`two segments` sweep scope defined),
F-14 (`requirements.md` added to plan § Documentation), F-15 (the implementation segment quotes the
record; it never re-judges it), F-16 (the census no longer cites the wrong FR), F-17 (DoD-7 uses
"carrier resolves", not "disposition resolved"), F-18/F-19 (missing `blockedBy` tags),
F-20 (a user waiver does not lift ARC's zero-pass refusal), F-21 (GW-14's docs-page limb scoped),
F-24 (the refusal never downgrades a `Ready for Review` claim).

Deferred as L-level hygiene, recorded rather than fixed: **F-22** (an obligation re-homed into DoD-6
and T009 without stating the carrier was adjudicated) and **F-23** (the `review-composition` probe's
grep line numbers in the checklist's reading list need refreshing). Neither changes a verdict, and
both are documentation-only.
