# Quickstart — 093-concurrency-by-default

**Owner of this page**: routing, not rules. Each scenario names what to run, what a passer sees, and what a
failure means; the normative statements live in `contracts/*` and are reached by clause id.

**Measured premise (2026-11-09, this worktree)**: `declaration_reader.py --action get --fact concurrency-class`
exits **1** with `no declaration for fact 'concurrency-class'`. Everything below that assumes the fact exists is
therefore *red today by construction* — that is the point of S-1 and S-9.

---

## S-0 — Verify the premise before touching anything (run today, passed)

```bash
cd <repo-root>
python3 .specify/scripts/python/declaration_reader.py --action list   # exit 0, JSON with `contract` + `exclusions`
python3 .specify/scripts/python/declaration_reader.py --action get --fact concurrency-class
# → "no declaration for fact 'concurrency-class'", exit 1  ← the unregistered shape (FR-031, C-039)
python3 .specify/scripts/python/sync-mirrors.py --check               # exit 0, zero drift (baseline captured)
```

**Executed**: yes — the `--action list` / `--action get` reading above is the live output of this check in this
worktree, and the mirror baseline is `test-evidence/mirror-baseline-plan.txt`. `--help` on both scripts exits 0
without acting (Constitution XXI).

**A passer sees**: list exit 0; get exit 1 with that exact message; mirrors exit 0 with an empty drift list.

---

## S-1 — The scope closed set is enumerable and complete

```bash
python3 scripts/python/concurrency-check.py classify --repo . --json-out /tmp/classify.json
python3 -c "import json;d=json.load(open('/tmp/classify.json'));print(d['decision']);[print(f['code'],f['subject']) for f in d['findings']]"
```

**A passer sees**: `decision: pass`, zero `uncovered` and zero `ambiguous` findings, and `measured` listing the
member counts per root **as enumerated** (measured 2026-11-09 in this worktree: 38 `skills/internal` dirs /
16 `skills/external` dirs / 29 `templates/commands` stems / 17 `agents/*.agent.md` files / 12 `.specify/teams` slugs /
6 `.specify/anchoring` slugs — the counts move, the *patterns* are the assertion, R-6; the anchoring tree was
`.specify/goal` before the 090 rename merged on 2026-11-09).

**Failure means**: a body was added without a class (add the root, not a whitelist entry, C-005/C-024).

---

## S-2 — Default concurrent, and the reason code is not optional

```bash
python3 scripts/python/concurrency-check.py serial-reason --repo . \
  --record <(printf 'pattern: serial\ncodes:\n  - budget-reserve\nevidence:\n  budget-reserve: "was probably tight"\n') \
  --json-out /tmp/serial.json
```

**A passer sees**: the fixture above **fails** — `form-reason-inconsistent` or an evidence-form finding — because
"was probably tight" is not a before/after slot-and-budget reading (C-029, C-051). A correctly evidenced record
passes; a record with `pattern: serial` and an empty `codes` list fails (C-030).

**Failure means**: either the code set is not closed (C-049) or the evidence check degraded to non-emptiness.

---

## S-3 — `effective` is interval overlap, never a declaration

```bash
python3 scripts/python/concurrency-check.py reading --repo . --record <your-run-record.json> --json-out /tmp/reading.json
```

**A passer sees**: `measured.effective` equal to the **maximum overlap count** of the units' `[dispatched_at,
settled_at]` intervals (C-031). Delete one unit's interval and it reports the literal `not_evaluated` and refuses
to pass (C-032). Supply `requested` + `effective` but no `effective_reason` → `reading-incomplete` (C-033).

---

## S-4 — Per-stage decomposition coverage

```bash
python3 scripts/python/concurrency-check.py coverage --repo . --stage requirements --json-out /tmp/coverage.json
```

**A passer sees**: for a stage with concurrent units, a `covered` decision resolved from
`decomposition-coverage.yaml`; for a stage that stays serial, a **named decision record** — never a silent default
([[STR-007]], C-035). The engine reports the relation it observed between the fact and the three spine keys and
fails on a fourth source (C-036).

---

## S-5 — Dispatch capability, and the 092 reproduction

```bash
python3 -m pytest tests/contract/test_concurrency_reproduction_092.py -q   # red before the repair
python3 scripts/python/concurrency-check.py capability --repo . --json-out /tmp/capability.json
```

**A passer sees**: the reproduction fixture (6 packages, an executor whose `capability-tools` has no dispatch tool,
no declared handoff) is **red before** the fix and green after (SC-005, C-040). The capability action reads the
existing frontmatter key only — introducing a new key is a defect (C-038). With
`coordinator-dispatch-verdict.yaml` absent the engine exits **2** with `owner-unavailable`, never a default (C-039).

---

## S-6 — A real run, honestly reported

```bash
python3 scripts/python/concurrency-check.py reading --repo . --record <the-real-run>.json --json-out /tmp/real.json
# the record is a declaration-layer YAML document (block-subset/v1), not free JSON — the engine parses it through
# the same subset its own facts use, so a run cannot smuggle a shape the declaration layer would reject.
```

**A passer sees**: `effective >= 2` measured on a **non-fixture** run, with per-unit verdicts, the deterministic
integration order and the duration, compared against the serial baseline recorded in `notes/serial-baseline.md` (091's own run record; its task count, agent count and duration are read from that record and are not restated here).
Any quantity the run did not produce is written `not_evaluated`; writing `0` or an estimate is a failure
(SC-006, FR-030).

**This feature's own run does not satisfy S-6** — see `plan.md` § Concurrency plan for this run: the feature's own concurrency mechanism has not landed yet (the declaration facts, the engine, and the FR-035 runner path), so the run declares serial with `mechanism-not-yet-landed` and records SC-006 as `not_evaluated`. A tool set is a per-run probe (RS-005), never a constant; the earlier "no dispatch tool" reason was measured false at analyze 2026-11-09 (F-093-012).

---

## Failure triage

| Symptom | First place to look |
|---|---|
| `classify` reports `ambiguous` | the root's `(root_id, produced_shape)` rule in `concurrency-class.yaml` (C-004) |
| a serial record passes with a `.` as evidence | `concurrency-check.py` evidence dispatch (C-029) |
| `effective` equals the configured value | the reading came from config, not intervals (C-031) |
| a stage silently stays serial | `decomposition-coverage.yaml` + the stage's decision record (C-035) |
| `capability` demands a new frontmatter key | it must not — C-038 |
| mirror drift after an edit | edit `templates/` or the source, never a `.specify/` projection alone (C-088) |
