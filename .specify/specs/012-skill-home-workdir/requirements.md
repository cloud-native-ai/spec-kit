# Requirements Specification: SKILL_HOME and SKILL_WORKDIR Path Conventions

**Requirement Branch**: `012-skill-home-workdir`  
**Created**: 2026-05-30  
**Status**: Draft  
**Input**: User description: "优化templates/commands/skills.md的实现,为了适配不同的Agent执行引擎,需要在SKILL的实现中明确的定义SKILL_HOME和SKILL_WORKDIR两个概念:1)SKILL_HOME=skill在文件系统中的真实目录,是skill中所有相对目录的根目录通常就是`dirname $(readlink -f SKILL.md)`的值,不同的Agent中通常SKILL的安装方法和安装路径不同,我希望的是通过这个变量能够统一描述中的所有路径引用;2)SKILL_WORKDIR指的是SKILL中各个脚本的运行目录,通常等于`bash -c 'pwd || echo ${PWD}'`,希望通过这个变量能够统一运行时的路径引用."

## Related Feature *(mandatory)*

**Feature ID**: 013  
**Feature Name**: Skills Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Author writes skill-resource paths once, runs everywhere (Priority: P1)

A skill author writing or improving a Skill needs to reference internal resources — scripts under `scripts/`, references under `references/`, and assets under `assets/` — without knowing how a particular agent (Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder, or future agents) installs the Skill on disk. The author writes path references using a single, well-defined variable that always resolves to the Skill's real on-disk root, regardless of whether the agent stores Skills under `.specify/skills/`, `.github/skills/`, `~/.copilot/skills/`, an agent-specific path, or a symlinked compatibility entry.

**Why this priority**: This is the core problem the user raised. Without it, Skill instructions either (a) bake in a specific install layout and break when an agent uses a different one, or (b) rely on relative paths that drift when the Skill is invoked from outside its directory. P1 because every existing and future Skill depends on it.

**Independent Test**: Can be fully tested by taking one Skill that uses the new convention, installing it under two different agent layouts (e.g., `.specify/skills/<name>/` and a symlinked `.github/skills/<name>/`), invoking it from each, and verifying the Skill correctly resolves its own scripts/references/assets in both setups without edits.

**Acceptance Scenarios**:

1. **Given** a Skill author is writing a SKILL.md, **When** they need to reference `scripts/init.sh` inside the same Skill, **Then** the orchestration template instructs them to write `${SKILL_HOME}/scripts/init.sh` and explains that SKILL_HOME is the resolved real directory of SKILL.md (computed as `dirname $(readlink -f SKILL.md)` in shell contexts).
2. **Given** the same Skill is installed under `.specify/skills/foo/` on one agent and under `~/.copilot/skills/foo/` on another, **When** the Skill is invoked on either agent, **Then** `${SKILL_HOME}` resolves to the correct absolute directory in each agent and all Skill-resource references work without modification.
3. **Given** a Skill is reached through a symlink (e.g., `.github/skills/foo` → `.specify/skills/foo`), **When** the Skill resolves `${SKILL_HOME}`, **Then** the value is the real target directory (not the symlink path), so resource lookups stay stable across compatibility entries.

---

### User Story 2 - Scripts operate on the user's working directory, not on the Skill (Priority: P1)

When a Skill executes a script that needs to read or write files in the user's project (the directory the user invoked the agent from), the script must distinguish between "where the Skill lives" (its own assets) and "where the user is working" (the operation target). The author writes runtime path references using a second well-defined variable that always resolves to the directory in which the script is currently executing — typically the user's project root.

**Why this priority**: Without this distinction, Skill scripts conflate the Skill's install directory with the user's working directory, causing them to read templates from the wrong place, write outputs into the Skill installation, or leak files between users. P1 because the bug class is silent and corruption-prone.

**Independent Test**: Can be fully tested by writing a Skill with one script that reads a template from `${SKILL_HOME}/assets/template.md` and writes the rendered output to `${SKILL_WORKDIR}/output.md`, invoking it from any user project directory, and verifying the input is read from the Skill installation and the output appears in the user's project — not the Skill's install path.

**Acceptance Scenarios**:

1. **Given** a Skill script needs the user's current project directory, **When** the script runs, **Then** `${SKILL_WORKDIR}` is defined as the script's runtime working directory (computed as `bash -c 'pwd || echo ${PWD}'` in shell contexts) and the orchestration template documents this as the canonical way to reference runtime/user paths.
2. **Given** a Skill author needs to read a Skill-owned reference and write to the user's project in the same script, **When** they author the script, **Then** the template guidance is unambiguous about using `${SKILL_HOME}` for the read and `${SKILL_WORKDIR}` for the write, without conflating the two.
3. **Given** an agent invokes a Skill from a user working directory `/Users/alice/proj`, **When** the Skill script reads `${SKILL_WORKDIR}`, **Then** it equals `/Users/alice/proj` regardless of where the Skill is installed on disk.

