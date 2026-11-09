# Improvement plan — /speckit.status (run 20261109T114345Z-speckit-status)

Entries ordered by priority; each names one concrete file+section and one concrete tweak.

1. **`templates/commands/status.md` § Wrap-up — add one line to the capture rule.** State that the digest output is
   read directly from the script's stdout (or captured under the sanctioned temp root
   `.specify/.tmp`/`~/tmp/<project>`), never in bare `/tmp`. *Tweak:* one sentence at the head of § Wrap-up.
   Evidence: D-2 (the trainee's disclosed /tmp violation and in-passing cleanup).
2. **`skills/external/coaching-skills/references/prompt-templates.md` § Execution Expectation Template — derive PE
   rows from the Trainee's whole contract, including its Wrap-up/close-out sections.** *Tweak:* one line under the
   PE derivation comment: "derive from every section the Trainee executes (Delegation, actions, Wrap-up, Close-out),
   not only the primary action." Evidence: D-1 (the expectation under-derived the wrap-up chain).
3. **Observation only, no Trainee edit — registry gap.** The digest lists only Line-Registry-backed entries; the
   active 093/094 lines are unregistered. *Tweak (owner: the line registration flow, not the command):* register the
   active lines via `line-registry.py --action register` so the digest shows them. Evidence: D-4.

## Run Status
- run: **success** — the Trainee's primary artifact exists (the verbatim digest block with exit=0), the lifecycle
  completed, and the destructive close-out step was correctly relayed instead of approved.
- optimization: **skipped** — the plan is recorded; no `improve-skills` invocation ran in this loop. Entry 1 targets a
  command template (outside improve-skills' Skill-only target ladder; queued for the command-surface channel), and
  entry 2 targets the coaching skill's own reference (queued for the next improve-skills run). The user's pending
  commit/push request takes priority over a nested optimization loop.
