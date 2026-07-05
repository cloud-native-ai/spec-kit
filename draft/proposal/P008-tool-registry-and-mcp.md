# P008 — Tool Registry & MCP Integration

- **Status:** Draft
- **Pillars:** Scripts
- **Source projects:** claude-code-ts, claw-code-agent, intellegix-code-agent-toolkit
- **Value:** H · **Effort:** M–H · **Phase:** 2
- **Related:** [[P001]], [[P002]], [[P011]], [[P013]]

## Problem / Gap

spec-kit already has a *tool* concept: four tool-template families
(`templates/tool-project-script-template.md`, `tool-system-binary-template.md`,
`tool-shell-function-template.md`, `tool-webhook-template.md`), a `/speckit.tools`
authoring command (`templates/commands/tools.md`), a discovery/authoring script
(`scripts/bash/create-new-tools.sh` + `scripts/python/tools-utils.py`), and a human-
and machine-readable Registry rendered into the `## Resource Registry → ### Tools`
table of `.specify/instructions.md`. This is a solid *catalog* of local capabilities.

Three gaps block it from becoming the "Scripts" spine of a universal framework:

1. **No behavioral contract.** A tool record carries RFC-2119 behavioral *rules* (prose
   the agent must obey) but no *machine* flags — nothing tells the harness whether a tool
   is read-only, destructive, or safe to run concurrently. Every consumer re-derives this
   from free text. Skills (`skills/*/SKILL.md`) and tools use *different* shapes, so the
   harness cannot reason about them uniformly.
2. **No MCP integration.** spec-kit has zero MCP story. MCP servers are the dominant way
   the ecosystem ships tools, and every supported harness (Claude Code, Copilot, opencode,
   Qwen, Qoder) can consume them — but spec-kit neither registers, documents, nor scaffolds
   them.
3. **Context bloat at scale.** The Registry is dumped whole into `instructions.md`. Once
   tools + skills + MCP tools number in the dozens, the instruction file balloons and the
   agent pays that cost on every turn.

## Proposal

Introduce a **uniform tool descriptor** that every capability — a `/speckit.tools` record,
a skill, or an MCP tool — can be projected onto, and build three thin layers on top of it,
all expressed as templates + scripts (no change to the `/speckit.*` flow):

- **A. Descriptor protocol.** Extend the tool-record + SKILL.md frontmatter with a small,
  fixed set of *behavioral flags* (`read_only`, `destructive`, `concurrency_safe`,
  `open_world`), a `permission` default (`allow`/`ask`/`deny`), and a `search_hint`. A
  `tools-utils.py` normalizer projects records/skills/MCP tools into one `ToolDescriptor`.
- **B. Deferred tools + tool-search.** Keep a small always-listed **core** set in
  `instructions.md`; index the rest by `search_hint`+`description` and expose a
  `search-tools` / `describe-tool` script pair so the agent discovers on demand instead of
  reading the whole Registry. O(1) instruction cost regardless of Registry size.
- **C. MCP client layer.** An `mcp-utils.py` that connects declared MCP servers, discovers
  their tools, maps MCP annotations to the same behavioral flags, and folds them into the
  same Registry/search machinery — plus a reusable **MCP server template** (FastMCP) and a
  `create-new-mcp.sh` scaffolder, mirroring the existing tool/skill authoring pattern.
- **D. Bash-security validator.** A stdlib `bash_security.py` returning
  ALLOW/ASK/DENY/PASSTHROUGH, callable by permission hooks ([[P001]]) and by the optional
  runtime ([[P011]]) before any shell tool runs.

## Design sketch

### D.1 Descriptor schema (added fields, backward-compatible)

Tool records gain a small frontmatter block (existing prose sections are untouched); the
same keys are added to SKILL.md frontmatter so both project onto one shape:

```yaml
# added to .specify/memory/tools/<name>.md frontmatter and skills/*/SKILL.md
behavior:
  read_only: true          # never mutates workspace / external state
  destructive: false       # can delete/overwrite/irreversibly change state
  concurrency_safe: true   # safe to run in parallel with other tools
  open_world: false        # touches network / non-deterministic external state
permission: ask            # allow | ask | deny  (default resolution for the harness)
search_hint: "format json filter query"   # extra keywords for tool-search ranking
core: false                # if true, always listed in instructions.md (never deferred)
```

The canonical Python shape both records and MCP tools normalize to:

```python
# scripts/python/tools_registry.py
@dataclass(frozen=True)
class ToolDescriptor:
    name: str
    kind: str            # project-script | system-binary | shell-function | webhook | skill | mcp
    source_id: str       # script path | binary | function | url | server::tool
    description: str
    read_only: bool = False
    destructive: bool = False
    concurrency_safe: bool = True
    open_world: bool = False
    permission: str = "ask"          # allow | ask | deny
    search_hint: str = ""
    core: bool = False
    behavioral_rules: list[str] = field(default_factory=list)   # existing RFC-2119 prose
```

Defaults are fail-safe: an MCP tool with no `readOnlyHint` is treated as *not* read-only;
an unknown `kind` defaults `permission: ask`. This mirrors claude-code-ts's `buildTool`
factory (fill safe defaults, declare only what is special).

### D.2 Deferred tools + tool-search

`instructions.md` lists only `core: true` descriptors (constitution-adjacent essentials)
plus a one-line pointer. Everything else is discovered via two scripts:

```
scripts/python/tools-utils.py search  --query "convert csv" --json
  → [{name, kind, score, search_hint, permission}, …]   # ranked, top-N
scripts/python/tools-utils.py describe --name <tool> --json
  → full ToolDescriptor incl. parameters/returns/behavioral_rules
```

Ranking = keyword score (0.4) + TF-IDF over `description + search_hint` (0.6), the merge
used by claude-code-ts's `SearchExtraToolsTool`. A budget-aware formatter caps the
listing (~1% of context, degrade to names-only under pressure) — the same discovery
mechanism [[P002]] proposes for skills, so tools and skills share one index.

### D.3 MCP layer

```
.specify/mcp/servers.yml          # declared servers (name, transport, command/url, env)
scripts/python/mcp-utils.py       # connect → discover → normalize → register
templates/mcp-server/             # reusable FastMCP server skeleton (scaffold target)
scripts/bash/create-new-mcp.sh    # /speckit.tools-adjacent scaffolder
```

`servers.yml`:

```yaml
servers:
  - name: filesystem
    transport: stdio            # stdio | http | sse
    command: ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."]
    permission_default: ask
  - name: search
    transport: http
    url: https://mcp.example.com/sse
    env: { API_KEY: "${SEARCH_MCP_KEY}" }
```

Discovery maps MCP annotations onto the descriptor (the key trick from
`mcp-client/src/discovery.ts` lines 65-107):

| MCP annotation | ToolDescriptor field |
|---|---|
| `readOnlyHint` | `read_only` |
| `destructiveHint` | `destructive` |
| `openWorldHint` | `open_world` |
| (no annotation) | fail-safe default |

Discovered MCP tools are named `mcp::<server>::<tool>`, cached per server, and written
into the same `### Tools` Registry table + search index — no downstream special-casing.
`mcp-utils.py` also emits each harness's native MCP config (`.mcp.json`, opencode/Qwen
equivalents) so the same `servers.yml` drives every supported assistant.

### D.4 CLI / command surface

```
specify tools search  <query> [--json]        # deferred-tool discovery
specify tools describe <name> [--json]
specify mcp add <name> --transport … [--url|--command …]
specify mcp list [--json]                      # servers + discovered tools + flags
specify mcp sync                               # (re)discover + regenerate harness configs
```

These wrap the scripts; `/speckit.tools` stays the interactive authoring path and simply
gains the new frontmatter fields in its collection step.

### D.5 Bash-security validator

```python
# scripts/python/bash_security.py  (stdlib only, drop-in)
class Behavior(Enum): ALLOW; ASK; DENY; PASSTHROUGH
@dataclass
class SecurityResult: behavior: Behavior; reason: str; matched_rule: str | None
def bash_command_is_safe(command: str) -> SecurityResult: ...
```

Composable validators detect destructive (`rm -rf /`), obfuscated (base64|`eval`), and
network-exfil patterns; the ASK tier maps onto spec-kit's existing confirmation UX (the
`Proceed with execution? (yes/no)` gate already in `templates/commands/tools.md` step 7).

## Source evidence

- Uniform descriptor + `buildTool` defaults, behavioral flags (`isReadOnly`/`isDestructive`/
  `isConcurrencySafe`/`isOpenWorld`), `checkPermissions`, `searchHint` →
  `_research/claude-code-ts-tools.md` idea #3 (`packages/agent-tools/src/types.ts` 111-203).
