# Contract — Observation, Promotion and Traceability

**Path**: declared in `shared/best-practices/README.md`; this file is the design face. Guard pinning: `tests/contract/test_general_best_practices.py` leg (d).
**Rule owners cited, never restated**: the feedback record shape and store disposition — `scripts/python/feedback-utils.py` (its `--help` is the action contract) and the feedback workflow owner; the promotion discipline — `shared/guidelines/knowledge-promotion.md`; entry shape — `contracts/entry-shape.contract.md`; category ownership — `contracts/manifest.contract.md`.

**C-301** Observation form.

A development observation is recorded through the existing feedback engine action `record`; its notes carry the literal [[STR-001]] marker and exactly one category owner-file stem — [[STR-002]], [[STR-003]], [[STR-004]] or [[STR-005]] without the `.md` suffix. The convention adds no feedback field, action or store; the observation itself is not written into the module. (FR-004, FR-007(d))

**C-302** Promotion rule.

An observation becomes an entry only when it is proven general — it recurs, or one explicit user correction establishes it. Promotion follows `shared/guidelines/knowledge-promotion.md` and lands the entry in the owner file named by the observation's stem, obeying C-201. Promotion MUST NOT rewrite the observation record, add a feedback state, or create a parallel promotion ledger. (FR-004)

**C-303** Traceability.

A promoted entry MUST carry a `**来源**` bullet naming at least one of: the feedback entry ID, a commit hash of at least seven hex characters, or a quoted session utterance. The same bullet MUST state the generality basis — recurrence or one explicit user correction. The seed is exempt (C-204). (FR-004, FR-007(b))

**C-304** Single mechanism.

The module MUST NOT declare or carry a second engine, store, renderer or index. The mechanism is reached only by pointer to the existing feedback and memory / knowledge-promotion owners. The guard's mechanical reading is: no file named `best-practices.py` or `best_practices.py` exists under `scripts/python/`. Textual second-mechanism claims are review's judgement, not the guard's. (FR-004, FR-007(d), SC-003)

**C-305** Rule ownership stays with the owners.

The manifest cites the feedback action, the marker convention and the promotion owner by path; it MUST NOT restate the feedback store's disposal rules, the promotion threshold or any owner enumeration. (FR-004)

**C-306** Red line.

A clean run MUST NOT append hollow entries. Numbers and evidence in an entry MUST be real; fabricated values are a review rejection. (FR-004)