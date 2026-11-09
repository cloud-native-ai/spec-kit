# Improvement plan — /speckit.history (run 20261109T121113Z-speckit-history)

1. **`templates/commands/history.md` § Skill Delegation — state the exclusive-window rule.** *Tweak:* one
   sentence: "the Step 0/A seam binds the whole tracked tree; a history seam run is exclusive per
   workspace — no second history run and no harness record/commit may write during its window." Evidence: D-2
   (the seam-stop caused by the coach's own commits and the overlapping sibling run).
2. **`templates/commands/history.md` (or the delegated seam) — pin the gate-time record rule.** *Tweak:* one
   sentence stating whether the run's own record chain may execute when the flow stops at Step B. Carried
   from the sibling run (D-2 there); still unpinned. Evidence: the sibling run's withheld wrap-up.
3. **Coach-side, no Trainee edit — the harness lesson** (feed the next `improve-skills` run on
   coaching-skills): when two coaching runs share a subject, serialize them and withhold harness commits for
   the duration of a live seam window. Evidence: D-1/D-2.

## Run Status
- run: **partial** — the Trainee's flow stopped mid-way (seam-stop before Step B) with the design artifact
  present; the stop is contract-faithful, the cause coach-caused (D-1).
- optimization: **skipped** — plan recorded; the Trainee is a command template (outside improve-skills'
  Skill-only target ladder). Entry 3 is queued for the next improve-skills run on the coaching skill itself.
