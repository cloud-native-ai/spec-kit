---
id: "20261019T164615Z-instructions-refresh-2026-10-20-rec-into-live-id-register-06"
scope: "session"
source: "/speckit.instructions"
feature: "063-review-p1-governance"
tags: ["instructions", "residual-report", "063-review-p1-governance"]
title: "instructions refresh 2026-10-20: REC- into live ID Register (063 C-12 live leg)"
created: "2026-10-19T16:46:15Z"
summary: "Residual report (targeted partial update, user adjudication routing 063 C-12 live leg through /speckit.instructions). CONVERGED: ID Register — added 'recommendation (REC-…)' to the durable-identifier "
---

Residual report (targeted partial update, user adjudication routing 063 C-12 live leg through /speckit.instructions). CONVERGED: ID Register — added 'recommendation (REC-…)' to the durable-identifier enumeration, single-line +28 B; section now byte-identical to the rendered template (machine snapshot flagged it delta=-28, placeholder=no, project-owned=no). TOLERATED: all other sections (23; tolerance band; no route candidates — largest deltas are placeholder=yes scaffolds excluded from R1, Recurring Operational Lessons 787 B < 4 KB R2 threshold). RECOVERED: none (07-11 backup legacy Resource Registry block = superseded by ## Skills & Tools, attributed not lost). PENDING: (1) budget 37415→37443 B of 32768 B (over by 4675; no R1/R2 candidate per snapshot filters — needs full-reconcile pass or budget revisit); (2) 'Fact, Correctness & Logic Checks' lags template by 403 B (inherited-premises clause missing) — same additive-only mechanism gap, left for next full reconcile per partial-update scope; (3) branch pre-existing failures (45 contract-marked + 9 unmarked, incl. 3 vs the 063 frozen baseline: test_neutrality_budget C-12, test_run_checks C-27, test_user_facing_comprehension_pointers C-14) = bd108d5a mirror-sync debt, zero caused by this edit (stash A/B proven). Mechanism notes: Action 1 setup script blocked by permission classifier under the brief's no-extension wording; documented Warning-level fallback exercised (manual backup instructions.md-2026-10-20-003045 + snapshot table reproduced programmatically). Red→green: test_c12_live_instructions_received_rec_through_the_generator (red-first in 063 verification.md). Commit a8c3c1f0 (instructions file only). Symlinks 9/9 unbroken, REC- visible through each.
