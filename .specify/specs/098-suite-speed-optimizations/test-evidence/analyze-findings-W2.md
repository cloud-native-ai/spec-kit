# Analyze Findings — 098 Suite Speed Optimizations — Wave W2 (Round 1)

- **Stage**: analyze (concurrent wave W2) · **Date**: 2026-11-10
- **Read domain (9 files, mutex)**: `plan.md`, `data-model.md`, `quickstart.md`,
  `contracts/{tier-selection,slow-membership,parallel-consistency,scan-cache,event-wait,inprocess-conversion}.contract.md`
- **Method**: analyze-artifacts detection passes A–G/I over the plan-stage design artifact set, severity per the
  four-tier heuristic; strictly read-only; nothing repaired.
- **Wave scope exclusion (no claim made)**: the skill's step-3 coverage accountant (`account-clause-coverage.py`),
  step-5 **H** checklist pass, **D** constitution pass and **G** feature-registry linkage pass were **not** executed
  in this wave — their inputs (`requirements.md`, `constitution.md`, `checklists/`, `tasks.md`, `.specify/features*`)
  lie outside this wave's read domain and are owned by the sibling waves.

## Findings

| id | severity | anchor | fact | suggested owner |
|----|----------|--------|------|-----------------|
| W2-01 | MEDIUM | `contracts/tier-selection.contract.md` TS-15/TS-16; `plan.md` §Summary row 2 ("both slots run with `--full`") + WP-9 item 1; `quickstart.md` S-13 | The baseline reading is anchored "implement-start" (pre-change; `--full` undeclared then per TS-05), yet WP-9 item 1 runs "the baseline slot with `--full --names-out`" (post-WP-1), plan Summary says both slots carry `--full`, and S-13 shows the flagless command commented "full tier, by construction of the slot command" while its premise says the slot command includes `--full` (WP-3) — three spellings for one measurement invite recording a post-optimization run as the baseline. *(Validator: downgraded HIGH→MEDIUM; the implement-start anchor is forced by TS-15/TS-16 + S-12, defect localized to WP-9.1 / Summary row / S-13 premise.)* | plan.md + quickstart S-13 (via `/speckit.plan` or `/speckit.clarify`) |
| W2-02 | MEDIUM | `contracts/scan-cache.contract.md` CA-08 vs CA-06; `data-model.md` E-3; `plan.md` R-8 | CA-08 lists `c20` among the five real-corpus callers "converted to consume the payload", while CA-06, E-3 and plan R-8 all require `test_c20`'s byte-identity check to stay subprocess and cache-free; no clause states which `c20` assertions, if any, may consume the cache. | scan-cache contract |
| W2-03 | MEDIUM | `contracts/parallel-consistency.contract.md` PC-03, PC-12, PC-M2 | PC-M2 expects a "recorded-tree identity check" to fail on lists from two trees, but PC-12's required evidence fields carry no tree identity/fingerprint, so no specified record or guard can ever detect that mutation. | parallel-consistency contract |
| W2-04 | MEDIUM | `contracts/scan-cache.contract.md` CA-04, §E CA-M2; `quickstart.md` S-5 | CA-M2 must fail "CA-04" (deep-copy isolation), yet neither §D proof duties (CA-09…CA-11) nor S-5's described guard contents include a copy-isolation case — the mutation leg has no executable case to turn red. | scan-cache contract §D + quickstart S-5 |
| W2-05 | MEDIUM | `contracts/event-wait.contract.md` EW-07, EW-09; `data-model.md` E-5 | EW-09's guard asserts `timeout <= 30` at adopted call sites while EW-07/E-5 permit a longer deadline with a recorded one-line reason; a permitted site would turn the guard red, so the contract contradicts itself at the exception. | event-wait contract |
| W2-06 | MEDIUM | `quickstart.md` S-1 (same construction in S-4) | S-1's `comm` comparison consumes raw, unsorted `--collect-only -q` output that also contains pytest's trailing summary line, so the stated MUST-equal check cannot hold as written; no `sort`/summary filter step or sortedness premise is stated. | quickstart S-1/S-4 |
| W2-07 | MEDIUM | `quickstart.md` S-1, S-4, S-12, S-13 vs plan.md Constitution Check XVII | Scenarios direct agent-created scratch to bare `/tmp/...`, while the project's Temporary Directory Discipline requires a sanctioned temp root; plan XVII's compliance evidence covers only research probes, not these scenarios. | quickstart scenarios |
| W2-08 | LOW | `data-model.md` E-8 vs `plan.md` WP-3; `quickstart.md` S-9 | E-8 says "three owner/restatement surfaces" change spelling, while WP-3 enumerates four rows (two slot rows + two stage-prompt restatements) and S-9 checks "both … both" — pin the surface count. | data-model E-8 |
| W2-09 | LOW | `contracts/parallel-consistency.contract.md` PC-07; `plan.md` R-10 | Both cite PC-10 as keeping the closure validation run out of the budget ledger, but PC-10's clause body is the missing-engine xdist shim; the budget proposition has no clause of its own. | parallel-consistency contract (retarget cite) |
| W2-10 | LOW | `data-model.md` E-1 | `excluded_slow`'s rule text ("members of the slow marker inside the caller's selection") conflicts with its own invariant (`tier=full ⇒ excluded_slow=0`); restate as "members the tier excluded". | data-model E-1 |
| W2-11 | LOW | `contracts/scan-cache.contract.md` CA-07 vs CA-02, CA-11; `data-model.md` E-3 | CA-07 defines builder, importlib loading and `traversals` counting only for `framework-specs-corpus`; the second managed surface `framework-root-inputs` has no build/count mechanics although CA-11's `build_count=1` obligation spans managed surfaces. | scan-cache contract CA-07 |
| W2-12 | LOW | `contracts/tier-selection.contract.md` TS-16; `quickstart.md` S-13 | TS-16 sanctions recording an anti-measurement (marked set re-merged into the default tier = full selection) while in the same clause forbidding "a third full run"; the anti-measurement's budget class is undefined. | tier-selection TS-16 |

