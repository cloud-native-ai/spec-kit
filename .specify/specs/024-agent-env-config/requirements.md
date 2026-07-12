# Requirements Specification: Unified Env-Var Agent Configuration

**Requirement Branch**: `024-agent-env-config`  
**Created**: 2026-07-12  
**Status**: Draft  
**Input**: User description: "在 skills/agent-setup 技能支持所有当前框架包含的AI工具。该技能的核心是方便地进行各种工具的一次性配置，因此需要深入了解每个工具的具体配置方法，只关心最核心的配置：API key、URL、模型。所有配置的输入都使用环境变量。在技能层使用统一的环境变量名，再根据不同的工具进行环境变量的二次赋值。最终配置要落到各个工具自身的配置文件中进行持久化。整体流程：1) 检查当前环境中的环境变量是否完整正确；2) 读取环境变量的值；3) 根据各个工具的配置文件位置和格式，将值写入对应的配置文件中。"

## Related Feature *(mandatory)*

**Feature ID**: 022  
**Feature Name**: AI Tools Support

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One-shot configuration of all supported tools from unified inputs (Priority: P1)

A developer has a single set of core credentials (an API key, a service base URL, and a model name) exported as environment variables. They run the agent-setup skill once, and every supported AI tool ends up with its own native configuration file populated with the correct key, URL, and model — without the developer hand-editing any per-tool config file or remembering each tool's variable names or file format.

**Why this priority**: This is the core value of the skill — "convenient one-time configuration." Without it the feature delivers nothing; every other capability is a refinement of this flow.

**Independent Test**: With valid unified environment variables set, invoke the skill's "configure all" action and confirm that each supported tool now has a persisted config file containing the intended key, URL, and model in that tool's expected location and format. Delivers a ready-to-run set of tools from a single action.

**Acceptance Scenarios**:

1. **Given** all required unified environment variables are set with valid values, **When** the user runs the configure-all action, **Then** each supported tool's own configuration file is created/updated with the mapped key, URL, and model, and a per-tool success summary is reported.
2. **Given** a supported tool already has an existing config file with unrelated settings, **When** the user runs configuration, **Then** the core config fields (key, URL, model) are updated while unrelated existing settings are preserved.
3. **Given** the target config directory for a tool does not yet exist, **When** the user runs configuration, **Then** the directory is created and the config file is written successfully.

---

### User Story 2 - Pre-flight validation of environment variables (Priority: P2)

Before any file is written, the skill verifies that the unified environment variables are present, non-empty, and well-formed. If anything is missing or malformed, the skill stops and tells the user exactly which variables are wrong and why — without leaving any tool half-configured.

**Why this priority**: Prevents silent, partial, or corrupt configurations. It protects the P1 flow by guaranteeing that writes only happen from a known-good input set, which is essential for trust in a "one-shot" tool.

**Independent Test**: Unset or corrupt one required variable, run the skill, and confirm it reports the offending variable(s) with an actionable message and writes zero config files.

**Acceptance Scenarios**:

1. **Given** a required unified variable is unset or empty, **When** the user runs configuration, **Then** the skill reports the specific missing variable(s) and writes no tool config files.
2. **Given** a required variable holds an obviously malformed value (e.g., a base URL with no scheme), **When** the user runs configuration, **Then** the skill reports which value failed the format check and writes no tool config files.
3. **Given** all variables are valid, **When** validation runs, **Then** validation passes and the skill proceeds to read values and write configs.

---

### User Story 3 - Configure a single named tool (Priority: P3)

A developer only wants one tool configured (or wants to re-apply configuration to just one tool) rather than all of them. They invoke the skill targeting a single tool name and only that tool's config file is written.

**Why this priority**: Convenience and precision for iterative use, but not required for the primary "configure everything once" value. It builds directly on the P1 mapping-and-persist mechanism.

**Independent Test**: Run the skill targeting one supported tool and confirm only that tool's config file changes.

**Acceptance Scenarios**:

1. **Given** valid unified variables, **When** the user targets a single supported tool, **Then** only that tool's config file is written and other tools are left untouched.
2. **Given** the user names an unsupported/unknown tool, **When** the skill runs, **Then** it reports the tool is not supported and lists the supported tools.

---

### Edge Cases

