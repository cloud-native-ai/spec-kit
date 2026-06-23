# Contract: `search-todo.sh` CLI

## 1. Scope

This contract governs the CLI surface, I/O semantics, discovery behavior, and diagnostic protocol of `.specify/scripts/bash/search-todo.sh` — a pure-bash+awk workspace scanner that locates `SPECKIT TODO` fenced blocks in eligible text files and emits structured JSON or human-readable key:value output. The contract defines flag syntax, exit codes, output schemas, discovery rules, and context extraction rules. It does not govern prompt-layer grouping, plan synthesis, or automatic execution.

## 2. Invocation

### 2.1 Synopsis

```
search-todo.sh [OPTIONS] [ROOT]
```

### 2.2 Options

The following options govern all invocations. Behavior marked **MUST** is normative and enforced by contract tests; behavior marked **SHOULD** is recommended and tested.

| Flag | Type | Required | Default | Effect |
|------|------|----------|---------|--------|
| `--json` | boolean | No | `false` | Emit a single-line JSON object to stdout (schema in §4.2). |
| `--help`, `-h` | boolean | No | — | Print synopsis and option summary to stdout, then exit 0. |
| `--root <path>` | string | No | `$GIT_ROOT` or script-cwd ancestor | Override the workspace root. MUST resolve to a readable directory; used when no positional `ROOT` is supplied. |
| `--exclude <pattern>` | string (repeatable) | No | — | Append `<pattern>` to the built-in ignore list. Patterns use `gitignore` semantics and match against workspace-relative paths. MUST NOT replace or override built-in excludes unless `--no-default-excludes` is also set. |
| `--no-default-excludes` | boolean | No | `false` | Disable the built-in ignore list. MUST be used with care: enables scanning of `.git/`, `node_modules/`, `.venv/`, etc. |
| `--context-depth <n>` | integer | No | `8` | Paragraph-boundary ceiling: scan up to `n` non-blank lines above and below each matched block for prologue/epilogue context. The scan MUST stop at the first blank line or Markdown section heading, whichever comes first. |
| `--context-only-headings` | boolean | No | `false` | Restrict `prologue` and `epilogue` to the nearest Markdown heading line only (no surrounding paragraph lines). MUST override `--context-depth` for prologue/epilogue content. |

### 2.3 Positional

- **`ROOT`** — Workspace root path (absolute or relative to current working directory). If omitted, uses `--root`. If both are omitted, falls back to `$GIT_ROOT`, then to the nearest ancestor of the current working directory that contains `.specify` or `.git`. If no such ancestor exists, exit 2.

## 3. Exit Codes

| Code | Meaning | When |
|------|---------|------|
| 0 | Success | Scan completed; JSON or key:value output written to stdout. |
| 1 | Argument error | Unknown flag, missing flag value, or contradictory flags. |
| 2 | Repository root undefined | Neither `--root`, `$GIT_ROOT`, positional `ROOT`, git root, nor `.specify`-ancestor found. |
| 3 | Scan I/O error | Permission denied, root unreadable, or file-system traversal failure. |
| 4 | Encoding error | A file cannot be decoded as UTF-8 and cannot be treated as text; reported in `excluded_files`. |

## 4. Output Format

### 4.1 Default (non-JSON) — key:value, one per line

Output order MUST be deterministic. Example:

```
BRANCH:          020-speckit-todo-command
REPO_ROOT:       /abs/path/to/workspace
TOTAL_FILES:     42
TOTAL_BLOCKS:    12
MALFORMED:       1
EXCLUDED_FILES:  7
SCANNED_AT:      2026-06-23T14:22:11Z
BLOCK[0]:        src/foo.md:42:58:heading "Authentication service"
BLOCK[1]:        docs/bar.md:11:27:heading "Deployment flow"
MALFORMED[0]:    src/bad.md:99:unclosed_fence
```

Each `BLOCK[i]` line: `<workspace-rel-file>:<opening_line>:<closing_line>:heading <heading|null>`.

Each `MALFORMED[i]` line: `<workspace-rel-file>:<opening_line>:<reason>` where reason ∈ `unclosed_fence`, `nested_fence`, `unparseable`, `encoding_error`.

### 4.2 JSON mode (`--json`)

One JSON object, single line, printed to stdout.

**Schema** (all fields MUST be present; arrays MAY be empty; strings MUST be escaped per RFC 8259):

