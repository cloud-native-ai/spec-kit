# Contract: Per-Tool Config Targets & Secondary Assignment

**Feature**: 024-agent-env-config | **Date**: 2026-07-12

Defines, for each in-scope tool, the config file target, format, and the exact **secondary assignment** from unified variables to tool-native fields. `{key}` = `AGENT_API_KEY`, `{model}` = `AGENT_MODEL`, `{url}` = `AGENT_BASE_URL`, `{anthro_url}` = `AGENT_ANTHROPIC_BASE_URL`.

## claude — `~/.claude/settings.json` (JSON, merge into `env`)

MUST merge these keys into the top-level `env` object and remove any conflicting `ANTHROPIC_API_KEY`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "{anthro_url}",
    "ANTHROPIC_AUTH_TOKEN": "{key}",
    "ANTHROPIC_MODEL": "{model}",
    "ANTHROPIC_SMALL_FAST_MODEL": "{model}"
  }
}
```
- Other existing keys under `env` and elsewhere MUST be preserved.

## codex — `~/.codex/config.toml` (TOML) + `~/.codex/auth.json` (JSON)

`config.toml` managed block:
```toml
model = "{model}"
model_provider = "agent"

[model_providers.agent]
name = "agent"
base_url = "{url}"
env_key = "CODEX_API_KEY"
wire_api = "responses"
```
`auth.json` (persists the key so codex resolves `CODEX_API_KEY` without a manual export):
```json
{ "OPENAI_API_KEY": "{key}" }
```
- The API key MUST be written to `auth.json` (mode `600`), not embedded in `config.toml`.

## qwen — `~/.qwen/.env` (dotenv)

```dotenv
OPENAI_API_KEY={key}
OPENAI_BASE_URL={url}
OPENAI_MODEL={model}
```
- MUST persist to a file (prior behavior only exported shell vars — corrected here per FR-007).
- Existing unrelated lines in `.env` MUST be preserved; only these three keys are upserted.

## qoder — `~/.qoder/config.json` (JSON, merge)

```json
{
  "provider": "openai",
  "model": "{model}",
  "apiKey": "{key}",
  "baseURL": "{url}"
}
```
- Unrelated keys (e.g., `general.enableAutoUpdate`) MUST be preserved.

## iflow — `~/.iflow/settings.json` (JSON, merge)

```json
{
  "selectedAuthType": "openai-compatible",
  "apiKey": "{key}",
  "baseUrl": "{url}",
  "modelName": "{model}"
}
```

## opencode — `~/.config/opencode/config.json` (JSON, merge)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "agent": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "agent",
      "options": { "baseURL": "{url}", "apiKey": "{key}" },
      "models": { "{model}": { "name": "{model}", "attachment": true } }
    }
  }
}
```
- The `provider.agent` block is regenerated; other providers/keys MUST be preserved.

## File Permissions

Any file containing the API key (`auth.json`, `.qwen/.env`, and JSON files holding `apiKey`) SHOULD be written with `600` permissions where the platform supports it.

## Protocol Mapping Summary

| Tool | protocol | URL source | key destination |
|------|----------|-----------|-----------------|
| claude | anthropic | `{anthro_url}` | `env.ANTHROPIC_AUTH_TOKEN` |
| codex | openai | `{url}` | `auth.json` OPENAI_API_KEY |
| qwen | openai | `{url}` | `.env` OPENAI_API_KEY |
| qoder | openai | `{url}` | `apiKey` |
| iflow | openai | `{url}` | `apiKey` |
| opencode | openai | `{url}` | `options.apiKey` |