---

### User Story 3 - Existing Skills migrate without breakage (Priority: P2)

Authors of already-shipped Skills (`create-skills`, `improve-skills`, `analysis-project`, `draw-d3js`, `draw-echarts`, `draw-plantuml`) need a clear migration path so updating to the new convention does not require an atomic rewrite. The template is explicit about which legacy idioms (relative `./` paths, `SKILL_ROOT` references, agent-specific install paths embedded in instructions) map to which new variable, so authors can migrate one Skill at a time without breaking the others.

**Why this priority**: Adoption depends on a non-disruptive transition. P2 because the new convention is most valuable for new Skills first; the old Skills can be migrated as part of normal `improve-skills` work.

**Independent Test**: Can be fully tested by picking one existing Skill that uses relative `./scripts/...` paths, applying the migration guidance from the updated template, and confirming behavior is identical before and after on at least one agent.

**Acceptance Scenarios**:

1. **Given** an existing Skill uses relative paths like `./references/checklist.md`, **When** the Skill author consults the updated template, **Then** the template provides explicit before/after examples mapping `./references/...` to `${SKILL_HOME}/references/...`.
2. **Given** the existing `create-skills` SKILL.md uses `SKILL_ROOT` to denote the Skill install directory, **When** the new convention is introduced, **Then** the template explains how `SKILL_HOME` and `SKILL_ROOT` relate (or supersede each other) so authors are not left with two competing concepts and unclear precedence.
3. **Given** a Skill has not yet been migrated, **When** an agent invokes it, **Then** the Skill continues to function under its existing path conventions during the migration window — adoption is opt-in per Skill rather than a flag-day change.

---

### Edge Cases