- What happens when a required unified variable is set but empty (whitespace-only)? → Treated as missing; validation fails.
- What happens when the base URL is malformed or uses an unexpected scheme? → Format check fails with a specific message; no writes.
- How does the system handle a tool whose native protocol needs a different endpoint shape than another tool (e.g., Anthropic-compatible vs OpenAI-compatible) from the same unified inputs? → The skill maps the unified URL to the correct per-tool endpoint form during secondary assignment.
- What happens when a tool's config file exists but is not valid/parseable? → The skill reports the file for that tool as failed and continues with the remaining tools; other tools are unaffected.
- What happens when writing one tool's config fails midway (e.g., permissions)? → That tool is reported as failed with a reason; already-written tools remain valid; the run reports a mixed result summary.
- What happens when a targeted tool's CLI is not installed? → Configuration of its config file still succeeds (config is independent of install); the report may note the tool is not yet installed.
- How are secret values handled in output? → API key values are never printed in logs or summaries.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST configure exactly the six framework AI tools whose core configuration consists of an API key, a base URL, and a model: `claude`, `codex`, `qwen`, `qoder`, `iflow`, and `opencode`. GitHub Copilot (IDE/subscription/OAuth) and Hermes Agent (OAuth portal) do NOT use an API-key/URL/model input model and are explicitly out of scope for this feature.
- **FR-002**: The skill MUST define a single, documented set of unified skill-layer environment variable names representing the three core config inputs: API key, base URL, and model.
- **FR-003**: The skill MUST verify, before writing any configuration, that the required unified environment variables are complete (present and non-empty) and correct (basic format sanity: base URL has a valid scheme, key is non-empty, model is non-empty).
- **FR-004**: When validation fails, the skill MUST report every offending variable (missing, empty, or malformed) with an actionable message and MUST NOT write any tool configuration file (fail fast, no partial writes).
- **FR-005**: The skill MUST read the core config values from the unified environment variables.
- **FR-006**: The skill MUST map (secondary assignment) the unified values onto each target tool's native, tool-specific variable names and value shapes.
- **FR-007**: The skill MUST persist the mapped values into each target tool's own configuration file, at that tool's canonical file location and in that tool's native file format.
- **FR-008**: The skill MUST preserve unrelated existing settings already present in a tool's configuration file when updating the core config fields.
- **FR-009**: The skill MUST support configuring all supported tools in one invocation, and MUST also support targeting a single named tool.
- **FR-010**: The skill MUST produce a per-tool result summary indicating, for each tool, whether it was configured, skipped, or failed (with a reason).
- **FR-011**: The skill MUST correctly account for per-tool protocol/endpoint differences (e.g., Anthropic-compatible vs OpenAI-compatible endpoints) when mapping the unified base URL to each tool.
- **FR-012**: The skill MUST create any missing configuration directories required to persist a tool's config file.
- **FR-013**: The skill MUST be idempotent: re-running configuration with unchanged unified inputs MUST yield the same persisted configuration with no unintended changes.
- **FR-014**: The skill MUST NOT print secret values (e.g., the API key) in any log line, summary, or error message.
- **FR-015**: When a user targets an unknown/unsupported tool, the skill MUST reject the request and list the supported tools.

### Key Entities *(include if requirement involves data)*

- **Unified Core-Config Input Set**: The skill-layer canonical representation of the three core inputs — API key, base URL, model — sourced exclusively from environment variables.
- **Tool Profile**: Describes one supported tool: its identity/name, its native variable names, the value shape it expects (including protocol/endpoint form), its config file location, and its config file format.
- **Per-Tool Config File**: The persisted artifact written for each tool at its canonical location in its native format.
- **Validation Result**: The outcome of the pre-flight check — pass, or a list of offending variables with reasons.
- **Configuration Report**: The per-tool summary of configured/skipped/failed outcomes returned to the user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user with valid unified inputs can configure all supported tools in a single action and in under 1 minute, without manually editing any per-tool config file.
- **SC-002**: 100% of supported tools targeted in a successful run have a persisted config file whose core fields (key, URL, model) match the intended unified inputs.
- **SC-003**: When any required unified variable is missing or malformed, 0 tool config files are written and the user receives a message that identifies every offending variable.
- **SC-004**: Re-running configuration with unchanged inputs produces byte-identical core config fields with 0 unintended diffs (idempotency).
- **SC-005**: Across all runs, secret values appear 0 times in command output, logs, and summaries.
- **SC-006**: When updating an existing tool config that contains unrelated settings, 100% of those unrelated settings remain intact after the run.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Timed execution of the configure-all action in a test environment; inspection of resulting per-tool config files.
- **SC-002 Source**: Automated comparison of each written config file's core fields against the unified input values.
- **SC-003 Source**: Negative-path tests that unset/corrupt each required variable and assert zero files written plus message content.
- **SC-004 Source**: Diff of config files across two consecutive runs with identical inputs.
- **SC-005 Source**: Scan of captured command output/logs for the secret value string.
- **SC-006 Source**: Pre/post comparison of a seeded config file containing unrelated settings.

## Assumptions

- The three core config inputs are: an API key, a service base URL, and a model identifier. Any additional per-tool fields (e.g., protocol markers, provider labels) are derived by the skill and are not additional user inputs.
- A single unified input set is applied across all targeted tools in a run (the "one-time convenient configuration" value); protocol- or endpoint-specific variants are derived by the skill rather than supplied separately by the user. If the underlying service exposes protocol-specific endpoints, the skill maps the unified base URL to the correct per-tool endpoint form.
- "Correct" in step 1 means completeness (present, non-empty) plus basic format sanity (URL scheme present, key/model non-empty). Validating the model name against a live catalog of supported models is out of scope for this feature unless clarified otherwise.
- Configuration writes are independent of whether a tool's CLI is installed; installing tool binaries is out of scope for this feature.
- Environment variables are the only supported input channel for core config; no interactive prompts or config-file inputs are introduced by this feature.

## Shared Strings *(optional)*

Unified skill-layer environment variable names (fixed during planning; single source of truth — see `contracts/unified-env-contract.md`).

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-ENV-KEY` | "AGENT_API_KEY" | FR-002, FR-003, FR-005; contracts/unified-env-contract.md; all 6 tools |
| `STR-ENV-MODEL` | "AGENT_MODEL" | FR-002, FR-003, FR-005; contracts/unified-env-contract.md; all 6 tools |
| `STR-ENV-URL` | "AGENT_BASE_URL" | FR-002, FR-003, FR-006, FR-011; contracts/*; codex/qwen/qoder/iflow/opencode |
| `STR-ENV-ANTHRO-URL` | "AGENT_ANTHROPIC_BASE_URL" | FR-011; contracts/*; claude (conditionally required) |

## Clarifications

### Session 2026-07-12

- Q: Which Feature should this spec bind to? → A: Feature 022 "AI Tools Support" (bind to existing feature; broadens its scope to include runtime credential configuration of AI tools).
- Q: The framework lists 8 tools, but Copilot and Hermes don't use API key/URL/model — which tools must this skill configure? → A: The six API-key CLIs only (`claude`, `codex`, `qwen`, `qoder`, `iflow`, `opencode`); GitHub Copilot and Hermes Agent are out of scope.
