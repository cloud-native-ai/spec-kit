# P003 — Skill Library Expansion

- **Status:** Draft
- **Pillars:** Skills
- **Source projects:** superpowers, intellegix-code-agent-toolkit
- **Value:** H · **Effort:** L–M · **Phase:** 1
- **Related:** [[P002]], [[P006]], [[P010]]

## Problem / Gap

spec-kit ships strong *authoring* and *domain* skills (create/improve/think-skills,
draw-*, database/document/browser-utils, git-workflow, git-submodule-edit) and has drafted the
core SDD process skills (`draft/skills/subagent-driven-development`,
`test-driven-development`, `delta-spec-change`, `spec-kit-extensions`). What it lacks is the
**process/discipline** layer that governs the work *between* specs and commits:

- No **pre-spec design** skill — the flow jumps from a raw idea to `/speckit.specify`.
- No **debugging methodology** — a total gap; nothing tells an agent to find root cause before
  patching symptoms.
- No **planning discipline** skill — the plan/tasks templates exist but not the "exact paths,
  Consumes/Produces interfaces, no placeholders" rigor that makes a plan executable unattended.
- No **verification gate**, no **completeness/stub check**, no **code-review discipline**
  (especially *receiving* review), and no **workspace-isolation / branch-completion** bookends.

These are exactly the high-leverage, largely language-agnostic skills mined from superpowers and
intellegix. They exercise the machinery from [[P002]] and feed the quality gates in [[P006]].

## Proposal

Add a focused set of **new process skills** under `draft/skills/`, authored to spec-kit's
`SKILL.md` schema (with the `when_to_use` field proposed in [[P002]]), calm tone, Python/pytest
examples, and explicit terminal-state handoffs into the `/speckit.*` flow. Do **not** re-port
SDD or TDD (already drafted). Reconcile git-related skills with the existing three-tier
`git-workflow` rather than shipping a parallel model.

### Prioritized skill table

| Priority | Skill | when_to_use (trigger) | Source | Effort | Status vs spec-kit |
|----------|-------|-----------------------|--------|--------|--------------------|
| P0 | `systematic-debugging` (+3 refs) | a test/behavior is wrong before attempting a fix | superpowers | L–M | Absent — total gap |
| P0 | `brainstorming` | a vague idea needs shaping before `/speckit.specify` | superpowers | M | Absent |
| P0 | `verification-before-completion` | before claiming done/passing/fixed | superpowers | L | Partial (template only) |
| P0 | `stub-check` | after `/speckit.implement`, confirm no stubs/TODOs | intellegix | L | Absent |
| P1 | `writing-plans` | turning a spec into an executable task plan | superpowers | M | Partial (templates) |
| P1 | `requesting-code-review` + `receiving-code-review` | dispatching / responding to a reviewer | superpowers | L | Partial / Absent |
| P2 | `using-git-worktrees` | isolating a feature workspace before implement | superpowers | L–M | Partial (git-workflow) |
| P2 | `finishing-a-development-branch` | wrapping a feature (merge/PR/keep/discard) | superpowers | L | Absent |
| P2 | `dispatching-parallel-agents` | fanning out independent problems | superpowers | L | Absent (see [[P010]]/[[P004]]) |

`root-cause-tracing`, `defense-in-depth`, and `condition-based-waiting` ship as **references**
inside `systematic-debugging`, not as standalone skills.

## Design sketch

Each skill is a directory under `draft/skills/<name>/` with `SKILL.md` + `references/` +
optional `assets/`/`scripts/`, following `draft/skills/test-driven-development/SKILL.md`
(status banner, `when_to_use`, quick-reference tables). Frontmatter template:

```yaml
---
name: systematic-debugging
description: |
  Root-cause-first debugging discipline: reproduce, trace to the true cause, fix the cause
  (not the symptom), verify. If three fixes fail, question the architecture.
when_to_use: >
  A test fails, a behavior is wrong, or output is unexpected — before attempting any fix.
  Trigger phrases: "why is this failing", "flaky test", "works locally", "regression".
skill_id: "<SKILL:draft/skills/systematic-debugging/SKILL.md>"
---
```

