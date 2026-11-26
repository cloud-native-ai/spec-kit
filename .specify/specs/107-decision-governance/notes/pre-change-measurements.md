# Pre-change measurements — 107-decision-governance (implement package P1)

**Captured**: 2026-11-26 (UTC), worktree `.specify/.tmp/sdd-loop/worktrees/decision-governance`, branch `107-decision-governance`, HEAD `0d7519521` (includes the master merge).
**Purpose (T002)**: freeze the pre-change side of every diff premise before any edit in this package, so later stages compare against a dated reading instead of a living one.
**Rule**: every row carries its exact command, the real reading and the capture date. Raw outputs follow the table verbatim.

| # | Premise | Command | Reading @ 2026-11-26 | Matches tasks.md premise? |
|---|---------|---------|----------------------|---------------------------|
| 1 | Live instruction size | `wc -c .specify/instructions.md` | `38894 .specify/instructions.md` | yes (38894) |
| 2 | Instruction budget constant | `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` | `107:INSTRUCTIONS_BUDGET_BYTES=38912` (also referenced at lines 137/160) | yes (line 107, 38912) |
| 3 | Legacy `D-` heading corpus | `grep -rn '^### D-' .specify/specs --include='*.md' \| wc -l` | `39` | yes (39) |
| 4 | Three-digit record form present? | `grep -rnE '^### D-[0-9]{3}' .specify/specs --include='*.md' \| wc -l` | `0` | yes (0 — discriminator safe) |
| 5 | Mirror pair state | `python3 scripts/python/sync-mirrors.py --check` | rc `0`; e.g. `ok shared/ == .specify/shared/ (116 files, byte-identical)`; projected pairs `ok` | yes (rc 0) |
| 6 | Per-tool command copies | `python3 scripts/python/regen-command-copies.py --check` | rc `0`; `OK: all per-tool command copies match the source templates.` | yes (rc 0) |
| 7 | Gate-neutrality baseline | `python3 scripts/python/scan-confirmation-gates.py --summary` | rc `0`; `blocking confirmation gates: 30` / destructive `22` / governance_kept `7` / reversible `1` / violations `0` | **NO — recorded baseline file says 31 (destructive 23)**; see drift note below |
| 8 | Decision-tension validator on this spec | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance` | rc `0`; `status: ok`, all six labels `pass (0)`, `scanned: 217 lines, 3 record(s)`, `0 error(s), 0 warning(s)` | yes (clean) |

## Drift note on row 7 (surfaced, not repaired here)

`test-evidence/scan-confirmation-gates-baseline.txt` (recorded 2026-11-25 at `08b59695c`) carries `blocking confirmation gates: 31` with `destructive: 23`. The current tree reads **30** with `destructive: 22`: one destructive hit disappeared when master (line 106) merged into this branch. The direction that matters for FR-025 / C-405 is *no new hit*; the current reading moves downward, so this package adds no gate. The exact-equality premise carried in `tasks.md` T043 ("31 blocking / 0 violations") is therefore stale by one and is handed to the package that owns T043/T045 for adjudication (re-baseline vs set-comparison); P1 records the real reading and does not edit any baseline file.

## Raw outputs (verbatim)

```text
$ wc -c .specify/instructions.md
38894 .specify/instructions.md
$ grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh
107:INSTRUCTIONS_BUDGET_BYTES=38912
137:    # Report the generated file's size against INSTRUCTIONS_BUDGET_BYTES, plus a
160:      budget_out="$(python3 - "$target" "$rendered" "$INSTRUCTIONS_BUDGET_BYTES" <<'PYEOF'
$ grep -rn '^### D-' .specify/specs --include='*.md' | wc -l
39
$ grep -rnE '^### D-[0-9]{3}' .specify/specs --include='*.md' | wc -l
0
$ grep -rn '^### D-' .specify/specs --include='*.md' | head -3
.specify/specs/100-seal-slice-archive/test-evidence/analyze-merged-2026-11-11.md:115:### D-01 — reject — same
.specify/specs/100-seal-slice-archive/test-evidence/analyze-merged-2026-11-11.md:123:### D-02 — confirm — same
.specify/specs/100-seal-slice-archive/test-evidence/analyze-merged-2026-11-11.md:131:### D-03 — confirm — CRITICAL
$ python3 scripts/python/sync-mirrors.py --check   # rc=0
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (116 files, byte-identical)
$ python3 scripts/python/regen-command-copies.py --check   # rc=0
OK: all per-tool command copies match the source templates.
$ python3 scripts/python/scan-confirmation-gates.py --summary   # rc=0
blocking confirmation gates: 30
  destructive: 22
  governance_kept: 7
  reversible: 1
violations (reversible gates still blocking): 0
$ python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance   # rc=0
spec: .specify/specs/107-decision-governance
status: ok
  [dtr-anchor] pass (0)
  [dtr-section-missing] pass (0)
  [dtr-record-incomplete] pass (0)
  [dtr-tension-id] pass (0)
  [dtr-rejected-form] pass (0)
  [expected-sacrifice-unmapped] pass (0)
scanned: 217 lines, 3 record(s)
channel: value_domain=HIGH-or-0, high=0
0 error(s), 0 warning(s)
```