- **Symlinked install paths**: When the Skill is reached through a directory-level symlink (e.g., `.github/skills` → `.specify/skills`), `${SKILL_HOME}` must resolve to the real target directory so resource lookups don't depend on which entrypoint the agent used.
- **Agents without a shell**: For agents that don't execute shell commands directly and reason about paths via the LLM, the template must define `SKILL_HOME` and `SKILL_WORKDIR` as conceptual variables so the agent can resolve them semantically (the LLM substitutes the right path) without literally running `readlink`.
- **`readlink -f` portability**: macOS BSD `readlink` historically lacked `-f`; the template must either provide a portable computation idiom or note the platform requirement so authors don't ship Skills that fail on a fresh macOS shell.
- **Skill invoked from a directory the user cannot read**: If `${SKILL_WORKDIR}` resolution via `pwd` fails (e.g., the directory was deleted mid-session), the documented fallback `bash -c 'pwd || echo ${PWD}'` must yield a usable value rather than an empty string.
- **Nested invocations**: If one Skill calls another Skill's script, each invocation should have its own `${SKILL_HOME}` (the called Skill's real directory), while `${SKILL_WORKDIR}` stays anchored to the user's working directory across the chain.
- **Variable expansion in non-bash contexts**: The template must specify that `${SKILL_HOME}` / `${SKILL_WORKDIR}` syntax is the canonical written form regardless of execution environment, while the *computation* idioms are shell-specific examples.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `/speckit.skills` orchestration template (`templates/commands/skills.md`) MUST define `SKILL_HOME` as a named, first-class concept with a single canonical meaning: the real on-disk directory containing the Skill's `SKILL.md`, after symlink resolution.
- **FR-002**: The same template MUST define `SKILL_WORKDIR` as a named, first-class concept with a single canonical meaning: the working directory in which a Skill script (or other Skill-invoked process) is currently executing — typically the user's project root.
- **FR-003**: The template MUST provide an explicit shell-form computation idiom for each variable suitable for two contexts: (a) reasoning *about* the Skill from its `SKILL.md` (`SKILL_HOME = dirname $(readlink -f SKILL.md)`, or a portable equivalent) and (b) self-computation from inside a script (resolving `${SKILL_HOME}` from the script's own location, and `${SKILL_WORKDIR}` from `pwd`). Authors rely on these named recipes rather than reinventing them. The script-side recipe is normative for FR-016.
- **FR-004**: The template MUST instruct Skill authors to use `${SKILL_HOME}` for every reference to a Skill-owned resource (`scripts/`, `references/`, `assets/`, sub-directory files) instead of bare relative paths or hard-coded install paths.
- **FR-005**: The template MUST instruct Skill authors to use `${SKILL_WORKDIR}` for every reference to a runtime/user-facing path (input files in the user's project, output files written for the user) instead of assuming `pwd` semantics implicitly.
- **FR-006**: The template MUST explicitly contrast the two variables — Skill-owned vs. runtime — with at least one paired example showing both in the same script (e.g., reading a Skill template from `${SKILL_HOME}` and writing rendered output to `${SKILL_WORKDIR}`).
- **FR-007**: The template MUST treat `SKILL_HOME` and `SKILL_WORKDIR` as agent-engine-agnostic concepts: the computation idioms are shell-form examples, but the named variables themselves are written the same way regardless of which agent executes the Skill.
- **FR-008**: The template MUST declare `SKILL_HOME` as the single canonical name for "the Skill's directory" and supersede the existing `SKILL_ROOT` notation used in `skills/create-skills/SKILL.md`. Existing `SKILL_ROOT` references in Skill-authoring guidance MUST be renamed to `SKILL_HOME` so authors are never presented with two overlapping concepts.
- **FR-009**: The Skill-authoring guidance in `skills/create-skills/SKILL.md` MUST be updated to reflect the new convention so newly created Skills adopt `${SKILL_HOME}` / `${SKILL_WORKDIR}` from day one.
- **FR-010**: The Skill-improvement guidance in `skills/improve-skills/SKILL.md` MUST recognize legacy path idioms (bare `./scripts/...`, `${SKILL_ROOT}/...`, agent-specific install paths) as candidates for migration to the new variables when a Skill is being improved.
- **FR-011**: The template MUST provide a migration mapping (legacy → new) covering at minimum: bare relative paths (`./X` → `${SKILL_HOME}/X`), `SKILL_ROOT` references (`${SKILL_ROOT}/X` → `${SKILL_HOME}/X`), and agent-specific install paths embedded in prose.
- **FR-012**: The convention MUST NOT require existing Skills to migrate atomically; pre-migration Skills MUST continue to function under their existing path idioms during the migration window.
- **FR-013**: The template MUST handle agents that don't execute shell commands directly by defining `SKILL_HOME` and `SKILL_WORKDIR` as conceptual variables the agent resolves semantically, in addition to the shell-form computation idioms.
- **FR-014**: The template MUST address the symlink case explicitly: `${SKILL_HOME}` is the *real* directory after symlink resolution, so Skills installed via compatibility symlinks (e.g., `.github/skills` → `.specify/skills`) resolve to a single canonical path regardless of entrypoint.
- **FR-015**: Updates MUST keep the canonical-path / symlink model documented in `CLAUDE.md` ("Spec Kit Runtime & Symlink Model") and the existing Skill registry rows in `.specify/instructions.md` consistent with the new variables.
- **FR-016**: The template MUST require every Skill shell script to self-compute `${SKILL_HOME}` and `${SKILL_WORKDIR}` using a fallback idiom (e.g., `SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)}"` and `SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd)}"`), so scripts function on any agent regardless of whether the agent runtime exports the variables. Agent runtimes that DO export them MUST take precedence (the `${VAR:-fallback}` pattern preserves the export when present).

### Key Entities

- **SKILL_HOME**: A named variable representing a Skill's real on-disk directory. Attributes: resolved-absolute, post-symlink, agent-independent. Relationship: every Skill-owned path reference (scripts, references, assets) is expressed relative to it.
- **SKILL_WORKDIR**: A named variable representing the runtime working directory of a Skill-invoked process. Attributes: runtime-bound, user-facing, distinct from SKILL_HOME. Relationship: every user-facing path reference (inputs, outputs, project-relative paths) is expressed relative to it.
- **Skill orchestration template** (`templates/commands/skills.md`): The single document where the two variables are defined, contrasted, and prescribed for use. Relationship: parent of all SKILL.md authoring guidance.
- **Skill authoring guide** (`skills/create-skills/SKILL.md`) and **Skill improvement guide** (`skills/improve-skills/SKILL.md`): Downstream consumers of the convention; teach new Skills to adopt it and flag legacy Skills for migration.
- **Migration mapping**: A documented set of before/after path patterns translating legacy idioms (relative `./`, `SKILL_ROOT`, hard-coded install paths) into the new variables.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After the change, 100% of newly created Skills (Skills created via `create-skills` post-merge) reference Skill-owned resources via `${SKILL_HOME}` and runtime paths via `${SKILL_WORKDIR}`, with zero bare relative paths or hard-coded install paths in their SKILL.md.
- **SC-002**: A reader of the updated `templates/commands/skills.md` can correctly identify which variable to use for any given path reference (Skill-owned vs. runtime) on the first read, without consulting external docs — measured by the template containing at least one paired example and an explicit "use SKILL_HOME for X, SKILL_WORKDIR for Y" rule.
- **SC-003**: The same Skill, installed under at least two different agent layouts (e.g., `.specify/skills/<name>/` and a symlinked compatibility path), produces identical behavior on both — verified by running its scripts and confirming Skill-owned reads and user-facing writes hit the correct directories in each layout.
- **SC-004**: Existing Skills that have not yet migrated continue to execute successfully against the updated template (no regression) — verified by running each pre-existing Skill (`create-skills`, `improve-skills`, `analysis-project`, `draw-d3js`, `draw-echarts`, `draw-plantuml`) post-change and confirming behavior is unchanged from pre-change.
- **SC-005**: The migration mapping in the template covers at minimum the three legacy idioms (bare relative paths, `SKILL_ROOT`, agent-specific install paths) with explicit before/after examples, so an author migrating a legacy Skill does not need to invent the translation themselves.
- **SC-006**: After the change, `SKILL_HOME` is the only name used for "the Skill's directory" in `templates/commands/skills.md`, `skills/create-skills/SKILL.md`, and `skills/improve-skills/SKILL.md`; zero `SKILL_ROOT` references remain in those three files, and the migration mapping explicitly lists `${SKILL_ROOT}/X` → `${SKILL_HOME}/X` so legacy Skills can be updated mechanically.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Static inspection of SKILL.md files generated by `create-skills` after the change; baseline is the current set of Skills (none use `SKILL_HOME`/`SKILL_WORKDIR`). Re-measured each time a new Skill is created.
- **SC-002 Source**: Review of `templates/commands/skills.md` against the rule "contains a paired example + an explicit usage rule"; verified once at merge and re-checked whenever the template is regenerated.
- **SC-003 Source**: Manual or scripted invocation of one canary Skill under at least two install layouts; baseline is current (untested across layouts). Re-measured per release of the convention.
- **SC-004 Source**: Regression run of each existing Skill pre- and post-change, comparing produced artifacts and exit status; baseline is current behavior captured before the change lands.
- **SC-005 Source**: Static inspection of the updated template; checked once at merge.
- **SC-006 Source**: Reader-comprehension review by at least one person who did not author the change, confirming `SKILL_HOME` vs. `SKILL_ROOT` precedence is clear after a single read.

## Assumptions

- The primary edit target is `templates/commands/skills.md`; downstream propagation to `skills/create-skills/SKILL.md` and `skills/improve-skills/SKILL.md` is in scope so the convention is consistently taught and enforced.
- Existing Skills migrate opportunistically (when next improved) rather than via a flag-day rewrite; both old and new path idioms must coexist during the migration window.
- The shell-form computation idioms (`dirname $(readlink -f SKILL.md)`, `bash -c 'pwd || echo ${PWD}'`) are the *example* recipes; agents that don't run a shell directly resolve the named variables semantically but write them in the same `${SKILL_HOME}` / `${SKILL_WORKDIR}` form.
- macOS BSD `readlink` lacking `-f` is a known portability concern; the template will document either a portable idiom or the platform requirement, but choosing the exact recipe is an implementation detail for the planning phase.
- The `SKILL_HOME` vs. `SKILL_ROOT` reconciliation is settled in this spec: `SKILL_HOME` supersedes `SKILL_ROOT` as the single canonical name across `templates/commands/skills.md`, `skills/create-skills/SKILL.md`, and `skills/improve-skills/SKILL.md`. Pre-existing Skills that still reference `SKILL_ROOT` continue to function during the migration window (per FR-012) and are converted opportunistically via the migration mapping (per FR-011).
- No new scripts are required by this change — the variables are conventions documented in templates and SKILL.md files; existing scaffolding scripts (`create-new-skill.sh`, `refresh-tools.sh`) are not in scope unless planning identifies a concrete gap.

## Clarifications

### Session 2026-05-30

- Q: What `Feature ID` and `Feature Name` should the `Related Feature` section reference? → A: Feature ID 013, Feature Name "Skills Command" (per `features.md` row and `features/013.md` Key Change #15).
- Q: How should the updated template reconcile the new `SKILL_HOME` with the existing `SKILL_ROOT`? → A: `SKILL_HOME` supersedes `SKILL_ROOT` everywhere; existing `SKILL_ROOT` usages in `skills/create-skills/SKILL.md` (and any other in-scope Skill-authoring guidance) are renamed to `SKILL_HOME` so authors see one canonical name. Legacy Skills that still use `SKILL_ROOT` continue to work during the migration window (FR-012) and migrate via the mapping in FR-011.
- Q: How should a Skill script obtain `${SKILL_HOME}` / `${SKILL_WORKDIR}` at execution time? → A: Hybrid with mandatory self-computation — every Skill shell script self-computes both via `${VAR:-<fallback>}` so it works regardless of agent runtime; runtimes that export the variables take precedence automatically via the parameter-expansion default. (See new FR-016.)
