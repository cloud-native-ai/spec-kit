# Contract: 证伪四元组（falsification-quartet）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-019…FR-023
**载体**: `shared/guidelines/critique-and-self-critique.md`（改写）、`shared/workflow/self-improvement-workflow.md` § SI-3C（改写）、`scripts/python/validate-falsification-quartet.py`（新建），各含 `.specify/` 镜像

本契约把「证伪尝试跑过了」从声明变成工件上可区分的事实。它同时钉死一个反向义务：
判决归程序，接收方不得反向覆盖——否则同一载荷换一次运行就会换一个 verdict。

## 条款

- **C-1** (quartet replaces the one-line form): the owner MUST define the falsification attempt's produced form as the closed quartet `attempt` / `exit_code` / `observation` / `would_go_red_if`, produced before dispatch, with the field set closed so that extending it is an owner revision; the earlier one-line description MUST remain byte-identical and the new subsection MUST declare that the quartet is the produced form, so the refinement is normative while the containment claim stays true. (FR-019)
- **C-2** (decidable field semantics): each field MUST have a decidable meaning — `attempt` is a command, grep, test or measurement a reviewer can replay verbatim; `exit_code` is an integer; `observation` is an excerpt of the original output carried behind the literal `raw:` marker, which is the mechanical proxy for 「not a paraphrase」; `would_go_red_if` names both the input to break and the red signal that must appear. (FR-020)
- **C-3** (rejection is a program verdict): a payload with a missing or empty field, a non-integer exit code, an `observation` without the `raw:` marker, or a `would_go_red_if` that cannot name both halves MUST be rejected by the deterministic checker `python3 scripts/python/validate-falsification-quartet.py <payload.md> [--json]`, whose exit codes are 0 accept / 1 reject / 2 unreadable payload (disposed as a rejection with reason `input-unreadable`); the payload form MUST be the four literal keys each appearing exactly once with the value on the same line or an indented continuation; rejection reasons MUST come from the closed set `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable` and MUST name the missing field or the failing half; the receiving agent MUST NOT override a non-zero verdict, MUST NOT invent a reason outside that set, MUST restrict extra concerns to non-blocking notes, and the checker MUST NOT replay `attempt`. (FR-021)
- **C-4** (carrier unchanged): the quartet MUST be recorded on the proposal's existing carrier — the SI-4 dispatch payload and the SI-7 intervention record — and MUST NOT introduce a ledger, a store, a probe or a score. (FR-022)
- **C-5** (workflow keeps a pointer only): § SI-3C MUST keep a step summary plus a pointer to the owner and MUST NOT restate the field list or the rejection rules; the contract test MUST assert both directions — the owner defines the fields, and the workflow contains no second definition of them. (FR-023)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-019 | test_owner_declares_closed_quartet |
| C-2 | FR-020 | test_field_semantics_decidable |
| C-3 | FR-021 | test_rejection_is_program_verdict_closed_reasons |
| C-4 | FR-022 | test_carrier_unchanged_no_new_store |
| C-5 | FR-023 | test_si3c_pointer_only_both_directions |

## FR 覆盖核对

- FR-019…FR-023 由本文件 C-1…C-5 承接；校验器的正负样本数目见 `quickstart.md` S4 与
  `tests/contract/test_falsification_quartet_validator.py`。
- 拒收原因的语义归属本契约，条目细节由 owner 与 `data-model.md` E6 共同钉住，不在两处各写一份。
