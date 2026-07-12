# Contract: Unified Environment Variable Interface

**Feature**: 024-agent-env-config | **Date**: 2026-07-12

This contract defines the skill-layer input surface and the command interface for the three-step flow (check → read → write). It is the single source of truth for variable names; `requirements.md` § Shared Strings cites these IDs.

## Unified Variables (skill-layer canonical names)

| String ID | Variable | Required | Rule |
|-----------|----------|----------|------|
| `STR-ENV-KEY` | `AGENT_API_KEY` | Yes | Non-empty after trim |
| `STR-ENV-MODEL` | `AGENT_MODEL` | Yes | Non-empty after trim |
| `STR-ENV-URL` | `AGENT_BASE_URL` | Yes | Non-empty; matches `^https?://` |
| `STR-ENV-ANTHRO-URL` | `AGENT_ANTHROPIC_BASE_URL` | Conditional | Required iff `claude` is targeted; matches `^https?://` |

Rules:
- These are the ONLY input channel (FR-002, Assumptions). No prompts, no config-file inputs.
- The same `AGENT_API_KEY` and `AGENT_MODEL` apply to every targeted tool (one-time convenient config).

## Commands

### `config_agent_env_validate [--all | <tool>...]`

- MUST return exit `0` when all required variables for the target set are present and well-formed.
- MUST return exit non-zero and print EVERY offending variable (grouped as missing vs malformed) when validation fails.
- MUST NOT write any file.
- When `claude` is in scope, MUST additionally require `AGENT_ANTHROPIC_BASE_URL`.

### `config_agent_env_apply [--all | <tool>...]`

- MUST call validation first; if validation fails, MUST exit non-zero having written nothing.
- Default target when no argument or `--all`: the six in-scope tools.
- For each target: secondary-assign unified values to native fields, create missing directories, merge-write the tool's config file, and record a per-tool result.
- MUST print a per-tool summary line: `configured | skipped | failed (<reason>)`.
- MUST return non-zero if any targeted tool ends `failed`; `skipped` alone does not fail the run.

### Behavioral rules (normative)

- **MUST NOT** print the value of `AGENT_API_KEY` (or any resolved key) in stdout, stderr, or files' log output (FR-014).
- **MUST** be idempotent: re-running with identical inputs yields identical managed fields (FR-013).
- **MUST** preserve unrelated pre-existing keys in JSON/dotenv config files (FR-008).
- **MUST** reject an unknown tool name with a message listing the six supported tools (FR-015).
- On an unparseable existing config file, the affected tool ends `failed`; other tools are unaffected.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All targeted tools configured (or validly skipped) |
| 1 | Validation failed (no writes performed) |
| 2 | One or more targeted tools failed during write |
| 3 | Unknown/unsupported tool requested |

## Output Examples (secret-free)

Validation failure:
```
[error] Missing required variables: AGENT_API_KEY, AGENT_MODEL
[error] Malformed variables: AGENT_BASE_URL (missing http(s):// scheme)
[error] No configuration written.
```

Successful apply:
```
[ok] claude   configured  (~/.claude/settings.json)
[ok] codex    configured  (~/.codex/config.toml, ~/.codex/auth.json)
[ok] qwen     configured  (~/.qwen/.env)
[ok] qoder    configured  (~/.qoder/config.json)
[ok] iflow    configured  (~/.iflow/settings.json)
[ok] opencode configured  (~/.config/opencode/config.json)
```
