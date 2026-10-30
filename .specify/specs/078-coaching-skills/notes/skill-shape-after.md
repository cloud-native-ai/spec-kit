# Skill Shape After — final `coaching-skills` body (T030)

**Date**: 2026-10-30
**Subject**: `skills/external/coaching-skills/SKILL.md` (final form, after T018/T019/T021-T024)
**Verdict**: **pass** — exit 0, controllable body ≈3278 tokens against the 5000 budget.

## Command and output (verbatim)

```text
$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/coaching-skills/SKILL.md --budget-tokens 5000
SKILL.md 形态检查 — skills/external/coaching-skills/SKILL.md
  判定        pass
  正文估算     ≈3278 tokens 可控 / 预算 5000（253 行）
  代码围栏     0 段 / 0 行 = 0%，其中非图示超 5 行 0 段
  最大章节     Dispatch Payload
  发现：
    ! [flags-outside-contract] 23 个具体 CLI flag 出现在非约束章节：Wrap-up(23)
$ echo $?
0
```

## Readings

| Field | Reading |
|-------|---------|
| Verdict | `pass` (exit 0) |
| Controllable body | ≈3278 tokens / budget 5000 — 65.6% of budget, 1722 tokens of headroom |
| Lines | 253 |
| Code fences | 0 blocks / 0 lines (0%), none over the 5-line non-diagram ceiling |
| Largest section | `## Dispatch Payload` |
| Findings | 1 warning: `flags-outside-contract` — 23 CLI flags in `## Wrap-up` |

## Findings, one by one

1. **`flags-outside-contract` — 23 CLI flags in `Wrap-up`**: the `## Wrap-up` block is
   the compiled probe face (`probe-utils.py --action compile-embeds`); its run-determination
   and exec-quant argv lines necessarily carry flag names. The block is generated from
   `.specify/shared/definitions/probe-definitions.md` and MUST NOT be hand-edited
   (C-3), so the warning is a property of the probe registry's wording, not of this
   skill's body. It does not affect the verdict and is identical to the pre-change
   baseline's same warning.
2. **No `oversized-section` finding**: the pre-change body carried
   `Workflow=51行`; the rewritten body's largest section is `## Dispatch Payload`, under
   the 40-line advisory. The reset comes from splitting the loop into `## Preflight` /
   `## Compare` / `## Improvement Plan` / `## Optimization` sections instead of one
   workflow block.

## Before / after (T001 baseline is comparison only)

| | Pre-change (T001, `think-skills`) | Final (`coaching-skills`) |
|---|---|---|
| Verdict | `pass` | `pass` |
| Controllable body | ≈1981 tokens (110 lines) | ≈3278 tokens (253 lines) |
| Largest section | `Workflow` (51 lines, oversized warning) | `Dispatch Payload` (within advisory) |
| Findings | `oversized-section` + `flags-outside-contract` | `flags-outside-contract` |

The body grew by ≈1297 tokens and 143 lines because it now owns four phases that the
pre-rename skill did not have (pre-dispatch expectation with two dimensions, single
dispatch with a closed payload, observation with a source per step, improvement plan
with evidenced entries), plus the compiled `## Wrap-up` face. The budget judgement is
this file's `--budget-tokens 5000` reading above; the T001 numbers are the dated
before-picture and do not replace it.
