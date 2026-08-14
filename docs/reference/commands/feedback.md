# `/speckit.feedback` — Feedback Command

Local management interface for the Feedback Probe system: three execution modes over the local store (`.specify/memory/feedback/`) and the probe truth source (`.specify/shared/definitions/probe-definitions.md`).

## Mode 1 — Probe Overview (default; no arguments)

```text
/speckit.feedback
```

Prints **every probe placed in the current project** as a vertical tree: kind (internal/external) → class (target slice, collection, processing) → objects (unit @ lifecycle point). Rendered from the merged truth source — framework Classes/Objects plus the project's injected external probes — never a hand-maintained list. Backing engine calls:

```bash
python3 .specify/scripts/python/feedback-utils.py --action probes           # tree (text)
python3 .specify/scripts/python/feedback-utils.py --action probes --format json
python3 .specify/scripts/python/feedback-utils.py --action probes --validate    # schema
python3 .specify/scripts/python/feedback-utils.py --action probes --reconcile   # 50↔embeds audit
python3 .specify/scripts/python/feedback-utils.py --action map              # rebuild probe-map.md
```

## Mode 2 — Process Collected Feedback

View → filter → dispose → package → post-package cleanup:

```bash
python3 .specify/scripts/python/feedback-utils.py --action status
python3 .specify/scripts/python/feedback-utils.py --action list --limit 0 --slice commands
python3 .specify/scripts/python/feedback-utils.py --action list --limit 0 --kind external
python3 .specify/scripts/python/feedback-utils.py --action dispose --id <entry-id> --to processed
python3 .specify/scripts/python/feedback-utils.py --action package
python3 .specify/scripts/python/feedback-utils.py --action cleanup --package latest --dry-run
python3 .specify/scripts/python/feedback-utils.py --action cleanup --package latest
```

Filters: `--slice`, `--kind <internal|external>`, `--disposition <processed|ignored|open>`, plus `--unit-id/--since/--contains`. Cleanup removes only entries actually inside the named zip and logs every removal to `cleanup-log.md`; the zip remains the archive of record. The agent never sends the zip (zero automated transmission).

## Mode 3 — Inject an External Probe

For host-project custom Skills/Agents/Commands (framework probes never cover them):

```bash
python3 .specify/scripts/python/feedback-utils.py --action probe-inject \
  --unit custom:myteam/deploy-skill --notes-file notes.md
```

Writes `.specify/memory/feedback/probes/ext-<slug>.md` (`ext-` prefix enforces the internal/external namespace split). External feedback is host-project-local (Dogfooding Loop B): filter it via `list --kind external`, use it to optimize your own custom units, and it is **never** included in upstream packages.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | success |
| 2 | validation verdict (unknown unit/probe, schema violation, reconcile gap, bad disposition, missing package) |
| 3 | IO/storage error |

## See Also

- Mechanism reference: [Feedback System](../skills/feedback.md)
- Probe registry contract: `.specify/specs/041-refactor-feedback-probe/contracts/probe-registry.md`
