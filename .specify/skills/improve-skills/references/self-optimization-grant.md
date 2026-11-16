# Self-Optimization Grant — 赋予目标技能自我优化的能力

> Owner of the flywheel model that `improve-skills` grants to a target Skill:
> **尝试 → 记录 → 优化 → 沉淀**, following 一回生二回熟. `SKILL.md` carries the core
> action and the workflow pointers; this file carries the model, the applicability
> gate, the grant checklist, the anti-patterns and the blueprint instance.

## Boundary — what this is, and what it is not

| It is | It is not |
|-------|-----------|
| A runtime capability the target uses **between** improvement loops: each attempt deposits knowledge, and later attempts start from it | Self-Improvement（自我提升）— that model owns definition-change loops and stays owned by `shared/definitions/self-improvement-definitions.md`; do not redefine or rename it here |
| Control of **baseline capability**: which path a later run takes, what it must record, when it must stop trusting an old path | Structural churn in the target Skill — no section rewriting, no workflow renumbering, no runtime mutation of `SKILL.md` |
| A deterministic knowledge layer (state machine + records + distilled knowledge + evidence) | A process log, a changelog, or a self-reported success diary |

**Naming discipline**: call it the *self-optimization flywheel* (自我优化飞轮), never
"self-improvement". A loop that confuses the two will either restate the SI workflow or
claim definition improvement from runtime learning — both are forbidden drift.

## The flywheel — four stages and their gates

| Stage | 一轮做什么 | 必须落盘 | 进阶门禁 | 回退触发 |
|-------|------------|----------|----------|----------|
| **尝试 attempt**（一回生） | Complete the user's task through the target's full path; exploration is allowed and expected | Structured attempt records for the subject key: actions, real requests/responses reduced to shape, failures with error, at least one success signal | Records pass schema + redaction validation; a failure record carries its error | — |
| **记录 record** | Persist the attempt through the deterministic engine, never by hand | One record entry per attempt, append-only, per subject key | Engine accepts the record; no raw credentials or business payloads | — |
| **优化 optimize**（二回熟） | Reuse the records to finish the same task, and distill the reusable form: request-level recipe, preset, decision branch, or checklist | Distilled artifact declaring its expected result per step; non-optimizable steps kept with a reason and blockers | Distilled artifact validates against the schema; every step has an expectation | Distillation cannot reproduce the outcome → keep the attempt-level path and record the blocker |
| **沉淀 consolidate** | Validate the distilled form on the real surface, then route later runs directly through it | Validation evidence: run id, verdict, steps passed/total, failures with expected/actual | All steps pass → consolidated (sealed) state; later runs use the direct path without re-exploration | Expectation drift → back to optimize; entry, auth or flow changed → back to attempt |

State lives per **subject key**, not per document section. A sealed path is a claim that
must keep paying rent: every failure demotes it with evidence, and a changed surface
demotes it further. The flywheel never lets a stale path impersonate success.

## Subject key — the unit of reuse

- Key by the target's natural repeated subject (for a browser skill: `site + capability`;
  for another skill: repo + task, document type + section, environment + action — whatever
  actually recurs). Never key by the calling project or by a one-off task.
- Semantic aliases dedupe equivalent requests; an inventory action lists existing keys, so
  no hand-written inventory drifts.
- Caller business data does not enter the runtime store; differences between callers enter
  through run-time parameters, not as duplicated knowledge.

## Applicability gate

Grant only when all four hold; otherwise record `not-applicable` with the failing condition:

1. the target is expected to execute **repeatedly**;
2. the facts that make it succeed **differ per subject** and are learnable from attempts;
3. there is an **observable success/failure signal** the engine can validate;
4. a runtime-data location exists that the caller owns and can keep.

A pure one-off utility, or a skill whose output has no verifiable signal, must not carry
the flywheel — machinery without payoff is a defect, not a feature.

## Grant checklist — the actual edit

When the assessment is `grant` or `repair`, land all items that apply; each is checkable:

1. **Subject key + inventory** — declared and deduplicated; no hand-written inventory.
2. **Two touchpoints wired into the target's main flow** — entry lookup (choose the path by
   state) and exit deposit (record the attempt or validation evidence). No other workflow
   change; no step renumbering.
3. **Deterministic engine owns state, schema, redaction and transitions** — hand-editing
   state is forbidden; human-authored notes are allowed and kept separate. The store
   location is a policy: take it from the target's declared environment or the user, never
   hard-code a user directory.
4. **Stage gates and rollback evidence** — the four stages above, each with its deposit and
   gate; every demotion carries expected/actual evidence.
5. **Layering** — shared notes (cross-subject quirks), per-subject records, distilled
   artifacts, validation evidence. Upper layers index lower layers; no duplicated detail.
6. **Redaction at write time** — credential-like keys (cookie, authorization, token,
   signature, secret, csrf, xsrf) become placeholders; response bodies never persist.
7. **Ownership surfaced** — runtime data belongs to the caller; the run report states the
   commit / backup / git-ignore choice so the caller decides consciously.
8. **Minimal instruction growth** — one reference plus the two touchpoints; the target's
   `SKILL.md` stays a contract and passes its shape gate.
9. **Second-run proof planned** — name the comparable later run and its expected signal;
   until it lands, report the grant as outcome pending, never "the skill now improves
   itself".

## Anti-patterns

| Symptom | Why it fails | Correct move |
|---------|--------------|--------------|
| Records pile up but the next run re-explores | Log-only flywheel: no distillation | Distill at stage 3; measure whether stage 4 is reached |
| A distilled path is trusted without validation evidence | Drift hides behind a green-looking path | Validate against the real surface; store expected/actual |
| State or knowledge hand-edited, or written into `SKILL.md` | Drift, merge conflicts between concurrent writers, contract bloat | Deterministic engine + caller-owned runtime store |
| Knowledge keyed by calling project | Duplicate stores, no reuse | Key by subject + capability; aliases for semantic matches |
| Forced onto a one-off skill | Cost without a second run | Applicability gate; record not-applicable |
| Declared improved immediately after the edit | Outcome claim without comparison | Intervention ledger + outcome pending until a later run |
| Called "self-improvement" | Collides with the owned SI model | Cite this file; keep the flywheel a runtime capability |

## Blueprint instance

The `profiles-browsers` skill's site-memory layer is a proven instance of this shape:
per-site `state.json`, `notes.md`, `records/<capability>.jsonl`,
`recipes/<capability>.json`, `validation/<capability>/<run>.json`, driven by a
deterministic engine with gate-enforced state transitions and evidence-carrying rollback.
Copy the **shape** — state machine, deterministic engine, layering, redaction, rollback —
not its site content, naming or local paths. When the user names a blueprint skill, resolve
it at run time through normal skill resolution; never hard-code its local path into the
target or into this reference.

## Wiring into the improve-skills loop

- **Step 3**: the assessment is a standing candidate — `grant` / `repair` / `not-applicable`
  with the reason, recorded before the candidate freeze. A grant is a capability addition,
  not a defect claim.
- **Step 5/7**: execute the grant edit per the checklist; capability control only.
- **Step 8**: execute the target's engine against a real sample (not files-exist checks);
  run the target's shape gate and affected contract tests; sync mirrors.
- **Step 9**: report the grant, its expected signal and `outcome pending`.