- Deferred tools + hybrid keyword+TF-IDF tool-search, budget-aware listing →
  `_research/claude-code-ts-tools.md` ideas #1/#6
  (`SearchExtraToolsTool.ts` 471-501, `SkillTool/prompt.ts` `formatCommandsWithinBudget` 71-172).
- MCP client folding tools into one registry + annotation→flag mapping →
  `_research/claude-code-ts-tools.md` idea #5 (`mcp-client/src/discovery.ts` 65-107).
- Declarative tool registry (`AgentTool` dataclass → OpenAI schema + handler) →
  `_research/claw-code-agent.md` idea #3 (`src/agent_tools.py` `AgentTool` line 78, registry 215).
- Bash-security ALLOW/ASK/DENY validator →
  `_research/claw-code-agent.md` idea #8 (`src/bash_security.py` 26-49).
- Reusable FastMCP server template + registration recipe →
  `_research/intellegix-commands-agents-mcp.md` idea #4 (`mcp-servers/minecraft/server.py`,
  `mcp-servers/browser-bridge/lib/{validator,rate-limiter,logger}.js`).
- spec-kit surfaces extended: `templates/commands/tools.md` (steps 4/7/8),
  `templates/tool-*-template.md`, `scripts/python/tools-utils.py` (`_CANONICAL_TOOL_TYPES`),
  `scripts/bash/create-new-tools.sh`, the `### Tools` Registry table in `.specify/instructions.md`.

## Adoption plan

Everything lands in `draft/` and is opt-in; the `/speckit.*` flow is untouched.

1. **Descriptor (A).** Add the optional `behavior`/`permission`/`search_hint`/`core` block
   to the tool-record templates and to `tools-utils.py` as a normalizer + `ToolDescriptor`
   dataclass. Records without the block get fail-safe defaults — fully backward-compatible.
   `/speckit.tools` step 4 gains one optional prompt for the flags.
2. **Search (B).** Add `search`/`describe` subcommands to `tools-utils.py` and switch
   `instructions.md` rendering to list only `core` tools + a search pointer. Share the index
   with [[P002]]'s skill discovery.
3. **Validator (D).** Vendor `bash_security.py`; wire it as a helper that [[P001]] hooks and
   [[P011]] call. Standalone and independently testable first.
4. **MCP (C).** Add `mcp-utils.py`, `.specify/mcp/servers.yml`, `templates/mcp-server/`, and
   `create-new-mcp.sh`; register discovered tools into the shared Registry + search index and
   emit per-harness MCP configs. Gate behind `specify mcp …` so no MCP means no behavior
   change.

Promotion to the real flow happens only after the descriptor + search are stable and the
MCP layer has round-tripped against at least Claude Code and one non-Claude harness.

## Risks & mitigations

- **Schema churn across records/skills/MCP.** Keep the flag set *small and fixed* (four
  booleans + one enum + one hint); resist per-tool bespoke fields. Normalizer owns all
  defaulting so consumers never branch on `kind`.
- **MCP dependency weight.** Use the official Python MCP SDK behind `mcp-utils.py` only;
  keep it an optional extra (`specify[mcp]`) so the base CLI stays lean, matching claw-code's
  "keep the runtime deps out of the core install" lesson.
- **Trusting untrusted server output.** Sanitize/limit discovered tool text; default any
  un-annotated MCP tool to `permission: ask` + `read_only: false` (fail-safe), and surface
  the source server in the Registry so users can audit before enabling.
- **Search misranking hides a tool.** Always allow `describe --name` direct lookup and keep
  a `--all` escape hatch that dumps the full Registry.
- **Bloat of the validator's deny-list.** Ship a conservative default set; make rules
  data-driven (a rules file) so teams tune ALLOW/DENY without code edits.

## Value / Effort rationale

**Value H:** this is the Scripts pillar's keystone — it unifies spec-kit's existing tool
templates, its skills, and (new) MCP tools under one contract the harness can reason about,
closes the named MCP gap, and makes the capability set scale without context cost. It is a
prerequisite for a safe optional runtime ([[P011]]) and pairs directly with permission hooks
([[P001]]).

**Effort M–H:** the descriptor, search, and validator are small, self-contained Python
additions on top of infrastructure spec-kit already has (`tools-utils.py`, the Registry
table). The MCP layer is the larger piece — SDK integration, annotation mapping, and
per-harness config emission — which is why the overall estimate lands at M–H and the MCP
sub-layer is sequenced last.
