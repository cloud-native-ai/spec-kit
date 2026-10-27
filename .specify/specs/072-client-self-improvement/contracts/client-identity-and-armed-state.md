# Contracts: Client identity & armed state (C-1…C-9)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns how "this is a client project" is judged (by reference to the existing hat owner), how the three-valued armed state is resolved and disclosed, and how client units and client entries are named and scoped. The hat criterion itself, the probe registry, and the feedback engine are cited, never redefined.
**Pinned by**: `tests/contract/test_client_armed_state.py` (planned), `tests/contract/test_client_capture.py` (planned)
**Measures**: SC-002, SC-003

**C-1**: The client/framework judgement is made only by the existing hat owner — `.specify/shared/definitions/dogfooding-definitions.md` § 2.1 (root ownership of `templates`, `skills`, `shared`, `scripts`, `src/specify_cli`). This feature defines no second criterion, does not let a `feedback/` directory participate in the judgement, and does not relax the test because a directory "looks like" a framework directory. The capture step and the digest report both read this verdict, never re-derive a variant of it (FR-001, SC-003).

**C-2**: The armed state is an explicit three-valued fact resolved once per run and reused unchanged for the whole run: caller-specified client unit first, then the unique external probe object in the store, then every other case. The three values are a closed set: armed (`client-channel-armed`), unarmed (`client-channel-unarmed`), ambiguous (`client-unit-ambiguous`) (FR-002, SC-002).

**C-3**: Existence of an external probe object is a necessary condition for armed. A caller-specified unit only disambiguates; it never waives the probe check. A specified unit with no matching external probe object resolves to unarmed (`client-channel-unarmed`), and the one-time guidance names probe injection for that unit as the preparation action (FR-002, FR-009, SC-002).

**C-4**: When the probe registry is unavailable (an un-upgraded `.specify/` runtime), the state resolves to unarmed (`client-channel-unarmed`), the capture step MUST NOT call the record action at all, and no legacy entry without `kind`/`slice` is written — such an entry would be routed as a framework entry by the existing routing and is a silent leak path. The one-time guidance points at re-initializing or upgrading `.specify/` (FR-002, FR-009, SC-002).

**C-5**: When the store holds more than one external probe object and the caller specified no unit, the state resolves to ambiguous (`client-unit-ambiguous`). The run MUST NOT guess, MUST NOT rotate, and MUST NOT pick a most-recently-used unit; only an explicit unit parameter resolves the ambiguity (FR-002, FR-009, SC-002).

**C-6**: The review command's optional unit parameter has the literal name `--client-unit` and a value grammar closed at `custom:<owner>/<name>`. A malformed value produces one disclosed skip line naming the expected grammar, writes zero entries, and does not block the review run. The parameter disambiguates the armed state and adds no command surface (FR-002, FR-026, SC-002).

**C-7**: A client finding is recorded only against a `custom:<owner>/<name>` unit with unit type `custom-unit`. The unit id families `/speckit.<command>` and `skill:<name>` are rejected for client findings: in a client project they either match no probe object (the engine refuses the record) or resolve as framework-internal units (the entry would be routed upstream). The Dogfooding Loop B recipe in `shared/guidelines/dogfooding.md` is rewritten to the `custom:` form with this reason stated; the rest of Loop B is unchanged (FR-003).

**C-8**: A client entry's scope is fully determined by the existing three fields and the existing one-unit-one-run semantics: `kind: external`, `slice: host-custom`, the `custom:` unit, and one run. This feature adds no fourth scope field, coins no new entry-id family, and never lets one entry belong to two units or two runs (FR-004, SC-003).

**C-9**: The armed state is resolved by counting external probe objects in the probe registry via the probe engine's machine-readable output; the resolution uses no hand-maintained list and no inference from entry history. The probe registry itself is not modified by this feature (FR-002, FR-027).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1 | FR-001 | SC-003 | capture step + digest report |
| C-2 | FR-002 | SC-002 | capture step |
| C-3 | FR-002, FR-009 | SC-002 | capture step |
| C-4 | FR-002, FR-009 | SC-002 | capture step |
| C-5 | FR-002, FR-009 | SC-002 | capture step |
| C-6 | FR-002, FR-026 | SC-002 | command template + script |
| C-7 | FR-003 | — | dogfooding guideline + engine grammar |
| C-8 | FR-004 | SC-003 | entry schema |
| C-9 | FR-002, FR-027 | — | probe engine citation |
