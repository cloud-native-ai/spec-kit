# Security Policy

## Reporting a vulnerability

Report privately. Do **not** open a public issue, pull request or chat message
that describes an unpatched vulnerability.

| Channel | Address | Status |
|---------|---------|--------|
| Confidential issue (internal GitLab) | `https://gitlab.alibaba-inc.com/cloud-native-ai/spec-kit/-/issues` — create the issue with confidentiality enabled | `<pending>` confirm reachability |
| Security email | `<pending>` | not yet published |

> **Contact placeholders**: entries marked `<pending>` are for the project
> owner to fill in. Until a private channel is published, contact a maintainer
> directly through the repository's member list.

Include: affected version (`specify --version`), the component and file path,
a reproduction path, the impact you observed, and any suggested mitigation.
Encrypt or redact secrets and client-project data in your report.

## Supported versions

Fixes land on `master` and ride the next published release; there are no backport branches.

| Version line | Receives security fixes |
|--------------|------------------------|
| Current `master` tip | yes |
| Latest published release of `specify-cli` | yes, by upgrading to the next release |
| Older releases and pinned snapshots | no — upgrade |

The version number is owned by `pyproject.toml`; this page does not restate it.

## Response expectations

The process is: acknowledge → triage and reproduce → fix or mitigate →
release → disclose with credit to the reporter.

Response-time targets are `<pending owner confirmation>`; no numeric service level is
committed until the owner sets one. An unreproducible report is returned with what was
tried, never closed silently.

## Scope

In scope: the `specify` CLI, `install.sh`, and the framework payloads shipped
to client projects (`templates/`, `shared/`, `scripts/`, `skills/`, `agents/`,
`memory/`) — including a script or skill that can be driven into unsafe
behaviour by repository content or by a prompt injection.

Out of scope: vulnerabilities in the third-party AI agent CLIs and in the
Python/Node packages listed in [NOTICE](NOTICE) (report those upstream), the
content of a client project, and upstream github/spec-kit.

## Safe harbour

Good-faith research on your own installation is welcome: no legal action is
intended for reports that avoid privacy violations, data destruction and
service disruption. Please do not test against a project you do not own.

Background reading on the project's security thinking:
[docs/concepts/security.md](docs/concepts/security.md).
