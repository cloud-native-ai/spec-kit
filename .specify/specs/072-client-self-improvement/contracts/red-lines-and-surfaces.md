# Contracts: Red lines, command surface & verification (C-51…C-62)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns what must not change: the four feedback red lines, the predecessor feature's closed surfaces, the command surface, the two-hats edit surface, client neutrality of shipped text, and the fixture-based verification duty. Existing tests and pins are named, not modified, by this plan.
**Pinned by**: `tests/contract/test_client_capture.py`, `tests/contract/test_client_armed_state.py` (planned); existing guard suites listed in C-61
**Measures**: SC-006, SC-007

**C-51**: The four feedback red lines are preserved and apply unchanged to client entries: the framework-side target stays the framework itself and the client-side target stays this project (the two-side closure of FR-012); feedback stays fully optional user data — no flow blocks, re-prompts, or degrades over unprocessed feedback; transmission stays zero-automatic, with manual delivery of a package as the only legal path; the local-workaround value is unchanged (FR-024).

**C-52**: This feature adds no network call, no external service, no new dependency, and no resident process, for both the framework repository and client projects (FR-024, FR-029).

**C-53**: The predecessor feature's closed surfaces stay in force: the code-segment record's form and rotation, the receipt's exit-code alphabet and field block, the report's code-subsection field list, the review command's closing-step set, and the per-run three-unit census are preserved verbatim. The single authorized amendment to any of them is the step enumeration of C-10 (FR-025, SC-007).

**C-54**: The predecessor feature's open recommendation items stay open: this feature neither implements nor depends on them, and the capture counts stay opinion-level counts taken from the summary command, independent of the receipt's file-level distinction between non-code and unreviewed (FR-025).

**C-55**: No `/speckit.*` command is added and no command-line entry face is added beyond the step-5 subcommand of C-11 and the opt-in output flag of C-17. The existing entries carry their segment: the review command carries capture (through its code segment) and accepts the optional `--client-unit` parameter; the feedback command carries digest, carrier assignment, and metric reporting; the improvement command carries the client-subject loop. If implementation finds an entry genuinely cannot carry its segment, the gap is reported as a decision item and no command is improvised (FR-026).

**C-56**: The edit surface is the framework sources only: skill bodies and skill-side references, command templates, shared owner documents (Dogfooding guideline, self-improvement definitions and workflow, feedback step), command reference docs, the two engine files, and contract tests. Runtime projections (per-tool command copies, `.specify/` mirrors) are produced by the existing regeneration and mirror scripts, never hand-edited. The probe registry is not touched by this feature; if implementation discovers a registry change is unavoidable, the existing compile-then-sync order runs first and the deviation is reported (FR-027).

**C-57**: Surfaces shipped with the framework stay client-neutral: new text references no framework-project spec key, feature number, or registry entry, and a reader in a client project needs no access to the framework repository to understand it. The two existing negative assertions — a client project's own feedback is never routed upstream, and the hat criterion tests framework source directories rather than runtime mirrors — are kept verbatim, and the total assertion count of the guarding suites only grows (FR-028, SC-006).

**C-58**: Client-side behavior is verified in a simulated client project — a fixture repository with no root-level framework source directories and a `.specify/` runtime installed from the framework — never by framework-repository self-testing, because the framework repository takes the other hat branch and would leave the whole client path unexecuted. Five behavior groups each carry deterministic checks: capture, the three-valued armed state, package exclusion, the client-subject loop, and read-built metrics. The same flow against a framework-hat twin fixture proves the other branch adds no external entry (FR-029, SC-006).

**C-59**: The fixture is built from a temporary git repository plus a minimal installed `.specify/` runtime (the existing engines, the probe definitions, and the feedback store directory), invoked by absolute engine paths with an explicit workspace root; the review script runs with the fixture as working directory. Hat predicate coverage goes both ways: client fixture (five source directories absent) and framework-hat twin (five source directories present) (FR-029, SC-006).

**C-60**: This feature rewrites no history: no existing review report or feedback entry is modified, no earlier feature is backfilled, and the legacy monolithic store, if present in a client project, is only ever read (FR-029, FR-020).

**C-61**: No existing contract assertion is deleted, weakened, or semantically drifted. The named guard suites stay green with assertions only added: the predecessor feature's six new suites, the expression-compatibility C-5 frozen hash, the review-P1 loop suite, and the feedback/probe contract families. Any change an implementation believes unavoidable requires a written compatibility plan, a justification, and a non-precedential declaration in the feature detail, and this clause is never cited as a basis for a second exception (FR-025, SC-006, SC-007).

**C-62**: The engine additions are bounded to exactly two faces on existing engines: one read-only `client-metrics` action on the feedback engine (C-47) and one `capture` subcommand plus one opt-in `--format json` flag on the code-review script (C-11, C-17). No new engine, store, ledger, scoring system, or id family is created (FR-022, FR-026, FR-027).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-51 | FR-024 | — | red lines |
| C-52 | FR-024, FR-029 | — | scope sweep |
| C-53 | FR-025 | SC-007 | predecessor closed surfaces |
| C-54 | FR-025 | — | open items |
| C-55 | FR-026 | — | command surface |
| C-56 | FR-027 | — | two-hats edit surface |
| C-57 | FR-028 | SC-006 | client neutrality |
| C-58 | FR-029 | SC-006 | fixture verification |
| C-59 | FR-029 | SC-006 | fixture construction |
| C-60 | FR-029, FR-020 | — | no history rewrite |
| C-61 | FR-025 | SC-006, SC-007 | guard suites |
| C-62 | FR-022, FR-026, FR-027 | — | engine bound |
