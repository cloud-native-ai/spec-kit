# Support

This project is an **independent fork** of GitHub Spec Kit. The upstream
repository's support channels do not apply here — use the channels below.

> **Contact placeholders**: entries marked `<pending>` are for the project
> owner to fill in. Until they are filled, use the repository issue tracker.

## Channels

| Channel | Address | Status |
|---------|---------|--------|
| Issue tracker (internal GitLab) | `https://gitlab.alibaba-inc.com/cloud-native-ai/spec-kit/-/issues` (derived from the `gitlab` remote) | `<pending>` confirm reachability |
| Issue tracker (GitHub mirror) | `https://github.com/cloud-native-ai/spec-kit/issues` (derived from the `github` remote) | `<pending>` confirm reachability |
| Maintainer email | `<pending>` | not yet published |
| Internal chat group | `<pending>` | not yet published |
| Documentation site | `<pending>` — until a site is published, read `docs/` in this repository | not yet published |

Security vulnerabilities: do **not** open a public issue — follow
[SECURITY.md](SECURITY.md).

## Before you ask

| Symptom | Read first |
|---------|-----------|
| Installation or CLI setup fails | [docs/tutorials/installation.md](docs/tutorials/installation.md) |
| First run / workflow questions | [docs/tutorials/quickstart.md](docs/tutorials/quickstart.md) |
| A skill or command misbehaves | [docs/reference/skills/problems.md](docs/reference/skills/problems.md) |
| An AI agent CLI is not detected or renders wrongly | [docs/reference/cli/supported-agent-tools.md](docs/reference/cli/supported-agent-tools.md) |
| Contributing a change | [CONTRIBUTING.md](CONTRIBUTING.md) |

## What to include in a report

1. Framework version: `specify --version` (the version field lives in
   `pyproject.toml`).
2. Agent CLI and its version, plus the operating system.
3. The exact command or `/speckit.*` invocation, and the working directory.
4. Expected behaviour, actual behaviour, and the relevant log output.
5. Whether the project was created by `specify init` or upgraded in place.

Reports without a reproduction path are triaged last.

## Scope

Supported: the `specify` CLI, the framework payloads it installs
(`templates/`, `shared/`, `scripts/`, `skills/`, `agents/`, `memory/`), and
`install.sh`.

Not supported here: the third-party AI agent CLIs themselves (report those to
their own vendors), content inside a client project, and upstream
github/spec-kit.
