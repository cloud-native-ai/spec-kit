# P007 — Context & Memory Management

- **Status:** Draft
- **Pillars:** Workflow/Process · Skills · Scripts
- **Source projects:** claude-code-ts, learn-claude-code
- **Value:** H · **Effort:** M · **Phase:** 2
- **Related:** [[P004]], [[P005]], [[P006]]

## Problem / Gap

A full Spec-Driven cycle — `/speckit.specify` → `plan` → `tasks` → `analyze` → `implement`
across many files, often over many turns — is one of the longest-running interactions a host
agent has. Two distinct durability problems bite:

1. **In-session context overflow.** As the transcript grows, the host compacts or the window
   fills, and the *plan itself* gets summarized away: the constitution constraints, the active
   task IDs, the next concrete step. spec-kit has **no compaction guidance and no transcript
   persistence** — when the host compacts, spec-kit contributes nothing to what is preserved,
   so the recovery is whatever the host happens to keep. This is the context half of the same
   durability gap [[P004]] addresses for task state.

2. **Cross-session memory is coarse.** spec-kit *does* have a memory layer —
   `.specify/memory/` with `constitution.md`, a `features.md` registry, per-feature
   `features/<ID>.md`, `tools.md`, and a `feedback/` dir. But it is a hand-maintained *feature
   registry*, not a general context store: there is no discipline for what durable
   non-derivable context (user preferences, prior review feedback, project conventions) should
   be saved, no way to select the *relevant* few memory files for a given task, and no cap to
   stop it bloating. There is also no bridge from a compacted/ended session back into memory.

The research repos supply both halves: a **multi-strategy compaction ladder** (cheap trimming →
LLM summary → save-to-disk) with a structured summary prompt, and an **LLM-selected memory
directory** with a strict taxonomy of what *not* to store. The task is to adopt these *on top
of* spec-kit's existing memory, not to replace it.

## Proposal

Three additive capabilities, all file-state + skills + one script, nothing that owns the loop:

1. **Compaction ladder** — a cheapest-first sequence (snip stale tool output → structured LLM
   summary → persist to disk), expressed as a `context-compaction` skill + a
   `/speckit.compact` command that produces a *resumable brief* preserving the constitution,
   active task IDs (from [[P004]]'s graph), and the verbatim next step.
2. **Transcript persistence** — before any summarization, the raw session is written to
   `.specify/specs/<KEY>/.transcripts/` so nothing is ever lost; the durable [[P004]] task
   graph is the recovery anchor the brief points back to.
3. **Memory directory with taxonomy** — extend `.specify/memory/` with a typed, LLM-selectable
   context store (a capped `MEMORY.md` entrypoint + typed files with a strict "what not to
   save" rule), reusing the existing registry rather than inventing a parallel store.

## Design sketch

### 1. Compaction ladder

Four rungs, invoked in order only as needed (the cheap rungs are conventions the host follows;
the expensive rungs are the `/speckit.compact` command):

```
Rung 1  snip / drop stale tool RESULTS (Read/Bash/Grep/Glob/WebFetch output) — keep the
        reasoning, replace bodies with "[old tool result cleared]". Keep head + tail.
Rung 2  micro-summary of the oldest N turns into 2-3 lines, in place.
Rung 3  structured LLM summary (the 9-section prompt below) at a token threshold.
Rung 4  persist full transcript to disk BEFORE summarizing (never summarize the un-saved).
```

**Critical invariant (from learn-claude-code):** when trimming, never break a `tool_use` from
its matching `tool_result` — drop or keep the pair together. The skill states this explicitly
because it is a subtle correctness rule a host can violate.

### `/speckit.compact` command + `templates/compact-summary.md`

Ship a structured summary template (adapted from claude-code-ts's 9-section prompt) tuned for
SDD, with an `<analysis>` scratchpad that is stripped before the summary re-enters context:

```
1. Feature & spec:      <KEY>, one-line objective, spec/plan/tasks paths
2. Constitution constraints in force  (copied verbatim — never summarized away)
3. All user messages / decisions this session   (list, do not paraphrase away intent)
4. Files changed so far  (path + why)
5. Task state snapshot   (from .tasks/ : done / in_progress / ready / blocked IDs)
6. Verification evidence captured  (SC statuses, commands run + results)
7. Open questions / blockers
8. What was JUST happening  (the in-flight task and its partial state)
9. NEXT STEP — verbatim, concrete, single next action  (prevents post-compaction drift)
```

Sections 2, 3, and 9 are load-bearing: they are exactly what a naive host compaction loses.
The command writes the brief to `.specify/specs/<KEY>/.transcripts/summary-<ts>.md` and returns
it as the resumption context.

### 2. Transcript persistence + recovery

```
.specify/specs/<KEY>/.transcripts/
   session-<ts>.jsonl        # raw turns, appended live (written before any summarize)
   summary-<ts>.md           # structured brief from /speckit.compact
```

Recovery flow after a compaction or restart: read the latest `summary-*.md`, re-read the
[[P004]] task graph (`task_graph.py status <KEY>`) as the authoritative live state, re-inject
identity/role (which agent, which task) — mirroring learn-claude-code's identity re-injection
that cures post-compaction amnesia. The task graph, not the transcript, is the source of truth;
the brief just re-orients the agent to it.

### 3. Memory directory with taxonomy (extends `.specify/memory/`)

Keep everything spec-kit already has (`constitution.md`, `features.md`, `features/<ID>.md`,
`tools.md`, `feedback/`). Add a *context* layer beside it:

```
.specify/memory/
   MEMORY.md                 # entrypoint, CAPPED (<= 200 lines / 25KB) — index + hot notes
   context/
     <slug>.md               # one durable note per file, frontmatter-typed
   (existing) constitution.md, features.md, features/, tools.md, feedback/   # unchanged
```

Each `context/*.md` carries frontmatter:

```yaml
---
type: user | feedback | project | reference   # 4-type taxonomy
description: "one line, used for LLM selection without opening the file"
updated: 2026-07-06
---
```

**Strict "what NOT to save" rule** (the discipline that keeps memory small — from
claude-code-ts): never store anything *derivable from project state* — code patterns,
architecture, git history, or anything already in the constitution / features registry. Memory
is only for **non-derivable** context: stable user preferences, prior review feedback that
should shape future work, cross-session project conventions not yet in the constitution.

**LLM selection at cost of headers only:** a `memory-select` step (skill or small script)
scans only the `description` frontmatter across `context/*.md` and picks up to ~5 relevant
files for the current task, rather than loading the whole store.

```
memory_select.py <KEY> "<task subject>"   # reads only frontmatter descriptions
                                          # -> ranked list of up to 5 context/*.md paths
```

### Wiring

```
long /speckit.implement run nears context limit
   -> Rung 1-2 (host trims stale tool output, keeps tool_use/result pairs intact)
   -> Rung 4 persist transcript  -> Rung 3 /speckit.compact -> summary-<ts>.md
   -> resume: read summary + task_graph.py status + memory_select -> continue
end of feature
   -> distill any NON-DERIVABLE learnings into .specify/memory/context/*.md (typed)
```

`/speckit.compact` is a candidate [[P001]] `PreCompact` hook so it fires automatically on host
compaction; without hooks it is invoked manually or by the [[P005]] loop when a token threshold
trips.

## Source evidence

- **Multi-strategy compaction (snip / microcompact / summary / auto) + 9-section structured
  summary prompt with `<analysis>` scratchpad** → `claude-code-ts`
  `src/services/compact/prompt.ts` (`BASE_COMPACT_PROMPT`, `NO_TOOLS_PREAMBLE`),
  `microCompact.ts`, `autoCompact.ts`, `snipCompact.ts`;
  `_research/claude-code-ts-agent-core.md` idea #6.
- **Cheap-first/expensive-last ladder, save-transcript-before-summarize, tool_use↔tool_result
  pairing invariant** → `learn-claude-code` `s08_context_compact/README.en.md`,
  `s08_context_compact/code.py` (`snip_compact`), `docs/en/s06-context-compact.md`;
  `_research/learn-claude-code.md` idea #3.
- **LLM-selected memory directory, 4-type taxonomy, capped entrypoint, "what not to save"** →
  `claude-code-ts` `src/memdir/memdir.ts` (caps), `findRelevantMemories.ts`
  (`SELECT_MEMORIES_SYSTEM_PROMPT`), `memoryTypes.ts`;
  `_research/claude-code-ts-agent-core.md` idea #7.
- **Identity re-injection to cure post-compaction amnesia** → `learn-claude-code`
  `docs/en/s11-autonomous-agents.md` (identity re-injection when `len(messages) <= 3`);
  `_research/learn-claude-code.md` idea #4.
- **Task graph as the durable recovery anchor** → `_research/learn-claude-code.md` idea #1
  (see [[P004]]).

## Adoption plan

**Phase 2a — compaction template + command (draft).** Ship `templates/compact-summary.md` and
a draft `/speckit.compact` command + `context-compaction` skill (encoding the ladder + the
tool_use/result invariant). Purely additive: an agent can invoke it, but nothing calls it
automatically. Validate the brief round-trips a real long session on an existing spec.

**Phase 2b — transcript persistence.** Add the `.transcripts/` convention under the per-feature
root and a tiny writer helper; document the recovery flow (read summary → `task_graph.py
status` → re-inject identity). Depends on [[P004]] for the task-graph anchor.

**Phase 2c — memory context layer.** Add `MEMORY.md` (capped) + `context/` with the typed
frontmatter and the "what not to save" rule to `.specify/memory/`, plus `memory_select.py`.
Extend, do not touch, the existing `features.md` / `constitution.md` semantics. A
`memory-curator` skill decides at feature end what non-derivable learnings to persist.

**Promotion.** Once proven, register `/speckit.compact` as a [[P001]] `PreCompact` hook and
have the [[P005]] loop trigger it at a token threshold; teach the `/speckit.*` flow to run
`memory_select` at task start. Until then everything lives in `draft/`; the main flow is
untouched and the existing memory registry keeps working unchanged.

## Risks & mitigations

- **Summary loses load-bearing intent.** Mitigation: the template mandates verbatim retention
  of constitution constraints (§2), all user decisions (§3), and the next step (§9) — the three
  things naive compaction drops; the raw transcript is persisted first so nothing is
  irrecoverable.
- **Broken tool_use/tool_result pairs corrupt the resumed context.** Mitigation: the skill
  states the pairing invariant explicitly and trims only complete pairs; provide a small
  validator the host can run on the trimmed transcript.
- **Memory bloat / storing derivable junk.** Mitigation: hard cap on `MEMORY.md`, the strict
  "what not to save" taxonomy, header-only selection so size never enters context, and a
  curator skill that prunes; memory is opt-in per project.
- **Duplicating the existing memory feature registry.** Mitigation: the new `context/` layer is
  explicitly *additive* and typed differently from `features.md`; the constitution and feature
  registry remain the source of truth for anything derivable, and the "what not to save" rule
  forbids overlap by construction.
- **spec-kit can't force host compaction.** Mitigation: express rungs 1–2 as conventions and
  make rungs 3–4 an explicit command / [[P001]] `PreCompact` hook — spec-kit contributes the
  *what to preserve*, the host owns *when*, consistent with the scaffolding-not-runtime
  principle.

## Value / Effort rationale

**Value: H.** Long SDD sessions are where spec-kit is most useful and most fragile; losing the
plan to a mid-run compaction is a common, expensive failure. A structured brief + persisted
transcript + durable task graph makes long sessions resumable, and a disciplined memory layer
gives cross-session continuity (user prefs, prior feedback) that compounds over a project.
Together they are the context complement to [[P004]]'s state durability and a prerequisite for
[[P005]]'s unattended runs.

**Effort: M.** The compaction template and command are mostly prompt/skill authoring over a
proven design (low). Transcript persistence is a small file convention. The memory context
layer plus header-only selection is moderate but builds directly on the existing
`.specify/memory/` structure rather than starting fresh, keeping total effort at M.