## C/H validation

- Candidates: W2-01 (HIGH at detection). One independent fresh-context read-only validator, disjoint from the
  detector, re-read the three anchors.
- Verdict: **downgrade → MEDIUM** (implement-start anchor forced by TS-15/TS-16 + S-12; defect localized).
  Downgrade rate: **1/1**. Confirmed CRITICAL/HIGH: **0**.
- Evidence boundary: 086 contract text, `efficiency-model.md`/`stage-prompts.md` and driver slot enforcement were
  unreadable in this wave; no finding here depends on them being read.

## Cross-check ledger (zero-finding floor, evidence that checked areas are clean)

- All 6 contract files present; clause IDs total **68** (16+9+12+11+10+10) — matches plan Phase-1 table exactly.
- `data-model.md` entities **E-1…E-8** match plan's count; E-6 boundary classes (7) match IC-02 verbatim;
  E-3 surfaces match CA-02; E-5 defaults match EW-07; E-7 lines match TS-10/TS-11.
- `quickstart.md` scenarios **S-0…S-13 (14)** match plan's count; S-0.3 "40 passed" matches TS-14/WP-1.
- Plan Summary acceptance table, EP-001…EP-004, WP-1…WP-9 coverage of the six contracts: no uncovered contract
  and no contract clause without a landing work package beyond the rows reported above.
- Scope-file list EW-01 (6 files) matches plan WP-6 items 3–8 and quickstart S-6/S-7.

## Metrics

- Findings: **12** (CRITICAL 0 · HIGH 0 · MEDIUM 7 · LOW 5) · overflow: 0 · rows ≤ 50 limit.
- Remediation is not applied here; proposed owners above, invoked by the user via `/speckit.plan` / `/speckit.clarify`.
