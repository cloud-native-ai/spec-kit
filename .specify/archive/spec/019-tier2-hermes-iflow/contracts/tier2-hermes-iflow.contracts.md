# Contracts: Tier 2 Agent Support for Hermes-Agent and iFlow

**Spec**: [requirements.md](../requirements.md) | **Plan**: [plan.md](../plan.md)

## C-001: AGENT_CONFIG entries exist

**Covers**: FR-001, FR-005

Both `"hermes"` and `"iflow"` MUST exist as keys in `AGENT_CONFIG` with the following structure:

```python
AGENT_CONFIG["hermes"] == {
    "name": "Hermes Agent",
    "folder": ".hermes/",
    "install_url": <any string or None>,
    "requires_cli": True,
}

AGENT_CONFIG["iflow"] == {
    "name": "iFlow",
    "folder": ".iflow/",
    "install_url": <any string or None>,
    "requires_cli": True,
}
```

**Assertion**: `"hermes" in AGENT_CONFIG and "iflow" in AGENT_CONFIG`

---

## C-002: Official assistant keys include both tools

**Covers**: FR-001, FR-005

`_OFFICIAL_ASSISTANT_KEYS` MUST contain both [[STR-HERMES_KEY]] and [[STR-IFLOW_KEY]].

**Assertion**: `"hermes" in _OFFICIAL_ASSISTANT_KEYS and "iflow" in _OFFICIAL_ASSISTANT_KEYS`

---

## C-003: Tier classification is tier2

**Covers**: FR-009

Both tools MUST be classified as [[STR-TIER2]] in `_ASSISTANT_TIERS`.

**Assertions**:
- `_ASSISTANT_TIERS["hermes"] == "tier2"`
- `_ASSISTANT_TIERS["iflow"] == "tier2"`

---

## C-004: Tier ordering — Tier 2 tools after Tier 1

**Covers**: FR-011

In `_OFFICIAL_ASSISTANT_KEYS`, all Tier 1 keys MUST appear before any Tier 2 key. Both `"hermes"` and `"iflow"` MUST appear in the Tier 2 section (after all Tier 1 entries).

**Assertion**: For every Tier 1 key `t1` and Tier 2 key `t2` in `_OFFICIAL_ASSISTANT_KEYS`, `index(t1) < index(t2)`.

---

## C-005: Command directory mapping

**Covers**: FR-003, FR-007, FR-016, FR-017

```python
_ASSISTANT_COMMAND_DIRS["hermes"] == ".hermes/commands"
_ASSISTANT_COMMAND_DIRS["iflow"] == ".iflow/commands"
```

---

## C-006: File extension mapping

**Covers**: FR-003, FR-007, FR-016, FR-017

```python
_ASSISTANT_EXTENSIONS["hermes"] == "md"
_ASSISTANT_EXTENSIONS["iflow"] == "md"
```

---

## C-007: Argument format mapping

**Covers**: FR-003, FR-007, FR-016, FR-017

```python
_ASSISTANT_ARG_FORMATS["hermes"] == "$ARGUMENTS"
_ASSISTANT_ARG_FORMATS["iflow"] == "$ARGUMENTS"
```

---

## C-008: Skills symlink membership

**Covers**: FR-012 (implicit — Tier 2 tools get skills symlinks)

```python
"hermes" in _SKILLS_SYMLINK_ASSISTANTS
"iflow" in _SKILLS_SYMLINK_ASSISTANTS
```

---

## C-009: Instructions file mapping

**Covers**: FR-013 (governance — instructions file is the mechanism for constitution/instructions sync)

```python
_INSTRUCTIONS_FILE_MAP["hermes"] == "HERMES.md"
_INSTRUCTIONS_FILE_MAP["iflow"] == "IFLOW.md"
```

---

## C-010: get_assistant_profile returns complete profile

**Covers**: FR-001, FR-005

`get_assistant_profile("hermes")` and `get_assistant_profile("iflow")` MUST return dicts containing all expected fields without `KeyError`.

**Required fields**: `key`, `name`, `folder`, `install_url`, `requires_cli`, `command_directory`, `command_format`, `arg_format`, `officially_supported`, `tier`, `skills_symlink`.

**Assertions**:
- `get_assistant_profile("hermes")["tier"] == "tier2"`
- `get_assistant_profile("hermes")["officially_supported"] is True`
- `get_assistant_profile("hermes")["skills_symlink"] is True`
- `get_assistant_profile("iflow")["tier"] == "tier2"`
- `get_assistant_profile("iflow")["officially_supported"] is True`
- `get_assistant_profile("iflow")["skills_symlink"] is True`

---

## C-011: Total official assistant count is 8

**Covers**: FR-009

`len(_OFFICIAL_ASSISTANT_KEYS) == 8`

The full ordered list MUST be: `["claude", "codex", "qoder", "copilot", "opencode", "qwen", "hermes", "iflow"]`

---

## C-012: Init creates tool directory and commands

**Covers**: FR-002, FR-006

After `specify init . --ai hermes`:
- `.hermes/` directory MUST exist
- `.hermes/commands/` directory MUST exist
- At least one `.md` command file MUST exist in `.hermes/commands/`

After `specify init . --ai iflow`:
- `.iflow/` directory MUST exist
- `.iflow/commands/` directory MUST exist
- At least one `.md` command file MUST exist in `.iflow/commands/`

---

## C-013: Init creates skills symlink

**Covers**: FR-012

After init with `--ai hermes`:
- `.hermes/skills` MUST exist and be a symlink pointing to `.specify/skills/` (or `.specify/skills` content)

After init with `--ai iflow`:
- `.iflow/skills` MUST exist and be a symlink pointing to `.specify/skills/` (or `.specify/skills` content)

---

## C-014: Init preserves existing core files

**Covers**: FR-012

Given a project with existing `.specify/` core files:
- After adding hermes or iflow support, all files in `.specify/` MUST be unchanged
- No core files (constitution, features, instructions) MUST be overwritten

---

## C-015: Capability matrix includes both tools

**Covers**: FR-010

`audit_capability_matrix(project_path)` MUST return entries for both `"hermes"` and `"iflow"` across all 6 dimensions.

**Assertion**: Result `entries` list contains exactly 12 entries (2 tools × 6 dimensions) with `tool_key` in `{"hermes", "iflow"}`.

---

## C-016: InitializationResultSummary shows Tier 2 labels

**Covers**: FR-004, FR-008

When `set_configured_assistants(["hermes"])` is called:
- `assistant_tiers["hermes"] == "tier2"`
- `render_rich()` output contains `"(Tier 2)"`

Same for `"iflow"`.

---

## C-017: CLI --ai flag accepts new keys

**Covers**: FR-002, FR-006, FR-015

`specify init . --ai hermes` MUST NOT produce "Invalid AI assistant" error.
`specify init . --ai iflow` MUST NOT produce "Invalid AI assistant" error.
