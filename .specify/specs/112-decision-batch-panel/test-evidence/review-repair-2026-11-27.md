# Review-Repair Evidence — F11 / F12 (C-204 identifier boundary)

Line `decision-batch-panel`; stage `review-repair`; baseline `fbc998496`; branch `112-decision-batch-panel`
(worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`).
Repair scope: the two blocking P1 findings recorded in `code-review.md` at commit `9536c0718` and carried
into `review.md` § 2.3 (F11 user-facing leak loci; F12 blind C-204 guard).

## What changed

| File | Change |
|------|--------|
| `scripts/python/decision-batch.py` | Added the presentation-layer display maps `SOURCE_TEXT` / `PRESENCE_TEXT` / `FIELD_TEXT`; `batch_context` now renders source names, presence readings and counts in plain language (was: `source_id` + raw `presence`); `state_sentence` renders missing required fields through `FIELD_TEXT` (was: raw field names). The structured payload is unchanged — `source_id`, `presence` and `missing_fields` keep their machine values. |
| `tests/contract/test_decision_batch_contract.py` | C-204 guard strengthened: `INTERNAL_TOKENS` gains the two roster source ids and the three presence words; `_identifier_leaks` masks repo-relative pointer spans before scanning (see Disclosures); reverse samples prove each leak form reds the detector; delivered bodies are scanned on `two-source`, `incomplete-block`, `autonomous` and `empty-project`; assertions pin the plain-language field/presence renderings and the machine payload's retained identifiers. |
| `.specify/scripts/python/decision-batch.py` | Mirror re-synced with `python3 scripts/python/sync-mirrors.py --write --only scripts/python/decision-batch.py`; `cmp` byte-identical, `sync-mirrors.py --check --only scripts/python/decision-batch.py` reports `ok`. |

Rendered before (baseline engine, verbatim):

```
本次扫描读取了封闭来源清单中的全部来源（register-open-decision-row 在场状态为 read，候选 2 项；authored-pending-item 在场状态为 read，候选 6 项）
当前状态：信息不完整，本次不会结案（缺少必填内容：decision_class）。
```

Rendered after (fixed engine, verbatim):

```
本次扫描读取了封闭来源清单中的全部来源（登记册中的待定决策行：已读取，候选 2 项；项目文档中的待决策条目：已读取，候选 6 项）
当前状态：信息不完整，本次不会结案（缺少必填内容：决策类别；未声明决策类别或类别值无法识别）。
当前状态：信息不完整，本次不会结案（缺少必填内容：上下文）。
```

## Red → green

| Run | Command | Reading | Evidence |
|-----|---------|---------|----------|
| Red (baseline engine + final guard) | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_batch_contract.py::test_presentation_identifier_boundary -q` with `scripts/python/decision-batch.py` restored from `git show fbc998496:scripts/python/decision-batch.py` | `1 failed in 6.26s`, RC=1 — leak tokens `['authored-pending-item', 'read', 'register-open-decision-row']` in the `two-source` body | `test-evidence/review-repair-c204-red.txt` |
| Green (contract file) | same runner, `tests/contract/test_decision_batch_contract.py -q` | `10 passed in 7.52s`, RC=0 | `test-evidence/review-repair-contract-green.txt` |
| Green (review smoke set) | same runner, `tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py tests/contract/test_decision_governance_guards.py tests/contract/test_migration_distribution.py tests/contract/test_probe_nonentity_catalog.py tests/unit/test_validate_decisions.py -q` | `108 passed in 8.47s`, RC=0 | `test-evidence/review-repair-smoke.txt` |

The final guard was mutated to prove failure: the baseline-engine run above reds on the real leak. The
reverse samples inside the guard (`register-open-decision-row`, `authored-pending-item`,
`在场状态为 read`, `在场状态为 absent`, `缺少必填内容：decision_class`) assert the detector fires on
every leak form before any delivered body is judged.

## Findings closed

- **F11 (P1)** — the completeness disclosure and the missing-field sentence render plain language;
  machine identifiers stay in the structured payload. Closed.
- **F12 (P1)** — the guard reds on all three leak forms (roster source id, presence reading, field name)
  and stays green on the delivered body across four fixtures. The blind spot is closed.

## Disclosures (corrections applied in passing)

1. **Pointer spans are masked before the token scan.** Scanning `incomplete-block` with a plain substring
   match reds on `['incomplete', 'no-default']`, both occurring only inside required source-pointer paths
   (`.specify/specs/demo/incomplete.md`, `.specify/specs/demo/no-default.md`). Carrier and evidence paths
   are mandated body content (C-203 source pointers); C-204's subject is identifiers — field names, script
   names, state/reason tokens — not paths. `_identifier_leaks` therefore masks repo-relative slash-path
   spans and scans the remaining text; the delivered body itself was not altered to satisfy the guard.
2. **Snapshot capture moved outside the watched tree.** The first smoke attempt teed its evidence file into
   `.specify/specs/112-decision-batch-panel`, which `test_engine_interface_contract` snapshots; the mid-run
   write tripped `before == after` (created/removed: `review-repair-smoke.txt`, 594 → 595 bytes). Re-ran with
   output captured under `/tmp` and copied into `test-evidence/` after completion; the recorded readings are
   from the clean re-runs.

## Boundaries held

- Only this feature's artifacts touched: the engine (source + mirror), the contract test, and this evidence
  directory. No spine, register, features registry, glossary or instructions edits; no main-tree edits;
  no push.
- No push, no network, no feedback-store write.