```json
{
  "repository": "/abs/path/to/workspace",
  "branch": "020-speckit-todo-command",
  "scanned_at": "2026-06-23T14:22:11Z",
  "counters": {
    "total_files_scanned": 42,
    "total_blocks_found": 12,
    "malformed_blocks": 1,
    "excluded_files_count": 7
  },
  "blocks": [
    {
      "block_id": "src/foo.md:42:0",
      "source_file": "src/foo.md",
      "opening_line": 42,
      "closing_line": 58,
      "content": "<raw body, original formatting preserved>",
      "context_heading": "Authentication service",
      "prologue": "<up to --context-depth lines above the block, or up to first blank line / section heading>",
      "epilogue": "<up to --context-depth lines below the block>"
    }
  ],
  "malformed": [
    {
      "source_file": "src/bad.md",
      "opening_line": 99,
      "reason": "unclosed_fence",
      "content_snippet": "<first 120 chars of body>",
      "line_after_eof": true
    }
  ],
  "excluded_files": [
    "node_modules/lib/x.js",
    ".git/objects/pack/a.pack"
  ]
}
```

- `blocks` order MUST be deterministic: `(source_file ASC, opening_line ASC)`.
- All string fields MUST be UTF-8; control characters MUST be JSON-escaped.
- `block_id` format: `<source_file>:<opening_line>:<zero-based-index-within-file>`.

## 5. Discovery Rules (normative)

