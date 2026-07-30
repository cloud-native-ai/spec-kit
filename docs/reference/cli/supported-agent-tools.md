# Supported Agent Tools

Spec Kit's `specify` CLI can bootstrap its `/speckit.*` command surface into a
number of AI coding agents. The authoritative list lives in `AGENT_CONFIG` and
`_ASSISTANT_TIERS` in [src/specify_cli/__init__.py](../../../src/specify_cli/__init__.py).

This directory collects a concise reference for each officially supported agent,
distilled from the tool's **official documentation** (source URL noted at the top
of each file). Docs were captured on 2026-07-11 — always confirm against the
upstream source for the latest details.

> **Terminology**: "tools" in this document means **AI agent CLIs** (Claude Code,
> Codex CLI, …). It does *not* mean the **Tool definition records** owned by
> `/speckit.tools` — those are pre-verified capability records under
> `.specify/memory/tools/`, defined in
> [tool-definitions.md](../../../shared/definitions/tool-definitions.md). A third
> sense, an agent's `tools:` frontmatter key, is its **tool-call list**.

## Support matrix

| Key | Name | Tier | Agent folder | CLI required | Official source |
|-----|------|------|--------------|--------------|-----------------|
| `claude`   | Claude Code    | Tier 1 | `.claude/`   | yes | https://docs.claude.com/en/docs/claude-code |
| `codex`    | Codex CLI      | Tier 1 | `.codex/`    | yes | https://github.com/openai/codex |
| `qoder`    | Qoder CLI      | Tier 1 | `.qoder/`    | yes | https://docs.qoder.com/en/cli |
| `copilot`  | GitHub Copilot | Tier 1 | `.github/`   | no (IDE-based) | https://docs.github.com/en/copilot |
| `opencode` | opencode       | Tier 1 | `.opencode/` | yes | https://opencode.ai/docs |
| `qwen`     | Qwen Code      | Tier 2 | `.qwen/`     | yes | https://github.com/QwenLM/qwen-code |
| `hermes`   | Hermes Agent   | Tier 2 | `.hermes/`   | yes | https://hermes-agent.nousresearch.com/docs |
| `iflow`    | iFlow CLI      | Tier 2 | `.iflow/`    | yes | https://platform.iflow.cn/en/cli |

- **Tier 1** — first-class targets validated by the contract/integration test suite.
- **Tier 2** — supported targets with a narrower validation surface.

Only these officially supported agents may be added (Constitution Principle V);
config parsing rejects unknown providers.

## Per-tool references

- [Claude Code](./claude-code.md)
- [Codex CLI](./codex-cli.md)
- [Qoder CLI](./qoder-cli.md)
- [GitHub Copilot](./github-copilot.md)
- [opencode](./opencode.md)
- [Qwen Code](./qwen-code.md)
- [Hermes Agent](./hermes-agent.md)
- [iFlow CLI](./iflow-cli.md)

## Selecting an agent

Pass the key via `--ai` at init time:

```bash
python -m specify_cli init <PROJECT_NAME> --ai <claude|codex|qoder|copilot|opencode|qwen|hermes|iflow>
```

Each agent receives its own native command directory (e.g. `.claude/commands`,
`.github/prompts`, `.qwen/commands`) and file format, rendered from the single
set of templates in `templates/commands/*.md`.
