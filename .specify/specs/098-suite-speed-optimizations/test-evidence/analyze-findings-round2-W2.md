# Analyze Findings — 098 Suite Speed Optimizations — Wave W2 (Round 2)

- **Stage**: analyze round 2 (post-repair re-gate; concurrent wave W2) · **Date**: 2026-11-10
- **Read domain (9 files, mutex)**: `plan.md`, `data-model.md`, `quickstart.md`,
  `contracts/{tier-selection,slow-membership,parallel-consistency,scan-cache,event-wait,inprocess-conversion}.contract.md`
- **Method**: analyze-artifacts round-2 full-set detection passes A–G/I over the plan-stage design artifact set;
  every round-1 W2 finding re-adjudicated; severity per the four-tier heuristic and its propagation-surface cap;
  strictly read-only; nothing repaired.
- **Authority**: the feature spec directory; `.specify/constitution.md` v1.19.0 (principle XX read at
  lines 427–451); the analyze-artifacts skill and its two references; the rule owners named by the skill
  (`one-source-of-truth.md`, `test-execution-efficiency.md`). Rule sources were consulted as authority, not
  as artifact read scope.
- **Wave scope exclusion (no claim made)**: `requirements.md`, `tasks.md`, `research.md`, `checklists/*`,
  `.specify/features*`, the constitution pass (D), the checklist pass (H) and the feature-registry pass (G)
  lie outside this wave's read domain and are owned by the sibling waves. The coverage accountant was not
  re-run; the driver's post-repair reading (`test-evidence/analyze-repair-gates-2026-11-10.txt` §7) is
  consumed as evidence: `status: baseline-missing` is the expected pre-T002 state, `[fr-uncovered] pass —
  27 of 27`, claimed clauses 68.

## 0. Round-2 verdict (this wave)

