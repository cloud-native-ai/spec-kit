<!-- AUTO-GENERATED from templates/commands/feedback.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. The input selects the execution mode and may carry a slice/kind/probe filter (Mode 2) or a target custom unit (Mode 3).

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`) and apply the protocol in `.specify/shared/workflow/glossary.md`: correct recorded homophone/confusable variants before acting; propose new terms at wrap-up with user confirmation.

## Outline

This command is the local management interface for the Feedback Probe system. It works in **three execution modes**; with no arguments it defaults to Mode 1.

### Mode 1 — Probe Overview (default; no arguments)

Print **every probe placed in the current project** as a graphical list / vertical (tree) structure.

```bash
python3 .specify/scripts/python/feedback-utils.py --action probes
python3 .specify/scripts/python/feedback-utils.py --action probes --validate     # schema check
python3 .specify/scripts/python/feedback-utils.py --action probes --reconcile   # embed audit
python3 .specify/scripts/python/feedback-utils.py --action map                  # OPTIONAL (writes): rebuild probe-map.md
```

Render the merged truth source (framework Classes/Objects + project external probes) as a tree: kind → class (with target slice, collection, processing) → objects (unit @ lifecycle point). Mark internal vs external. The overview MUST be rendered from the truth source — never a hand-maintained list. Empty external section: show the `external-custom` class with its zero-object marker, no error.

### Mode 2 — Process Collected Feedback

Guide the user through the local processing loop:

1. **Status view**: `--action status` (count / threshold / should_prompt).
2. **Summary view**: `--action list --limit 0` with filters as requested — `--slice <commands|skills|host-custom|...>`, `--kind <internal|external>`, `--disposition <processed|ignored|open>`, plus the pre-existing `--unit-id/--since/--contains`.
3. **Disposition**: `--action dispose --id <entry-id> --to processed|ignored` (local metadata only).
4. **Package** (on user confirmation, internal entries only): `--action package` → print zip path + manual-send guidance. The agent NEVER sends the zip.
5. **Post-package cleanup** (only after the user confirms the batch is dealt with): `--action cleanup --package <zip|latest> --dry-run` to preview, then run without `--dry-run`. Cleanup removes only entries actually inside that zip; `cleanup-log.md` records every removal.

### Mode 3 — Inject an External Probe

For host-project custom Skills/Agents/Commands (assets the framework's own probes never cover):

1. Elicit the target unit (`custom:<owner>/<name>`), lifecycle point (default `wrap-up`), and a short collection-intent note (`--notes-file`).
2. Run `--action probe-inject --unit custom:<owner>/<name> --notes-file <file>` — writes `.specify/memory/feedback/probes/ext-<slug>.md`.
3. Verify the injection: the object appears in `--action probes` and after `--action map`.

External-probe feedback is **host-project-local** (Loop B — the project's own use→feedback→iterate loop): it feeds the project's own optimization, is separately filterable via `--kind external`, and is **never** included in upstream packages.

## Behavior Rules

- Zero network operations of any kind (red line); `mark-submitted` remains local bookkeeping.
- All actions run against the local store `.specify/memory/feedback/`; never edit store files by hand.
- Exit code 2 from the engine is a verdict — report it, do not argue around it.
- Probe truth source: `.specify/shared/definitions/probe-definitions.md` (+ project `probes/`); derived views (`probe-map.md`) are rebuilt, never hand-edited.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this command reached its wrap-up stage. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against `/speckit.feedback`'s declared purpose and produce a short review plus ≥1 concrete, command-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this command's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a nested skill/command already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "/speckit.feedback" --unit-type command \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
   Probe attribution: the engine resolves the unit to its probe object automatically — the entry inherits kind/slice from the probe registry. External custom units record via `--unit-id custom:<owner>/<name> --unit-type custom-unit`; their entries stay host-project-local and never enter upstream packages.
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.

## Handoffs

**Before**: none (any Spec Kit project; requires the probe registry installed by `/speckit.instructions`).

**After**: Mode 3 injection → the host project's own improvement loop (`improve-skills` / `improve-agent` consume `list --kind external` findings). Mode 2 cleanup → `mark-submitted` if not yet run for the batch.