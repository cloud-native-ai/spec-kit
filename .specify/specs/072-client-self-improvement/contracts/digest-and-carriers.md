# Contracts: Digest path & follow-up carriers (C-25…C-32)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns how client entries are digested, which follow-up carrier each digested entry receives, and what the digest report states. Path A's atomic cleanup, the packaging engine, and the routing backlog are owned by the feedback skill and engine; they are cited here, never re-specified.
**Pinned by**: `tests/contract/test_client_package_exclusion.py` (planned)
**Measures**: SC-003

**C-25**: Client entries are digested only through the feedback command's existing in-place digest path. This feature adds no second consumption path, no second inventory, and no second cleanup flow. The packaging path keeps excluding `kind: external` entries unconditionally, keeps reporting the excluded count, and gains no switch, parameter, or environment variable that could bypass the exclusion (FR-010, SC-003).

**C-26**: A digested client entry receives exactly one follow-up carrier, drawn from a closed set of three existing mechanisms: the todo command's Park mode (the default landing for free-floating improvement ideas), a new requirements specification (when the finding constrains what this project's source must implement), or one subject loop of the improvement command (when the finding lands on a client artifact that meets the Execution Subject criteria). No fourth carrier is introduced, and no entry is ever assigned two carriers (FR-011).

**C-27**: The three carriers' boundaries and storage locations are owned by their existing owners — the todo-in-context guideline (Park store), the requirements flow (spec creation), and the self-improvement workflow (subject loop). This contract specifies only the must-pick-one rule and cites those owners; it restates none of their content (FR-011).

**C-28**: The two-side target closure is unchanged: framework-side entries remain framework friction only, client code defects are never posted as framework-side entries, framework friction is never registered on client units, and the same observation never appears on both sides. The existing one-directional content refinement (an internal entry may move toward this project, never an external entry upstream) is preserved, and every move is reported in the digest (FR-012, SC-003).

**C-29**: The digest report of a client project carries at least three existing facts: this run's hat and armed state plus how the armed state was resolved; the entry count and disposition of each side; and the readings of the four loop metrics. The digest keeps the existing atomic-cleanup semantics, and metric computation is never merged into the cleanup action (FR-013, FR-021).

**C-30**: The carrier assignment of each digested external entry is written as one routing-backlog row naming exactly one carrier and is listed in the digest report. An entry whose carrier cannot be decided is reported as undecided and left for the next digest, never silently dropped (FR-011, FR-013).

**C-31**: When a client unit disappears from the probe registry, its existing entries stay readable and are never rewritten, deleted, or re-attributed; the digest reports the resolution failure for that unit as a named finding (FR-010, SC-003).

**C-32**: When both sides are non-empty (only possible in a client project), the digest runs both sides in the same session and reports both; one side is never silently dropped to keep the run short (FR-013, SC-003).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-25 | FR-010 | SC-003 | digest path + package engine |
| C-26 | FR-011 | — | carrier closed set |
| C-27 | FR-011 | — | owner citations |
| C-28 | FR-012 | SC-003 | two-side closure |
| C-29 | FR-013, FR-021 | — | digest report |
| C-30 | FR-011, FR-013 | — | routing backlog |
| C-31 | FR-010 | SC-003 | vanished unit |
| C-32 | FR-013 | SC-003 | both-sides rule |
