# `specify migrate` — Migrate Command

One-shot convergence after `specify install` + `specify init`: compares a workspace against the assets of the currently installed CLI, reports every difference (dry-run, the default), and with `--apply` converges the workspace — obsolete residue is archived (recoverable), missing assets are written, edited framework files are replaced with the old content archived first, and anchor-layout drift is relocated or merged. Every destructive step is archive-first and recorded in the run receipt, so `--apply` is the single write authorization and executes in both interactive and non-interactive environments. The command performs neither install nor init.

## Execution Flow

```text
specify migrate [--dry-run | --apply] [--workspace PATH] [--format text|json]
```

1. **Precondition** — `<workspace>/.specify/` must exist. When it is missing, the command names `specify init` as the repair entry, exits 2, and creates or modifies nothing.
2. **Plan** — the planner compares five dimensions against the reference tree built from the installed CLI's own assets: `templates-generated`, `anchor-layout`, `compat-links`, `mirror-consistency`, `migration-residue`. Each item carries current state, expected state, the intended disposition and its evidence path.
3. **Dry-run (default)** — prints the plan and exits with the outcome mapping below; zero writes to the workspace tree.
4. **Apply (`--apply`)** — enters write mode (the single authorization). Every destructive item is archive-first: the original is copied into the run's archive root before the target changes. These actions are therefore reversible and execute automatically in both interactive and non-interactive environments; no second confirmation is requested and no confirmation flag exists.
5. **Receipt** — an apply run writes `.specify/memory/migrate/receipts/<run-id>.json` and archives every replaced, merged or removed object under `.specify/archive/migrate/<run-id>/`.

## Options

| Option | Value | Default | Meaning |
|--------|-------|---------|---------|
| `--dry-run` | flag | **default** | Plan only; the explicit form exists for scripts |
| `--apply` | flag | off | Enter write mode (single authorization); archive-first items execute automatically and are recoverable from the receipt; mutually exclusive with `--dry-run` |
| `--workspace` | PATH | `.` | Target workspace root; must already contain `.specify/` |
| `--format` | `text` \| `json` | `text` | `json` emits the machine-readable envelope (`planVersion`, `mode`, `workspaceKind`, `outcome`, `exitCode`, `items`, `summary`, `notes`, `pointers`, `receipt`, `receiptPath`) |
| `--help` | flag | — | Zero-side-effect answer declaring the outcomes and exit codes |

There is no confirmation-class flag (`--yes`, `--force`, `--non-interactive`, `--confirm`); undeclared options are rejected with exit 2. `--apply` itself is the authorization, and the archive-first receipt is the recovery contract.

## Outcomes and Exit Codes

| outcome | condition | exit |
|---------|-----------|------|
| `clean` | the plan is empty (dry-run or apply) | 0 |
| `planned` | dry-run found differences | 1 |
| `applied` | apply completed with nothing refused / blocked / failed | 0 |
| `blocked` | refused / blocked / failed items remain after apply (e.g. an unmergeable structural conflict or an execution I/O failure) | 3 |

Input and precondition errors (`--apply --dry-run` together, an undeclared option, a missing `.specify/`) exit 2 with a stderr message and no outcome envelope; `error` is not an outcome token.

## Receipts and Archives

| Path | Content |
|------|---------|
| `.specify/memory/migrate/receipts/<run-id>.json` | one file per apply run: volatile fields (`runId`, `startedAt`, `finishedAt`, workspace path), per-item `disposition` / `status`, `archives[]` (with `change` and `digest`), `recover`, plus record-only source/target version fields |
| `.specify/archive/migrate/<run-id>/<rel>` | every replaced or removed object, preserving its workspace-relative layout |

Archive-not-delete: the original object is copied into the run's archive before any new content lands, and the legacy copy is removed only after its archive copy is verified, so every destructive step is recoverable. Recovery follows the receipt's `recover` field. An interrupted apply leaves a `status=running` receipt; the next run reports the interrupted stage and continues from that receipt's own archive records without moving the same object twice. A dry-run writes no receipt file — its receipt body travels in the stdout envelope only.

## Anchor merge

The `anchor-layout` dimension compares the legacy anchors (`.specify/memory/{features,constitution,glossary,register,tools}.md`) with their current location (`.specify/<anchor>.md`) and never silently picks a winner:

| Situation | Action |
|-----------|--------|
| only the legacy anchor exists | relocate it, archive-first |
| the current location holds the packaged placeholder | archive the placeholder and install the legacy real content |
| only the legacy anchor is a placeholder | archive the legacy placeholder; the current file stays |
| both sides are byte-identical | archive the legacy duplicate |
| both sides hold real content | merge: `features.md` unions table rows by feature ID with the current row winning on duplicates and legacy-only rows appended; other anchors keep the current file and append the legacy content under a fixed merge marker |
| a non-file target (broken link, populated directory) or unreadable content | refuse, name both candidates, keep both |

Every merged anchor archives both originals under `.specify/archive/migrate/<run-id>/anchor-layout/` and records the result digest in the receipt. The merge marker is deterministic (no timestamp or run id); a second run is clean. Reconcile a merged constitution or registry with its owner command (`/speckit.constitution`, `/speckit.feature`) after the run.

## Boundaries

- **`specify init`** — this command is the one-shot closeout after `specify install` + `specify init`; it performs neither install nor init. A missing `.specify/` is repaired by `specify init`, never by this command.
- **`/speckit.sanitize`** — the sanitize Migration wrap-up lane remains the periodic recheck fallback; `specify migrate` is the one-shot closeout main entry, and the lane's checkers and dispositions are unchanged.
- **goal/team definitions** — archive migration stays with `/speckit.goal` (`migrate-archive`); `specify migrate` only emits a static pointer and never touches those archives.
- **agent sessions** — `/speckit.migrate` runs exactly the commands this page documents (`specify migrate` dry-run first, then `specify migrate --apply` automatically because every destructive step is archive-first and receipt-recoverable); the template carries no second plan or check implementation and no confirmation flag.

## See Also

- [Sanitize Command](sanitize.md) — periodic recheck lane behind the one-shot closeout
- [Installation](../../tutorials/installation.md) — `specify install` and `specify init`, the two steps this command follows
