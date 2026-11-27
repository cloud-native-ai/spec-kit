# Pre-Change Measurements — 110-context-management

**Purpose**: the pre-change side of every diff premise for this feature (T003). Every row records its command, its real output and the capture date. Captured at implement entry, worktree `.specify/.tmp/sdd-loop/worktrees/context-management`, branch `110-context-management`, HEAD `2cbbb3c8a`, 2026-11-27, before any edit of this package.

Machine-readable protocol baseline is delimited by the `protocol-baseline` comment markers below; `tests/contract/test_context_management_owner.py` parses that block and compares it with the super↔sub protocol owner and with the owner document's dispatch-mapping statement.

## 1. Live instructions size, section counts and the generator budget constant

Command:

```bash
wc -c < .specify/instructions.md
grep -c '^## ' .specify/templates/instructions-template.md
grep -c '^## ' .specify/instructions.md
grep -n 'INSTRUCTIONS_BUDGET_BYTES' scripts/bash/generate-instructions.sh
```

Real output (2026-11-27):

```
40170
39
40
119:INSTRUCTIONS_BUDGET_BYTES=40960
```

Headroom: `40960 - 1 - 40170 = 789 B`. The generator's `BUDGET:` line is the only size judge (owner: `scripts/bash/generate-instructions.sh`); the template carries 39 `##` sections and the live file 40 (the live-only `## Recurring Operational Lessons` section is pre-existing drift the additive reconcile preserves).

## 2. Mirror baseline

Command:

```bash
python3 scripts/python/sync-mirrors.py --check
```

Real output (2026-11-27, exit status `0`):

```
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (439 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok    scripts/ == .specify/scripts/ (133 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (117 files, byte-identical)
```

The implement-time criterion is **no NEW drift** against this baseline (never a pre-written absolute exit code).

## 3. Super↔sub protocol declared item set (protected surface)

Command:

```bash
/usr/local/bin/python3 - <<'PY'
import re
from pathlib import Path
text = Path("shared/definitions/superagent-definitions.md").read_text(encoding="utf-8")
m = re.search(r"seven role fields in its existing payload channel: ((?:`[a-z_]+`(?:,\s*)?)+)\.", text)
print("role_fields:", ", ".join(re.findall(r"`([a-z_]+)`", m.group(1))))
inj = re.search(r"The four pre-existing injections keep their owners and travel by pointer: (.*?)\.\s", text, re.S)
items = re.findall(r"(?:^|,\s*(?:and\s+)?|\s+and\s+)(the [a-z][^(),]*?)\s*\(`", inj.group(1))
print("injections:", ", ".join(i[4:] for i in items))
PY
```

Real output (2026-11-27):

```
role_fields: parent_identity, child_label, role_declaration, dispatch_duty, depth_position, authority_ref, return_channel
injections: fast-fail clause, concurrency obligation, reporting duty, re-anchoring anchor digest
```

Machine-readable baseline consumed by the protocol-boundary guard leg:

<!-- protocol-baseline:begin -->
role_fields: parent_identity, child_label, role_declaration, dispatch_duty, depth_position, authority_ref, return_channel
injections: fast-fail clause, concurrency obligation, reporting duty, re-anchoring anchor digest
<!-- protocol-baseline:end -->

Owner read: `shared/definitions/superagent-definitions.md` § The super↔sub Protocol (Downlink).

## 4. Memory recall on the populated stores (protected surface)

Command and real output — session scope (2026-11-27, exit status `0`):

```bash
python3 scripts/python/memory-utils.py --action recall --scope session --query context --format json
```

```json
{
  "count": 5,
  "matches": [
    {
      "id": "20261127T082658Z-run-determination-skill-analyze-artifacts-r20261127t070000z",
      "file": "20261127T082658Z-run-determination-skill-analyze-artifacts-r20261127t070000z.md",
      "scope": "session",
      "source": "skill:analyze-artifacts",
      "feature": "110-context-management",
      "tags": ["run-determination", "r20261127t070000z-110a"],
      "title": "run-determination skill:analyze-artifacts r20261127T070000Z-110a",
      "created": "2026-11-27T08:26:58Z",
      "summary": "skill:analyze-artifacts run=r20261127T070000Z-110a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated",
      "score": 3,
      "path": ".specify/session/20261127T082658Z-run-determination-skill-analyze-artifacts-r20261127t070000z.md"
    },
    {
      "id": "20261127T081302Z-run-determination-skill-create-checklist-r20261127t070000z-1",
      "file": "20261127T081302Z-run-determination-skill-create-checklist-r20261127t070000z-1.md",
      "scope": "session",
      "source": "skill:create-checklist",
      "feature": "110-context-management",
      "tags": ["run-determination", "r20261127t070000z-110a"],
      "title": "run-determination skill:create-checklist r20261127T070000Z-110a",
      "created": "2026-11-27T08:13:02Z",
      "summary": "skill:create-checklist run=r20261127T070000Z-110a token=not_evaluated elapsed=regressed artifact=not_evaluated satisfaction=not_evaluated",
      "score": 3,
      "path": ".specify/session/20261127T081302Z-run-determination-skill-create-checklist-r20261127t070000z-1.md"
    },
    {
      "id": "20261127T080408Z-run-determination-skill-create-tasks-r20261127t070000z-110a",
      "file": "20261127T080408Z-run-determination-skill-create-tasks-r20261127t070000z-110a.md",
      "scope": "session",
      "source": "skill:create-tasks",
      "feature": "110-context-management",
      "tags": ["run-determination", "r20261127t070000z-110a"],
      "title": "run-determination skill:create-tasks r20261127T070000Z-110a",
      "created": "2026-11-27T08:04:08Z",
      "summary": "skill:create-tasks run=r20261127T070000Z-110a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated",
      "score": 3,
      "path": ".specify/session/20261127T080408Z-run-determination-skill-create-tasks-r20261127t070000z-110a.md"
    },
    {
      "id": "20261127T074847Z-run-determination-skill-create-plan-r20261127t070000z-110a",
      "file": "20261127T074847Z-run-determination-skill-create-plan-r20261127t070000z-110a.md",
      "scope": "session",
      "source": "skill:create-plan",
      "feature": "110-context-management",
      "tags": ["run-determination", "r20261127t070000z-110a"],
      "title": "run-determination skill:create-plan r20261127T070000Z-110a",
      "created": "2026-11-27T07:48:47Z",
      "summary": "skill:create-plan run=r20261127T070000Z-110a token=not_evaluated elapsed=not_evaluated artifact=not_evaluated satisfaction=not_evaluated",
      "score": 3,
      "path": ".specify/session/20261127T074847Z-run-determination-skill-create-plan-r20261127t070000z-110a.md"
    },
    {
      "id": "20261127T073329Z-run-determination-skill-clarify-artifact-r20261127t070000z-1",
      "file": "20261127T073329Z-run-determination-skill-clarify-artifact-r20261127t070000z-1.md",
      "scope": "session",
      "source": "skill:clarify-artifact",
      "feature": "110-context-management",
      "tags": ["run-determination", "r20261127t070000z-110a"],
      "title": "run-determination skill:clarify-artifact r20261127T070000Z-110a",
      "created": "2026-11-27T07:33:29Z",
      "summary": "skill:clarify-artifact run=r20261127T070000Z-110a token=not_evaluated elapsed=improved artifact=not_evaluated satisfaction=not_evaluated",
      "score": 3,
      "path": ".specify/session/20261127T073329Z-run-determination-skill-clarify-artifact-r20261127t070000z-1.md"
    }
  ]
}
```

Command and real output — knowledge scope (2026-11-27, exit status `0`):

```bash
python3 scripts/python/memory-utils.py --action recall --scope knowledge --query context --format json
```

```json
{
  "count": 0,
  "matches": []
}
```

Comparison note for the protected-surface leg: the session store is this line's own run-determination records and may legitimately grow as this line runs; the comparison at US5 re-runs the same two commands and compares the knowledge-scope reading verbatim plus the session-scope readings present at implement entry.

## 5. Rendered-agent fixture output (protected surface)

Command (renders the repository's own `agents/` definitions through the standing render path into a temporary project; the digest covers every rendered `*.agent.md` in name order — `name NUL bytes`):

```bash
PYTHONPATH=src /usr/local/bin/python3 - <<'PY'
import hashlib, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, "src")
import specify_cli
repo = Path.cwd()
with tempfile.TemporaryDirectory(dir=".specify/.tmp") as td:
    proj = Path(td) / "proj"
    shutil.copytree(repo / "agents", proj / ".specify" / "agents" / "templates")
    (proj / ".specify" / "agents" / "execution" / "logs").mkdir(parents=True)
    stats = specify_cli.render_agents_for_tool(proj, "qoder")
    out = sorted((proj / ".qoder" / "agents").glob("*.agent.md"))
    digest = hashlib.sha256()
    for p in out:
        digest.update(p.name.encode("utf-8") + b"\0")
        digest.update(p.read_bytes())
    print("rendered:", stats["rendered"], "files:", len(out), "backups:", len(stats["backups"]))
    print("sha256-tree:", digest.hexdigest())
