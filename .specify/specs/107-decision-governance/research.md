# Phase 0 Research — 107-decision-governance

**Stage**: plan · **Measured at**: worktree `decision-governance`, HEAD `08b59695c` (`107-decision-governance`), 2026-11-25.
**Method**: every count and carrier fact below was measured by the command shown; nothing is inherited from the requirements stage's baseline except where explicitly marked as the spec's own dated measurement.

## Baseline measurements (taken before any plan write)

| # | Fact | Command | Reading |
|---|------|---------|---------|
| M-1 | No general decision owner exists | `ls shared/definitions/decision-definitions.md .specify/shared/definitions/decision-definitions.md` | both absent (exit 2) — the owner page is a genuine new concept (A-2 holds) |
| M-2 | Instruction template has no Decision section and no production rules | `grep -n "^## " templates/instructions-template.md` | 38 top-level sections; none names decisions; no full-name / same-name / region-id rule text |
| M-3 | Instructions budget headroom | `wc -c .specify/instructions.md`; `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` | live 38,894 B; budget `38,912`; generator reports `over` at `size >= budget` (`scripts/bash/generate-instructions.sh:160-167`) → **17 admissible bytes remain**, so any new section requires a recorded budget ruling |
| M-4 | Instruction generation reconciles whole sections | `.specify/constitution.md` Sync Impact Report (1.13.0) follow-up (b); `scripts/bash/generate-instructions.sh` | a bullet added inside an existing section never reaches already-initialized projects; a whole new section does → the section must be **whole**, not bullets in an existing section |
| M-5 | Mirror pairs | `grep -n "MIRROR_PAIRS" -A 7 scripts/python/sync-mirrors.py` | `templates→.specify/templates` (excl. `commands`), `skills/external→.specify/skills`, `skills/internal→.specify/skills/internal`, `agents→.specify/agents/templates`, `scripts→.specify/scripts` (strict extras), `shared→.specify/shared`; the templates-commands runtime mirror is retired (absent by design) |
| M-6 | Mirror baseline | `python3 scripts/python/sync-mirrors.py --check` | rc 0; 6 pairs ok; zero DIFF (baseline saved at `test-evidence/sync-mirrors-baseline.txt`) |
| M-7 | Command-copy baseline | `python3 scripts/python/regen-command-copies.py --check` | rc 0 — no command template changes are planned, so this stays green (`test-evidence/regen-copies-baseline.txt`) |
| M-8 | Gate-scanner baseline | `python3 scripts/python/scan-confirmation-gates.py` | 31 blocking gates (23 destructive / 7 governance-kept / 1 reversible), 0 violations; scan dirs are `templates/commands`, `skills`, `shared`, `templates/*.md` — the new owner page under `shared/definitions/` **is scanned**, so its wording must stay gate-neutral (`test-evidence/scan-confirmation-gates-baseline.txt`) |
| M-9 | Legacy corpus, current base | `grep -n '^### T-[0-9]{3}' .specify/specs/*/plan.md | wc -l`; checkpoints; run reports; `grep` of register `D-…`/`T-…` rows | 101 `T-NNN` record headings; 127 checkpoint files; 43 `*-report.md` run reports; register carries `D1–D9`, `D-A`, `D-B`, `D-001`, `D-001-a`, `D-1 (092)`–`D-9 (092)`, `D-098-01`, `D-102-01` and `T-001`…`T-018` |
| M-10 | Legacy `D-` headings never use the new form | `grep -rn '^### D-' .specify/specs --include='*.md'` (39 hits: one/two-digit forms only); `grep -rnE '^### D-[0-9]{3}' …` (0 hits) | 39 pre-existing `D-…` headings, **zero** three-digit `D-\d{3}` record-form headings → a safe legacy discriminator: only `^### D-\d{3}` with the record field grammar is new-form; everything else is `legacy` |
| M-11 | Tension ids are plan-local, register-global | `decision-tension.md` § 记录形态 (unique per plan); register rows `T-013`…`T-018` map plan-local ids to global entries | this plan uses `T-001`…`T-003` locally and registers them as the next global entries `T-019`…`T-021` |
| M-12 | Test stack | `pyproject.toml` (`requires-python`, pytest); `scripts/bash/run-tests.sh` (`SPECKIT_PYTHON` ladder) | Python ≥3.8, stdlib-only new checker; pytest through the single entry |
| M-13 | Migrate surface | `templates/commands/migrate.md`; `src/specify_cli/` migrate planner; tests `test_migrate_*` | `/speckit.migrate` is a thin projection over `specify migrate`; its plan dimensions are a closed set (`templates-generated`, `anchor-layout`, `compat-links`, `mirror-consistency`, `migration-residue`, `store-layout`) — this feature adds **no seventh dimension**; BC rows map to existing-dimension behavior or to a deterministic no-transform/refusal pinned by tests |
| M-14 | Carry-over protocol shape | `shared/definitions/superagent-definitions.md` § The super↔sub Protocol | seven role fields + four injections downlink; five-item uplink; the decision block is additive task-authority content, not an eighth role field (A-7 holds by reading) |
| M-15 | Adoption of section-budget precedent | `tests/contract/test_instructions_budget_superagent_section.py` | a section-level cap is declared in the template (`**本节字节上限：600` precedent: 2,000 B at the SDD-routing section) and the total budget constant is derived from the script — never pinned twice |
| M-16 | Register is hand-maintained | `AGENTS.md` § ID Register; `.specify/register.md` | new `D-NNN`/`T-NNN` rows are authored by hand; duplicate collision repair is `/speckit.sanitize --lane renumber` |

