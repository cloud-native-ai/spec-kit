---
name: decide-batch
description: Run one batch decision panel session — relay the complete presentation of every pending decision item, capture the user's objection-only reply verbatim, delegate the deterministic engine's scan / record / replay actions, and never recompute a judgement. This is the interaction carrier of `/speckit.decide`; the rules live in the decision-governance owner page and the fixed-rule judgements live in scripts/python/decision-batch.py. Use this when the user mentions ["decide batch", "batch decision", "批量决策", "待决策项", "决策面板", "objection", "异议", "accept defaults", "沉默接受默认", "replay batch", "重放批次"].
classification: internal
skill_id: "<SKILL:.specify/skills/internal/decide-batch/SKILL.md>"
---

# decide-batch

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Overview

One invocation = one batch: scan the closed pending-source roster, present every pending decision item with complete information and a recommended default, let the user object only to contested items, record the batch through the existing carriers, and make the batch replayable from its record alone.

The mechanism's rules are owned by `shared/definitions/decision-definitions.md` § 批量决策面 (reached by pointer — this skill MUST NOT restate its criteria tables). The deterministic judgements belong to `scripts/python/decision-batch.py` (closed actions `scan` / `record` / `replay`); this skill owns the interaction and the verbatim relay.

## When to use

- The user asks to review their pending decision items in one pass, or reply with objections only.
- A recorded batch must be audited/replayed from its record without the conversation history.

## Workflow

1. **Scan.** Run the engine from the repository root:
   `python3 .specify/scripts/python/decision-batch.py scan --workspace-root <root> --format json`
   Parse the payload for the machine hand-off; render the presentation to the user from the engine's own `--format text` face (the batch-level context floor and every item row come from the engine — never re-author them). `scan` writes nothing.
2. **Present and wait.** Print the presentation verbatim to the user and stop. Answer follow-up questions about the content, then keep waiting: a follow-up question is not a reply and MUST NOT be turned into one.
3. **Capture the reply.** When the user replies explicitly (an objection to a named item, a park, or "no objections"), write the reply file: the user's exact text preserved verbatim, plus structured entries bound **by item identity** (the item's subject, plus its locator for the same-name family) and, for alternatives, the full option label. Never bind by position or order; never paraphrase the verbatim layer. An aborted session or a follow-up-only conversation writes nothing and stops here.
4. **Record.** Run the engine with the caller-declared authorization:
   `python3 .specify/scripts/python/decision-batch.py record --workspace-root <root> --presentation <scan payload> --reply <reply file> --authorization interactive`
   Relay the engine's result verbatim. A refusal (drift, unknown identity, non-member label, unattended or missing authorization) is final for this attempt; correct the reply and retry on the **same** presentation when the engine allows it.
5. **Replay (on request).** Run `python3 .specify/scripts/python/decision-batch.py replay --workspace-root <root> --batch <batch record>` and relay the reconstruction and its exit status. Any unresolvable pointer is reported by the engine; never complete it from conversation memory.

## Boundaries

- **Never recompute a judged verdict.** The engine alone computes the grounding join, pointer resolution and prior-decision-conflict detection; this skill performs no semantic retrieval, infers no additional evidence, and never overrides an engine-judged status at presentation time.
- **Never invent content.** A missing slot is shown empty and named; the skill MUST NOT fill a missing slot with an invented value, a default label or an option.
- **Never record without an explicit reply and declared interaction authorization.** A missing authorization level is treated as unattended and the engine refuses to record; the skill MUST NOT infer authorization from terminal shape, environment or silence.
- **Never present or settle an `ai-autonomous` item.** Excluded candidates stay excluded and are counted by the engine.
- **No second store, no network, no feedback-store write, no automatic transmission.** The batch record is one dated entry in the existing knowledge store, written by the engine; the skill writes only the reply file.

## Pointers

| What | Where |
|------|-------|
| Batch rules (roster, block grammar, presentation, grounding, disposition, record, replay, completeness) | `shared/definitions/decision-definitions.md` § 批量决策面 |
| Deterministic engine | `scripts/python/decision-batch.py` (`scan` / `record` / `replay`, `--help` for the flag and exit-code surface) |
| Command entry | `templates/commands/decide.md`; reference doc `docs/reference/commands/decide.md` |
| Choice-signal vocabulary (disposition mapping) | `shared/guidelines/confirmation-gates.md` § 门控观察协议（指针） |

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 2845f5641171 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:decide-batch" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:decide-batch" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:decide-batch" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