### P0 skills

**`systematic-debugging`** — Iron Law "find the root cause before fixing"; 4 phases
(reproduce → trace → fix cause → verify); Phase 4.5 escape hatch ("3+ fixes = question the
architecture"). References:
- `references/root-cause-tracing.md` — backward tracing from symptom to origin.
- `references/defense-in-depth.md` — the multi-layer validation pattern.
- `references/condition-based-waiting.md` — poll-for-condition to kill flaky arbitrary-timeout
  tests (re-exampled for pytest).
- `assets/find-polluter.sh` — test-bisection to locate a state-polluting test.
Terminal state → hand to `test-driven-development` for the failing-test-first fix.

**`brainstorming`** — pre-spec design dialogue: one question at a time, propose 2–3 approaches,
gate against coding before an approach is approved, write + self-review a short design note.
Terminal state → invoke `/speckit.specify` (or `writing-plans`). Drop superpowers' Node-based
browser visual companion.

**`verification-before-completion`** — gate: no "done/passing/fixed" claim without fresh
command evidence (run → read output → then claim). Ships a red-flag phrase list. Cross-links
the existing `verification-log-template.md`; pairs with [[P006]] and a possible Stop-hook
reminder from [[P001]].

**`stub-check`** — completeness audit after implement: static Grep/Glob scan for stub markers
(`TODO`, `pass`, `NotImplementedError`, `raise NotImplementedError`, empty handlers,
`...`), cross-checked against each `tasks.md` item and the changed files; flags shallow/skeletal
code. Provider-free — pure scan plus one summarization pass. Pairs with `/speckit.analyze` and
the `/speckit.verify-completeness` command in [[P010]].

### P1 skills

**`writing-plans`** — planning discipline that enriches, not replaces, `plan-template.md` /
`tasks-template.md`: exact file paths per task, Consumes/Produces interface contracts between
tasks, a "No Placeholders" failure blacklist, and a self-review-against-spec checklist.
Terminal state → the SDD implement flow.

**`requesting-code-review`** (+ `references/code-reviewer.md`) and **`receiving-code-review`** —
the first ships a read-only reviewer prompt with severity buckets (reconciled with
`templates/review-template.md` and the existing
`draft/skills/subagent-driven-development/assets/final-code-reviewer-prompt.md`). The second is
the genuinely-absent discipline: verify a finding before implementing it, no performative
agreement, YAGNI check, push-back-with-reasoning protocol.

### P2 skills

**`using-git-worktrees`** — Step-0 isolation detection (including a submodule guard that defers
to `git-submodule-edit`), native-tool-first with a git-worktree fallback, baseline-test gate
before starting. Runs *before* `/speckit.implement`; explicitly reconciled with the three-tier
`git-workflow` (worktree isolation is orthogonal to branch sync).

**`finishing-a-development-branch`** — structured completion menu (merge / PR / keep / discard),
environment detection, provenance-based cleanup, typed-confirm on discard. Runs *after*
implement; hands back to `git-workflow` for the actual sync/merge.

**`dispatching-parallel-agents`** — when to fan out one agent per *independent* problem domain,
the self-contained prompt structure, and when **not** to. Referenced by
`systematic-debugging` (multi-domain failures) and the SDD skills; underpins [[P004]] /
[[P010]]'s orchestration commands.

### Skill-chaining map

```
brainstorming → /speckit.specify → writing-plans → /speckit.tasks
   → using-git-worktrees → /speckit.implement (SDD/TDD)
      → systematic-debugging (on failure)
   → stub-check → requesting/receiving-code-review
   → verification-before-completion → finishing-a-development-branch
```

## Source evidence

- superpowers catalog → `/cws_work/superpowers/skills/`: `systematic-debugging/SKILL.md` (Iron Law, 4 phases, "3 fixes = question architecture") with `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`, `find-polluter.sh`; `brainstorming/SKILL.md` (HARD-GATE, spec self-review, terminal→writing-plans); `verification-before-completion/SKILL.md` (Gate Function, red-flag table); `writing-plans/SKILL.md` (Consumes/Produces, No-Placeholders, self-review); `requesting-code-review/code-reviewer.md` + `receiving-code-review/SKILL.md`; `using-git-worktrees/SKILL.md` + `finishing-a-development-branch/SKILL.md`; `dispatching-parallel-agents/SKILL.md`.
- `stub-check` → `/cws_work/intellegix-code-agent-toolkit/commands/stub-check.md` (3-phase completeness audit; Grep/Glob stub scan).
- spec-kit anchors to reconcile / extend → `draft/skills/test-driven-development/SKILL.md` (draft skill format), `draft/skills/subagent-driven-development/assets/final-code-reviewer-prompt.md`, `templates/review-template.md`, `templates/plan-template.md`, `templates/tasks-template.md`, `skills/git-workflow/SKILL.md`, `skills/git-submodule-edit/SKILL.md`, and the existing `verification-log-template.md`.

## Adoption plan

**Phase 1, all under `draft/skills/`, no `/speckit.*` change:**

1. **P0 first:** `systematic-debugging` (+3 references + `find-polluter.sh`), `brainstorming`,
   `verification-before-completion`, `stub-check`. These are the largest gaps and mostly
   copy-and-re-example work.
2. **P1:** `writing-plans` (also propose the template enrichments to `tasks-template.md` /
   `plan-template.md`), `requesting-code-review` + `receiving-code-review`.
3. **P2:** `using-git-worktrees`, `finishing-a-development-branch`, `dispatching-parallel-agents`
   — authored to defer to the existing `git-workflow` / `git-submodule-edit` skills.
4. Register each in the Resource Registry (with `when_to_use` per [[P002]]) only when promoted
   out of `draft/`.

Every skill re-examples TypeScript/Node source snippets in Python/pytest, softens superpowers'
coercive framing to spec-kit's calm instruction style, and declares an explicit terminal-state
handoff so the library composes into a pipeline rather than a pile.

## Risks & mitigations

- **Duplicating existing skills.** SDD/TDD are explicitly excluded; git skills defer to
  `git-workflow`/`git-submodule-edit`; reviewer prompts reconcile with the SDD draft and
  `review-template.md` rather than forking them.
- **Over-strong mandates conflict with user precedence.** Keep gates and checklists, drop the
  "no choice / not negotiable / dishonesty" rhetoric; spec-kit honors user instructions first.
- **Language mismatch.** Superpowers examples are TS/Node; every ported skill is re-exampled in
  Python/pytest since spec-kit is a Python project.
- **Skill sprawl outpaces discovery.** [[P002]]'s budgeted index + `when_to_use` is the
  companion mechanism; these skills are authored specifically to feed it.
- **Not wired into the flow.** Intentional — they incubate in `draft/` and only affect behavior
  once promoted; handoffs point at real `/speckit.*` commands so promotion is a small step.

## Value / Effort rationale

**Value H.** These skills close spec-kit's biggest *process* gaps (no debugging methodology, no
design front-door, no completeness/verification gate) with high-leverage, largely
language-agnostic content. They make the difference between an agent that patches symptoms and
one that finds root cause, and between a plan that runs unattended and one that stalls.

**Effort L–M.** Most content is copy-and-re-example from superpowers, plus one static-scan skill
from intellegix. No infra, no runtime, no dependency — pure markdown skills in `draft/`. The
only M-effort items are `brainstorming` and `writing-plans` (dialogue design + template
reconciliation); everything else is L. The prioritized table lets adoption stop after P0 and
still deliver most of the value.
