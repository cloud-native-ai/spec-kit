# `/speckit.feedback` — Feedback Command

Single entry point for every operation on the local feedback store (`.specify/memory/feedback/`) and the probe truth source (`.specify/shared/definitions/probe-definitions.md`). The command does not ask the caller to pick a mode by keyword: it reads the store, judges **where each item points**, and routes itself to one of **two execution paths**. An explicit `package` request short-circuits to Path B; probe injection stays an explicitly-requested capability because a target unit id cannot be inferred from repo state.

The discriminator is the stored `kind` field, which the engine resolves from the probe registry at record time and already enforces at three layers: `kind: external` (recorded against a `custom:<owner>/<name>` unit, `slice: host-custom`) points at this project and is excluded from upstream packages by contract; `kind: internal` points at the framework upstream. Content analysis may refine an `internal` entry toward this project, but never an `external` entry toward upstream — the engine's report validation rejects that outright.

```text
/speckit.feedback                    # judge and route
/speckit.feedback package            # go straight to Path B
```

## Routing

| Feedback points at | Path | What happens |
|---|---|---|
| **This project** — `kind: external` entries, plus inbound bundles in the `feedback/` intake directory when this repo is the framework source | **Path A — digest in place** | inventory → introspection → route to this project's own improvement channels → dispose → cleanup |
| **The framework upstream** (normally Spec Kit itself) — `kind: internal` | **Path B — package for manual delivery** | status → package → print the zip and the delivery guidance → `mark-submitted` → post-package cleanup |
| Injecting a probe for a custom unit | *(outside the automatic router)* | see [Probe Injection](#probe-injection-explicit-request-only) |

Both sides non-empty → Path A runs first, then Path B, in the same session. Nothing in scope → the empty inventory is reported and the run ends normally without writing a report file.

The **inventory** step is where the old probe overview lives — a step the judgment needs, not a destination of its own. It prints every probe placed in the current project as a vertical tree: kind (internal/external) → class (target slice, collection, processing) → objects (unit @ lifecycle point), rendered from the merged truth source and never a hand-maintained list.

```bash
python3 .specify/scripts/python/feedback-utils.py --action probes           # tree (text)
python3 .specify/scripts/python/feedback-utils.py --action probes --format json
python3 .specify/scripts/python/feedback-utils.py --action probes --validate    # schema
python3 .specify/scripts/python/feedback-utils.py --action probes --reconcile   # objects↔embeds audit
python3 .specify/scripts/python/feedback-utils.py --action map              # rebuild probe-map.md
python3 .specify/scripts/python/feedback-utils.py --action status
python3 .specify/scripts/python/feedback-utils.py --action list --disposition open --format json
```

## Path A — Digest In This Project

**A1 Intake** (framework hat only — `templates/` + `skills/` + `src/specify_cli/` at root; the gate scopes this sub-step, never the whole path): enumerate `feedback/feedback-*.zip`, process ALL bundles as ONE consolidated batch, and cross-check every filename against `consume-log.md` so a re-delivered copy is named as such instead of being re-routed. A client project skips A1/A2 and starts at A3.

**A2 Read**: small batches inline via `unzip -p`; larger batches extract to a temp dir and dispatch balanced parallel read-only verifiers returning a compact verdict table. Bundle identity comes from the MANIFEST (`Install source`, `Generated`, entry-file set), which catches a re-delivery the filename check cannot.

**A3 Introspection(自省)** — scenario-grounded deep processing, five steps: (1) 范围快照 via `list --disposition open --format json` (summary-first; narrow with `--slice/--kind/--since`); (2) 场景化分析 — agent-side verification of each entry against the live scenario (unit source, referenced files) with a verdict per entry, clustering same-root-cause entries into findings of five elements (statement / root cause / evidence anchors / routing decision / optimization proposal); (3) 报告产出 — draft persisted to `.specify/memory/feedback/introspection/<report-id>.md`, validated and linked via `introspect-register`; (4) 用户确认 — per-finding routing overrides are recorded, then `introspect-register --confirm` applies the report's `建议处置` rows as batch dispositions; (5) 路由建议 — advisory only, nothing auto-applied or auto-transmitted.

```bash
python3 .specify/scripts/python/feedback-utils.py --action introspect-register --report-file <path>
python3 .specify/scripts/python/feedback-utils.py --action introspect-register --report-file <path> --confirm
```

Reports live under `introspection/` (never the store root — `reindex` globs root `*.md`); lifecycle `draft → confirmed → superseded`, superseded reports retained. Findings with `external` members are always `local-sink` — never upstream-bound, and the engine enforces it.

**A4 Route** each finding to the channel that owns it: direct fix, `/speckit.requirements`, `improve-skills` / `improve-agent` / `improve-team`, `improve-tools`, `improve-docs`, or acknowledge-only.

**A5 Cleanup** (mandatory closing step): the user confirms the routing decisions in the digest report, then the processed bundles are removed — named marks never a silent uniform delete, orphans copied to a preserve path first, and one row appended to `consume-log.md` (`| Date | Bundles | Entries | Findings Routed | Conflicts | Cleanup |`). The `feedback/` directory itself remains as the permanent intake point.

**A6 Dispose** local entries:

```bash
python3 .specify/scripts/python/feedback-utils.py --action dispose --id <entry-id> --to processed \
  [--reason "<provenance text>"] [--ref "introspection-<ts>#F-<nn>"]
```

## Path B — Package For The Framework Upstream

Status → summary → dispose → package → post-package cleanup → `mark-submitted`:

```bash
python3 .specify/scripts/python/feedback-utils.py --action status
python3 .specify/scripts/python/feedback-utils.py --action list --limit 0 --slice commands
python3 .specify/scripts/python/feedback-utils.py --action list --limit 0 --kind internal
python3 .specify/scripts/python/feedback-utils.py --action dispose --id <entry-id> --to processed
python3 .specify/scripts/python/feedback-utils.py --action package [--include-introspection]
python3 .specify/scripts/python/feedback-utils.py --action cleanup --package latest --dry-run
python3 .specify/scripts/python/feedback-utils.py --action cleanup --package latest
python3 .specify/scripts/python/feedback-utils.py --action mark-submitted
```

Filters: `--slice`, `--kind <internal|external>`, `--disposition <processed|ignored|open>`, plus `--unit-id/--since/--contains`. `list --format json` emits `{"count": N, "matches": [...]}`, not a bare array. Cleanup removes only entries actually inside the named zip and logs every removal to `cleanup-log.md`; the zip remains the archive of record. **The agent never sends the zip** — zero automated transmission; delivery is manual. When the batch contains entries carrying an `introspection_ref`, the flow offers `--include-introspection` by default so the covering reports ride along under `introspection/` with a `## Introspection Reports` MANIFEST section; declining never blocks packaging. `external` entries are excluded by the engine and reported only as an `excluded_external` count — they belong to Path A.

Running Path A's introspection before packaging is advised, not required: skipping it affects nothing downstream.

## Probe Injection (explicit request only)

For client-project custom Skills/Agents/Commands (framework probes never cover them). Outside the automatic router because the target unit id cannot be inferred:

```bash
python3 .specify/scripts/python/feedback-utils.py --action probe-inject \
  --unit custom:myteam/deploy-skill --notes-file notes.md
```

Writes `.specify/memory/feedback/probes/ext-<slug>.md` (`ext-` prefix enforces the internal/external namespace split); verify via `--action probes` and `--action map`. External feedback is client-project-local (Dogfooding Loop B): filter it via `list --kind external`, use it to optimize your own custom units, and it is **never** included in upstream packages.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | success |
| 2 | validation verdict (unknown unit/probe, schema violation, reconcile gap, bad disposition, missing package) |
| 3 | IO/storage error |

## See Also

- Mechanism reference: [Feedback System](../skills/feedback.md)
- Probe registry contract: `.specify/specs/041-refactor-feedback-probe/contracts/probe-registry.md`
- Introspection contracts: `.specify/specs/047-feedback-introspection/contracts/`(introspection-report / engine-cli / command-mode — the last of these is a dated record of the five-mode design this command replaced)
