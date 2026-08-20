#!/usr/bin/env python3

"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import json
import os
import re
import shlex
import shutil
import ssl
import subprocess
import sys
import traceback

# Check Python version
if sys.version_info < (3, 8):
    sys.exit("Error: Specify CLI requires Python 3.8 or higher.")

# For cross-platform keyboard input
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import httpx

# For cross-platform keyboard input
import readchar
import typer
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from typer.core import TyperGroup

try:
    import truststore

    ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
except (ImportError, AttributeError):
    ssl_context = ssl.create_default_context()

client = httpx.Client(verify=ssl_context)

# Get the directory where this module is located
MODULE_DIR = Path(__file__).parent.resolve()


# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://www.anthropic.com/claude-code",
        "requires_cli": True,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "hermes": {
        "name": "Hermes Agent",
        "folder": ".hermes/",
        "install_url": None,
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "qoder": {
        "name": "Qoder CLI",
        "folder": ".qoder/",
        "install_url": "https://qoder.com/cli",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
}

# ---------------------------------------------------------------------------
# Neutral agent metadata (Feature 044 — Agent Metadata Portability)
#
# Tool-agnostic metadata vocabulary for agent definitions. The frontmatter of
# every *.agent.md under agents/ and .specify/agents/{templates,instances}/
# MUST use only these keys (kebab-case). Per-tool field names are produced at
# render time by _AGENT_METADATA_MAPPING, never authored here.
#
# model-tier domain note (analyze U-1): `lite` is a documented tier on at
# least one supported tool and maps 1:1; `none` means "no model preference"
# and renders as field-omission via the unmapped-field policy (D3).
# ---------------------------------------------------------------------------

# key -> (value_domain, default, renders_to_tools)
# value_domain: None = any non-empty string; set = enumerated; "bool";
#               "int"; "str-list"
NEUTRAL_AGENT_METADATA_KEYS = {
    "name": (None, None, True),
    "description": (None, None, True),
    "user-invocable": ("bool", True, True),
    "disable-model-invocation": ("bool", False, True),
    "model-tier": (
        {"auto", "lite", "efficient", "performance", "ultimate", "none"},
        "auto",
        True,
    ),
    "capability-tools": ("str-list", [], True),
    "skills": ("str-list", [], True),
    "run-turn-budget": ("int", 10, True),
    "display-color": (None, None, True),
    # Framework assembly keys — never rendered to any tool (C-6).
    # `role-scope` is the team-domain counterpart of `capacity-scope`
    # (used by agent-team-supervisor-template.md); `project` marks
    # project-custom agents (agent-project-custom-template.md).
    "supervisor": ("bool", False, False),
    "capacity-scope": (None, None, False),
    "role-scope": (None, None, False),
    "project": (None, None, False),
}

NEUTRAL_AGENT_REQUIRED_KEYS = ("name", "description")

# Keys reserved for framework assembly; excluded from tool rendering (C-6).
NEUTRAL_AGENT_FRAMEWORK_KEYS = frozenset(
    {"supervisor", "capacity-scope", "role-scope", "project"}
)

# Tool-dialect vocabulary forbidden anywhere in agent metadata (C-4).
FORBIDDEN_AGENT_METADATA_KEYS = frozenset(
    {
        "maxTurns",
        "disallowedTools",
        "timeoutMins",
        "mcpServers",
        "permissionMode",
        "background",
        "isolation",
        "tools",
        "color",
        "model",
    }
)


class AgentMetadataError(ValueError):
    """Structured agent metadata violation: file path + offending key(s)."""

    def __init__(self, path, message, keys=()):
        self.path = str(path)
        self.keys = tuple(keys)
        super().__init__(f"{path}: {message}")


def split_agent_frontmatter(text):
    """Split an agent definition into (frontmatter_lines, body).

    Frontmatter is the block between a leading '---' line and the next '---'
    line. Returns ([], text) when no frontmatter is present.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], "\n".join(lines[idx + 1 :])
    return [], text


def _parse_agent_scalar(raw):
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        return value


def parse_agent_frontmatter(frontmatter_lines):
    """Parse frontmatter lines into an ordered dict (stdlib-only subset).

    Supports `key: value` scalars, quoted strings, booleans, integers and
    inline lists. Nested/multi-line YAML constructs are out of scope for
    agent metadata and raise AgentMetadataError.
    """
    data = {}
    for line in frontmatter_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1] in (" ", "\t"):
            raise AgentMetadataError(
                "<frontmatter>",
                "nested/multi-line YAML is not supported in agent metadata: "
                f"{stripped!r}",
            )
        key, sep, value = stripped.partition(":")
        if not sep:
            raise AgentMetadataError(
                "<frontmatter>",
                f"malformed frontmatter line (missing ':'): {stripped!r}",
            )
        data[key.strip()] = _parse_agent_scalar(value)
    return data


def _check_agent_value_domain(key, value):
    domain, _default, _renders = NEUTRAL_AGENT_METADATA_KEYS[key]
    if domain == "bool":
        if not isinstance(value, bool):
            return f"key '{key}' expects a boolean, got {value!r}"
    elif domain == "int":
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            return f"key '{key}' expects a positive integer, got {value!r}"
    elif domain == "str-list":
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item for item in value
        ):
            return f"key '{key}' expects a list of non-empty strings, got {value!r}"
    elif isinstance(domain, set):
        if value not in domain:
            allowed = "/".join(sorted(domain))
            return f"key '{key}' expects one of [{allowed}], got {value!r}"
    else:
        if not isinstance(value, str) or not value.strip():
            return f"key '{key}' expects a non-empty string, got {value!r}"
    return None


def validate_agent_metadata(path, text):
    """Validate one agent definition against the neutral metadata contract.

    Returns (metadata_dict, body). Raises AgentMetadataError for: missing
    frontmatter, out-of-set keys (C-1), forbidden dialect keys (C-4),
    non-kebab-case keys (C-3), missing required keys (C-2), domain
    violations, and placeholders inside the metadata block (C-7).
    """
    frontmatter_lines, body = split_agent_frontmatter(text)
    if not frontmatter_lines:
        raise AgentMetadataError(path, "missing frontmatter block")
    metadata = parse_agent_frontmatter(frontmatter_lines)

    unknown = sorted(set(metadata) - set(NEUTRAL_AGENT_METADATA_KEYS))
    if unknown:
        raise AgentMetadataError(
            path,
            "metadata keys outside the neutral set: " + ", ".join(unknown),
            keys=unknown,
        )
    kebab_violations = sorted(k for k in metadata if k != k.lower() or "_" in k)
    if kebab_violations:
        raise AgentMetadataError(
            path,
            "metadata keys must be kebab-case: " + ", ".join(kebab_violations),
            keys=kebab_violations,
        )
    missing = [k for k in NEUTRAL_AGENT_REQUIRED_KEYS if k not in metadata]
    if missing:
        raise AgentMetadataError(
            path, "missing required metadata keys: " + ", ".join(missing), keys=missing
        )
    for key, value in metadata.items():
        problem = _check_agent_value_domain(key, value)
        if problem:
            raise AgentMetadataError(path, problem, keys=(key,))
    placeholder_keys = sorted(
        k
        for k in frontmatter_lines
        if "{{" in k and "}}" in k
    )
    if placeholder_keys:
        raise AgentMetadataError(
            path,
            "unresolved placeholders in metadata block (authoring templates "
            "must not enter the render input)",
        )
    return metadata, body


def load_project_agent_definitions(project_path):
    """Collect validated agent definitions from the neutral source layers.

    Reads ``.specify/agents/templates/`` then ``.specify/agents/instances/``
    (instance wins on slug collision), validates every ``*.agent.md`` against
    the neutral metadata contract, and returns one record per definition:
    ``{"slug", "metadata", "body", "source"}`` sorted by slug. Any violation
    raises AgentMetadataError naming the offending file and key(s).
    """
    agents_root = Path(project_path) / ".specify" / "agents"
    collected = {}
    for layer in ("templates", "instances"):
        layer_dir = agents_root / layer
        if not layer_dir.is_dir():
            continue
        for entry in sorted(layer_dir.iterdir()):
            if not entry.is_file() or entry.suffix != ".md":
                continue
            if not entry.name.endswith(".agent.md"):
                continue
            slug = entry.name[: -len(".agent.md")]
            metadata, body = validate_agent_metadata(entry, entry.read_text())
            collected[slug] = {
                "slug": slug,
                "metadata": metadata,
                "body": body,
                "source": f"{layer}/{entry.name}",
            }
    return [collected[slug] for slug in sorted(collected)]


# ---------------------------------------------------------------------------
# Tool metadata mapping + renderer (Feature 044 — init-time distribution)
#
# unmapped-field policy (D3, contracts/tool-mapping.md M-5): a neutral field
# with no counterpart on the target tool is SKIPPED (never emitted) and
# reported per-agent in the init feedback; the policy applies identically to
# every tool. Provenance rows cite the official docs the field knowledge was
# verified from (FR-010); codex/hermes are annotated rows, not rendered.
# ---------------------------------------------------------------------------

_AGENT_METADATA_MAPPING = {
    "qoder": {
        "mode": "render",
        "target_dir": ".qoder/agents",
        "file_naming": "{slug}.agent.md",
        "fields": {
            "name": {"emit": "name"},
            "description": {"emit": "description"},
            "user-invocable": None,
            "disable-model-invocation": None,
            "model-tier": {"emit": "model"},
            "capability-tools": {"emit": "tools", "style": "list"},
            "skills": {"emit": "skills", "style": "list"},
            "run-turn-budget": {"emit": "maxTurns"},
            "display-color": {"emit": "color"},
        },
        "provenance": "https://docs.qoder.com/cli/subagent",
    },
    "claude": {
        "mode": "render",
        "target_dir": ".claude/agents",
        "file_naming": "{slug}.md",
        "fields": {
            "name": {"emit": "name"},
            "description": {"emit": "description"},
            "user-invocable": None,
            "disable-model-invocation": None,
            # Claude model identifiers are product names, not preference
            # tiers — no faithful mapping (D3).
            "model-tier": None,
            "capability-tools": {"emit": "tools", "style": "comma-string"},
            "skills": None,
            "run-turn-budget": None,
            "display-color": None,
        },
        "provenance": (
            "https://code.claude.com/docs/en/sub-agents (official page; the "
            "field list was verified 2026-08-13 via the VS Code docs, which "
            "document the Claude sub-agents format for .claude/agents/)"
        ),
    },
    "copilot": {
        "mode": "render",
        "target_dir": ".github/agents",
        "file_naming": "{slug}.agent.md",
        "fields": {
            "name": {"emit": "name"},
            "description": {"emit": "description"},
            "user-invocable": {"emit": "user-invocable"},
            "disable-model-invocation": {"emit": "disable-model-invocation"},
            # Copilot model values are product-specific; tiers don't map (D3).
            "model-tier": None,
            "capability-tools": {"emit": "tools", "style": "list"},
            "skills": None,
            "run-turn-budget": None,
            "display-color": None,
        },
        "provenance": (
            "https://code.visualstudio.com/docs/copilot/customization/"
            "custom-agents; https://docs.github.com/en/copilot/concepts/"
            "agents/cloud-agent/about-custom-agents"
        ),
    },
    "opencode": {
        "mode": "render",
        "target_dir": ".opencode/agents",
        # opencode: the FILENAME is the agent name — `name` is not emitted.
        "file_naming": "{slug}.md",
        "omit_name": True,
        "mode_from_invocability": True,
        "fields": {
            "name": None,
            "description": {"emit": "description"},
            "user-invocable": None,
            "disable-model-invocation": None,
            # opencode model values are provider/model IDs; tiers don't map (D3).
            "model-tier": None,
            # `tools` is deprecated in opencode agent frontmatter (D3).
            "capability-tools": None,
            "skills": None,
            "run-turn-budget": {"emit": "steps"},
            "display-color": {"emit": "color"},
        },
        "provenance": "https://opencode.ai/docs/agents/",
    },
    "codex": {
        "mode": "annotated",
        "provenance": (
            "https://github.com/openai/codex (source: codex-rs/core/src/"
            "config/agent_roles.rs; official docs page unreachable at "
            "verification time)"
        ),
        "note": (
            "Codex agents are TOML files under the user-level config layer "
            "($CODEX_HOME/agents/), outside project scope — not rendered this "
            "round (FR-012)."
        ),
    },
    "hermes": {
        "mode": "annotated",
        "provenance": "https://hermes-agent.nousresearch.com/docs",
        "note": (
            "No documented project-level agent file convention — silent skip "
            "(FR-014)."
        ),
    },
}

_AGENT_MANIFEST_NAME = ".render-manifest.json"
_AGENT_BACKUP_DIR = ".backups"


def _format_agent_frontmatter_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(value) + "]"
    text = str(value)
    if any(ch in text for ch in ":#{}[]") or text != text.strip():
        return '"' + text.replace('"', "'") + '"'
    return text


# --------------------------------------------------------------------------
# framework source provenance (043-init-commit-stamp)
#
# The grammar, resolution, and timestamp live in specify_cli._provenance
# (stdlib-only so the hatchling build hook can load them in the build
# environment); this module re-exports the SAME objects and binds them to
# MODULE_DIR.
# --------------------------------------------------------------------------

from . import _provenance as _provenance

_probe_head_commit = _provenance._probe_head_commit
_read_embedded_source_commit = _provenance._read_embedded_source_commit
_SOURCE_COMMIT_FILENAME = _provenance._SOURCE_COMMIT_FILENAME
_utc_compact_stamp = _provenance.utc_compact_stamp


def resolve_source_commit():
    """Module-dir-bound wrapper (043 contract §C-2) — see _provenance."""
    return _provenance.resolve_source_commit(MODULE_DIR)


def write_source_stamp(project_path) -> bool:
    """Write the framework source stamp (043 contract source-stamp-write):
    `<project>/.specify/source.json` = {framework, commit, [reason],
    stamped_at}, a full overwrite on every init (refresh leaves no stale id).
    Stamping is an incidental record, never a gate: any failure warns on the
    console and returns False — it MUST NOT fail init."""
    try:
        resolved = resolve_source_commit()
        payload = {"framework": "spec-kit",
                   "commit": resolved["commit"],
                   "stamped_at": _utc_compact_stamp()}
        if resolved["commit"] is None:
            payload["commit"] = "unavailable"
            payload["reason"] = resolved["reason"] or "source commit unresolvable"
        specify_dir = Path(project_path) / ".specify"
        specify_dir.mkdir(parents=True, exist_ok=True)
        (specify_dir / "source.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        return True
    except OSError as exc:
        console.print(
            f"[yellow]Warning:[/yellow] Source stamp not written: {exc}")
        return False


def _agent_file_sha256(path):
    import hashlib

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def render_agents_for_tool(project_path, tool, tracker=None):
    """Render validated agent definitions into the target tool's agent dir.

    Real files only (no symlinks). Semantics: instance beats template
    (load order), drift detection via the render manifest (modified outputs
    are backed up before overwrite), stale outputs pruned, user assets
    untouched, legacy per-file/whole-dir symlinks replaced (migration).
    Returns stats: {"tool", "rendered", "backups", "unmapped"}.
    """
    project_path = Path(project_path)
    stats = {"tool": tool, "rendered": 0, "backups": [], "unmapped": {}}
    row = _AGENT_METADATA_MAPPING.get(tool)
    if not row or row["mode"] != "render":
        return stats

    definitions = load_project_agent_definitions(project_path)
    target_dir = project_path / row["target_dir"]

    # Legacy migration: a whole-dir symlink at the target is removed first,
    # then every legacy per-file symlink in the dir (even dangling ones whose
    # source slug is gone) — real files are left for drift handling below.
    if target_dir.is_symlink():
        target_dir.unlink()
    target_dir.mkdir(parents=True, exist_ok=True)
    for entry in sorted(target_dir.iterdir()):
        if entry.is_symlink():
            entry.unlink()

    manifest_path = project_path / ".specify" / "agents" / _AGENT_MANIFEST_NAME
    manifest = {"version": 1, "tool": tool, "rendered_at": "", "entries": {}}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
        except (ValueError, OSError):
            pass
    previous_entries = dict(manifest.get("entries", {}))
    new_entries = {}

    def _backup(rel_path, target_file):
        backup_root = (
            project_path / ".specify" / "agents" / _AGENT_BACKUP_DIR / tool
        )
        backup_root.mkdir(parents=True, exist_ok=True)
        backup_path = backup_root / (
            f"{target_file.stem}.{_utc_compact_stamp()}{target_file.suffix}"
        )
        shutil.copy2(target_file, backup_path)
        stats["backups"].append(str(backup_path))

    for definition in definitions:
        slug = definition["slug"]
        metadata = definition["metadata"]
        out_lines = ["---"]
        if row.get("mode_from_invocability") and not metadata.get(
            "user-invocable", True
        ):
            out_lines.append("mode: subagent")
        for key in NEUTRAL_AGENT_METADATA_KEYS:
            if key not in metadata or key not in row["fields"]:
                continue
            rule = row["fields"][key]
            if rule is None:
                if key == "name" and row.get("omit_name"):
                    continue  # carried by the filename, not an unmapped intent
                if key in metadata and NEUTRAL_AGENT_METADATA_KEYS[key][2]:
                    stats["unmapped"].setdefault(slug, []).append(key)
                continue
            value = metadata[key]
            style = rule.get("style")
            if style == "comma-string":
                if not isinstance(value, list):
                    continue
                out_lines.append(f"{rule['emit']}: " + ", ".join(value))
            else:
                out_lines.append(
                    f"{rule['emit']}: {_format_agent_frontmatter_value(value)}"
                )
        out_lines.append("---")
        body = definition["body"].lstrip("\n")
        content = "\n".join(out_lines) + "\n" + body
        if not content.endswith("\n"):
            content += "\n"

        filename = row["file_naming"].format(slug=slug)
        target_file = target_dir / filename
        rel_path = f"{row['target_dir']}/{filename}"

        if target_file.is_symlink():
            target_file.unlink()  # legacy per-file link → replaced by render
        elif target_file.exists():
            previous = previous_entries.get(rel_path)
            if previous and previous.get("sha256") != _agent_file_sha256(target_file):
                _backup(rel_path, target_file)
        target_file.write_text(content)
        new_entries[rel_path] = {
            "source": definition["source"],
            "sha256": _agent_file_sha256(target_file),
        }
        stats["rendered"] += 1

    # Prune stale outputs (source removed) — scoped to THIS tool's target
    # dir; other tools' entries are carried forward untouched (R-7).
    scope_prefix = row["target_dir"] + "/"
    carried_entries = {
        rel_path: entry
        for rel_path, entry in previous_entries.items()
        if not rel_path.startswith(scope_prefix)
    }
    for rel_path, entry in previous_entries.items():
        if rel_path in new_entries or not rel_path.startswith(scope_prefix):
            continue
        stale = project_path / rel_path
        if stale.is_symlink():
            stale.unlink()
        elif stale.exists():
            if entry.get("sha256") != _agent_file_sha256(stale):
                _backup(rel_path, stale)
            stale.unlink()

    manifest = {
        "version": 1,
        "tool": tool,
        "rendered_at": _utc_compact_stamp(),
        "entries": {**carried_entries, **new_entries},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    if tracker:
        tracker.complete(
            "local-templates",
            f"rendered {stats['rendered']} agents for {tool} "
            f"({len(stats['backups'])} backups)",
        )
    return stats


# ---------------------------------------------------------------------------
# Assistant support profile helpers (Feature 022)
# ---------------------------------------------------------------------------

# Official assistant keys – the canonical list for this feature.
_OFFICIAL_ASSISTANT_KEYS = [
    "claude",
    "codex",
    "qoder",
    "opencode",
    "hermes",
    "copilot",
]

# Assistant → command output directory mapping (relative to project root)
_ASSISTANT_COMMAND_DIRS = {
    "copilot": ".github/prompts",
    "claude": ".claude/commands",
    "hermes": ".hermes/commands",
    "opencode": ".opencode/command",
    "qoder": ".qoder/commands",
    "codex": ".codex/commands",
}

# Assistant → file extension for generated command files
_ASSISTANT_EXTENSIONS = {
    "copilot": "prompt.md",
    "claude": "md",
    "hermes": "md",
    "opencode": "md",
    "qoder": "md",
    "codex": "md",
}

# Assistants whose generated command files carry YAML frontmatter with a
# `description` field (shown in the tool's slash-command palette). Qoder
# documents `description` as a required field of `.qoder/commands/*.md`.
_ASSISTANT_COMMAND_FRONTMATTER = {"qoder"}

# Assistant → argument format placeholder
_ASSISTANT_ARG_FORMATS = {
    "copilot": "$ARGUMENTS",
    "claude": "$ARGUMENTS",
    "hermes": "$ARGUMENTS",
    "opencode": "$ARGUMENTS",
    "qoder": "$ARGUMENTS",
    "codex": "$ARGUMENTS",
}

# ---------------------------------------------------------------------------
# Obsolete framework artifacts (structural cleanup on init/upgrade)
#
# These names are derived from Git history: framework-owned skills, commands, and
# top-level templates that were renamed, consolidated, or removed across versions.
# On init/upgrade the additive copytree (dirs_exist_ok=True) never deletes stale
# files, so an upgraded workspace accumulates old structure. cleanup_obsolete_
# framework_assets() removes ONLY these enumerated, framework-owned artifacts —
# never user-authored skills, commands, or templates.
#
# NOTE: the names below are historical, framework-owned identifiers that are
# named here solely so init can DELETE them. Legacy-reference guardrail tests
# treat the region between the OBSOLETE-ASSET-REGISTRY markers as sanctioned
# (it is a removal manifest, not a live dependency).
# ---------------------------------------------------------------------------
# OBSOLETE-ASSET-REGISTRY:START

# Skill directories that once shipped but were renamed/consolidated/removed.
# (agent-setup→cli-setup→agent-cli-setup; docx/pdf/pptx/xlsx-utils→document-utils;
# export-session→archive-session; extension-e2e-test→browser-extension;
# mysql/postgres-utils→database-utils;
# playwright-utils/web-test→browser-utils; organize-agents→create-team;
# thought-experiment-verifier→think-skills;
# manage-project→visualize-project→summarize-project;
# sdd-workflow→shared/workflow;
# mcp-creator/refresh-mcp-tools/notebooklm-utils/theme-creator removed).
_OBSOLETE_SKILLS = (
    "agent-setup",
    "cli-setup",
    "docx-utils",
    "export-session",
    "extension-e2e-test",
    "manage-project",
    "mcp-creator",
    "mysql-utils",
    "notebooklm-utils",
    "organize-agents",
    "pdf-utils",
    "playwright-utils",
    "postgres-utils",
    "pptx-utils",
    "refresh-mcp-tools",
    "sdd-workflow",
    "skill-creator",
    "theme-creator",
    "thought-experiment-verifier",
    "visualize-project",
    "web-test",
    "xlsx-utils",
)

# Files a skill once shipped but no longer owns, relative to .specify/skills/.
# (Hugo mount-mode scaffolder + reference + asset templates moved
# create-docs → create-pages when presentation was decoupled from structure;
# create-pages/scripts/scaffold.sh → scaffold-ci.sh when rendering and hosting
# were split into separate stages.)
_OBSOLETE_SKILL_FILES = (
    "create-docs/scripts/scaffold-hugo.py",
    "create-docs/references/hugo-site.md",
    "create-docs/assets/hugo/hugo.toml.tmpl",
    "create-docs/assets/hugo/dotgitignore",
    "create-docs/assets/hugo/layouts/index.html",
    "create-docs/assets/hugo/layouts/_default/baseof.html",
    "create-docs/assets/hugo/layouts/_default/list.html",
    "create-docs/assets/hugo/layouts/_default/single.html",
    "create-docs/assets/hugo/layouts/_default/_markup/render-link.html",
    "create-docs/assets/hugo/layouts/_default/_markup/render-image.html",
    "create-docs/assets/hugo/static/css/site.css",
    "create-pages/scripts/scaffold.sh",
)

# Command stems that were renamed or removed (specify→requirements; converge,
# mcpcall, taskstoissues removed). Generated command files are named
# ``speckit.<stem>.<ext>`` per agent, plus ``<stem>.md`` in the fallback
# .specify/templates/commands directory.
_OBSOLETE_COMMANDS = (
    "converge",
    "mcpcall",
    "specify",
    "taskstoissues",
)

# Top-level template files that were renamed, moved into skill directories, or
# removed and therefore no longer ship at .specify/templates/<file>.
_OBSOLETE_TEMPLATES = (
    "agent-ask-template.md",
    "agent-common-template.md",
    "agent-explore-template.md",
    "agent-file-template.md",
    "agent-knowledge-template.md",
    "agent-plan-template.md",
    "agent-research-template.md",
    "agent-role-knowledge-manager-template.md",
    "agent-role-module-designer-template.md",
    "agent-role-qa-engineer-template.md",
    "agent-role-requirements-analyst-template.md",
    "agent-role-system-designer-template.md",
    "agent-role-test-engineer-template.md",
    "agent-subrole-evaluator-template.md",
    "agent-subrole-executor-template.md",
    "agent-subrole-improver-template.md",
    "agent-supervision-delegation.md",
    "agent-triad-orchestration-template.md",
    "consitution-template.md",
    "feature-template.md",
    "mcptool-template.md",
    "spec-template.md",
    "tool-mcp-call-template.md",
    "tool-project-script-template.md",
    "tool-shell-function-template.md",
    "tool-system-binary-template.md",
    "tool-webhook-template.md",
)
# OBSOLETE-ASSET-REGISTRY:END

# Skills symlink assistants (those that need .<agent>/skills → .specify/skills link)
_SKILLS_SYMLINK_ASSISTANTS = {
    "copilot",
    "qoder",
    "claude",
    "hermes",
    "opencode",
    "codex",
}

# Assistant → support tier classification
# Tier 1 = common CLI-form AI tools; Tier 2 = non-CLI-form tools (IDE-based / platform agents)
_ASSISTANT_TIERS = {
    "claude": "tier1",
    "codex": "tier1",
    "qoder": "tier1",
    "opencode": "tier1",
    "hermes": "tier2",
    "copilot": "tier2",
}


def get_official_assistants() -> List[str]:
    """Return the ordered list of officially supported assistant keys."""
    return list(_OFFICIAL_ASSISTANT_KEYS)


def get_assistant_profile(key: str) -> dict:
    """Return the full assistant profile dict or raise KeyError."""
    profile = dict(AGENT_CONFIG[key])
    profile.setdefault("key", key)
    profile.setdefault("command_directory", _ASSISTANT_COMMAND_DIRS.get(key, ""))
    profile.setdefault("command_format", _ASSISTANT_EXTENSIONS.get(key, "md"))
    profile.setdefault("arg_format", _ASSISTANT_ARG_FORMATS.get(key, "$ARGUMENTS"))
    profile["officially_supported"] = key in _OFFICIAL_ASSISTANT_KEYS
    profile["tier"] = _ASSISTANT_TIERS.get(key, "tier2")
    profile["skills_symlink"] = key in _SKILLS_SYMLINK_ASSISTANTS
    return profile


class InitializationResultSummary:
    """Structured summary of an initialization or refresh operation."""

    def __init__(self):
        self.created: List[str] = []
        self.reused: List[str] = []
        self.skipped: List[str] = []
        self.preserved: List[str] = []
        self.conflicts: List[str] = []
        self.attention_required: List[str] = []
        self.configured_assistants: List[str] = []
        self.assistant_tiers: Dict[str, str] = {}

    def add_created(self, *paths: str):
        self.created.extend(paths)

    def add_reused(self, *paths: str):
        self.reused.extend(paths)

    def add_skipped(self, *paths: str):
        self.skipped.extend(paths)

    def add_preserved(self, *paths: str):
        self.preserved.extend(paths)

    def add_conflict(self, *paths: str):
        self.conflicts.extend(paths)

    def add_attention(self, *msgs: str):
        self.attention_required.extend(msgs)

    def set_configured_assistants(self, assistants: List[str]):
        self.configured_assistants = list(assistants)
        self.assistant_tiers = {k: _ASSISTANT_TIERS.get(k, "tier2") for k in assistants}

    def is_empty(self) -> bool:
        """Return True when no operation touched any asset."""
        return not any(
            [
                self.created,
                self.reused,
                self.skipped,
                self.preserved,
                self.conflicts,
                self.attention_required,
            ]
        )

    def to_dict(self) -> dict:
        return {
            "created": list(self.created),
            "reused": list(self.reused),
            "skipped": list(self.skipped),
            "preserved": list(self.preserved),
            "conflicts": list(self.conflicts),
            "attention_required": list(self.attention_required),
            "configured_assistants": list(self.configured_assistants),
            "assistant_tiers": dict(self.assistant_tiers),
        }

    def render_rich(self) -> str:
        """Return a rich-formatted summary string suitable for console output."""
        lines = []
        if self.created:
            lines.append(f"[green]Created:[/green] {', '.join(self.created)}")
        if self.reused:
            lines.append(f"[dim]Reused:[/dim] {', '.join(self.reused)}")
        if self.skipped:
            lines.append(f"[yellow]Skipped:[/yellow] {', '.join(self.skipped)}")
        if self.preserved:
            lines.append(f"[cyan]Preserved:[/cyan] {', '.join(self.preserved)}")
        if self.conflicts:
            lines.append(f"[red]Conflicts:[/red] {', '.join(self.conflicts)}")
        if self.attention_required:
            lines.append(
                f"[yellow]Attention required:[/yellow] {'; '.join(self.attention_required)}"
            )
        if self.configured_assistants:
            labeled = []
            for a in self.configured_assistants:
                tier = self.assistant_tiers.get(a, "")
                label = (
                    " (Tier 1)"
                    if tier == "tier1"
                    else " (Tier 2)"
                    if tier == "tier2"
                    else ""
                )
                labeled.append(f"{a}{label}")
            lines.append(f"[green]Configured assistants:[/green] {', '.join(labeled)}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core workspace asset preservation helpers
# ---------------------------------------------------------------------------

# Paths under project/.specify/ that constitute the shared core and should
# be preserved when they already exist.
_CORE_SPECIFY_ASSETS = [
    ".specify/memory",
    ".specify/templates",
    ".specify/scripts",
    ".specify/skills",
    ".specify/agents",
    ".specify/shared",
    ".specify/instructions.md",
]


def core_asset_relpaths() -> List[str]:
    """Return the list of relative paths considered core workspace assets."""
    return list(_CORE_SPECIFY_ASSETS)


def is_core_asset_initialized(project_path: Path, rel_path: str) -> bool:
    """Return True if the core asset already exists in the workspace."""
    return (project_path / rel_path).exists()


def detect_initialized_core_assets(project_path: Path) -> List[str]:
    """Return the list of core asset relpaths that already exist."""
    return [
        p for p in _CORE_SPECIFY_ASSETS if is_core_asset_initialized(project_path, p)
    ]


def detect_configured_assistants(project_path: Path) -> List[str]:
    """Detect which assistants appear to be configured in the workspace."""
    configured = []
    for key in _OFFICIAL_ASSISTANT_KEYS:
        profile = get_assistant_profile(key)
        folder = profile.get("folder", "")
        if folder and (project_path / folder).exists():
            configured.append(key)
    return configured


# ---------------------------------------------------------------------------
# Assistant command coverage helpers
# ---------------------------------------------------------------------------


def get_canonical_command_stems() -> List[str]:
    """Return the sorted list of canonical command template stems found on disk."""
    resource_path = get_resource_path()
    if not resource_path:
        return []
    commands_dir = resource_path / "templates" / "commands"
    if not commands_dir.exists():
        return []
    return sorted(f.stem for f in commands_dir.glob("*.md") if f.is_file())


def get_assistant_generated_commands(
    project_path: Path, assistant_key: str
) -> List[str]:
    """Return the sorted list of generated speckit.* command stems for an assistant."""
    dir_rel = _ASSISTANT_COMMAND_DIRS.get(assistant_key, "")
    if not dir_rel:
        return []
    output_dir = project_path / dir_rel
    if not output_dir.exists():
        return []
    stems = set()
    for f in output_dir.iterdir():
        if f.is_file() and f.name.startswith("speckit."):
            stem = f.name.replace("speckit.", "", 1)
            # Strip extension
            for ext in [".prompt.md", ".md", ".toml"]:
                if stem.endswith(ext):
                    stem = stem[: -len(ext)]
                    break
            stems.add(stem)
    return sorted(stems)


def compute_command_coverage(project_path: Path, assistant_key: str) -> dict:
    """Return {canonical, generated, missing, coverage_pct} for an assistant."""
    canonical = get_canonical_command_stems()
    generated = get_assistant_generated_commands(project_path, assistant_key)
    generated_set = set(generated)
    canonical_set = set(canonical)
    missing = sorted(canonical_set - generated_set)
    coverage_pct = (
        round(100.0 * len(canonical_set & generated_set) / len(canonical_set), 1)
        if canonical_set
        else 100.0
    )
    return {
        "canonical": canonical,
        "generated": generated,
        "missing": missing,
        "coverage_pct": coverage_pct,
    }


_CAPABILITY_DIMENSIONS = [
    "initialization",
    "command_templates",
    "instructions",
    "ignore_config",
    "skills_symlink",
    "refresh_protection",
]

_IGNORE_FILE_MAP = {
    "claude": ".claudeignore",
    "codex": ".codexignore",
}

_INSTRUCTIONS_FILE_MAP = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "qoder": "AGENTS.md",
    "hermes": "HERMES.md",
    "copilot": ".github/copilot-instructions.md",
    "opencode": ".opencode/instructions.md",
}


def _check_initialization(project_path: Path, tool_key: str) -> str:
    profile = get_assistant_profile(tool_key)
    folder = profile.get("folder", "")
    if folder and (project_path / folder).exists():
        return "pass"
    return "fail"


def _check_command_templates(project_path: Path, tool_key: str) -> str:
    coverage = compute_command_coverage(project_path, tool_key)
    if coverage["coverage_pct"] == 100.0:
        return "pass"
    return "fail"


def _check_instructions(project_path: Path, tool_key: str) -> str:
    instr_file = _INSTRUCTIONS_FILE_MAP.get(tool_key)
    if not instr_file:
        return "missing"
    if (project_path / instr_file).exists():
        return "pass"
    return "fail"


def _check_ignore_config(project_path: Path, tool_key: str) -> str:
    ignore_file = _IGNORE_FILE_MAP.get(tool_key)
    if not ignore_file:
        return "missing"
    if (project_path / ignore_file).exists():
        return "pass"
    return "fail"


def _check_skills_symlink(project_path: Path, tool_key: str) -> str:
    if tool_key not in _SKILLS_SYMLINK_ASSISTANTS:
        return "missing"
    profile = get_assistant_profile(tool_key)
    folder = profile.get("folder", "")
    if not folder:
        return "fail"
    skills_path = project_path / folder / "skills"
    if skills_path.exists():
        return "pass"
    return "fail"


def _check_refresh_protection(project_path: Path, tool_key: str) -> str:
    specify_dir = project_path / ".specify"
    if not specify_dir.exists():
        return "missing"
    core_assets = detect_initialized_core_assets(project_path)
    if core_assets:
        return "pass"
    return "fail"


_DIMENSION_CHECKERS = {
    "initialization": _check_initialization,
    "command_templates": _check_command_templates,
    "instructions": _check_instructions,
    "ignore_config": _check_ignore_config,
    "skills_symlink": _check_skills_symlink,
    "refresh_protection": _check_refresh_protection,
}


def audit_tool_dimension(project_path: Path, tool_key: str, dimension: str) -> str:
    checker = _DIMENSION_CHECKERS.get(dimension)
    if not checker:
        return "missing"
    return checker(project_path, tool_key)


def audit_capability_matrix(project_path: Path) -> dict:
    entries = []
    for tool_key in _OFFICIAL_ASSISTANT_KEYS:
        for dimension in _CAPABILITY_DIMENSIONS:
            status = audit_tool_dimension(project_path, tool_key, dimension)
            entries.append(
                {
                    "tool_key": tool_key,
                    "dimension": dimension,
                    "status": status,
                }
            )

    tier1_entries = [
        e for e in entries if _ASSISTANT_TIERS.get(e["tool_key"]) == "tier1"
    ]
    tier2_entries = [
        e for e in entries if _ASSISTANT_TIERS.get(e["tool_key"]) == "tier2"
    ]

    tier1_pass = sum(1 for e in tier1_entries if e["status"] == "pass")
    tier2_pass = sum(1 for e in tier2_entries if e["status"] == "pass")

    tier1_rate = (
        round(100.0 * tier1_pass / len(tier1_entries), 1) if tier1_entries else 0.0
    )
    tier2_rate = (
        round(100.0 * tier2_pass / len(tier2_entries), 1) if tier2_entries else 0.0
    )

    return {
        "entries": entries,
        "summary": {
            "tier1_pass_rate": tier1_rate,
            "tier2_pass_rate": tier2_rate,
        },
    }


SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)"}


BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"


class StepTracker:
    """Track and render hierarchical steps without emojis, similar to tree output.
    Supports live auto-refresh via an attached refresh callback.
    """

    def __init__(self, title: str, plain: bool = False):
        self.title = title
        self.plain = plain
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {
            "pending": 0,
            "running": 1,
            "done": 2,
            "error": 3,
            "skipped": 4,
        }
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append(
                {"key": key, "label": label, "status": "pending", "detail": ""}
            )
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._plain_log(s)
                self._maybe_refresh()
                return

        step = {"key": key, "label": key, "status": status, "detail": detail}
        self.steps.append(step)
        self._plain_log(step)
        self._maybe_refresh()

    def _plain_log(self, step):
        if not self.plain or step["status"] in ("pending", "running"):
            return
        tags = {
            "done": ("ok", "green"),
            "error": ("error", "red"),
            "skipped": ("skip", "yellow"),
        }
        word, color = tags.get(step["status"], (step["status"], "white"))
        detail = f": {step['detail']}" if step["detail"] else ""
        console.print(
            f"[{color}]{word:>5}[/{color}] {step['label']}{detail}",
            highlight=False,
        )

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = (
                        f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                    )
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


def get_resource_path() -> Optional[Path]:
    """
    Get the path containing templates/memory/scripts.
    Checks MODULE_DIR first (installed package), then repo root (local dev).
    """

    if (MODULE_DIR / "templates").exists():
        return MODULE_DIR

    return None


def has_local_templates() -> bool:
    """Check if local templates are available."""
    return get_resource_path() is not None


def rewrite_paths(content: str) -> str:
    """Rewrite root-relative paths in content to use the .specify/ prefix."""
    import re

    # Only rewrite a segment that STARTS a path reference. The lookbehind rejects
    # any preceding path character, which covers both an existing `.specify/`
    # prefix and nested references such as `skills/<name>/templates/`.
    for segment in ("memory", "scripts", "templates", "shared"):
        content = re.sub(rf"(?<![\w./-]){segment}/", rf".specify/{segment}/", content)
    return content


def generate_commands(
    agent: str, ext: str, arg_format: str, output_dir: Path, script_variant: str
) -> None:
    """Generate command files from templates for the specified agent."""
    output_dir.mkdir(parents=True, exist_ok=True)

    resource_path = get_resource_path()
    if not resource_path:
        return

    commands_dir = resource_path / "templates" / "commands"
    template_files: List[Path] = []
    seen_stems: Set[str] = set()

    if commands_dir.exists():
        for template_file in commands_dir.glob("*.md"):
            if template_file.is_file() and template_file.stem not in seen_stems:
                template_files.append(template_file)
                seen_stems.add(template_file.stem)

    # Fallback to repo templates if available (helps in local dev when package templates lag)
    repo_commands_dir = MODULE_DIR.parent.parent / "templates" / "commands"
    if (
        repo_commands_dir.exists()
        and repo_commands_dir.resolve() != commands_dir.resolve()
    ):
        for template_file in repo_commands_dir.glob("*.md"):
            if template_file.is_file() and template_file.stem not in seen_stems:
                template_files.append(template_file)
                seen_stems.add(template_file.stem)

    if not template_files:
        return

    for template_file in template_files:
        if not template_file.is_file():
            continue

        name = template_file.stem

        # Read template content
        with open(template_file, "r", encoding="utf-8") as f:
            file_content = f.read()

        # Normalize line endings
        file_content = file_content.replace("\r\n", "\n").replace("\r", "\n")

        # Extract description from YAML frontmatter
        import re

        description_match = re.search(
            r'^description:\s*["\']?([^"\']+)["\']?', file_content, re.MULTILINE
        )
        description = (
            description_match.group(1) if description_match else f"Command for {name}"
        )

        # Single-line description emitted into command-file frontmatter (see
        # _ASSISTANT_COMMAND_FRONTMATTER); falls back to the full description.
        short_description_match = re.search(
            r'^short-description:\s*["\']?([^"\'\n]+)["\']?\s*$',
            file_content,
            re.MULTILINE,
        )
        frontmatter_description = (
            short_description_match.group(1).strip()
            if short_description_match
            else description
        )

        # Extract script command for the script variant
        script_match = re.search(
            rf"^\s*{script_variant}:\s*\|\s*$", file_content, re.MULTILINE
        )
        if script_match:
            # Multi-line block starting after the `sh: |` line until the next dedented key or frontmatter end
            lines = file_content.split("\n")
            start_idx: Optional[int] = None
            indent_prefix = ""
            for i, line in enumerate(lines):
                if re.match(rf"^\s*{script_variant}:\s*\|\s*$", line):
                    start_idx = i + 1
                    if start_idx < len(lines):
                        indent_match = re.match(r"^(\s+)", lines[start_idx])
                        indent_prefix = (
                            indent_match.group(1) if indent_match else "    "
                        )
                    break

            block_lines: List[str] = []
            if start_idx is not None:
                for j in range(start_idx, len(lines)):
                    ln = lines[j]
                    # Stop when we reach a new top-level/frontmatter key
                    if ln.strip().startswith(
                        (
                            "description:",
                            "scripts:",
                            "agent_scripts:",
                            "handoffs:",
                            "---",
                        )
                    ) and not ln.startswith(indent_prefix):
                        break
                    # Only strip the leading indent corresponding to the block
                    if indent_prefix and ln.startswith(indent_prefix):
                        block_lines.append(ln[len(indent_prefix) :])
                    else:
                        block_lines.append(ln)

            script_command = (
                "\n```bash\n" + "\n".join(block_lines).rstrip("\n") + "\n```\n"
                if block_lines
                else "(Missing script command)"
            )
        else:
            # Fallback: single-line form like `sh: some-command {ARGS}`
            single_line_match = re.search(
                rf"^\s*{script_variant}:\s*(.+)$", file_content, re.MULTILINE
            )
            script_command = (
                single_line_match.group(1).strip()
                if single_line_match
                else "(Missing script command)"
            )

        # Replace {ARGS} placeholder in script command
        script_command = script_command.replace("{ARGS}", arg_format)

        # Remove scripts: and agent_scripts: sections from frontmatter
        # This is complex, so we'll keep the original frontmatter but remove those sections
        lines = file_content.split("\n")
        new_lines = []
        in_frontmatter = False
        skip_scripts_section = False

        for line in lines:
            if line.strip() == "---":
                new_lines.append(line)
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                if line.strip().startswith("scripts:") or line.strip().startswith(
                    "agent_scripts:"
                ):
                    skip_scripts_section = True
                    continue
                if skip_scripts_section and line.strip() and not line.startswith(" "):
                    skip_scripts_section = False

                if skip_scripts_section:
                    continue

            new_lines.append(line)

        # Reconstruct content without scripts sections
        cleaned_content = "\n".join(new_lines)

        # Extract body (everything after the frontmatter)
        body_parts = cleaned_content.split("---")
        if len(body_parts) >= 3:
            body = "---".join(body_parts[2:]).strip()
        else:
            body = cleaned_content.strip()

        # Replace placeholders in the final body
        body = body.replace("{SCRIPT}", script_command)
        body = body.replace("__AGENT__", agent)

        # Apply path rewrites
        body = rewrite_paths(body)

        # Write the command file based on format
        output_path = output_dir / f"speckit.{name}.{ext}"
        marker = (
            f"AUTO-GENERATED from templates/commands/{name}.md — do not edit; "
            "edit the source template, then run scripts/python/regen-command-copies.py"
        )
        if ext == "toml":
            toml_content = (
                f"# {marker}\n"
                + f'description = "{description}"\n\n'
                + 'prompt = """\n'
                + body
                + '\n"""\n'
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(toml_content)
        else:
            # For "prompt.md" and "md" just write the body; tools that read a
            # description from command frontmatter get it prepended on top.
            content = f"<!-- {marker} -->\n" + body
            if agent in _ASSISTANT_COMMAND_FRONTMATTER:
                content = (
                    f"---\ndescription: {frontmatter_description}\n---\n" + content
                )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)


