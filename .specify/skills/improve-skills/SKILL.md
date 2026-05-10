---
name: improve-skills
description: This skill can continuously improve an existing Skill from actual execution history, user feedback, failure cases, and observed inefficiencies. Use this when the user mentions ["improve skills after use", "skill execution feedback", "refine SKILL.md", "skill retrospective", "skill iteration", "技能执行反馈", "基于执行问题优化skill", "持续改进Skill"]
skill_id: "<SKILL:.specify/skills/improve-skills/SKILL.md>"
---

# improve-skills

## Goal

Continuously improve an existing SpecKit Skill using evidence from real executions. The expected result is a focused Skill update that fixes observed problems, captures reusable lessons, and makes the next execution more reliable.

## Workflow

1. **Identify the target Skill and execution window**
   - If the user names a Skill, improve only that Skill.
   - If the user says “this Skill”, infer the target from the active file or recent conversation.
   - Treat `.specify/skills/<name>/SKILL.md` as the canonical source of truth; use `.github/skills/<name>` only as a compatibility entrypoint.
   - Re-read the canonical `SKILL.md` before editing, especially when the system reports recent user or formatter changes, or when a refresh/script may have modified metadata.
   - Define the execution window to review: current conversation, last Skill run, failed command output, user correction, test failure, or recent edits.
   - When improving `improve-skills` itself, use the most recent improvement loop as the execution window and avoid reapplying the same lesson unless new evidence shows the previous fix was insufficient.

2. **Collect execution history and feedback**
   - Gather concrete evidence before editing: user feedback, steps that were confusing, tool failures, wrong assumptions, repeated manual fixes, validation gaps, and changed files from the execution.
   - Include terminal/test outputs and error messages when they explain what went wrong.
   - Review changed files as evidence, but classify generated validation artifacts such as `tools/*.json` separately from hand-edited Skill instructions.
   - Separate facts from interpretation. Do not optimize from generic best-practice principles when no execution evidence supports the change.
   - If evidence is insufficient, ask one targeted question about what failed, what was inefficient, or what should happen differently next time.

3. **Organize the evidence into improvement items**
   - Group observations by failure mode: trigger/discovery, scope inference, missing context, wrong tool choice, unsafe step, unclear output, validation gap, or resource/reference issue.
   - For each item, record: observed symptom, likely cause in the current Skill instructions, desired next behavior, and the file section to change.
   - Discard one-off environment noise unless the Skill should explicitly handle it in future runs. If a refresh command exits successfully with a fallback after an optional source warning, record it as a validation note rather than a root cause.

4. **Analyze root causes and choose minimal changes**
   - Prefer changing the step that caused the observed problem over adding broad new rules.
   - Convert repeated user corrections into explicit decision branches.
   - Convert repeated manual checks into checklist items or deterministic scripts when appropriate.
   - Move detailed lessons to `./references/` only when they are useful but not needed every run.

5. **Update the Skill for the next execution**
   - Edit `SKILL.md` to make the improved behavior executable and checkable.
   - Update frontmatter `description` only when execution feedback shows trigger/discovery mismatch.
   - Update `./references/`, `./scripts/`, or `./assets/` only when the evidence shows they will reduce future mistakes.
   - Avoid adding process logs, changelogs, or full retrospectives to the Skill; distill only reusable lessons.

6. **Validate the improvement loop**
   - Re-read the changed Skill and verify that each edit maps to an observed execution issue.
   - Check frontmatter, resource paths, line count, compatibility entry, and registry row when metadata changed. If `skill_id` is added or corrected, ensure `.specify/instructions.md` has one deduplicated Skills registry row for the canonical Skill.
   - Accept a directory-level `.github/skills -> ../.specify/skills` symlink as a valid compatibility entrypoint; do not require a separate per-Skill symlink when the directory symlink already exposes the Skill.
   - When project scripts are available, refresh Skill tool manifests with `.specify/scripts/bash/create-new-skill.sh --refresh-only --name <name> --json` or `.specify/scripts/bash/refresh-tools.sh --mcp --system --shell --project --json` as appropriate.
   - If a combined validation command returns only partial output or omits later checks, rerun the missing checks individually before concluding validation passed.
   - After refresh, distinguish intended generated manifests from instruction changes in the final report, and mention non-blocking source warnings separately. If generated manifests changed only in timestamps, call that out as low-signal validation churn rather than behavior change.
   - Do not document `.specify/scripts/` as a Skill-owned resource directory; Skill-owned executable resources belong in `./scripts/`.

7. **Report the feedback-driven changes**
   - Summarize the execution feedback that drove the update.
   - List changed Skill files and the behavior expected to improve next time.
   - Note any unresolved feedback that needs another real execution to validate.

## Quality Checklist

Use [the Skill quality checklist](./references/skill-quality-checklist.md) to structure execution feedback, root-cause analysis, and validation when the improvement involves more than one observed issue.

## Resource ID

- Canonical ID: `<SKILL:.specify/skills/improve-skills/SKILL.md>`
- Canonical Path: `.specify/skills/improve-skills/SKILL.md`