## Resolved design points

### R-1 — Owner-page section plan (`shared/definitions/decision-definitions.md`, new)

Sections: (1) Ownership declaration + pointer duty; (2) closed vocabulary; (3) decision classes by holder and per-class presentation templates; (4) decision text contract (full name, `same_name_conflict`, `resource_locator`, per-class emphasis); (5) option-set contract (closed set, five elements, `other` + path, `forced`); (6) decision record (serialization grammar, mandatory field set, conditional fields, four timestamps, supersession, id); (7) archive-as-projection and the normative Decision Producer Inventory; (8) transmission and implementation (decision block, acknowledgement, `implementation_receipt`, audit chain, silent re-decision prohibition); (9) machine/behavior enforcement boundary (M/B tables); (10) legacy and migration rules; (11) field→owner mapping and pointer obligations. The page states up front what it owns; the requirements spec's inventory (§ Decision Producer Inventory) is the dated requirements-stage declaration, and the page becomes the normative home after landing (single owner; the spec copy is a dated record).

### R-2 — Record serialization grammar (feeds T-002)

A record is carried by a level-3 heading `### D-NNN — <one-line title>`; the id appears once (heading). Fields are single lines `- **<field>**: <value>` with **lowercase, unquoted, un-spaced** labels — the proven line grammar of `decision-tension.md` that `validate-decision-tensions.py` already parses. Option entries are indented `- <label> | consequences: … | reversibility: … | default: yes|no | evidence: …` sub-lines under the `options` field; an `other` option carries an indented `path:` sub-line. Mandatory fields are FR-014's ten; conditional fields are `same_name_conflict` + `resource_locator` (required when true) and `superseded_by` (required when superseded). Four timestamps: `created_at` (ISO-8601 Z, mandatory value), `dispatched_at` / `acknowledged_at` / `implemented_at` (ISO-8601 Z or the literal `not-yet`; presence is mandatory). `transmission_status` closed domain: `not-transmitted` / `dispatched` / `acknowledged` / `implemented` / `diverged` / `blocked` — the implementation-result dimension rides this field (clarify ruling 2026-11-25), not an eleventh field.

Legacy discriminator: only `^### D-\d{3}` headings carrying the field grammar are new-form records; pre-existing `### D-…` headings in non-`D-NNN` forms (39 measured) and register rows in non-`D-NNN` forms are `legacy` — readable, never rewritten, never judged (A-10, M-10).

### R-3 — Checker engine (feeds T-003)