def strip_comments(text: str) -> str:
    """Removes C-style comments (// and /* */) from text."""

    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)


def detect_tech_stack(root_dir: Path) -> Set[str]:
    stack = set()
    # Java
    if (root_dir / "pom.xml").exists() or (root_dir / "build.gradle").exists():
        stack.add("java")

    # Python
    if (
        (root_dir / "pyproject.toml").exists()
        or (root_dir / "requirements.txt").exists()
        or (root_dir / "setup.py").exists()
    ):
        stack.add("python")

    # Node/JS/TS
    if (root_dir / "package.json").exists():
        stack.add("javascript")
        if (root_dir / "tsconfig.json").exists():
            stack.add("typescript")

    return stack


def configure_vscode_settings(
    project_path: Path, tracker: Optional[StepTracker] = None
) -> None:
    """Generate VS Code settings based on project context."""
    template_path = project_path / ".specify" / "templates" / "vscode-settings.json"
    output_path = project_path / ".vscode" / "settings.json"

    if not template_path.exists():
        # Try using existing settings file as template
        if output_path.exists():
            template_path = output_path
        # Fallback to source template if not found in project (e.g. during local dev copy)
        elif (resource_path := get_resource_path()) and (
            resource_path / "templates" / "vscode-settings.json"
        ).exists():
            template_path = resource_path / "templates" / "vscode-settings.json"
        else:
            return

    if tracker:
        tracker.start("vscode-settings", "Configuring VS Code settings")

    try:
        # Load template
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            json_content = strip_comments(content)
            settings = json.loads(json_content)

        # Analyze context
        stack = detect_tech_stack(project_path)

        # Apply settings
        if "java" in stack:
            settings.setdefault(
                "java.configuration.updateBuildConfiguration", "automatic"
            )
            settings.setdefault(
                "java.format.settings.url", ".vscode/java-formatter.xml"
            )

        if "python" in stack:
            settings.setdefault("python.analysis.typeCheckingMode", "basic")
            settings.setdefault("python.formatting.provider", "black")

        if "typescript" in stack or "javascript" in stack:
            settings.setdefault("editor.defaultFormatter", "esbenp.prettier-vscode")

        # Ensure .vscode exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        if tracker:
            tracker.complete(
                "vscode-settings",
                f"Updated for {', '.join(stack) if stack else 'generic'}",
            )

    except Exception as e:
        if tracker:
            tracker.error("vscode-settings", str(e))
        else:
            console.print(f"[red]Error configuring VS Code settings:[/red] {e}")


