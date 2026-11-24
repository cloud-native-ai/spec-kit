# Contract — `view-team` Skill (`skills/internal/view-team/SKILL.md`)

**Runtime path referenced by the command**: `.specify/skills/internal/view-team/SKILL.md`
**Source path (framework)**: `skills/internal/view-team/SKILL.md`
**Pinning tests**: `tests/contract/test_team_view_command.py` (wiring), `tests/integration/test_team_view_program.py` (behaviour through the program), `tests/contract/test_team_view_program_contract.py` (no-write surface).
**Concept owners cited, never restated**: team concept `skills/internal/create-team/references/conceptual-model.md`; run/report shape `skills/internal/run-team/SKILL.md`; team schema `skills/internal/create-team/references/create-mode.md`; engine actions `scripts/python/goal-utils.py --help`.

**C-13** Input contract.

- Input is `view [team-slug]`; no slug means the overview of every team, slug ascending.
- Slug resolution is exact; a near-miss is `[[STR-001]]`, never a fuzzy hit.
- `--scope` and `--spec-dir` follow the command's Scope section; any value the team archive cannot serve is reported explicitly, never silently ignored.
- `--target` is refused before invocation as a mode/parameter conflict (the program declares no such option); the skill MUST NOT reroute to run.

**C-14** One delegation.

The skill invokes the deterministic program `scripts/python/team-view.py` (runtime `.specify/scripts/python/team-view.py`) and consumes its output. It MUST NOT re-derive definitions, reports, ledger counts, binding records or anchor facts in prose, and MUST NOT call any engine write action or `run-checks`.

**C-15** Presentation is verbatim and complete.

The skill presents the program's six-group rendering (or overview / error rendering) **verbatim**:
- it MUST NOT drop, reorder or merge a group;
- it MUST NOT replace a missing-state label (`缺失` / `为空` / `不可读` / `未记录`, closed set owned by the program contract C-30 and `data-model.md` § Rendering Line Types) with a zero, a placeholder or an inferred value;
- it MAY add at most one framing line naming the mode (single / overview) and the as-of pointer.

**C-16** Read-only is unconditional.

One view invocation MUST NOT write any file, create any directory, dispatch any seat or register any run line. The skill MUST NOT call `binding` / `list` / `targets` for anything other than reading, and MUST NOT call `bind`, `status`, `create`, `migrate`, `targets --add` or any other write action.

**C-17** Not a run preview.

The skill MUST NOT run the five-check preflight, MUST NOT render a `blocked` verdict, and MUST NOT claim the team "can run". It presents persisted state and binding facts only; a reader who wants the run judgement is pointed to `/speckit.team run`.

**C-18** Error navigation (closed set).

| Program exit | Skill action |
|--------------|--------------|
| `0` | present the rendering |
| `2` | explain the input error (option/scope/extra positional) and show the accepted form `view [team-slug]`; execute nothing |
| `3` | present `[[STR-001]]`, the available slug list (bounded, omissions counted) and the `/speckit.team create` suggestion |
| `4` | present `定义损坏` with the exact path; explicitly state it is not "not found"; execute nothing |
| `5` | present the rendering together with the degraded-engine explanation (which group is `不可读` and why); do not retry, do not invent data |

**C-19** No new format, no new store.

The skill adds no machine-readable user-facing output, no cache, snapshot, index, registry or second team store. The program's `--json` envelope is an internal test surface (A-5).

**C-20** Wording obligations.

The rendered message follows `.specify/shared/guidelines/user-facing-comprehension.md`: identifiers (slug, pattern, lifecycle values, paths, mode names) retain their canonical form; explanations are Chinese (A-13); each error names the slug/path and the next command.

**C-21** Boundaries.

The skill:
- MUST NOT accept create / modify / run semantics (those belong to `create-team` / `improve-team` / `run-team`);
- MUST NOT serve single-agent authoring (that is `/speckit.agents`);
- MUST NOT become a single-agent operation entry.

**C-22** Lifecycle block.

The skill carries the standard `## Wrap-up` block compiled by `python3 scripts/python/probe-utils.py --action compile-embeds`; `--check` MUST exit 0 after the compile. The block is generated, never hand-written.

**C-23** Mirror.

`skills/internal/view-team/**` is mirrored to `.specify/skills/internal/view-team/**` by `scripts/python/sync-mirrors.py`; the source is authoritative and the mirror is never hand-edited.
