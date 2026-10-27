# Contracts: The code-review skill's own evolution (C-17…C-30)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the skill-level obligations: the non-interactive path, base resolution, the record header, the renderer-absence rewrite, the single gate verdict source, the sibling boundary, and the constraint that new capability lands on the existing script entity. The receipt's internal grammar is owned by `coverage-receipt.md`; the severity vocabulary and the `P0`–`P6` dimensions stay owned by the skill body itself and are not restated here.
**Pinned by**: `tests/contract/test_code_review_skill_contract.py`
**Measures**: SC-003, SC-005

**C-17**: The skill MUST provide a fully non-interactive path that runs to completion with no interactive prompt: record creation (and rotation), opinion capture, coverage receipt, and the summary verdict are each reachable as a deterministic subcommand with arguments only. A caller MUST NOT have to answer a prompt, invent a terminal, or hand-write a record file to finish a review (FR-021).

**C-18**: Base resolution MUST be implemented in the skill's deterministic script and MUST be overridable by an explicit caller parameter. The order is: explicit value, else the parent of the first commit that added this feature's `requirements.md`, else the merge base with the repository's default trunk. The same repository state MUST resolve to the same base on every run, and the resolution MUST NOT be delegated to prompt-time judgement (FR-004, FR-022).

**C-19**: The feature-slice tier derives its commit from the first-add instrument `git log --diff-filter=A -- <spec>/requirements.md`, never from `git log -1` over the directory. That instrument is the one the flow-classification wall-clock baseline already pins, so the code segment and the baseline measure the same freeze point (FR-004, FR-022).

**C-20**: The composed path MUST NOT rely on the script's built-in base default or on any branch name. When no tier resolves, the code segment records [[STR-002]] together with a reproducible command and the failure reason; it MUST NOT fall back to a guessed base or to "a commit that looks close" (FR-004, FR-006).

**C-21**: The record header MUST carry: branch, base and head commit identifiers (full and short), the base source tier, the renderer mode marker, the reviewer, and the run date. One header form exists; a second header layout is a violation (FR-022).

**C-22**: When the renderer (`delta`) is unavailable the code segment MUST still complete, and the record MUST carry the renderer marker in its text form [[STR-003]]. When the renderer is available the marker carries the rendered form and rendering is the default (FR-013).

**C-23**: The record MUST NOT contain any statement claiming that a rendered, visual or side-by-side review was performed while the text mode ran. The false claim — not the missing tool — is the defect this clause forbids (FR-013, SC-003).

**C-24**: The previous "renderer missing ⇒ stop" clause MUST be rewritten, not deleted. The skill body MUST keep one statement naming (a) the replaced clause, (b) its substitute evidence form — the coverage receipt — and (c) the reason for the replacement. The same rewrite MUST reach every surface that carried the old assertion: the `Strict Requirements` block, the Phase 0 environment-confirmation step, and the skill's `references/` wording. No surface may retain a "stop when the renderer is missing" assertion. The neighbouring invariant survives verbatim: the skill never installs the renderer itself, and the absent-renderer path is announced with the install pointer rather than attempted silently (FR-013, SC-003).

**C-25**: "The whole diff was read" has exactly one evidence form: the coverage receipt. A diff overview, a changed-file listing, a small changed-line count, or the mere existence of tool output MUST NOT substitute for it, and none of them alone may be cited as evidence that a review happened (FR-015).

**C-26**: The merge-gate verdict MUST continue to be produced by the skill's deterministic script. After composition exactly one verdict source exists: the command reuses that verdict and MUST NOT compute a second criterion set, a second threshold, or a second green/red judgement (FR-023).

**C-27**: The verdict subcommand MUST take the record path explicitly. It MUST NOT select its target by "newest file in the directory": one feature directory holds both `review.md` and [[STR-004]], and an implicit pick can read the process report, find no `blocking` heading in it, and return a false allow. An invocation that omits the path is a legacy mode that labels its selection as implicit and is never used by the composed path (FR-023).

**C-28**: The interactive human path MUST be preserved and MUST NOT degrade: with the renderer available it is the default, the per-file walk keeps its tests-first ordering and its focus option, and the six-level severity validation keeps rejecting any value outside the closed set (FR-024).

**C-29**: The boundary between the two review skills MUST be decidable from the documents alone: each skill declares its own judgment object, and both declare that the command composes them in a fixed order. The wording "the two are unrelated, keep them separate" MUST NOT survive anywhere, because after composition it is false — the surviving statement is "distinct judgment objects, composed by the command" (FR-025).

**C-30**: Every new deterministic capability this feature adds — base resolution, record creation and rotation, the coverage receipt, and the explicit-input verdict — MUST land as subcommands of the skill's existing script entity. No new engine, helper daemon, background process, external service, or package dependency may be introduced (FR-026).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-17 | FR-021 | — | skill body + script |
| C-18 | FR-004, FR-022 | — | script |
| C-19 | FR-004, FR-022 | — | script |
| C-20 | FR-004, FR-006 | — | script + skill body |
| C-21 | FR-022 | — | script |
| C-22 | FR-013 | SC-003 | skill body + script |
| C-23 | FR-013 | SC-003 | skill body |
| C-24 | FR-013 | SC-003 | skill body + references |
| C-25 | FR-015 | — | skill body |
| C-26 | FR-023 | — | script + command |
| C-27 | FR-023 | — | script |
| C-28 | FR-024 | — | skill body + script |
| C-29 | FR-025 | — | both skill bodies |
| C-30 | FR-026 | — | script |