def ensure_specify_symlink(
    root_path: Path, agent_dir_name: str, specify_subdir: str
) -> None:
    """Create a directory-level symlink from <agent_dir>/<specify_subdir> to .specify/<specify_subdir>.

    Handles migration of existing regular directories and stale symlinks.
    Works for both skills and agents (and any future .specify/ subdirectory).
    """
    agent_dir = root_path / agent_dir_name
    agent_dir.mkdir(parents=True, exist_ok=True)

    specify_target = root_path / ".specify" / specify_subdir
    specify_target.mkdir(parents=True, exist_ok=True)
    link_path = agent_dir / specify_subdir
    relative_target = Path(os.path.relpath(specify_target, start=agent_dir))

    if link_path.is_symlink():
        try:
            if link_path.resolve() == specify_target.resolve():
                return
        except OSError:
            pass
        try:
            linked_path = link_path.resolve()
            if linked_path.exists() and linked_path.is_dir():
                shutil.copytree(linked_path, specify_target, dirs_exist_ok=True)
        except OSError:
            pass
        link_path.unlink(missing_ok=True)

    if link_path.exists():
        if link_path.is_dir():
            shutil.copytree(link_path, specify_target, dirs_exist_ok=True)
            shutil.rmtree(link_path)
        else:
            return

    link_path.symlink_to(relative_target, target_is_directory=True)


