# Contract — Observer Role（观察者角色面）

Scope: `agents/sdd-observer.agent.md` (source), its `.specify/agents/templates/` mirror and its four per-tool rendered copies; the instance duty text; the execution carrier constraints. Requirements: FR-001, FR-002, FR-003, FR-004, FR-006, FR-016, FR-018, FR-019, FR-022.

## C-01 — Template exists, ships, and mirrors

The template source is `agents/sdd-observer.agent.md`; the mirror `.specify/agents/templates/sdd-observer.agent.md` is byte-identical and produced by `sync-mirrors.py`; the four per-tool copies are produced by `specify render-agents --ai <tool>` (qoder, claude, copilot, opencode), never hand-written.

(FR-001)

## C-02 — Neutral frontmatter

The frontmatter carries `name`, `description`, `user-invocable: false`, `disable-model-invocation: false`, `supervisor: false`, `model-tier: auto`, `capability-tools` (read/search/shell tools only), `skills: []`, `run-turn-budget: 500`. `capability-tools` MUST NOT contain a dispatch-class tool.

(FR-001)

## C-03 — Role face is declared, not implied

The body states the role as `observer`: it observes exactly one SDD line and participates in no execution, evaluation, review or decision. It is not a stage executor, reviewer or reporter seat and holds no write authority over the development line.

(FR-001, FR-002)

## C-04 — Objectivity prohibition, verbatim

The body contains the verbatim sequence 「不评价、不建议、不推断」 and states that journal entries are deterministic projections of carrier facts with no field able to carry evaluation, suggestion, causal inference, severity or recommendation.

(FR-001)

## C-05 — Read domain and write surface are explicit

The body declares the read domain (state spine, stage logs and sentinels, checkpoints, git history, the positive-evidence quartet, execution records; driver conversation and stage prompts excluded) and the write surface (journal through the engine + own execution artifacts under the existing execution log layout). It states that writing the state spine, stage artifacts, feature registry or glossary is a defect.

(FR-001, FR-016)

## C-06 — Layer binding uses the current three-layer model

The body binds Template → Instance → Execution per `shared/definitions/agent-definitions.md` and references no artifact of an unmerged feature. The role face is written so a future superagent model can bind by reference without redefining the journal format or the startup point.

(FR-002)

## C-07 — Internal subagents: allowed, serial, inherited bounds

The body permits internal subagents for observation duties and states: serial execution only; never a concurrency carrier; the host-internal in-process path is BANNED; subagents inherit the same read domain, write surface and objectivity structure.

(FR-022)

## C-08 — Forbidden capabilities and the fast-fail clause

The body forbids referencing or loading the driver/loop skill, hosting or starting an SDD run, and emitting user-visible reports, questions or approval requests. It carries the fast-fail injection block byte-identical to its owner literal in `shared/guidelines/fast-fail.md` § 子代理派发注入.

(FR-018, FR-022)

## C-09 — Instance identity and creation duty

An Observer Instance slug derives from `line_id`; its duty text names the line, the spec key, the journal path, the spine path and the state dir. Instances are created by the driver's startup step through `create-agent`; no stage command creates one. Two parallel lines resolve to two distinct instance slugs.

(FR-003, FR-004)

## C-10 — Execution carrier

An observer execution is dispatched through `run-agent` on the external mode's fork or subprocess carrier; native and virtual modes MUST NOT carry it. The execution label follows the existing three-segment supervision convention and names the triplet directory.

(FR-006, FR-019)
