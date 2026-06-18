# /speckit.review

Critically review the SDD process for the current feature and produce a self-contained, improvement-focused report for spec-kit maintainers.

## When to Use

- After `/speckit.implement` completes — to evaluate the SDD process quality
- When you want to identify friction, ambiguity, and improvement opportunities in the spec-kit workflow
- To generate a portable report that can be shared with framework maintainers

## Syntax

```text
/speckit.review [review criteria or focus areas]
```

`[review criteria or focus areas]` is optional — specify quality dimensions or reporting preferences.

## Execution Flow

1. **Capture portable project context** — Collects repo name, URL, branch, commit SHA, environment info, spec-kit version, and an artifact inventory table. All paths are absolute or paired with `{REPO_URL}@{COMMIT_SHA}` for portability.

2. **Reconstruct process execution history** — Analyzes git log, scoped to the requirements directory, to determine:
   - Which `/speckit.*` commands were run and in what order
   - Deviations from the prescribed workflow
   - Manual workarounds and ad-hoc files
   - Friction moments (dirty working tree, toolchain issues, template gaps)

3. **Load core SDD artifacts**:
   - **Required**: `requirements.md`, `plan.md`, `tasks.md`
   - **Optional**: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `checklists/`, `feature-ref.md`
   - **Reference**: constitution, templates, scripts, command instruction files

4. **Diagnostic review** — For each artifact and the workflow as a whole, identifies:
   - **Friction**: Template/prompt/script elements that forced extra work
   - **Ambiguity/contradiction**: Conflicting instructions across templates and commands
   - **Cargo-cult/boilerplate**: Template content from another stack/domain
   - **Missing structure**: Information invented ad hoc because no template field captured it
   - **Drift risk**: Same facts in multiple places without a single source of truth
   - **Process gaps**: Lifecycle steps lacking automation or checks

5. **Findings** — Each finding includes:
   - ID (F1, F2, ...), Severity (P0/P1/P2), Category
   - Location (absolute path or repo URL)
   - Quoted evidence excerpt
   - Why it's a problem
   - Proposed fix targeting a specific file/section

6. **Generate report** — Instantiates the review template with:
   - Section 0: Portable Project Context
   - Section 1: Process Execution Timeline
   - Section 2: Findings Summary (counts by severity and category)
   - Section 3: Detailed Findings
   - Section 4: What Worked (short bullet list)
   - Section 5: Improvement Recommendations (grouped by category)
   - Section 6: Priority Roadmap

7. **Self-containment check** — Verifies every path is absolute, every finding has evidence, and no placeholders remain.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Review report | `.specify/specs/<key>/review.md` |

## Key Characteristics

- **Problem-first, not summary-first** — focuses on what to change, not what each artifact contains
- **Self-contained** — works without filesystem access; evidence is quoted inline
- **Process scope only** — evaluates the SDD workflow, not the feature's business merits
- **Evidence-backed** — findings without quoted excerpts are dropped

## Severity Levels

| Severity | Meaning |
|----------|---------|
| P0 | Blocks correct use of spec-kit or creates silent corruption risk |
| P1 | Recurring friction across specs |
| P2 | Quality-of-life improvement |

## Prerequisites

- Run after [`/speckit.implement`](implement.md) so there is a complete artifact chain to review

## Next Steps

- Apply improvements to spec-kit templates, command prompts, and scripts
- Optionally iterate on [`/speckit.requirements`](requirements.md) or [`/speckit.plan`](plan.md) to fix current-spec findings
- Optionally run [`/speckit.analyze`](analyze.md) to validate consistency after revisions
