# Contract — Run Command Wiring (`templates/commands/agents.md` + `skills/internal/run-agent/SKILL.md` input + `docs/reference/commands/agents.md` Syntax)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each one off; the pinning test below enforces the machine-readable clauses.
**Pinning test**: `tests/contract/test_agents_run_command_contract.py` (artifact-class clauses C-01…C-04, C-06, C-07, C-09, C-10; the routing sample set C-08; C-05 by the same module).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md` (canonical `**C-N**` form).
**Shared Strings**: `[[STR-001]]` = `[create|refine|run] [agent-name] [task]`; `[[STR-002]]` = `agent not found`; `[[STR-003]]` = `missing agent name`; `[[STR-004]]` = `missing task`.

**C-01** The template declares the argument grammar.

`templates/commands/agents.md` frontmatter MUST carry `argument-hint` whose value is exactly `[[STR-001]]`. The key is new to this file; `templates/commands/team.md`, `goal.md` and `anchor.md` are the sibling form. The hint is the **command-level** argument grammar shared by the three modes — it is not a per-mode permission table. (FR-001, SC-001)

**C-02** The three-skill delegation table is preserved and run stays first-class.

The delegation table MUST keep exactly the three rows whose skill paths are `.specify/skills/internal/run-agent/SKILL.md`, `.specify/skills/internal/create-agent/SKILL.md` and `.specify/skills/internal/improve-agent/SKILL.md`; the run row's input cell MUST carry `run <agent-name> [task]`; the create and refine rows keep their existing inputs/outputs; no fourth verb alias is introduced. (FR-001, FR-002)

**C-03** Explicit verb wins; team intent is redirected, never served.

The delegation section MUST state, in substance: an explicit leading verb (`run` / `create` / `refine`) wins over context inference; a multi-agent or team intent (parallel / serial / iteration / continuous, "organize/run several agents") MUST NOT be served by this command and is directed to `/speckit.team`; a non-empty ambiguous input reports the three capabilities (create / refine / run) and requests the missing intent without executing any mode. (FR-002, FR-014)

**C-04** Explicit `run` without an agent name stops at the command.

The template MUST state that an explicit `run` with no agent name reports `[[STR-003]]`, the three capabilities and the usage line, and dispatches nothing; it MUST NOT infer an agent from conversation context and MUST NOT execute the no-argument listing behaviour in its place. (FR-003)

**C-05** The no-argument behaviour is unchanged.

Empty arguments MUST keep the existing sequence owned by the `run-agent` skill: list every existing agent with layer/name/description/tools/model, give grounded contextual suggestions, and show the three-mode capability summary; the sequence is informational and non-destructive. (FR-002, FR-018)

**C-06** The three syntax faces agree verbatim.

`[[STR-001]]` MUST appear verbatim in exactly these three faces: the template `argument-hint` (C-01), the `run-agent` input contract (`.specify/skills/internal/run-agent/SKILL.md` § Input Contract), and the `docs/reference/commands/agents.md` Syntax block. The run-specific form `run <agent-name> [task]` MUST appear in the `run-agent` input contract and in the docs Syntax block. (FR-001, SC-001)

**C-07** The skill owns the missing-task stop.

The `run-agent` input contract MUST state that `run <agent-name>` without task text presents the resolved agent (name, layer, description), reports `[[STR-004]]`, and requests the task; it MUST NOT dispatch an empty task brief and MUST NOT fall into the no-argument listing behaviour. (FR-004, A-4)

**C-08** Routing sample set.

The contract carries this sample set; the pinning test asserts each sample's deterministic proxy (distinctive tokens present in the expected target, absent from the forbidden targets). The test does not execute an LLM.

| # | Sample input | Expected route | Deterministic proxy |
|---|--------------|----------------|---------------------|
| 1 | `run sdd-debt-governor 审计 src/ 下的技术债` | run → `run-agent` | verb `run` + `run-agent` path in the run row |
| 2 | `运行代理 code-reviewer 跑一次审查` | run → `run-agent` | the run row's intent text includes 运行/执行/run |
| 3 | `create a security-review agent` | create → `create-agent` | create row + `create-agent` path |
| 4 | `refine the qa-engineer agent` | refine → `improve-agent` | refine row + `improve-agent` path |
| 5 | `并行运行三个 agent 并汇总` | team → `/speckit.team` | team-redirect sentence; the run row MUST NOT claim multi-agent orchestration |
| 6 | `` (empty) | no-argument listing behaviour | template delegates empty input to the skill's Default Behavior |
| 7 | `do the agent thing` | ambiguous → three capabilities | the ambiguity sentence lists create / refine / run |

(FR-002, SC-001)

**C-09** Per-tool copies are generated, never hand-edited.

The four `.qoder/`, `.claude/`, `.github/` and `.opencode/` copies of `speckit.agents` MUST be regenerated from the template by `regen-command-copies.py`, never hand-edited. The generator projects the template **body** only: frontmatter keys (including `argument-hint`) are not copied, so the copy face is the body's run row, and each copy MUST contain `run <agent-name> [task]`; `[[STR-001]]` agreement is a source-template face (C-01), not a copy face. A hand edit of a copy is a defect. (FR-001, FR-022⑤)

**C-10** The three error paths stop with zero dispatches.

The three strings `[[STR-002]]`, `[[STR-003]]` and `[[STR-004]]` MUST each be present in their owning surface (skill input for agent-not-found; template for missing-name; skill input contract for missing-task), and each path MUST be stated as a stop with no dispatch. (FR-003, FR-004, FR-005)
