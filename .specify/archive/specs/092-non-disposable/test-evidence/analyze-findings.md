# Analyze findings — 092 (2026-11-09, read-only)

1 CRITICAL · 8 HIGH · 13 MEDIUM · 2 LOW. Repair phases: contracts 8, plan 6, tasks 5, requirements 3, EP+quickstart 1, team 1.

| id | Sev | finding | owner stage |
|---|---|---|---|
| F-1 | HIGH | FR-062 cited by C-206 but its real carrier is C-107/DoD-2; move the citation | contracts |
| F-2 | HIGH | shift-list granularity three numbers (12 rows / 15 entries / 19 ids), none owned | tasks |
| F-3 | CRITICAL | `Planned` vs closure `accept` (corpus A3) not detectable: C-202's state domain lacks Planned | contracts |
| F-4 | HIGH | FR lane 57/65: 4 FRs only need citation adds (030/046/063/065), 4 are truly unowned (050/051/057 + 064-iv) | tasks+contracts |
| F-5 | HIGH | FR-050/051/057 have no contract clause | contracts |
| F-6 | MEDIUM | FR-064(iv) "owner page keeps a Constitution relation section" has zero task row | tasks |
| F-7 | HIGH | A3/A4/A5/A6 classes not closed by C-203 (object is only verification.md; A6's evidence is requirements.md) | contracts |
| F-8 | HIGH | 8 references to nonexistent clauses C-028/C-016 in quickstart/plan/tasks | plan+tasks |
| F-9 | MEDIUM | plan Source Code misses surfaces feature-ref lists (DoD-1 references it) | plan |
| F-10 | HIGH | tier-II handoff marker has no contract clause | contracts |
| F-11 | MEDIUM | G2 classified as deferral-marker on one page and superseded-live on another | plan |
| F-12 | MEDIUM | four-stage vs Steps 1–6 wiring gap; execute has no step number; history.md still says Steps 1–6 | tasks+contracts |
| F-13 | HIGH | `--scope`/shard naming two readings; C-606 shard-of-files vs category conflict with C-102 | contracts |
| F-14 | MEDIUM | empty-surface exit code stated three ways | requirements+contracts |
| F-15 | MEDIUM | action count vs option count (`--roots`/`--emit-categories` outside the verdict domain) | contracts |
| F-16 | MEDIUM | manage-history SKILL named by two packages | plan |
| F-17 | MEDIUM | Constitution Check XI cites wrong FRs (058/054 → 056/045) | plan |
| F-18 | MEDIUM | data-model Fact Owners anchors nine facts to one heading; owner page absent | plan/data-model |
| F-19 | HIGH | DoD-3/GATE-5 ("FR lane empty") currently unreachable | tasks |
| F-20 | MEDIUM | DoD-4's 15 markers contradict the 12-row shift list; corpus rows not re-verified | plan/tasks |
| F-21 | MEDIUM | SC-014 baseline has three readings (4345/4352/4357) plus today's 4389, none designated | plan |
| F-22 | MEDIUM | `.specify/.tmp` ignore match and `history/.work` ignore unverified (zero-write legs depend on them) | plan EP+quickstart |
| F-23 | MEDIUM | C-505's predicate source does not cover `## Clarifications` | contracts+requirements |
| F-24 | LOW | FR-041 "history-dir-shaped" is circular | requirements |
| F-25 | LOW | team.md forbidden list contradicts P6's repair territory | tasks/team |

Two decisions reserved for the owner page, not implement: F-3's state×verdict contradiction table, and F-13's shard subject (files vs categories).
