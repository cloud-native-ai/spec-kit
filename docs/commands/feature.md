# /speckit.feature

Maintain and refresh the project feature registry — the long-lived backbone that tracks features from inception through completion.

## When to Use

- After project setup to generate the initial feature list from repo scanning
- When the codebase has evolved and features need to be refreshed
- To discover future features via gap analysis (DFX catalog)
- To update specific feature metadata after commits, PRs, or branch changes

## Syntax

```text
/speckit.feature [feature management action]
```

The command operates in three modes based on input:

| Input | Mode | Behavior |
|-------|------|----------|
| No arguments | Global generate/refresh | Scan repo, infer features, discover future features |
| Concrete context (commit, PR, branch) | Context mining | Update features impacted by the change |
| Description only | Index-locate-and-refresh | Find matching feature and refresh its metadata |

## Execution Flow

1. **Determine project type and delivery model** — Infers from repo structure, README, and build config:
   - `PROJECT_TYPE`: CLI, Library/SDK, Framework, Microservice, Web App, etc.
   - `DELIVERY_MODEL`: Runtime code, Document/prompt artifacts, or Hybrid

2. **Generate/refresh current feature list**:
   - **Functional features**: Tailored to project type (CLI → commands/subcommands; Library → core APIs; etc.)
   - **Non-functional features**: Derived from repo's current state (testing, observability, security, etc.)

3. **Discover future features** — Project-intrinsic gap analysis:
   - Prioritizes features that improve core value delivery
   - For document-artifact projects: template validation, cross-consumer compatibility, artifact lifecycle
   - For runtime code projects: applies the DFX Catalog (Testability, Observability, Reliability, Security, Performance, etc.)
   - Creates future features with `Draft` status (max 8–12 per run)

4. **Allocate new IDs** — Sequential three-digit `FEATURE_ID` by scanning `.specify/memory/features/`.

5. **Instantiate or update feature detail files** — From `feature-details-template.md`:
   - Replaces all placeholders
   - Sets status (Draft / Planned / Implemented / Ready for Review / Completed)
   - Sets creation and last-updated dates

6. **Update feature index** — Ensures `.specify/memory/features.md` table has all features with correct columns. Auto-derives `FEATURE_COUNT` from the table row count.

7. **Sync README feature list** — Generates or replaces a "Feature List" section split into Functional and Non-functional features.

8. **Validate** — No leftover placeholders, unique sequential IDs, valid dates, correct table formatting.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Feature detail files | `.specify/memory/features/<ID>.md` |
| Feature index | `.specify/memory/features.md` |
| README feature list | `README.md` |

## Feature Statuses

| Status | Meaning |
|--------|---------|
| Draft | Identified but not yet planned |
| Planned | Requirements and plan created |
| Implemented | Code written and tasks completed |
| Ready for Review | Awaiting quality review |
| Completed | Fully delivered and verified |

## DFX Catalog Categories

The command checks for coverage of these design-for-X categories (filtered by project type and delivery model):

DFT (Testability), DFO (Observability), DFR (Reliability), DFSec (Security), DFP (Performance), DFS (Scalability), DFD (Deployment), DFM (Maintainability), DFC (Compatibility), DFA (Accessibility), DFI (Internationalization), DFCfg (Configuration), DFDoc (Documentation), DFDat (Data Integrity)

## Prerequisites

- Run [`/speckit.constitution`](constitution.md) if changing governance rules that affect feature definitions

## Next Steps

- Typically proceed to [`/speckit.requirements`](requirements.md) to produce a requirements specification for a chosen feature
