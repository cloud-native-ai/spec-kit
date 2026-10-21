# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows)
- AI coding agent (Tier 1): [Claude Code](https://www.anthropic.com/claude-code), [Codex CLI](https://github.com/openai/codex), [Qoder CLI](https://qoder.com/cli), or [opencode](https://opencode.ai/); (Tier 2): Hermes Agent, [GitHub Copilot](https://code.visualstudio.com/)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init .
# or use the --here flag
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```

### Specify AI Agent

You can proactively specify your AI agent during initialization:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai claude
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai codex
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai qoder
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai opencode
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai hermes
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai copilot
```

### Specify Script Type (Shell)

All automation scripts now have Bash (`.sh`) variants.

Auto behavior:

- All OS default: `sh`

Force a specific script type:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --script sh
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai copilot --ignore-agent-tools
```

## Cold-Start Bootstrap: install.sh (intranet-first)

`uvx --from git+https://github.com/...` above assumes public GitHub and a public PyPI are reachable. In intranet environments (internal GitLab, internal PyPI mirror) that path is unavailable — the repo-root `install.sh` is the single owner of cold-start install logic:

```bash
# Intranet cold start (bash + python3/pip + git assumed present, never auto-installed):
git clone --depth 1 https://gitlab.alibaba-inc.com/cloud-native-ai/spec-kit.git /tmp/spec-kit
bash /tmp/spec-kit/install.sh

# Already inside a spec-kit checkout (self-hosting / dev):
./install.sh --local

# Constrained machine: internal GitLab only, zero public network contact:
./install.sh --intranet-only

# Preview the full plan (python resolution, index pairing, per-source preflight):
./install.sh --dry-run
```

Design contract:

- **Python ladder**: `--python` / `SPECIFY_PYTHON` → `$PWD/.venv/bin/python` → PATH `python3` (`python`) → newest system `python3*`. All levels missing → hard exit (Python is never auto-installed).
- **Upgrade semantics**: install is a clean reinstall, and the ladder's upgrade-in-place level — between the cwd `.venv` level and PATH — prefers the python of an existing `specify` on PATH, so re-running `install.sh` from any directory upgrades the existing installation instead of installing a duplicate into an unrelated environment. Caller-controlled destination still wins: pin `--python` or run from the project venv's directory (the fleet upgrade workflow).
- **Source × index pairing**: the pip index actually configured (explicit flag > `PIP_INDEX_URL` > pip config > pypi.org) is probed once up front, because dependency resolution always needs the index even when the git source hosts the specify-cli tree itself; an unreachable index fails fast (exit 3). The install command pins `--index-url` (and `--trusted-host` for plain-HTTP mirrors) explicitly.
- **Intranet-first fallback**: internal GitLab → gitee → github; `--intranet-only` drops the public mirrors entirely. Probing is lazy and short-circuited — it stops at the first reachable source (a working GitLab costs exactly one probe), and later mirrors are probed only if the chosen source fails to install. Reachability probes are bounded (never hang on a black-holed host); `--no-probe` skips probing.
- **uv is an opt-in accelerator, never a bootstrap dependency**: `--uv` / `SPECIFY_INSTALLER=uv` requires an existing uv on PATH (exit 2 otherwise, uv is never installed here) and injects the resolved index (`UV_DEFAULT_INDEX` / `UV_INDEX_URL`, plus `UV_INSECURE_HOST` for plain-HTTP mirrors).
- **Post-install verification**: `specify check` runs before the script reports success; failure is exit 5, not a silent pass.
- Exit codes: `0` ok · `2` missing prerequisite (python/pip/git/uv) · `3` no viable source × index · `5` verification failed.

Wrapper note: downstream wrappers (e.g. cws-lib-bash `specify_install`) must only **locate or fetch this script and delegate** — resolution ladders, source lists, and index handling live here, single-sourced.

## Source Stamp (来源标识)

Every `specify init` writes `.specify/source.json` into the target project — the record of **which framework source commit** produced this scaffolding. The commit id is the **sole version identifier** (formal version numbers are deliberately not used):

```json
{
  "framework": "spec-kit",
  "commit": "<40-hex git commit id>",
  "stamped_at": "20260817T115529Z"
}
```

**Reverse lookup** — answer "which code slice built my `.specify/`?" with one command in the spec-kit repo:

```bash
cat .specify/source.json           # read the commit id
git -C <spec-kit-repo> show <commit> --stat
```

Three states, never a fourth:

| `.specify/source.json` | Meaning | Action |
|---|---|---|
| `commit` is 40-hex | Valid provenance | `git show <commit>` in the framework repo |
| `commit` is `"unavailable"` (+ `reason`) | Explicitly unresolvable | inspect `reason`; never guess |
| file missing | Source unknown (pre-043 project, or deleted) | re-run `specify init` to (re)gain it |

Notes: re-running init (upgrade path) **overwrites** the stamp with the new source commit — it always reflects the most recent init. Installed wheels carry the commit embedded at build time (`python3 -m build --wheel`); a development checkout installed editable (`pip install -e .`) probes the commit straight from git. Note: running `init` from a bare checkout without installing is not supported — templates ship only inside the built distribution. Stamping never blocks init: a failed write only warns.

## Verification

After initialization, you should see the following structure and commands:

**Directory structure**:
- `.specify/scripts/` — Automation scripts (`.sh`)
- `.specify/templates/` — Spec/plan/task templates
- `.specify/skills/` — Installed skills (symlinked to tool-specific paths)
- `.specify/agents/` — layered agent workspace: `templates/` (bundled role agents, installed by init), `instances/` (project-authored agents), `execution/` (dispatch configs/scripts; runtime `logs/` gitignored). Definition files are per-file symlinked to `.github/agents/`, `.qoder/agents/`, etc.
- `.specify/memory/` — Project memory (constitution, features)

**All 18 commands available in your AI agent**:

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Establish project governance principles |
| `/speckit.feature` | Manage feature lifecycle and registry |
| `/speckit.requirements` | Create/update the requirements specification (WHAT/WHY) |
| `/speckit.clarify` | Resolve ambiguities in specifications |
| `/speckit.interview` | Interview you in rounds until an artifact converges |
| `/speckit.research` | Conduct technical research to inform decisions |
| `/speckit.derive` | Derive an architecture by replaying verified sources' reasoning methods |
| `/speckit.plan` | Generate implementation plans from specs |
| `/speckit.tasks` | Break down plans into actionable tasks |
| `/speckit.checklist` | Generate quality gate checklists |
| `/speckit.analyze` | Cross-artifact consistency checks |
| `/speckit.implement` | Execute tasks with built-in validation |
| `/speckit.review` | Review implementation against specs and plan |
| `/speckit.agents` | Generate role-based agents or create custom agents |
| `/speckit.team` | Organize and run multi-agent teams (create / modify / run) |
| `/speckit.goal` | Author project-level goal definitions and coordinate teams sharing one |
| `/speckit.skills` | Create or refresh project skills |
| `/speckit.tools` | Define or discover reusable tools |
| `/speckit.instructions` | Generate/update AI agent instructions and symlinks |
| `/speckit.todo` | Discover TODO blocks in files and turn them into execution plans |
| `/speckit.history` | Distill past AI conversations into a theme-aggregated knowledge base |
| `/speckit.docs` | Standardize and manage the project documentation space |
| `/speckit.feedback` | Manage local feedback: probe overview, disposition, packaging |
| `/speckit.sanitize` | Detect stale framework material and clean it under the two-level criteria |
| `/speckit.session` | Export the current session to a user-named directory |

**Next step**: Run `/speckit.agents` (no arguments) in your AI agent to generate seven role-based development workflow agents tailored to your project's context.

## Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```