PY
```

Real output (2026-11-27, twice in a row — byte-identical both runs):

```
rendered: 20 files: 20 backups: 0
sha256-tree: ff7aab2e4c0a3b2ea59f9d0da2f7bc1045906e3932080c744b4e865b6ab98d30
```

## 6. FR / SC / clause counts, with trap forms

Commands and real output (2026-11-27):

```bash
grep -cE '^- \*\*FR-[0-9]+\*\*:' .specify/specs/110-context-management/requirements.md   # → 29
grep -cE '^- \*\*SC-[0-9]+\*\*:' .specify/specs/110-context-management/requirements.md   # → 11
grep -cE '^## C-[0-9]+' .specify/specs/110-context-management/contracts/*.md            # → 7 / 8 / 7 / 10 / 7, TOTAL=39
grep -ohE '\bC-[0-9]+\b' .specify/specs/110-context-management/contracts/*.md | wc -l   # trap form
```

Real output:

```
[FR] 29
[SC] 11
[CLAUSE-DEFS]
declarations-and-domains.contract.md:7
engine-and-distribution.contract.md:8
guards-and-boundaries.contract.md:7
matrix-and-triggers.contract.md:10
owner-and-layout.contract.md:7
TOTAL=39
[TRAP] 65
```

**Measured-premise drift disclosed (attributed)**: `tasks.md` § Measured Premises records the trap form as **54** at generation time (HEAD `ae9922ca8`). The implement-entry re-measurement reads **65**; `git grep` over the same command at `ae9922ca8` → 54, at `badc0e149` (the analyze AN-01/AN-04 repair) → 65, at `2cbbb3c8a` → 65. Attribution: **upstream repair** (the analyze-stage repair commit added in-body `C-*` cross-references). The authoritative unit — the `## C-NNN` definition heading — is unchanged at **39**; no acceptance criterion moves.

## 7. Absence checks for the twelve new artifacts (red-first prerequisite)

Command and real output (2026-11-27, before any edit of this package):

```bash
for p in shared/definitions/context-management-definitions.md \
         shared/declarations/facts/context-categories.yaml \
         shared/declarations/facts/context-layers.yaml \
         shared/declarations/facts/context-forms.yaml \
         shared/declarations/facts/context-classes.yaml \
         scripts/python/context-audit.py \
         tests/contract/test_context_management_owner.py \
         tests/contract/test_context_management_declarations.py \
         tests/contract/test_context_management_engine.py \
         tests/contract/test_context_management_readonly.py \
         tests/integration/test_context_management_init.py \
         tests/fixtures/context-management; do
  if test -e "$p"; then echo "present $p"; else echo "ABSENT  $p"; fi
done
```

Real output:

```
ABSENT  shared/definitions/context-management-definitions.md
ABSENT  shared/declarations/facts/context-categories.yaml
ABSENT  shared/declarations/facts/context-layers.yaml
ABSENT  shared/declarations/facts/context-forms.yaml
ABSENT  shared/declarations/facts/context-classes.yaml
ABSENT  scripts/python/context-audit.py
ABSENT  tests/contract/test_context_management_owner.py
ABSENT  tests/contract/test_context_management_declarations.py
ABSENT  tests/contract/test_context_management_engine.py
ABSENT  tests/contract/test_context_management_readonly.py
ABSENT  tests/integration/test_context_management_init.py
ABSENT  tests/fixtures/context-management
```

**12/12 ABSENT** at capture time. The two guard files and the fixture directory listed above are created by this package after this capture; the owner document, the four facts and the engine stay absent until their own implementation rows.