One new read-only engine `scripts/python/validate-decisions.py` (stdlib, Python ≥3.8, `--help`/`--version`, undeclared options rejected, exit 0/1/2) with three actions:
- `--action records` (default): scan a spec dir's formal carriers (`requirements.md`, `plan.md`, `checkpoints/*.md`, `research.md`, `feature-ref.md`, `contracts/*`) plus `--carrier PATH` for run reports; judge M-01, M-02, M-03, M-04, M-08.
- `--action payload`: judge M-06 on a dispatch-payload fixture; `--action chain`: judge M-05 + M-07 on record+dispatch+receipt fixtures.
- `--action inventory`: compare the declared producer set (owner page table) with a code-face scan output supplied by the caller (SC-001 observation set); emit `observed == declared ± exempt` verdict.
`scan-confirmation-gates.py` gains no change; zero new gate hits is a measured acceptance.

### R-4 — Instruction section and budget (feeds T-001)

New whole section `## Decision Items（决策项）` after `## ID Register (编号登记)`, pointer-form: two production rules as the minimum bar, one line per class emphasis, owner-page pointer, and the literal `**本节字节上限：1,500 B**` (A-13). Total budget ruling: `INSTRUCTIONS_BUDGET_BYTES` 38,912 → **40,960** (+2,048), sized as measured live 38,894 + A-13 cap 1,500 + 512 B generation/normalization margin, rounded up to the next 512 boundary; the budget stays a warning surface (`over` at `size >= budget`) and a future section needs its own ruling. The section text must avoid the gate scanner's blocking patterns (M-8).

### R-5 — Payload and uplink additions

Downlink: a named `decision_block` inside the existing payload: `decision_id`, `decision_class`, chosen option full label, implementation constraints, archive pointer. Uplink: `acknowledgement` (returns the `decision_id`) and `implementation_receipt` (`decision_id`, implementation summary, evidence pointers, `divergence: none` or `diverged` + reason). Decision-backed dispatch without a block is refused at payload construction (M-06); a receipt missing an item makes the return incomplete (parent MUST NOT consume — existing rule); `transmission_status` is updated by the receipt. Multi-hop: every hop carries the block; every receipt names the same `decision_id`. Silent re-decision becomes an explicit fast-fail escalation (P-07 pointer).

### R-6 — Landing map and mirrors (two hats)

Framework sources only; mirrors regenerated in the same change. Landing list is closed in plan.md § Project Structure and § Mirror Obligations. `agents/` templates need no edit: the uplink contract addition lands in `superagent-definitions.md`, which every role template already reaches by pointer; no role-template file carries a decision-block literal to update (measured: `grep -l "implementation_receipt" agents/` → none).

### R-7 — Backward-incompatible change inventory (closed)

BC-01…BC-06 (requirements § Landing & Compatibility Inventory candidates) are adopted as the closed list, each with a named behavior and a test: BC-01/05/06 compatibility bridge (no block = legacy; only new blocks judged; only new decisions bound), BC-03 bridge (grouped `D-NNN` register rows; collision via `/speckit.sanitize --lane renumber`), BC-04 existing migrate `templates-generated` dimension re-renders `.specify/instructions.md` (pinned by a `specify migrate --format json` dry-run test asserting the new section's convergence plan and zero rewrite of legacy record bodies), BC-02 bridge for non-decision dispatches + deterministic refusal (`M-06`) for decision-backed dispatches without a block. No new migrate dimension; SC-009's per-row mapping is pinned by `tests/integration/test_decision_governance_migrate_dryrun.py` plus the guard tests.

### R-8 — Evidence and review surfaces

M guards: red-first contract/unit fixtures under `tests/fixtures/decision-governance/` with one reverse sample per M rule (M-01…M-08). B rules: named surfaces in the owner page and in `analyze-artifacts` / `review-feature-quality` / `review-sdd-process` pointer lines; the review stage is the executing surface. Producer-inventory closure (SC-001): the `--action inventory` observation scan is a documented command in the guard test, attached to its output.

## External sources

None. The feature consumes only in-repo owners and contracts; no vendor or API research applies.

## Open questions

None material. Two recorded clarities: (a) FR-014's field closure is the mandatory set; the structured identity fields (`same_name_conflict`, `resource_locator`, `superseded_by`) are conditional fields declared by the owner page and required exactly when their trigger holds — this keeps FR-014 authoritative while making M-02/M-04 decidable; (b) this plan's own load-bearing decisions use the existing `T-NNN` carrier because the `D-NNN` contract binds only records created after landing (A-10) — the plan therefore contains no `D-`-block and is not retroactively judged.