- **New findings: 5** — CRITICAL 0 · HIGH 0 · MEDIUM 3 · LOW 2.
- **Round-1 W2 residue: 12** — fixed 1 (W2-10) · rejected 1 (W2-09, round-1 claim not supported on re-read) ·
  deferred 10 (open MEDIUM/LOW; not in the repair round's C/H scope).
- **C/H repair verification in this read domain: pass** — every round-1 C/H whose repair anchor lands in
  this domain shows the repaired text (W1-01, W1-02, W1-08/09, W1-17, W1-21, W3-01, W3-11). Two residual
  observations are filed as new W2-15 / W2-17, not as reopens of those C/H findings.
- **Validation wave**: none dispatched by this wave — 0 new CRITICAL/HIGH; MEDIUM/LOW skip validation per the
  skill. The driver's merge/validation wave remains authoritative for any cross-wave C/H.
- **Gate impact from W2 alone**: no C/H blocker; the 3 new MEDIUM + 2 new LOW are advisory.

## 1. New findings (round 2)

| id | severity | anchor | fact | suggested owner |
|----|----------|--------|------|-----------------|
| W2-13 | MEDIUM | `plan.md:135` vs `plan.md:217` + `quickstart.md` scenario list | The plan's Project Structure block says quickstart has "scenarios S-0…S-11", while the same plan's Phase-1 summary says "14 scenarios S-0…S-13" and quickstart actually carries S-0…S-13 (14); one count is stale in a copy. | `plan.md` (via `/speckit.plan`) |
| W2-14 | MEDIUM | `contracts/tier-selection.contract.md` C-001 vs C-003/C-010; `data-model.md` E-1 | C-001 declares exactly two tiers (`fast`/`full`) while the machine-consumed `tier` field has three values (`fast`/`full`/`caller`) per C-003/C-010 and E-1; no clause says whether `caller` is a tier state or the absence of a tier. | tier-selection contract + data-model E-1 |
| W2-15 | MEDIUM | `quickstart.md` S-10 (second command) vs its Proves text and `plan.md` WP-9 item 5 | S-10's second command counts **added** `@pytest.mark.parametrize` lines (`^\+\s*@pytest...`), while the stated MUST is "parametrize removals MUST be zero"; the command cannot detect a removal, so the scenario does not prove the claim it states. | `quickstart.md` S-10 |
| W2-16 | LOW | `plan.md:79` (Constitution Check XXI) vs `contracts/event-wait.contract.md` C-004; `data-model.md` E-4 | Row XXI cites event-wait C-004 as the evidence for the `--now` option being help-documented / zero-side-effect, but C-004 owns only the ordering use of the injected clock; the `--help` documentation obligation lives in E-4 (and requirements), not C-004. | `plan.md` Constitution Check XXI |
| W2-17 | LOW | `plan.md:78` (Constitution Check XX evidence cell) vs `plan.md` §Summary no-restatement sentence and constitution §XX | The row's evidence parenthetical "(no selection shrink, skip, or retry)" compresses three of the owner's / constitution's prohibited means, while §Summary says "this plan does not restate that list"; a residual drifting copy that contradicts the plan's own claim. | `plan.md` Constitution Check XX |

## 2. Round-1 W2 residue (round-2 re-adjudication)

| id | round-1 severity | status | disposition and evidence |
|----|------------------|--------|--------------------------|
| W2-01 | MEDIUM | deferred (open) | Not in the repair round's C/H scope. The three spellings persist: plan Summary row 2 and WP-9 item 1 run the baseline slot with `--full`; S-13's baseline command omits `--full` while its premise says the slot command includes it; C-015/C-016 anchor the baseline at implement-start. In-domain addendum: S-12 consumes `/tmp/full-baseline.txt` with no producing command in the same scenario; the implement-start collection reading remains an implicit deliverable. |
| W2-02 | MEDIUM | deferred (open) | C-008 still lists `c20` among the five real-corpus callers "converted to consume the payload", while C-006 says `test_c20`'s byte-identity check MUST NOT consume the cache; which `c20` assertions, if any, may consume remains unstated. |
| W2-03 | MEDIUM | deferred (open) | PC-M2 still expects a "recorded-tree identity check" to fail on lists from two trees, while C-012's required evidence fields still carry no tree identity / fingerprint. |
| W2-04 | MEDIUM | deferred (open) | C-004 / CA-M2 still require the copy-isolation mutation to fail, but C-009…C-011 and quickstart S-5 still describe no executed copy-isolation case. |
| W2-05 | MEDIUM | deferred (open) | C-009's guard still asserts `timeout <= 30` at adopted call sites while C-007 / E-5 permit a longer deadline with a recorded reason; a permitted site still turns the guard red. |
| W2-06 | MEDIUM | deferred (open) | S-1/S-4 still pipe raw `--collect-only` / `--names-out` output into `comm` without a sort or summary-line filter; the stated MUST-equal checks still cannot hold as written. |
| W2-07 | MEDIUM | deferred (open) | S-1/S-4/S-12/S-13 still direct scratch to bare `/tmp/...`; plan Constitution row XVII's compliance evidence still covers only research probes. |
| W2-08 | LOW | deferred (open) | E-8 still says "three owner/restatement surfaces" while WP-3 enumerates four rows and S-9 checks both slot rows and both stage-prompt restatements. |
| W2-09 | LOW | rejected | Re-read shows C-007 itself states "The validation run consumes no budget slot and its duration is not an SC-004/SC-005 wall-clock reading"; the trailing `C-010` citation is a redundant adjacent cross-reference to the missing-engine clause, not an ownerless proposition. Round-1 claim not supported. |
| W2-10 | LOW | fixed | `data-model.md` E-1 now says `excluded_slow` = "members of the slow marker excluded by this tier from the caller's selection (0 for `tier=caller` / `tier=full`)", aligning the field rule with its invariant. |
| W2-11 | LOW | deferred (open) | C-007 still defines builder / importlib / `traversals` counting only for `framework-specs-corpus`; the second managed surface `framework-root-inputs` still has no build/count mechanics although C-011's `build_count=1` probe spans managed surfaces. |
| W2-12 | LOW | deferred (open) | C-016 still sanctions recording the anti-measurement (marked set re-merged into the default tier = full selection) while forbidding "a third full run ... for measurement"; the anti-measurement's budget class is still undefined. |

## 3. C/H repair verification (anchors inside this read domain)

| round-1 id | severity | in-domain anchor(s) | round-2 reading |
|------------|----------|---------------------|-----------------|
| W1-01 | CRITICAL | `plan.md` §Summary | §Summary now points to the owner (`test-execution-efficiency.md` §「不可采纳的提速手段」) and keeps only the 098-specific SC-010 increment; no prohibited-means list is restated there. Residual row-XX parenthetical filed as W2-17 (LOW). The requirements-side anchor is outside this domain. |
| W1-02 | HIGH | `quickstart.md` S-10 | S-10's Proves text now names the AST leg (conditional skips, retry-until-green loops) and `test-evidence/forbidden-shortcuts.txt`. Residual command/text mismatch filed as W2-15 (MEDIUM). |
| W1-08 / W1-09 | HIGH | `data-model.md` E-1 | Per-tier exclusion rule present: fast = members in the caller's selection; caller / full = 0 and, for full without caller `-m`, the collection returns to global-full. E-1's rule and invariant now agree. |
| W1-17 | HIGH | `contracts/event-wait.contract.md` C-001 | Six-file closed enumeration present and matches `plan.md` WP-6 items 3–8 and quickstart S-6/S-7. |
| W1-21 | HIGH | `data-model.md` E-5; `contracts/event-wait.contract.md` C-007 | Default 30 s and interval ≤ 0.2 s present; the "existing convention" claim is in requirements (outside this domain) and no longer appears here. |
| W3-01 | HIGH | all six contracts + `plan.md` + `quickstart.md` | All 68 clauses parse as `md-bold-closed` C-001…; zero old-prefix matches in the 9 read-domain files; plan Phase-1 counts and quickstart Proves citations use the new ids; repair gates §8 confirms 68. |
| W3-11 | HIGH | `plan.md` (unchanged); tasks side out of domain | Plan's "no third full run for measurement" and C-007 / C-016 wording remain consistent with the repaired task wording; no plan edit was needed and none was made. |

## 4. Cross-check ledger (zero-finding floor evidence for the clean areas)

- **Contract clause census**: 6 files / 68 clauses — tier-selection 16, slow-membership 9,
  parallel-consistency 12, scan-cache 11, event-wait 10, inprocess-conversion 10; matches `plan.md` Phase-1
  table and repair gates §8 (`md-bold-closed`, 68 total).
- **Renumbering closure**: grep `\b(TS|CA|PC|EW|IC|SL)-\d` over the 9 read-domain files → 0 matches; no
  stale pre-renumbering clause id survives here.
- **Decision-tension structure**: `python3 scripts/python/validate-decision-tensions.py --spec
  .specify/specs/098-suite-speed-optimizations --json` → `status: ok`, 0 errors, 3 records; all six labels
  (`dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form`,
  `expected-sacrifice-unmapped`) pass.
- **Data-model ↔ contract matches**: E-1…E-8 (8 entities) as planned; E-6's 7 boundary classes match
  inprocess-conversion C-002; E-3's two surfaces match scan-cache C-002; E-5's 30 s / 0.2 s match
  event-wait C-007; E-7's appended fields match tier-selection C-010.
- **Quickstart**: 14 scenarios S-0…S-13 present; S-0.1's 8543 matches plan scale; S-0.3's 40 passed matches
  tier-selection C-014 and plan WP-1; every scenario carries its premise list.
- **Work packages**: WP-1…WP-9 present; the six contracts are all represented in the Summary acceptance
  table; SC-001 is not in that table's SC column but is covered by WP-9 item 4 + S-12 / C-015 (no coverage
  gap).
- **FR coverage (sibling-run evidence)**: 27 of 27 FRs cited from clause citation groups; 68 claimed clauses.

## 5. Metrics

- New: 5 (MEDIUM 3, LOW 2; CRITICAL/HIGH 0). Residue: 12 (fixed 1, rejected 1, deferred 10).
  Total findings rows: 17 (≤ 50). Overflow: 0.
- Validation wave: 0 C/H sent; downgrade rate N/A.
- Same-author delegation: not applicable — the artifacts were authored by earlier SDD stages, not by this
  wave.

## 6. Boundaries and fast-fail statement

- No artifact was modified; the only write is this findings file.
- No decision-type anomaly was encountered; no in-passing repair was applied (analysis only).
- Wrap-up engines (Run Determination / Exec Quant / Feedback Record) were not run in this bounded read-only
  wave; stage-level records remain the driver's.
- The read-domain exclusions and sibling-wave ownership stated at the top are the only boundary claims.
