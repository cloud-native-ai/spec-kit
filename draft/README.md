# draft/ — Incubating integrations

This directory is the **staging area** for skills, agents, and tools that are not yet
promoted into the formal house-style locations (`skills/`, `.specify/agents/`, `templates/`).
Items here are **draft**: they follow the SKILL.md / `.agent.md` frontmatter conventions,
but are **not wired into the main `/speckit.*` workflow** and do not affect existing behavior.
Promotion into the formal flow is a separate, deliberate step (see *Promotion* below).

## What lives here

This batch integrates the **core ideas of three sibling spec-driven projects** into Spec Kit,
per `design.md` (OpenSpec + Superpowers + upstream spec-kit `main`). Each core capability is
captured as a self-contained skill (plus supporting agents), so it can be trialed in isolation
before any decision to fold it into the constitution-governed `/speckit.*` pipeline.

| Draft resource | Source project | Core capability imported |
|----------------|----------------|--------------------------|
| `skills/delta-spec-change/` | **OpenSpec** (`@fission-ai/openspec`) | Delta Spec change management — capture a change as a proposal with `## ADDED / MODIFIED / REMOVED / RENAMED Requirements` deltas, apply, **sync** deltas into living capability specs, then **archive**. Brownfield-first. |
| `skills/subagent-driven-development/` | **Superpowers** | Subagent-Driven Development — a fresh implementer subagent per task, a **two-verdict task review** (spec compliance + code quality) with a fix-and-re-review loop, then one broad whole-branch review. File handoffs + durable progress ledger. |
| `skills/test-driven-development/` | **Superpowers** | The TDD Iron Law and RED → verify-RED → GREEN → verify-GREEN → REFACTOR cycle. Complements the master constitution's *Test-First* principle. |
| `skills/spec-kit-extensions/` | **spec-kit `main`** | The Extension / Preset / Bundle ecosystem + resumable **Workflow** YAML orchestration, template-resolution priority stack, and compose strategies. |
| `agents/sdd-implementer.agent.md` | **Superpowers** | Single-task implementer role dispatched by the SDD controller. |
| `agents/sdd-task-reviewer.agent.md` | **Superpowers** | Two-verdict (spec + quality) per-task reviewer role. |

## How the three fit together

The three projects are complementary rather than competing (see `design.md`):

```
        OpenSpec                 Superpowers                spec-kit (main)
   Delta Spec change mgmt   subagent-driven dev + TDD    extensions / presets /
   (what should change)     (how it gets built well)     bundles / workflows
        │                          │                          │
        ▼                          ▼                          ▼
  delta-spec-change   →   subagent-driven-development   →   spec-kit-extensions
                          + test-driven-development          (packaging & orchestration)
```

A natural draft flow: use **delta-spec-change** to describe *what* changes as reviewable
deltas → drive execution with **subagent-driven-development** (which enforces
**test-driven-development** per task) → package/orchestrate reusable pieces with
**spec-kit-extensions**.

## Isolation guarantees (does not affect the main flow)

- Nothing outside `draft/` is modified. The master `/speckit.*` commands, `.specify/`,
  `skills/`, `templates/`, and `memory/` are untouched.
- No draft skill/agent is registered in the instructions **Resource Registry**
  (`.specify/instructions.md`), so the model will not auto-route the main workflow through them.
- Runtime scratch and working artifacts for these skills stay under **draft-local roots**
  (`draft/changes/`, `draft/specs/`, `draft/.sdd/`) so they never collide with the master
  spec flow under `.specify/specs/`.

## Conventions

- Each skill is a directory whose name equals its frontmatter `name`, containing `SKILL.md`
  (< 500 lines) plus optional `references/` (on-demand docs) and `assets/` (templates).
- `skill_id` uses the draft path form `<SKILL:draft/skills/<name>/SKILL.md>` while incubating.
- Agents are `<name>.agent.md` files with `supervisor: false` (SDD roles are single-pass workers).
- No `README.md` / `LICENSE` / `CHANGELOG` inside individual skill directories (this root
  README is the only index).

## Promotion (when a draft graduates)

Following the precedent in this repo's history (*"consolidate draft skills into formal skills"*):

1. Move the skill dir into `skills/` (and agents into `.specify/agents/`).
2. Rewrite `skill_id` from `<SKILL:draft/...>` to `<SKILL:.specify/skills/<name>/SKILL.md>`.
3. Repoint working roots (`draft/changes` → `.specify/specs`, etc.) as appropriate.
4. Add a deduplicated, sorted row to the Resource Registry in `.specify/instructions.md`
   and refresh via `/speckit.instructions`.
5. Reconcile overlaps with existing principles/commands (e.g. TDD ↔ *Test-First*,
   delta specs ↔ feature specs) so there is one source of truth.
