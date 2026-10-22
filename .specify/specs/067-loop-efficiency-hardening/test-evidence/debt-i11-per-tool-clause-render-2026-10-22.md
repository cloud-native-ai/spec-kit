# FB-06 dated debt record — test_i11_channel_two_mirrors_and_per_tool_copies — 2026-10-22

- **failing pinned test**: `tests/contract/test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies`
- **predates this scope**: yes — present in the pre-change baseline failure set
  (`baseline-failures-2026-10-22-implement-start.txt` line 33, 83-name FB-01
  authority); not introduced by any 067 implement part.
- **observed mechanism (2026-10-22, post-sync rerun)**: the agents→
  `.specify/agents/templates` mirror-pair half of C-11 is fixed by the T023
  engine sync (`1d40ebeb`); the residual failure is the per-tool agent tree
  arm — e.g. `.claude/agents/skill-verifier.md` renders the fast-fail clause
  with the runtime path `.specify/shared/guidelines/fast-fail.md` while the
  pin compares the clause interval byte-for-byte against the owner DOC's
  `shared/guidelines/...` spelling. The runtime rewrite is the established
  render semantics for per-tool copies, so the pin reads as legally moved
  (stale-pin), but the three-way ruling (pin update with rationale /
  mechanism fix / keep registered) belongs to the T025-class per-name triage,
  whose files are outside this part's write surface.
- **chosen path**: registered — fix before close via the per-name triage task
  that owns `test_fast_fail_discipline.py` rows; this record never claims
  green (FB-06). The test is NOT deleted (FB-07).
- **risk if unresolved at closure**: one in-register baseline name stays red;
  SC-008 closure diff must carry it as a known name, not a NEW one.

## Resolution (2026-10-22, T025-class triage, part F)

Resolved as `pin-updated+rationale` — the anticipated T025-class ruling. The per-tool arm now
compares each rendered copy's clause interval against the **engine-rendered owner literal**
(`specify_cli.rewrite_paths(owner)`, the recorded owner of the `shared/` → `.specify/shared/`
render rewrite), preserving exact byte-identity strength; the mirror arm keeps raw byte
identity. Fix lands in the part F triage commit; the triage row for the name is updated in
place (one row per name, V-E5-1). This record remains as the dated history of the registered
interval; it no longer represents an open debt.