def ensure_agent_layer_dirs(root_path: Path) -> Path:
    """Ensure the three-layer agent directory skeleton under ``.specify/agents/``.

    Layout (canonical taxonomy: ``shared/definitions/agent-definitions.md``):

    - ``templates/``  Agent Templates — shipped role set installed by ``specify init``
    - ``instances/``  Agent Instances — project-authored agents (``create-agent``)
    - ``execution/``  Agent Execution — dispatch ``configs/``, ``scripts/`` and
      runtime ``logs/`` (logs are gitignored via the shipped ``.specify/.gitignore``)

    Also migrates the legacy flat layout: any top-level
    ``.specify/agents/*.agent.md`` predates the layered layout and is moved into
    ``templates/`` — everything ``specify init`` installed at the top level was the
    shipped template set.
    Returns the ``.specify/agents`` root.
    """
    agents_root = root_path / ".specify" / "agents"
    for sub in ("templates", "instances", "execution/configs", "execution/scripts", "execution/logs"):
        (agents_root / sub).mkdir(parents=True, exist_ok=True)

    templates_dir = agents_root / "templates"
    for legacy in sorted(agents_root.glob("*.agent.md")):
        target = templates_dir / legacy.name
        if not target.exists():
            shutil.move(str(legacy), str(target))
        else:
            legacy.unlink()

    return agents_root