| Rule | Text |
|------|------|
| **D-1** | A block is matched iff the opening fence line (either ` ``` ` or `~~~`) contains the substring `SPECKIT TODO` (case-exact, anywhere on the line). |
| **D-2** | A block ends at the first subsequent fence line of the same character and **at least the same length** as the opening fence, before end-of-file. |
| **D-3** | If no matching closing fence is found before EOF, the block MUST be reported as `MalformedBlock` with reason `unclosed_fence`. |
| **D-4** | If an opening fence containing `SPECKIT TODO` appears inside another fenced block, it MUST be ignored. If the outer block also contains `SPECKIT TODO`, the inner occurrence MUST be reported with reason `nested_fence`. Otherwise the inner line is treated as ordinary content. |
| **D-5** | Files listed in the default excludes (`.git/`, `.venv/`, `node_modules/`, `__pycache__/`, built artifact dirs, and other generated outputs) or matching any `--exclude` pattern MUST NOT be scanned. |
| **D-6** | Binary files (content not decodable as UTF-8 within the first 8192 bytes) MUST be reported in `excluded_files` with reason `encoding_error` and MUST NOT be scanned. |
| **D-7** | Files larger than 16 MB MUST be reported in `excluded_files` with reason `too_large` and MUST NOT be scanned. |
| **D-8** | The marker substring match MUST be case-exact: `speckit todo`, `Speckit Todo`, and all other case variants MUST NOT match. |

## 6. Context Rules (normative)

| Rule | Text |
|------|------|
| **C-1** | `context_heading` is the text of the nearest Markdown heading (line beginning with `#`, `##`, `###`, …) **above** the opening fence. If no such heading exists in the file, the value MUST be `null`. |
| **C-2** | `prologue` is the sequence of non-blank lines above the opening fence, up to (but not including) the first blank line or Markdown section heading, capped at `--context-depth`. |
| **C-3** | `epilogue` is the sequence of non-blank lines below the closing fence, up to (but not including) the first blank line or Markdown section heading, capped at `--context-depth`. |
| **C-4** | If `--context-only-headings` is set, `prologue` and `epilogue` MUST include only the nearest heading line and MUST be empty if no such heading exists. |

## 7. Error Messages (normative)

The script MUST write all diagnostic messages to stderr (never stdout). Exact strings below are consumed by contract tests and MUST match verbatim.

| Exit Code | Situation | Message (stderr) |
|-----------|-----------|------------------|
| 1 | Unknown option `--foo` | `search-todo: error: unknown option --foo` |
| 1 | `--exclude` without value | `search-todo: error: --exclude requires a value` |
| 1 | `--root` without value | `search-todo: error: --root requires a value` |
| 1 | `--context-depth` without value | `search-todo: error: --context-depth requires a value` |
| 1 | `--context-depth` non-integer | `search-todo: error: --context-depth must be an integer` |
| 1 | `--context-depth` negative | `search-todo: error: --context-depth must be >= 0` |
| 2 | No root resolvable | `search-todo: error: cannot determine repository root` |
| 3 | Root unreadable | `search-todo: error: cannot read repository root: <path>` |
| 0 | Warning: encoding skipped | `search-todo: warning: excluded file (encoding_error): <path>` |
| 0 | Warning: size skipped | `search-todo: warning: excluded file (too_large): <path>` |
| 0 | Info: scan summary | `search-todo: info: scanned <N> files in <S> seconds` |

All warnings and info messages MUST be written to stderr. Exit code for warnings and info MUST remain 0 unless another error condition applies.

## 8. Examples

### Example 1 — Minimal invocation (default key:value output)

```sh
./search-todo.sh /path/to/workspace
```

Output (stdout):
```
BRANCH:          feature/xyz
REPO_ROOT:       /path/to/workspace
TOTAL_FILES:     18
TOTAL_BLOCKS:    3
MALFORMED:       0
EXCLUDED_FILES:  4
SCANNED_AT:      2026-06-23T10:00:00Z
BLOCK[0]:        docs/auth.md:12:22:heading "Token refresh"
BLOCK[1]:        src/api.py:45:60:heading "Rate limiter"
BLOCK[2]:        tests/integration.rs:88:95:heading null
```

### Example 2 — JSON invocation

```sh
./search-todo.sh --json /path/to/workspace
```

Output (stdout, single-line JSON):
```json
{"repository":"/path/to/workspace","branch":"feature/xyz","scanned_at":"2026-06-23T10:00:00Z","counters":{"total_files_scanned":18,"total_blocks_found":3,"malformed_blocks":0,"excluded_files_count":4},"blocks":[{"block_id":"docs/auth.md:12:0","source_file":"docs/auth.md","opening_line":12,"closing_line":22,"content":"...","context_heading":"Token refresh","prologue":"...","epilogue":"..."}],"malformed":[],"excluded_files":["node_modules/pkg/index.js"]}
```

### Example 3 — Invocation with custom excludes

```sh
./search-todo.sh --exclude "draft/**" --exclude "*.bak" /path/to/workspace
```

Files matching `draft/**` or `*.bak` (in addition to built-in excludes) are recorded in `excluded_files` and MUST NOT be scanned.

### Example 4 — Invocation with `--no-default-excludes`

```sh
./search-todo.sh --no-default-excludes /path/to/workspace
```

All files under `.git/`, `node_modules/`, `.venv/`, etc. are now eligible for scanning. `EXCLUDED_FILES` counter reflects only `--exclude` pattern matches (zero in this example if no `--exclude` flags are passed).

### Example 5 — Malformed block case (stderr warning)

```sh
./search-todo.sh /path/to/workspace
```

Given `src/broken.md` contains an unclosed `SPECKIT TODO` fence at line 99:

stderr:
```
search-todo: info: scanned 22 files in 0.3 seconds
```

stdout:
```
...
MALFORMED[0]:    src/broken.md:99:unclosed_fence
```

JSON mode includes the malformed entry:
```json
{"malformed":[{"source_file":"src/broken.md","opening_line":99,"reason":"unclosed_fence","content_snippet":"...","line_after_eof":true}]}
```

## 9. Traceability Mapping

| Rule | Maps to FR | Maps to SC |
|------|-----------|-----------|
| D-1 | FR-004, FR-006 | SC-001, SC-002 |
| D-2 | FR-004 | SC-001 |
| D-3 | FR-007, FR-012 | SC-004 |
| D-4 | FR-004, FR-007 | SC-001, SC-004 |
| D-5 | FR-003 | SC-002 |
| D-6 | FR-003 | SC-002 |
| D-7 | FR-003 | SC-002 |
| D-8 | FR-004, FR-006 | SC-001, SC-002 |
| C-1 | FR-005 | SC-003 |
| C-2 | FR-005 | SC-003 |
| C-3 | FR-005 | SC-003 |
| C-4 | FR-005 | SC-003 |
| Exit 1 (arg errors) | FR-001 | SC-001 |
| Exit 2 (root undefined) | FR-001 | SC-001 |
| Exit 3 (I/O error) | FR-001, FR-003 | SC-001, SC-002 |
| Warning (encoding_error) | FR-003, FR-007 | SC-002, SC-004 |
| Warning (too_large) | FR-003 | SC-002 |
| Info (scan summary) | FR-012 | SC-001, SC-004 |

## 10. Non-Goals

This contract does **not** cover:

- **Prompt-layer veto**: The safety gate that rejects TODO blocks requesting destructive, secret-exposing, or out-of-scope operations is enforced by the chat prompt (`speckit.todo.prompt.md`), not by `search-todo.sh`.
- **Work-group clustering**: Grouping related TODO blocks into thematic units is performed by the agent consuming the JSON output, not by the scanner.
- **Batching logic**: Splitting TODO groups into sequential execution batches (when valid count > 10) is handled at the prompt/agent layer per FR-013.
- **Auto-execution**: The command presents a reviewable plan and awaits user confirmation; execution orchestration is outside the scanner's scope.
- **Workspace mutation**: The scanner is read-only; it does not modify source files.
- **Multi-workspace scanning**: Only one workspace root is supported per invocation.
- **Live file-system change detection**: The scanner does not snapshot the workspace; if a file changes mid-scan, the result reflects the state at read time.
