# Contract — Observation, Promotion and Traceability

**Path**: declared in `shared/best-practices/README.md`; this file is the design face. Guard pinning: `tests/contract/test_general_best_practices.py` leg (d).
**Rule owners cited, never restated**: the feedback record shape and store disposition — `scripts/python/feedback-utils.py` (its `--help` is the action contract) and the feedback workflow owner; the knowledge-recording obligation and emphasis escalation — `shared/guidelines/knowledge-promotion.md`; **the promotion procedure and generality criterion — this module's manifest `shared/best-practices/README.md` § 逐步积累机制, for which this contract is the design face**; entry shape — `contracts/entry-shape.contract.md`; category ownership — `contracts/manifest.contract.md`.

**C-301** Observation form.

A development observation is recorded through the existing feedback engine action `record`. The literal [[STR-001]] marker and exactly one category owner-file stem — [[STR-002]], [[STR-003]], [[STR-004]] or [[STR-005]] without the `.md` suffix — are written into the record's `--review` text; the record shape, its remaining arguments and the store disposition stay with the engine's `--help` contract. Identity convention: an observation made within a framework command or skill run uses that run's unit id and type (`/speckit.<command>` + `command`, or `skill:<name>` + `skill`) and the run's id as `--run-id`; an ad-hoc observation with no such run uses `--unit-id custom:best-practices/observation --unit-type custom-unit --run-id bp-<yyyy-mm-dd>-<slug>`, and a workspace carrying the probe registry first needs that custom unit's external probe (`probe-utils.py --action probe-inject`, an obligation owned by the probe system). The convention adds no feedback field, action or store; the observation itself is not written into the module. (FR-004, FR-007(d))

**C-302** Promotion rule.

An observation becomes an entry only when it is proven general — it recurs, or one explicit user correction establishes it. The manifest's 逐步积累机制 section **owns** this promotion procedure and this generality criterion; promotion follows that procedure and lands the entry in the owner file named by the observation's stem, obeying C-201. Promotion MUST NOT rewrite the observation record, add a feedback state, or create a parallel promotion ledger. (FR-004)

**C-303** Traceability.

A promoted entry MUST carry a `**来源**` bullet naming at least one of: the feedback entry ID, a commit hash of at least seven hex characters, or a quoted session utterance. The same bullet MUST state the generality basis — recurrence or one explicit user correction. The seed is exempt (C-204). (FR-004, FR-007(b))

**C-304** Single mechanism.

The module MUST NOT declare or carry a second engine, store, renderer or index. Observation recording is reached only by pointer to the existing feedback engine; the promotion procedure and generality criterion are the manifest's own declared rules (C-302); no memory, knowledge-promotion or other parallel mechanism is instantiated. The guard's mechanical reading is: no file named `best-practices.py` or `best_practices.py` exists under `scripts/python/`. Textual second-mechanism claims are review's judgement, not the guard's. (FR-004, FR-007(d), SC-003)

**C-305** Rule ownership stays with the owners.

The manifest cites the feedback action and the knowledge-recording obligation owner by path; it MUST NOT restate the feedback store's disposal rules, the knowledge-promotion owner's emphasis threshold or any owner enumeration. The promotion procedure and the generality criterion are this module's own rules — the manifest declares them as their owner, and that declaration is ownership, not restatement. (FR-004)

**C-306** Red line.

A clean run MUST NOT append hollow entries. Numbers and evidence in an entry MUST be real; fabricated values are a review rejection. (FR-004)