<!--
     Fixture case: acceptance-hardening/audit-history — see the per-spec-dir notice in
     .specify/specs/901-audit-blocked/requirements.md for the fixture declaration.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.

     This is the audit-root case 081d's data model assigns: a self-contained audit root — a
     `.specify/features.md` registry plus `.specify/specs/<key>/` directories INSIDE the
     case, each carrying the artifacts its registry row claims. It is the only case shape that can
     exercise `--audit-existing --repo <case>`, because that mode enumerates registry rows across a
     repository root.

     The case carries one `Implemented` feature that would become `Blocked` under the new rules
     (901 — the 026 shape: tasks closed, every `final`-path criterion non-`pass`, no smoke record)
     and one that would not (902 — the complete shape, judged `accept`). No row references a real
     feature directory; every path in this case resolves inside the case itself.

     This directory starts with a dot-prefixed component on purpose: it reproduces the audited
     root's real anatomy (`.specify/features.md`), and it is the shape C-11's zero-write
     assertion is strongest on — an implementation that cached, locked or rewrote anything under
     the root it reads would touch exactly these paths.
-->

# 🌱 Fixture Feature Index (audit-history case)

**Total Features**: 2

## Features

| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |
|----|------|-------------|--------|-----------------|-----------|--------------|
| 901 | Acceptance fixture — audit blocked | Declarative audit subject that would become `Blocked` under the 081 rules. | Implemented | .specify/specs/901-audit-blocked/feature-detail.md | .specify/specs/901-audit-blocked/requirements.md | 2026-11-03 |
| 902 | Acceptance fixture — audit clean | Declarative audit subject whose evidence already satisfies the 081 rules. | Implemented | .specify/specs/902-audit-clean/feature-detail.md | .specify/specs/902-audit-clean/requirements.md | 2026-11-03 |
