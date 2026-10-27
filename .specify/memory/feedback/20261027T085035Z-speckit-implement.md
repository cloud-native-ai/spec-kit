---
id: "20261027T085035Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "r20261027T061144z-a3ec"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-27T08:50:35Z"
summary: "implement part 7b on Feature 071: ran quickstart A-H through the installed mirror path and closed the band (221 passed over the six new plus five neighbouring suites, zero failing names, clause covera"
---

## Review
implement part 7b on Feature 071: ran quickstart A-H through the installed mirror path and closed the band (221 passed over the six new plus five neighbouring suites, zero failing names, clause coverage ok at 74 claimed). The scenario band surfaced one integration seam that the six contract groups could not see, because they drive the script with an explicitly supplied range and the documented invocation does not.

## Optimization Points
- The receipt's base is resolved independently of the record header, so the skill's step-4 form \`receipt --review-file <record>\` (and quickstart D/E/F, which copy it) inherits whatever tier resolves without a --spec, while \`start --spec\` wrote the feature-tier base into the same record header: in this repository that means the block would carry base=926836e0 (trunk merge-base) inside a record whose header says base=e57052ef, and here the wider range contains a binary asset so the command exits 2 (C-41) and the whole drill cannot run as written. Two readings exist and nothing recorded chooses between them - the documented invocation should pass the range, or receipt should inherit base/head from the record header - so it is left unresolved; owner candidates are the skill's step-4 line plus quickstart D/E/F, and coverage-receipt.md C-32/C-33 for the inheritance rule if that reading wins; The quickstart's per-scenario premises are repository-shaped: F's \`src/legacy/**\` selector matches nothing in a Python+markdown framework repo, so the literal command returns skipped_files=0 and a pass verdict, which is the opposite of the scenario's stated expectation. A selector that matches real paths demonstrates the intended behaviour, so the defect is in the fixture value, not the mechanism - but a reader who runs the block as written is told the focus path is broken; A per-part evidence convention needs its own completeness check: test-evidence/implement-stage-status.jsonl carries one row per implement part, but part 7a (the pin, the docs rewrite and the mirror close) has no row at all and nothing notices, because no gate reads that file. The convention therefore degrades silently exactly where the audit trail matters most.
