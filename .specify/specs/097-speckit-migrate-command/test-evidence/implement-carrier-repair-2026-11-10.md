# Implement-stage carrier repair — verification.log → verification.md (2026-11-10)

## Trigger
Constitution v1.19.1 (commit 27ccbab93, user ruling 2026-11-10) corrected the Pre-Status-Flip Gate carrier from `verification.log` to `verification.md`. The framework chain that reads it — `scripts/python/closure-acceptance-check.py` `REQUIRED_INPUTS` and `shared/workflow/acceptance-hardening.md` § Gates ② — only reads `verification.md`. The repo `.gitignore` keeps `*.log` ignored.

## Finding
The r3 repair of this spec had kept `verification.log` with a `.gitignore` negation (`!.specify/specs/*/verification.log`). Implementing T048 literally would have written a file the closure gate never reads and contradicted constitution VII. The r3 evidence line "carrier name per constitution VII (`verification.log`)" was a stale premise predating the amendment.

## Repair
- `tasks.md`: DoD-7, GATE-4, package map `pkg07-polish`, and T048 now name `verification.md`; T048's `.gitignore` negation mechanics replaced with the plain version-controlled check (`git check-ignore -q` exits 1).
- `plan.md:103`: tree listing corrected to `verification.md`.
- `.gitignore:39`: dead negation `!.specify/specs/*/verification.log` removed (root cause: no ignored path remains).

## Disposition
Correction consistent with the recorded user ruling; analyze-gate self-repair policy (unattended) applied. Dated analyze evidence (`analyze-merged-r3-2026-11-10.md` R14/W3-16) is left unchanged as a historical record.
