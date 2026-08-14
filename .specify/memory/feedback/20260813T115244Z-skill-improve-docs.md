---
id: "20260813T115244Z-skill-improve-docs"
unit_id: "skill:improve-docs"
unit_type: "skill"
run_id: "20260813T115200Z-feedback-intake-doc"
scope: "local"
partial: false
created: "2026-08-13T11:52:44Z"
summary: "Improved docs/reference/skills/feedback.md on a completeness gap: the doc documented the sending half of Dogfooding Loop A but the receiving half was unnamed ('an MR to the feedback intake directory')"
---

## Review
Improved docs/reference/skills/feedback.md on a completeness gap: the doc documented the sending half of Dogfooding Loop A but the receiving half was unnamed ('an MR to the feedback intake directory'). Two section-level edits: named the directory at its reference site, and added an 'Intake side' section (bundle naming kept verbatim, the gitignore negation that keeps bundles tracked, the one-consolidated-batch rule with its rationale). Discipline held: no existing heading renamed so no anchor repair was needed, untouched sections byte-for-byte, validate identical to baseline (one pre-existing unrelated note-frontmatter violation), Hugo build clean. Every asserted fact was re-verified against the repo before writing rather than copied from the requesting prompt — which mattered, since the git-ignore negation claim needed 'git add -n' to confirm (check-ignore -v was misleading).

## Optimization Points
- Step 2's evidence list has no entry for "a convention the user just established", which was this run's actual driver. It is neither a machine finding nor a verified staleness signal — the doc was not wrong, it was silent. I treated it as a completeness gap with the user statement as evidence, which worked, but the skill should name this source explicitly (user-established convention → completeness gap) so the next run does not have to improvise the classification.
- The verification table lacks a check for "did I assert a mechanism I only read about?". Here the trackability claim (`!feedback-*.zip` beating the root `*.zip`) was easy to get wrong: `git check-ignore -v` prints the negation line and exits 0, which reads as "ignored". Only `git add -n` / `git status --ignored` settled it. A one-line rule — when documenting git/tooling behavior, verify by the observable outcome, not by the diagnostic command's exit code — would prevent a confidently wrong sentence.
- The two-part edit (name the thing at its reference site + document it in a new section) is a recurring shape when a doc mentions an unnamed entity. Step 4 could name it: fix the dangling reference and add the section in the same run, since fixing only one leaves either a section nobody reaches or a name with no definition.