def cleanup_obsolete_framework_assets(
    project_path: Path,
    ai_assistant: str,
    tracker: Optional[StepTracker] = None,
) -> List[str]:
    """Remove obsolete framework-owned structure from an upgraded workspace.

    Init copies assets additively (``copytree(dirs_exist_ok=True)``) and never
    deletes files that a newer framework version dropped or renamed. This prunes
    ONLY the enumerated, framework-owned artifacts in ``_OBSOLETE_SKILLS``,
    ``_OBSOLETE_SKILL_FILES``, ``_OBSOLETE_COMMANDS``, and ``_OBSOLETE_TEMPLATES``
    — restricted to the ``.specify/`` tree and the active agent's command
    directory. User-authored skills, commands, and templates are never touched.

    Returns the list of removed paths (relative to ``project_path``) for reporting.
    """
    removed: List[str] = []
    specify_dir = project_path / ".specify"

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(project_path))
        except ValueError:
            return str(p)

    # 1) Obsolete skills: .specify/skills/<name>/ (agent .<tool>/skills dirs are
    #    symlinks to this canonical location, so a single removal is enough).
    skills_dir = specify_dir / "skills"
    for name in _OBSOLETE_SKILLS:
        target = skills_dir / name
        if target.is_symlink() or not target.exists():
            continue
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
            removed.append(_rel(target))

    # 2) Files a skill no longer owns (e.g. moved to another skill): delete the
    #    file, then prune directories it leaves empty, bounded to that skill dir.
    for rel in _OBSOLETE_SKILL_FILES:
        target = skills_dir / rel
        if target.is_symlink() or not target.is_file():
            continue
        target.unlink()
        removed.append(_rel(target))
        skill_root = skills_dir / Path(rel).parts[0]
        parent = target.parent
        while parent != skill_root and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent

    # 3) Obsolete top-level templates: .specify/templates/<file>
    templates_dir = specify_dir / "templates"
    for filename in _OBSOLETE_TEMPLATES:
        target = templates_dir / filename
        if target.is_file() and not target.is_symlink():
            target.unlink()
            removed.append(_rel(target))

    # 4) Obsolete commands: speckit.<stem>.<ext> in the active agent's command
    #    dir, plus the fallback .specify/templates/commands/<stem>.md.
    command_targets: List[Path] = []
    cmd_dir_rel = _ASSISTANT_COMMAND_DIRS.get(ai_assistant)
    cmd_ext = _ASSISTANT_EXTENSIONS.get(ai_assistant)
    for stem in _OBSOLETE_COMMANDS:
        if cmd_dir_rel and cmd_ext:
            command_targets.append(
                project_path / cmd_dir_rel / f"speckit.{stem}.{cmd_ext}"
            )
        command_targets.append(specify_dir / "templates" / "commands" / f"{stem}.md")
    for target in command_targets:
        if target.is_file() and not target.is_symlink():
            target.unlink()
            removed.append(_rel(target))

    if tracker:
        if removed:
            tracker.complete(
                "local-templates",
                f"removed {len(removed)} obsolete framework asset(s)",
            )
        else:
            tracker.complete("local-templates", "no obsolete assets to remove")

    return removed


