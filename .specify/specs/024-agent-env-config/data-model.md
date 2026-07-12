# Data Model: Unified Env-Var Agent Configuration

**Feature**: 024-agent-env-config | **Date**: 2026-07-12

This feature has no persistent database; its "data" is (a) the unified input variables read from the environment, (b) a static per-tool profile registry, and (c) transient validation/report structures. Entities below map directly to the Key Entities in [requirements.md](./requirements.md).

## Entity: UnifiedConfigInput

The skill-layer canonical inputs, read exclusively from environment variables.

| Field | Env Variable | Required | Format / Rule | Consumed by |
|-------|--------------|----------|---------------|-------------|
| api_key | `AGENT_API_KEY` | Yes | Non-empty (after trim) | all 6 tools |
| model | `AGENT_MODEL` | Yes | Non-empty (after trim) | all 6 tools |
| base_url | `AGENT_BASE_URL` | Yes | Non-empty; must start with `http://` or `https://` | codex, qwen, qoder, iflow, opencode (OpenAI-compatible) |
| anthropic_base_url | `AGENT_ANTHROPIC_BASE_URL` | Conditional | Required only when `claude` is a target; same URL scheme rule | claude (Anthropic-compatible) |

**Validation rules (FR-003, FR-004)**:
- A variable that is unset, empty, or whitespace-only is treated as **missing**.
- A URL variable that is present but lacks an `http(s)://` scheme is **malformed**.
- Validation collects **all** offenders before returning; it never stops at the first.
- If validation fails, zero config files are written (no-partial-writes).

## Entity: ToolProfile (static registry)

Describes how one supported tool consumes the unified inputs. This registry is fixed to the six in-scope tools; any other tool name is rejected (FR-015).

| Field | Meaning |
|-------|---------|
| name | Tool key: `claude`, `codex`, `qwen`, `qoder`, `iflow`, `opencode` |
| protocol | `anthropic` (claude) or `openai` (the other five) |
| url_source | Which unified URL feeds this tool: `anthropic_base_url` for claude, else `base_url` |
| config_path | Absolute path (under `$HOME`) of the tool's own config file |
| format | `json` \| `toml` \| `dotenv` |
| native_fields | The tool-native variable names produced by secondary assignment (see `contracts/tool-config-targets.md`) |
| merge_policy | `merge` (preserve unrelated keys) for JSON/dotenv; `regenerate` for the managed block |

Registry (protocol / primary config file):

| name | protocol | config file |
|------|----------|-------------|
| claude | anthropic | `~/.claude/settings.json` |
| codex | openai | `~/.codex/config.toml` (+ `~/.codex/auth.json` for the key) |
| qwen | openai | `~/.qwen/.env` |
| qoder | openai | `~/.qoder/config.json` |
| iflow | openai | `~/.iflow/settings.json` |
| opencode | openai | `~/.config/opencode/config.json` |

## Entity: ValidationResult (transient)

| Field | Meaning |
|-------|---------|
| ok | Boolean — true only if no offenders |
| missing[] | Variable names that are unset/empty |
| malformed[] | Variable names present but failing format |

State: `ok=true` → proceed to read+apply; `ok=false` → emit offenders, exit non-zero, write nothing.

## Entity: ToolResult / ConfigurationReport (transient)

Per-tool outcome aggregated into a run report (FR-010).

| Field | Values |
|-------|--------|
| tool | tool name |
| status | `configured` \| `skipped` \| `failed` |
| reason | present when `skipped`/`failed` (e.g., "AGENT_ANTHROPIC_BASE_URL not set", "permission denied", "existing config not parseable") |

**Report rules**:
- Secret values MUST NOT appear in any `reason` or summary line (FR-014).
- A per-tool `failed` does not abort remaining tools; the run reports a mixed summary.
- Overall exit code is non-zero if any targeted tool ends `failed`.

## Lifecycle (per invocation)

```
validate(targets) ──ok? no──▶ report offenders, exit≠0 (no writes)
        │ yes
        ▼
read()  → capture api_key, model, base_url[, anthropic_base_url]
        ▼
for each target tool:
        secondary-assign → ensure dir → merge-write config file
        record ToolResult
        ▼
emit ConfigurationReport (secret-free), exit 0 unless any failed
```
