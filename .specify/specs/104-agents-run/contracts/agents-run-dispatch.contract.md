# Contract — Run Dispatch Wiring (`skills/internal/run-agent/SKILL.md`)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each one off.
**Pinning test**: `tests/contract/test_agents_run_skill_wiring.py` (artifact-class text pins). Behavior-class clauses are declared here and in `quickstart.md`, and are evidenced by truth-source text + review + mutation drill recorded in `test-evidence/` — never claimed as contract-test coverage (FR-023).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md` (canonical `**C-N**` form).
**Owners reached by pointer (never restated)**: `superagent-definitions.md` § The super↔sub Protocol / § Role-Transition Injection / § Role Edges / § Visualization & Tracking; `subagent-definitions.md` § Dispatch-Time Governance Obligation / § The Concurrency Obligation / § External Dispatch Visibility Contract; `shared/guidelines/fast-fail.md` § 子代理派发注入; `shared/guidelines/reporting-obligations.md`; `shared/definitions/re-anchoring-definitions.md`; `.specify/skills/sdd-loop-driver/references/watch-model.md` § 11.

**C-11** The presentation discloses the role relation — *behavior-class*.

The presentation step MUST disclose, beside the existing config disclosure (E5), the three role elements: this session is the edge's **superagent (root)**; the **child label**; the **return channel**. It MUST reference the role and protocol owners by pointer and MUST NOT restate their rule text; it stays **disclosure, not a blocking gate** (the user may stop before dispatch). (FR-007)

**C-12** The downlink carries the seven role fields — *artifact-class presence / behavior-class content*.

The dispatch step MUST name all seven fields — `parent_identity`, `child_label`, `role_declaration`, `dispatch_duty`, `depth_position`, `authority_ref`, `return_channel` — and carry them in the outgoing payload by pointer to `superagent-definitions.md` § The super↔sub Protocol. Their semantics MUST NOT appear as a copied table. (FR-008)

**C-13** The four pre-existing injections travel by pointer — *artifact-class presence / behavior-class content*.

The dispatch step MUST name the four injections and their owners: the fast-fail clause (`shared/guidelines/fast-fail.md` § 子代理派发注入 — its owner literal is injected verbatim, already required by the existing dispatch-time injection block), the concurrency obligation, the reporting duty, and the re-anchoring anchor digest. Rule text MUST NOT be copied. (FR-008)

**C-14** The role-transition self-check is extended item-by-item — *artifact-class*.

When `dispatch_duty: granted`, the outgoing payload MUST carry the `role-transition` identifier **and each of the nine item-id slugs**; the pre-dispatch self-check MUST be stated as requiring each item (identifier alone is insufficient). The existing block's literal phrases (`role-transition`, `Role-Transition Injection`, `nine item-id slugs`, `identifier alone is insufficient`, `payload-construction defect`) MUST remain. (FR-008, FR-009)

**C-15** The uplink carries the five return elements — *behavior-class*.

The report step MUST require the five uplink elements owned by `superagent-definitions.md` § The super↔sub Protocol: result or deliverable path; evidence pointer(s); an explicit anomaly line (stating `未发现异常` when none); the concurrency reading triple; the returning executor's identity. A return missing any element is **incomplete**: the parent MUST NOT consume its conclusion and MUST NOT backfill the missing fields. (FR-010)

**C-16** The child label reuses the existing dispatch convention — *artifact-class presence / behavior-class uniqueness*.

The dispatch section MUST state: the child label is the `dispatch.sh <label>` value passed verbatim as the dispatch's `run_id` to `exec-quant.py --action collect-dispatch`; the external artifact triplet is named `<label>.live.log` / `<label>.jsonl` / `<label>.status`; every run uses a new label, a retry is a new attempt and the old attempt's artifacts are kept; a stale attempt's late return is not consumed as the current result (attribution: watch-model § 11); no label generator, child list or registry is introduced. (FR-011)

**C-17** Multi-child visibility is a pointer to existing carriers — *artifact-class*.

The skill MUST point at the three existing carriers — the external artifact triplet, the `exec-quant` dispatch records, and the `status-digest.py` role view (`parent` / `roles` / `role_set_marker` / `depth`) — and MUST state that no new child list, registry, renderer or state store is added. (FR-012)

**C-18** The SDD probe's applicability condition is written down — *artifact-class presence / behavior-class execution*.

The pre-dispatch probe section MUST state that `sdd-route.py --action authorize` runs **only** when the payload assigns or names an SDD driver under the narrowed predicate owned by `subagent-definitions.md` § Dispatch-Time Governance Obligation, and that a normal run assignment (no SDD driver named) MUST NOT invoke the probe and MUST NOT be blocked by a missing team/seat. The existing refusal shape (failing half `agent` / `seat` / `both`, resolved values, both source paths, seat slug) MUST remain. (FR-016)

**C-19** The run stays a single unit — *artifact-class boundary / behavior-class reading*.

The section MUST keep the exact sentence `**Scope boundary**: Run mode executes a **single** agent on a **single** task.` and state that one run MUST NOT fan out multiple agents, that multiple runs are multiple command invocations, and that each run records the `requested` / `effective` / `effective_reason` triple with `single-unit` naming the serial reason and `not_evaluated` where intervals are absent — never `0` and never an estimate. (FR-013, FR-014, FR-017, A-13)

**C-20** Anti-nesting red lines are preserved — *artifact-class*.

The existing anti-nesting obligation MUST remain: the outgoing prompt MUST NOT reference any driver/loop skill, MUST NOT instruct the subagent to load any skill, and MUST NOT contain loop logic; the narrowed depth-2 chain stays by pointer to its owner. (FR-008)

**C-21** The role is decided only by the edge — *artifact-class*.

The skill text MUST NOT introduce an activation switch, a role entity, a fourth agent category or a second role definition; the role relation is stated as a product of the dispatch edge, with the owner cited. (FR-006, A-5)

**C-22** Zero second mechanism and clause-class honesty — *artifact-class*.

The skill MUST NOT introduce a second dispatch mechanism, scheduler, queue, transport, notification channel or persistence root; every capability is reached through the existing `run-agent` workflow, `execution-config.py`, `dispatch.sh`, `exec-quant.py` and `role-edge-check.py`. The behavior-class label on C-11 / C-12 / C-13 / C-15 / C-16 / C-18 / C-19 is normative: a contract test MUST NOT be described as covering those runtime behaviors. (FR-015, FR-021, FR-023)
