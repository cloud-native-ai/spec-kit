# Quickstart — Decision Governance（107-decision-governance）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**Reader**: framework maintainer or downstream project maintainer who must author, transmit, archive or audit one decision item.

> **Pre-implementation status (2026-11-25, plan stage)**: the checker `scripts/python/validate-decisions.py`, the owner page `shared/definitions/decision-definitions.md` and the instruction section do not exist yet — they are this feature's deliverables. Examples below are split into (A) commands that **were executed in this stage** and are green today, and (B) examples whose surfaces land with the implementation. Each (B) group states, per example, the premises it rests on and the contract test that will pin it — a file-level disclaimer does not vouch for unlisted examples. No (B) expected result is asserted as current output.

## Scenario 1 — Author one ai-autonomous decision record (planned surface)

1. Write the record into its producer's existing carrier (e.g. a checkpoint or a run report) using the record grammar owned by `shared/definitions/decision-definitions.md` § Decision Record: heading `### D-NNN — <title>`, then one `- **<field>**: <value>` line per mandatory field, options as indented sub-lines, four timestamps (`created_at` + three `…-at` lines carrying ISO-8601 UTC or `not-yet`).
2. Register the id in `.specify/register.md` (one row or a carrier+range grouped row) at birth.
3. Validate:

```bash
python3 scripts/python/validate-decisions.py --action records --spec .specify/specs/107-decision-governance
```

**Premises (per example)**: the checker path exists; `--action records` scans the spec's formal carriers; exit `0` = pass / `1` = a documented check failed / `2` = input error. **Pinned by**: `tests/unit/test_validate_decisions.py::test_cli_surface` and `tests/contract/test_decision_governance_contracts.py::test_record_line_grammar` (authored in the implement stage).

## Scenario 2 — The two production accidents are blocked (planned surface)

1. Same-name conflict, no locator: a record carrying `same_name_conflict: true` with an empty `resource_locator` → M-02 red; add business resource group + region id → green.
2. Registered abbreviation: a record whose structured subject matches a glossary variant whose canonical exists → M-08 red; replace with the full name → green.

```bash
python3 scripts/python/validate-decisions.py --action records --spec .specify/specs/107-decision-governance --json
```

**Premises**: the fixture pair lives under `tests/fixtures/decision-governance/m02/` and `m08/`; the glossary carries at least one registered variant row (today: measured 0 decision-related rows — the guard fixture stubs the glossary input). **Pinned by**: `tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green` and `::test_m08_registered_variant_red`.

## Scenario 3 — Closed option set (planned surface)

Build a fixture decision with an empty set, duplicate labels, `other` without `path`, and a missing element; each run of the checker reports M-03; complete the five elements and the `path`, then M-03 is clean.

```bash
python3 scripts/python/validate-decisions.py --action records --spec .specify/specs/107-decision-governance
```

**Premises**: forward+reverse fixtures under `tests/fixtures/decision-governance/m03/`. **Pinned by**: `tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples`.

## Scenario 4 — Decision transmission round-trip (planned surface)

1. Build the dispatch payload with a `decision_block` (decision id, class, chosen option full label, implementation constraints, archive pointer) — a decision-backed dispatch without it is refused (exit `1`).
2. The child returns an acknowledgement plus an `implementation_receipt`; a receipt missing an item is reported (exit `1`).
3. Chain check:

```bash
python3 scripts/python/validate-decisions.py --action payload --fixture tests/fixtures/decision-governance/m06/
python3 scripts/python/validate-decisions.py --action chain --fixture tests/fixtures/decision-governance/m07/
```

**Premises**: `--fixture` accepts a fixture directory holding the payload/return pair; the chain action reads record+dispatch+receipt fixtures; the checker never mutates the record. **Pinned by**: `tests/contract/test_decision_governance_guards.py::test_m06_block_completeness`, `::test_m05_receipt_reverse_samples`, `::test_m07_chain_three_segments`.

## Scenario 5 — Audit reconstruction (planned surface)

Given a fixture decision set spanning four carrier types (requirements, plan, checkpoint, run report), reconstruct FR-014's fields from the register + carriers only; delete one field or break one evidence pointer → M-01/M-04 red.

```bash
git -C . diff --name-only 08b59695c..HEAD -- .specify/register.md .specify/specs/107-decision-governance/checkpoints .specify/specs/107-decision-governance/plan.md
```

**Executed today**: this exact command returns empty (no legacy carrier was rewritten) — the C-502 reading at plan time.
**Premises (per planned example)**: the reconstruction runbook is the checker's `--action records` output plus the register fixture; the four-carrier fixture set lives under `tests/fixtures/decision-governance/reconstruct/`. **Pinned by**: `tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy` and `::test_broken_pointer_red`.

## Scenario 6 — Legacy read and mirror closure (executed today)

1. Legacy two-digit `D-NN` headings are reported `legacy`, never judged:

```bash
grep -rn '^### D-' .specify/specs --include='*.md' | wc -l   # measured 39 pre-existing D- headings, all legacy (one/two-digit forms); three-digit record-form headings: 0
```

2. Mirror and copy closure, judged against the baselines captured before any edit:

```bash
python3 scripts/python/sync-mirrors.py --check      # rc 0 at the pre-edit baseline (test-evidence/sync-mirrors-baseline.txt)
python3 scripts/python/regen-command-copies.py --check   # rc 0 (test-evidence/regen-copies-baseline.txt)
python3 scripts/python/scan-confirmation-gates.py   # 31 blocking gates / 0 violations at baseline; zero NEW hits after landing
```

**Executed today**: all three ran in this stage with the readings above (`test-evidence/`). After landing, the acceptance is "no NEW drift" and "zero NEW gate hits" against these baselines — not a bare exit code.
