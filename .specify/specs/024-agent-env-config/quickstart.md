# Quickstart: Unified Env-Var Agent Configuration

**Feature**: 024-agent-env-config | **Date**: 2026-07-12

Configure all supported AI-tool CLIs from one set of environment variables.

## 1. Export the unified variables

```bash
export AGENT_API_KEY="sk-..."                       # your provider API key
export AGENT_MODEL="glm-5.2"                          # model id
export AGENT_BASE_URL="https://<host>/compatible-mode/v1"   # OpenAI-compatible endpoint
# Only needed if you also configure claude (Anthropic protocol):
export AGENT_ANTHROPIC_BASE_URL="https://<host>/apps/anthropic"
```

## 2. Validate (no files written)

```bash
source .specify/skills/agent-setup/scripts/config-agent.sh
config_agent_env_validate --all
```
If anything is missing or malformed, every offending variable is listed and nothing is written.

## 3. Apply — write each tool's own config file

```bash
# Configure all six tools:
config_agent_env_apply --all

# Or a single tool:
config_agent_env_apply qwen
```

Result (secret-free summary):
```
[ok] claude   configured  (~/.claude/settings.json)
[ok] codex    configured  (~/.codex/config.toml, ~/.codex/auth.json)
[ok] qwen     configured  (~/.qwen/.env)
[ok] qoder    configured  (~/.qoder/config.json)
[ok] iflow    configured  (~/.iflow/settings.json)
[ok] opencode configured  (~/.config/opencode/config.json)
```

## Notes

- **Scope**: `claude`, `codex`, `qwen`, `qoder`, `iflow`, `opencode`. GitHub Copilot and Hermes Agent use subscription/OAuth and are out of scope.
- **Idempotent**: re-running with the same variables produces identical config — safe to repeat.
- **Non-destructive**: unrelated settings already in a tool's config file are preserved.
- **Secrets**: the API key is never printed to the terminal.
- If `AGENT_ANTHROPIC_BASE_URL` is unset when running `--all`, `claude` is reported as `skipped` (reason noted); the other five still configure.
