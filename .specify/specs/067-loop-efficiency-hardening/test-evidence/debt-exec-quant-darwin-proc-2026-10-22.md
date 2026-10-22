# Debt — exec-quant engine requires Linux /proc; darwin host cannot resolve — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned tests (7, one family / one root cause)

- `tests/contract/test_exec_quant_engine.py::TestAgentCollection::test_resolved_agent_fields_from_wrapper_host`
- `tests/contract/test_exec_quant_engine.py::TestCredentialDefense::test_engine_masks_credential_shaped_config_values`
- `tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_endpoint_candidates_origin_only`
- `tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_missing_config_face_degrades_to_marker`
- `tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_config_face`
- `tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_per_model_effort_when_set`
- `tests/contract/test_exec_quant_engine.py::TestSizeCap::test_oversized_record_is_field_truncated_and_capped`

## Failure shape

All seven drive the real engine (`scripts/python/exec-quant.py`) through
`run_via_host_wrapper`, which impersonates a host CLI with bash `exec -a qodercli` and relies on
`/proc/<pid>/cmdline` for D8 agent resolution (the helper's own docstring: "deterministic on any
**Linux** host"). `collect_agent()` hard-gates on `if not os.path.isdir("/proc"): return
unresolved`, and the engine exposes no host-name override (no `SPECKIT_HOST`-style env). On this
darwin host `/proc` does not exist, so resolution is always `unresolved` and every quantified
field degrades to `not_evaluated` — exactly what the assertions observe.

## Why not repaired here

1. The blocking surface is the **engine** (`scripts/python/exec-quant.py`) — part F's write
   surface excludes `scripts/` and `src/`.
2. No test-local isolation fix exists that would not fake a pass: the assertions measure real
   host-resolution outcomes; stubbing resolution or skipping on darwin would fabricate the
   evidence the pins exist to collect (forbidden).
3. **Not introduced by this scope**: all seven names are in the pre-stage baseline
   (`baseline-failures-2026-10-22.txt`) and the T007 in-stage baseline; the exec-quant family
   landed with feature 059.

## Repair path (owned elsewhere)

Add a host-override path to the engine (e.g. an env knob consumed by `collect_agent()`) or a
non-`/proc` resolution fallback, owned by the exec-quant feature's flow; then the wrapper tests
pass deterministically on any platform. Until then these seven stay a KNOWN red family for
SC-008 (known names, never new ones).
