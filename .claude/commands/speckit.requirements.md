<!-- AUTO-GENERATED from templates/commands/requirements.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). The text after `/speckit.requirements` IS the feature description.

## Glossary

Apply the glossary protocol in `.specify/shared/workflow/glossary.md`, reading the project glossary at `.specify/memory/glossary.md` (ambient via the Documentation Map). That file owns every rule of this step and this section restates none of them: input correction and anchoring, **including the constraint-side reading of a registered term** (§1); progressive enrichment at wrap-up (§2); conflict detection and which writes proceed directly (§3); manual edits and user precedence (§4).

## Outline

1. **Generate short name** (2-4 words, action-noun format, e.g., "user-auth", "fix-payment-timeout").

2. **Check existing branches**:
   - `git fetch --all --prune`
   - Derive the next number from `.specify/specs/` directories (INCLUDING `.specify/specs/.archive/` — archived specs keep their numbers and a globally-max archived number would otherwise collide) plus branch names in the exact top-level `<NNN>-<slug>` form ONLY. Slash-namespaced remote branches (e.g. `origin/community/4059-*`, `origin/fix/4198-*`) are NOT spec numbering — their trailing digits must be excluded, or the next number gets inflated (e.g. 200 instead of 045)
   - Next number = highest + 1 (or 1 if none found)

3. **Run script** 
```bash
cat << 'EOF' | .specify/scripts/bash/create-new-requirements.sh --json --short-name "<SHORT_NAME>"
$ARGUMENTS
EOF
```
 from repo root (replace `<SHORT_NAME>`). Parse JSON for BRANCH_NAME and SPEC_FILE. Run only once.
   - Note: the script **pre-creates SPEC_FILE** with template placeholder content — you MUST `Read` it before writing (or overwrite via `Edit`); a blind `Write` fails with "File has not been read yet".

4. **Load** `.specify/templates/requirements-template.md` for required sections.

5. **Execute spec generation**:
   1. Parse user description. If empty: ERROR. **Conceptual/idea-level input** (long-form essays, methodology explanations, advocacy material): first distill it into landable requirement slices — identify the landing level(s) the material maps to (e.g. the framework/tool itself vs. the downstream projects adopting it) and draft stories for each level separately, instead of transcribing the material's own structure into the spec.
   2. Extract key concepts: actors, actions, data, constraints.
   3. Initialize `Related Feature`: `Feature ID: Need clarification`, `Feature Name: Need clarification` (resolved by `/speckit.clarify`).
   4. **Peek at house conventions (bounded, summary-first)**: sample the highest-numbered existing spec directory under `.specify/specs/<NNN>-<slug>/` and read its **`requirements.md`** — the same artifact filename this command writes (SPEC_FILE, step 3), and the same one `.specify/templates/requirements-template.md` scaffolds — with targeted excerpts: heading structure (`grep -n '^#'`), one user story, a few FR/SC lines, instead of reading the whole spec (see `.specify/shared/guidelines/token-efficiency.md`). Match its language, section conventions (e.g. Assumptions subsection), and Shared Strings usage. Aligning with the most recent merged spec reduces convention drift at zero clarification cost.
   5. **Concept-owner check**: when a requirement introduces, constrains, or redefines a concept the framework already defines, locate that concept's owner document under `.specify/shared/definitions/` **before drafting** and write to the owner's definition — not to recall of it, and not to a paraphrase from training knowledge. A concept with no locatable owner is a **new** concept: say so in the spec instead of defining it inline. Concept *names* additionally go through the glossary's constraint-side reading (`## Glossary` above).
   6. **Reserved identifier check**: if the spec names any new identifier (env var, macro, CLI flag, config key), grep the codebase for that name before drafting — a collision with an existing/reserved identifier (e.g. a build env var) must be surfaced with a proposed alternate name and an explicit user-override note, not silently adopted.
   7. **Port/integration input hygiene**: when the feature ports or integrates an external codebase, (a) treat the upstream's docs/roadmap as claims and verify capability statements against its **source code** before they shape story priorities (docs routinely lag code); (b) write any fact still pending async verification (inventory sizes, entry counts, platform matrices) in "dynamically probed at runtime" phrasing from the first draft — hard-coded point-in-time numbers force multi-section rewrites when verification returns.
   8. For unclear aspects: make informed guesses. Only use `[NEEDS CLARIFICATION: question]` if choice significantly impacts scope/UX, multiple interpretations exist, and no reasonable default. **Max 3 markers.**
   9. Fill User Scenarios & Testing — write as many stories as the feature decomposes into (the template's three slots are open-ended scaffolding, not a quota; delete unused slots).
   10. Generate testable Functional Requirements.
   11. Define measurable, technology-agnostic Success Criteria.
   12. Identify Key Entities (if data involved).

6. **Write spec** to SPEC_FILE. Preserve section order. Keep `Related Feature` with default "Need clarification" values.

7. **Quality Validation**: Follow the validation process in `.specify/shared/guidelines/requirements-guidelines.md`:
   - Create checklist at `FEATURE_DIR/checklists/requirements.md`
   - Validate spec against each item
   - Handle failures (max 3 iterations) and remaining clarifications (max 3 questions with table format)
   - Update checklist with pass/fail status

8. **Report**: Branch name, spec file path, checklist results, next phase readiness.

## Feature Integration

Apply [Feature Integration Protocol](.specify/shared/workflow/feature-integration.md) § Feature Binding Rules for lookup rules and integration responsibilities. **Binding timing**: this command does NOT create or bind Features itself — it always initializes `Related Feature` with `Need clarification` values (Outline steps 3/6) and defers the actual Feature lookup/creation/binding to the `/speckit.clarify` checkpoint, where the Binding Rules are applied.

## Guidelines

For detailed quality validation, success criteria guidelines (including the reader baseline these artifacts are written for), and AI generation best practices, see `.specify/shared/guidelines/requirements-guidelines.md`.

Key rules:
- Focus on WHAT and WHY, not HOW
- No embedded checklists (separate command)
- Max 3 [NEEDS CLARIFICATION] markers

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.requirements" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Artifact Commit

At wrap-up, **before** the Feedback and Documentation steps, commit the artifact this command produced — and only that artifact, staged by explicit path. Follow the canonical convention in `.specify/shared/workflow/artifact-commit-step.md`: run the deletion-surface audit first, use a single-line message per `.specify/templates/commit-template.md`, never `git add -A`, and never fold another command's uncommitted artifacts into this commit (report that as an upstream deviation instead). A read-only run that produced no artifact skips this step and says so in one line rather than creating an empty commit. Committing here does not advance the feature's lifecycle status and does not push.

## Handoffs

**Before**: Optional `/speckit.feature` to ensure feature registry is up to date — **recommended whenever `.specify/memory/features.md` is absent or still a placeholder**, otherwise `/speckit.clarify` has to bootstrap the registry mid-run while binding the Feature.

**After**: If spec has `[NEEDS CLARIFICATION]` or `Related Feature: Need clarification` → `/speckit.clarify`. Otherwise → `/speckit.plan`.