def copy_local_templates(
    project_path: Path,
    ai_assistant: str,
    script_type: str,
    is_current_dir: bool = False,
    tracker: Optional[StepTracker] = None,
) -> Path:
    """Copy local templates to create a new project.
    Returns project_path.
    """
    resource_path = get_resource_path()
    if not resource_path:
        raise RuntimeError("Local templates not found")

    if tracker:
        tracker.add("local-templates", "Using local templates")
        tracker.start("local-templates", "checking template structure")

    # Create project directory only if not using current directory
    if not is_current_dir:
        project_path.mkdir(parents=True, exist_ok=True)

    try:
        # Create the .specify directory structure that the original template expects
        specify_dir = project_path / ".specify"
        specify_dir.mkdir(exist_ok=True)

        # Copy memory directory
        if (resource_path / "memory").exists():
            memory_src = resource_path / "memory"
            memory_dest = specify_dir / "memory"
            memory_dest.mkdir(exist_ok=True)

            # Specific files to handle
            memory_files = ["constitution.md", "features.md"]

            for filename in memory_files:
                src_file = memory_src / filename
                dest_file = memory_dest / filename

                if src_file.exists():
                    if tracker:
                        tracker.start("local-templates", f"copying {filename}")

                    # Check if destination file already exists
                    if dest_file.exists():
                        console.print(
                            f"[yellow]Memory file {filename} already exists - skipping copy to preserve existing content[/yellow]"
                        )
                    else:
                        # Copy the file
                        shutil.copy2(src_file, dest_file)
                        if tracker:
                            tracker.complete("local-templates", f"{filename} copied")
                else:
                    if tracker:
                        tracker.skip(
                            "local-templates", f"{filename} not found in source"
                        )

            # Copy memory subdirectories (e.g. session/, knowledge/) so the
            # dynamic memory-as-files scaffolding matches what ships in git.
            # Existing files are preserved to avoid clobbering user content.
            for sub_dir in sorted(p for p in memory_src.iterdir() if p.is_dir()):
                dest_sub = memory_dest / sub_dir.name
                if tracker:
                    tracker.start(
                        "local-templates", f"copying memory/{sub_dir.name}"
                    )
                for src_item in sub_dir.rglob("*"):
                    rel = src_item.relative_to(sub_dir)
                    dest_item = dest_sub / rel
                    if src_item.is_dir():
                        dest_item.mkdir(parents=True, exist_ok=True)
                    elif not dest_item.exists():
                        dest_item.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_item, dest_item)
                dest_sub.mkdir(parents=True, exist_ok=True)
                if tracker:
                    tracker.complete(
                        "local-templates", f"memory/{sub_dir.name} copied"
                    )

        # Copy scripts directory
        if (resource_path / "scripts").exists():
            if tracker:
                tracker.start("local-templates", "copying scripts")
            shutil.copytree(
                resource_path / "scripts",
                specify_dir / "scripts",
                dirs_exist_ok=True,
            )

            # Handle script type filtering if needed
            # Only bash scripts are supported now
            pass

        # Copy templates directory (excluding commands which will be handled specially)
        if (resource_path / "templates").exists():
            if tracker:
                tracker.start("local-templates", "copying templates")
            # Copy all templates except commands directory
            for item in (resource_path / "templates").iterdir():
                if item.name != "commands":
                    if item.is_dir():
                        shutil.copytree(
                            item,
                            specify_dir / "templates" / item.name,
                            dirs_exist_ok=True,
                        )
                    else:
                        specify_dir.mkdir(parents=True, exist_ok=True)
                        (specify_dir / "templates").mkdir(exist_ok=True)
                        shutil.copy2(item, specify_dir / "templates" / item.name)

        # Handle AI assistant specific command files using the same logic as release script
        if (resource_path / "templates" / "commands").exists():
            if tracker:
                tracker.start("local-templates", f"generating {ai_assistant} commands")

            # Map AI assistant to their command directory and format (same as release script)
            if ai_assistant == "copilot":
                generate_commands(
                    "copilot",
                    "prompt.md",
                    "$ARGUMENTS",
                    project_path / ".github" / "prompts",
                    script_type,
                )
                # VS Code settings are handled by configure_vscode_settings() later
            elif ai_assistant == "opencode":
                generate_commands(
                    "opencode",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".opencode" / "command",
                    script_type,
                )
            elif ai_assistant == "qoder":
                generate_commands(
                    "qoder",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".qoder" / "commands",
                    script_type,
                )
            elif ai_assistant == "claude":
                generate_commands(
                    "claude",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".claude" / "commands",
                    script_type,
                )
            elif ai_assistant == "codex":
                generate_commands(
                    "codex",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".codex" / "commands",
                    script_type,
                )
            elif ai_assistant == "hermes":
                generate_commands(
                    "hermes",
                    "md",
                    "$ARGUMENTS",
                    project_path / ".hermes" / "commands",
                    script_type,
                )
            else:
                # Fallback: copy commands to .specify/templates/commands
                shutil.copytree(
                    MODULE_DIR / "templates" / "commands",
                    specify_dir / "templates" / "commands",
                    dirs_exist_ok=True,
                )

        # Also copy any root-level files that might be in the original project structure
        root_files = ["README.md", ".gitignore", "spec-driven.md", "LICENSE"]
        for file_name in root_files:
            # Look for these files in the parent directory of the module (src/specify_cli -> .. -> spec-kit root)
            src_file = MODULE_DIR.parent.parent / file_name
            if src_file.exists():
                shutil.copy2(src_file, project_path / file_name)
            else:
                # If not found in development structure, check if they exist at module level (installed package)
                src_file = MODULE_DIR / file_name
                if src_file.exists():
                    shutil.copy2(src_file, project_path / file_name)

        if ai_assistant == "claude":
            claudeignore_template = (
                resource_path / "templates" / "claudeignore-template"
            )
            if not claudeignore_template.exists():
                fallback_template = (
                    MODULE_DIR.parent.parent / "templates" / "claudeignore-template"
                )
                if fallback_template.exists():
                    claudeignore_template = fallback_template
            if claudeignore_template.exists():
                shutil.copy2(claudeignore_template, project_path / ".claudeignore")

        if ai_assistant == "codex":
            codexignore_template = resource_path / "templates" / "codexignore-template"
            if not codexignore_template.exists():
                fallback_template = (
                    MODULE_DIR.parent.parent / "templates" / "codexignore-template"
                )
                if fallback_template.exists():
                    codexignore_template = fallback_template
            if codexignore_template.exists():
                shutil.copy2(codexignore_template, project_path / ".codexignore")

        # Ship the framework-owned .specify/.gitignore so target projects ignore
        # the transient /speckit.history and /speckit.team .work/ scratch dirs
        # created inside their own .specify/ tree during daily development.
        gitignore_specify_template = (
            resource_path / "templates" / "gitignore-specify-template"
        )
        if not gitignore_specify_template.exists():
            fallback_template = (
                MODULE_DIR.parent.parent / "templates" / "gitignore-specify-template"
            )
            if fallback_template.exists():
                gitignore_specify_template = fallback_template
        if gitignore_specify_template.exists():
            shutil.copy2(gitignore_specify_template, specify_dir / ".gitignore")

        # Copy skills directory
        if (resource_path / "skills").exists():
            if tracker:
                tracker.start("local-templates", "copying skills")

            skills_dest = project_path / ".specify" / "skills"
            skills_dest.mkdir(parents=True, exist_ok=True)

            shutil.copytree(
                resource_path / "skills",
                skills_dest,
                dirs_exist_ok=True,
            )
            if tracker:
                tracker.complete("local-templates", "skills copied")

        # Copy agents directory (shipped Agent Templates -> .specify/agents/templates/)
        if (resource_path / "agents").exists():
            if tracker:
                tracker.start("local-templates", "copying agents")

            agents_dest = ensure_agent_layer_dirs(project_path) / "templates"

            shutil.copytree(
                resource_path / "agents",
                agents_dest,
                dirs_exist_ok=True,
            )
            if tracker:
                tracker.complete("local-templates", "agents copied")

        # Copy shared directory (shared reference documents)
        if (resource_path / "shared").exists():
            if tracker:
                tracker.start("local-templates", "copying shared")

            shared_dest = project_path / ".specify" / "shared"
            shared_dest.mkdir(parents=True, exist_ok=True)

            shutil.copytree(
                resource_path / "shared",
                shared_dest,
                dirs_exist_ok=True,
            )
            if tracker:
                tracker.complete("local-templates", "shared copied")

        if ai_assistant == "copilot":
            if tracker:
                tracker.start(
                    "local-templates", "linking .github/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".github", "skills")
            if tracker:
                tracker.complete("local-templates", ".github/skills symlink ready")

        if ai_assistant == "qoder":
            if tracker:
                tracker.start(
                    "local-templates", "linking .qoder/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".qoder", "skills")
            if tracker:
                tracker.complete("local-templates", ".qoder/skills symlink ready")

        if ai_assistant == "claude":
            if tracker:
                tracker.start(
                    "local-templates", "linking .claude/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".claude", "skills")
            if tracker:
                tracker.complete("local-templates", ".claude/skills symlink ready")

        if ai_assistant == "opencode":
            if tracker:
                tracker.start(
                    "local-templates", "linking .opencode/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".opencode", "skills")
            if tracker:
                tracker.complete("local-templates", ".opencode/skills symlink ready")

        if ai_assistant == "codex":
            if tracker:
                tracker.start(
                    "local-templates", "linking .codex/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".codex", "skills")
            if tracker:
                tracker.complete("local-templates", ".codex/skills symlink ready")

        if ai_assistant == "hermes":
            if tracker:
                tracker.start(
                    "local-templates", "linking .hermes/skills to .specify/skills"
                )
            ensure_specify_symlink(project_path, ".hermes", "skills")
            if tracker:
                tracker.complete("local-templates", ".hermes/skills symlink ready")

        # Agent distribution: render the neutral metadata into the target
        # tool's own agent format as real files (Feature 044; the per-file
        # symlink model is retired). Annotated rows (codex/hermes) skip
        # silently per FR-012/FR-014.
        agent_row = _AGENT_METADATA_MAPPING.get(ai_assistant)
        if agent_row and agent_row["mode"] == "render":
            if tracker:
                tracker.start(
                    "local-templates",
                    f"rendering agents for {ai_assistant}",
                )
            render_stats = render_agents_for_tool(project_path, ai_assistant)
            summary = (
                f"rendered {render_stats['rendered']} agents for {ai_assistant}"
            )
            if render_stats["backups"]:
                summary += f" ({len(render_stats['backups'])} hand-edited backups)"
            if render_stats["unmapped"]:
                summary += (
                    f"; unmapped intents on {len(render_stats['unmapped'])} agent(s)"
                )
            if tracker:
                tracker.complete("local-templates", summary)

        # Structural cleanup: remove obsolete framework-owned skills, commands,
        # and templates left behind by earlier versions (upgrade path). Scope is
        # strictly the framework's own enumerated artifacts; user content is safe.
        if tracker:
            tracker.start("local-templates", "cleaning obsolete framework assets")
        cleanup_obsolete_framework_assets(project_path, ai_assistant, tracker)

    except Exception as e:
        last_step = ""
        if tracker:
            last_step = next(
                (
                    s["detail"]
                    for s in tracker.steps
                    if s["key"] == "local-templates"
                ),
                "",
            )
        step_prefix = f"failed during '{last_step}': " if last_step else ""
        message = f"{step_prefix}{type(e).__name__}: {e}"
        if tracker:
            tracker.error("local-templates", message)
        else:
            console.print(f"[red]Error copying local templates:[/red] {message}")
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise

    return project_path


def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"

    if key == readchar.key.ENTER:
        return "enter"

    if key == readchar.key.ESC:
        return "escape"

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key


def select_with_arrows(
    options: Dict,
    prompt_text: str = "Select an option",
    default_key: Optional[str] = None,
) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row(
            "", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]"
        )

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(
            create_selection_panel(),
            console=console,
            transient=True,
            auto_refresh=False,
        ) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key


console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split("\n")
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if (
        ctx.invoked_subcommand is None
        and "--help" not in sys.argv
        and "-h" not in sys.argv
    ):
        show_banner()
        console.print(
            Align.center("[dim]Run 'specify --help' for usage information[/dim]")
        )
        console.print()


def run_command(
    cmd: List[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(
                cmd, check=check_return, capture_output=True, text=True, shell=shell
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, "stderr") and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, tracker: Optional[StepTracker] = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found


def is_git_repo(path: Optional[Path] = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(
    project_path: Path, quiet: bool = False
) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.

    Args:
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Specify template"],
            check=True,
            capture_output=True,
            text=True,
        )
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"

        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)


def ensure_executable_scripts(
    project_path: Path, tracker: Optional["StepTracker"] = None
) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: List[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat()
            mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400:
                new_mode |= 0o100
            if mode & 0o040:
                new_mode |= 0o010
            if mode & 0o004:
                new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (
            f", {len(failures)} failed" if failures else ""
        )
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(
                f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]"
            )
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")


@app.command()
def init(
    project_name: str = typer.Argument(
        None,
        help="Name for your new project directory (optional if using --here, or use '.' for current directory)",
    ),
    ai_assistant: str = typer.Option(
        None,
        "--ai",
        help="AI assistant to use: claude, codex, qoder, opencode (Tier 1), or hermes, copilot (Tier 2)",
    ),
    script_type: str = typer.Option(
        None, "--script", help="Script type to use: sh or ps"
    ),
    ignore_agent_tools: bool = typer.Option(
        False,
        "--ignore-agent-tools",
        help="Skip checks for AI agent tools like Claude Code, Codex CLI, Qoder CLI, opencode, Hermes Agent, or GitHub Copilot",
    ),
    no_git: bool = typer.Option(
        False, "--no-git", help="Skip git repository initialization"
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Initialize project in the current directory instead of creating a new one",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force merge/overwrite when using --here (skip confirmation)",
    ),
    skip_tls: bool = typer.Option(
        False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Show verbose diagnostic output for network and extraction failures",
    ),
):
    """
    Initialize a new Specify project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant
    3. Use local templates (GitHub download is no longer supported)
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
        specify init my-project
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init . --ai claude         # Initialize in current directory with Claude Code
        specify init . --ai hermes         # Initialize in current directory with Hermes Agent
        specify init . --ai qoder          # Initialize in current directory with Qoder
        specify init .                     # Initialize in current directory (interactive AI selection)
        specify init --here --ai opencode  # Alternative syntax for current directory
        specify init --here
        specify init --here --force  # Skip confirmation when current directory not empty
    """

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print(
            "[red]Error:[/red] Cannot specify both project name and --here flag"
        )
        raise typer.Exit(1)

    if not here and not project_name:
        console.print(
            "[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag"
        )
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(
                f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)"
            )
            console.print(
                "[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]"
            )
            if force:
                console.print(
                    "[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]"
                )
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        # project_name is not None here due to validation above
        assert project_name is not None
        project_path = Path(project_name).resolve()
        if project_path.exists():
            console.print(
                f"[red]Error:[/red] Directory '{project_name}' already exists"
            )
            console.print(
                "Choose a different project name or remove the existing directory."
            )
            raise typer.Exit(1)

    current_dir = Path.cwd()

    console.print("[cyan]Specify project setup[/cyan]", highlight=False)
    console.print(f"  Project:      {project_path.name}", highlight=False)
    console.print(f"  Working path: {current_dir}", highlight=False)
    if not here:
        console.print(f"  Target path:  {project_path}", highlight=False)

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print(
                "[yellow]Git not found - will skip repository initialization[/yellow]"
            )

    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(
                f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AGENT_CONFIG.keys())}"
            )
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Create options dict for selection (agent_key: display_name)
        ai_choices = {
            key: AGENT_CONFIG[key]["name"] for key in _OFFICIAL_ASSISTANT_KEYS
        }
        selected_ai = select_with_arrows(
            ai_choices, "Choose your AI assistant:", "claude"
        )

    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not check_tool(selected_ai):
                console.print(
                    f"[red]Error:[/red] '{selected_ai}' not found - "
                    f"{agent_config['name']} is required for this project type."
                )
                console.print(f"Install from: {install_url}")
                console.print("Tip: use --ignore-agent-tools to skip this check")
                raise typer.Exit(1)

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(
                f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}"
            )
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        if sys.stdin.isatty():
            selected_script = select_with_arrows(
                SCRIPT_TYPE_CHOICES,
                "Choose script type (or press Enter)",
                default_script,
            )
        else:
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    tracker = StepTracker("Initialize Specify Project", plain=True)

    tracker.add("local-check", "Check for local templates")
    tracker.add("features-dir", "Prepare features directory")
    tracker.add("git", "Initialize git repository")
    tracker.add("vscode-settings", "Configure VS Code")

    git_error_message = None

    try:
        verify = not skip_tls
        local_ssl_context = ssl_context if verify else False
        local_client = httpx.Client(verify=local_ssl_context)

        # First, check if local templates are available
        if has_local_templates():
            tracker.complete("local-check", "found - using local templates")

            # Use local templates
            copy_local_templates(
                project_path, selected_ai, selected_script, here, tracker
            )
        else:
            tracker.error("local-check", "not found")
            console.print(
                "[red]Error:[/red] Local templates not found. GitHub download is no longer supported."
            )
            raise typer.Exit(1)
        # Ensure the features directory exists under .specify/memory for downstream workflows
        features_dir = project_path / ".specify" / "memory" / "features"
        try:
            features_dir.mkdir(parents=True, exist_ok=True)
            tracker.complete("features-dir", f"created {features_dir}")
        except Exception as e:
            tracker.error("features-dir", str(e))

        ensure_executable_scripts(project_path, tracker=tracker)

        if not no_git:
            if is_git_repo(project_path):
                tracker.complete("git", "existing repo detected")
            elif should_init_git:
                success, error_msg = init_git_repo(project_path, quiet=True)
                if success:
                    tracker.complete("git", "initialized")
                else:
                    tracker.error("git", "init failed")
                    git_error_message = error_msg
            else:
                tracker.skip("git", "git not available")
        else:
            tracker.skip("git", "--no-git flag")

        # Configure VS Code settings
        configure_vscode_settings(project_path, tracker=tracker)
    except Exception as e:
        if isinstance(e, typer.Exit):
            detail = "aborted by an earlier error (see messages above)"
        else:
            detail = f"{type(e).__name__}: {e}"
        console.print(f"[red]Error:[/red] Initialization failed: {detail}")
        if debug:
            console.print(traceback.format_exc().rstrip(), highlight=False)
            console.print(
                f"Python {sys.version.split()[0]} on {sys.platform}, cwd: {Path.cwd()}",
                highlight=False,
            )
        else:
            console.print("[dim]Re-run with --debug for the full traceback.[/dim]")
        if not here and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)

    write_source_stamp(project_path)
    console.print("\n[bold green]Project ready.[/bold green]")

    # Show git error details if initialization failed
    if git_error_message:
        console.print(
            "[yellow]Warning:[/yellow] Git repository initialization failed: "
            f"{git_error_message}"
        )
        cd_target = project_path if not here else "."
        console.print(
            f"Initialize manually: cd {cd_target} && git init && git add . "
            '&& git commit -m "Initial commit"',
            highlight=False,
        )

    # Agent folder security notice
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"]
        console.print(
            f"[yellow]Note:[/yellow] agents may store credentials in {agent_folder}; "
            "consider adding it (or parts of it) to .gitignore.",
            highlight=False,
        )

    console.print("\n[cyan]Next steps[/cyan]")
    step_num = 1
    if not here:
        console.print(
            f"  {step_num}. Go to the project folder: cd {project_name}",
            highlight=False,
        )
        step_num += 1

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"
        console.print(
            f"  {step_num}. Set CODEX_HOME before running Codex: {cmd}",
            highlight=False,
        )
        step_num += 1

    if selected_ai == "claude":
        console.print(
            f"  {step_num}. Claude Code commands are in .claude/commands/ "
            "and ignore rules are in .claudeignore",
            highlight=False,
        )
        step_num += 1

    console.print(
        f"  {step_num}. Start with slash commands: /speckit.constitution -> "
        "/speckit.feature -> /speckit.requirements -> /speckit.plan -> "
        "/speckit.tasks -> /speckit.implement",
        highlight=False,
    )
    console.print(
        "  Optional: /speckit.clarify /speckit.interview /speckit.analyze "
        "/speckit.checklist /speckit.research /speckit.review /speckit.agents "
        "/speckit.tools /speckit.skills /speckit.instructions",
        highlight=False,
    )


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # IDE-based agent - skip CLI check and mark as optional
            tracker.skip(agent_key, "IDE-based, no CLI check")
            agent_results[agent_key] = False  # Don't count IDE agents as "found"

    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
