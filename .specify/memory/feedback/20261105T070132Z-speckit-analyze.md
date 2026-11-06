---
id: "20261105T070132Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "083-mechanism-policy-separation-analyze2-20261105"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "083-mechanism-policy-separation"
feature_id: "082"
partial: false
created: "2026-11-05T07:01:32Z"
summary: "Analyze round 2 (read-only re-check) on Feature 083 after the repair commit 974db180: both reported HIGH clusters are measurably closed (Decision Tensions validates 0 error/0 HIGH with the section in "
---

## Review
Analyze round 2 (read-only re-check) on Feature 083 after the repair commit 974db180: both reported HIGH clusters are measurably closed (Decision Tensions validates 0 error/0 HIGH with the section in the mandated position and four expected_sacrifice rows each bound to one SC source; coverage-baseline.txt frozen with 513 names and clause-uncovered pass). The re-check did not close the round clean: the repair's own evidence file records a red coverage reading without its rc, validate-requirements still returns rc=1 on SC-005's path marker (left OPEN by the brief), and two new MEDIUMs appear — tasks.md carries no explicit FR anchors for FR-020/021/022/023/024/030 and the owner-count wording differs between E-8 and GR-01.

## Optimization Points
- ## Optimization Points
- **token-efficiency** — the run consumed the whole single-stage budget on re-deriving evidence already present in `test-evidence/analyze-repair-gates.txt` (notably re-running `pre-analyze-check.py` three times to explain a 127→0 advisory delta). A future analyze round should read the committed gate evidence first and re-run a gate only when its date-relative premise changed.
- The coverage accountant runs from the spec-dir path and therefore includes the feature's own contracts in its corpus, so the committed `analyze-repair-gates.txt` (127 advisories, 252 scanned files) and a live re-run (0 advisories, 240 files) disagree without either saying why. The gate evidence for this feature should record the exact invocation, including how the spec's own contracts are excluded, so a later round can tell "the artifacts changed" from "the command changed".
- A repair round that cites a previously red reading (H-02's `fr-uncovered 30` / `rc=1`) should carry the re-run rc into the evidence file. As committed, `analyze-repair-gates.txt` shows the red reading inside an "ok" section, which is exactly the "green check is a claim, not evidence" trap the feature itself is about.
