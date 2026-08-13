---
id: "20260813T114254Z-speckit-instructions"
unit_id: "/speckit.instructions"
unit_type: "command"
run_id: "20260813T114300Z-feedback-intake"
scope: "local"
partial: false
created: "2026-08-13T11:42:54Z"
summary: "Partial-update run driven by a user convention: designate repo-root feedback/ as the central intake for user feedback bundles (feedback-*.zip) and mandate consolidated batch processing. The reconcile "
---

## Review
Partial-update run driven by a user convention: designate repo-root feedback/ as the central intake for user feedback bundles (feedback-*.zip) and mandate consolidated batch processing. The reconcile discipline worked well — I verified the observed facts before writing (zip contents and MANIFEST, feedback-utils package path, root *.zip ignore vs feedback/.gitignore negation, git status showing the bundles trackable), so the recorded text states verified behavior rather than the user's paraphrase. Tolerance band was honored: only two cells changed, everything else byte-for-byte. Friction: the command gives no guidance on which section a newly-supplied convention belongs to, and the docs side still calls this directory an unnamed 'feedback intake directory' (docs/reference/skills/feedback.md:136), so the naming now lives only in instructions.md.

## Optimization Points
- The command's partial-update path lacks a "where does a new fact belong" rule. The user's input was a *convention* (a directory's role + a processing rule), and the template offers no obvious home for it: Documentation Map rows point at owning docs, Key Directories describes layout, Recurring Operational Lessons holds gotchas. I placed it in Key Directories + a Map row cross-reference, but that choice was unguided. Suggest Action 5 gain a short routing table: location fact → Key Directories; doc ownership → Documentation Map; binding rule with no owning doc → the section owning that domain, plus a note to flag "no owning doc exists yet" as PENDING for improve-docs.
- Action 6's coverage check only prescribes diffing against backups for *dropped* content; it has no positive check that the new fact actually landed in a place a fresh agent would read. A one-line assertion ("grep the new fact back out of the final file") would close the loop cheaply.
- The Documentation Map path-existence check (Action 5) is worth scripting into the repo rather than re-improvising it each run: this run wrote an ad-hoc python loop over Location cells. A tiny `--check-map` mode on an existing script would make it deterministic and Program-First compliant.
