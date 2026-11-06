import re

P = '/storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/tasks.md'
M = 'contracts/measure-report.contract.md#'
E = 'contracts/efficiency-element.contract.md#'
O = 'contracts/ownership-map.contract.md#'

ROWS = [
 ('T062',
  ' Author the one store reading and the element projection into `scripts/python/status-digest.py` behind its existing `--action digest` and `--action report` renders: obtain records only by importing `scripts/python/exec-quant.py`\'s read path in-process (the engine\'s own composition of the legacy stream and the per-record directory, never a re-parse, never a shell-out, never a cache), select per listed unit the record with the latest `collected_at` resolving ties by the record\'s own identity ascending, and emit the element as content of the entry — identity, then elapsed unconditionally, then tokens and invocations only while the whole element fits the surface\'s existing entry bound, withdrawn render-wide and named once in that render\'s existing omitted summary — with the explicit not-evaluated marker wherever the record carries no value, zero folds, and no new action, file or unit set — [blockedBy: T055,T056,T061] [green: ' + E + 'C-63] [covers: FR-023, FR-024]'),
 ('T063',
  ' Complete the efficiency element\'s two ordering faces in the same renderer: the listed-unit-with-no-record case still renders the element with the marker, and an absent or empty store renders the explicit `no measurements` state leaving the units, content floor, ordering and exit status byte-identical to a render without the dimension, with the store never opened for writing and no path created under it by either read — [blockedBy: T062] [green: ' + E + 'C-67] [covers: FR-024, FR-025]'),
 ('T064',
  ' Author `scripts/python/measure.py` as one stdlib-only file behind `templates/commands/measure.md`\'s single entry: the half-open window (`--since` start, `--window` span, neither meaning all records, an unresolvable pair or a start after the resolved end an input error), the set selection over exact `(unit_id, unit_type)` identities, the declared per-unit cap printed on every run with its omitted count beside the four exclusion classes, the rows (record count, elapsed median with min and max, token sum, invocation count, each with the provenance and `covered=<k>/<n>` the records state, each absent quantity the explicit marker), the accounting identity over the five exclusion-side counts, and the closed action set `summary` / `json` as two projections of one computed result — records reached only by importing the store engine\'s read path, never by parsing the format, never by spawning — [blockedBy: T058,T059] [green: ' + M + 'C-53] [covers: FR-026, FR-027, FR-028]'),
 ('T065',
  ' Close the measure report\'s window, selection and distribution faces in `scripts/python/measure.py`: the window states its own resolved half-open bounds with no wall-clock text beyond them (and none when unbounded), the selection echoes the `(unit_id, unit_type)` set it resolved, and the per-unit figures print median with min and max beside `covered=<k>/<n>` — each absent quantity the explicit marker, never `0` — [blockedBy: T064] [green: ' + M + 'C-54] [covers: FR-026, FR-027]'),
 ('T066',
  ' Complete the measure report\'s cap and exclusion faces in `scripts/python/measure.py`: the declared per-unit cap prints on every run with its omitted count, `--cap` re-truncates by record identity, and the four exclusion classes (`unreadable`, `legacy-format`, `outside-window`, `unknown-unit`) each print their count with the accounting identity `contributed + unreadable + legacy-format + outside-window + unknown-unit + outside-cap == read` — [blockedBy: T065] [green: ' + M + 'C-55] [covers: FR-027, FR-028]'),
 ('T067',
  ' Close the measure report\'s closed exit-status set and its two closed actions in `scripts/python/measure.py`: `0` also covering a report whose window selected records but measured no figure (stated as `0 figures measurable`), `2` naming the offending input on one line, `3` printing `no measurements`, `1` reserved for any other failure and for neither of the two above, with `summary` and `json` as the only actions and the JSON carrying the same figures under exactly the asserted top-level key set — [blockedBy: T066] [green: ' + M + 'C-59] [covers: FR-026, FR-028]'),
 ('T068',
  ' Close the measure report\'s determinism and read-only faces in `scripts/python/measure.py`: rows ordered by `(unit_type, unit_id)` ascending and records by identity ascending, two consecutive runs of each action byte-identical, no `datetime.now` / `time.time` in the render path, and no write of any kind — no file opened for writing, no directory created under the store, no subprocess, no network call — [blockedBy: T067] [green: ' + M + 'C-61] [covers: FR-026, FR-028]'),
 ('T069',
  ' Author `templates/commands/measure.md` as the thin command: `/speckit.measure` front matter, a body naming only `scripts/python/measure.py`, the two actions (`summary` / `json`) and the closed four-value exit-status set, plus the standard `## Wrap-up` delegation block — no rendering, no analysis, no store reading of its own, no store or registry entry or long-running process — [blockedBy: T064] [green: ' + M + 'C-62] [covers: FR-026, FR-029]'),
 ('T070',
  ' Generate the measure command\'s four per-tool copies and both new script mirrors through the framework\'s own engines, never by hand: `python3 scripts/python/regen-command-copies.py` then `--check` must print `OK` with the four `speckit.measure.*` paths present, and `sync-mirrors.py --write --only scripts/python/measure.py` plus `--only scripts/python/status-digest.py` (both STRICT pairs) then `sync-mirrors.py --check` must report `ok` with no NEW drift against plan.md § Mirror Obligations — readings into `.specify/specs/088-speckit-visualization/test-evidence/polish-second-slice.txt` — [blockedBy: T063,T069] [green: ' + E + 'C-64] [covers: FR-029]'),
 ('T071',
  ' Capture the `/speckit.measure` runs as real output: a summary and a json run over a populated fixture store (window, selection and printed cap stated; per-unit rows with provenance; the four exclusion counts and the omitted count), a run over an absent store and a run over a window selecting nothing (each the explicit `no measurements` at exit `3`), a bad-input run (exit `2`, the offending value echoed) and an all-`not_evaluated` run (exit `0`, `0 figures measurable`) — verbatim output, exit codes and the fixture store\'s record paths into `.specify/specs/088-speckit-visualization/test-evidence/us5-measure.txt` — [blockedBy: T068] [green: ' + E + 'C-66] [covers: FR-026, FR-027, FR-028]'),
 ('T072',
  ' Capture the efficiency element on both visible surfaces: one status-line render and one digest render over the same fixture store (measured, not-evaluated and absent-store cases), a tight-bound render proving the render-wide withdrawal with the omitted summary naming the withdrawn quantity, and a window-truncated digest render carrying the element inside the cap — verbatim output and the fixture record paths into `.specify/specs/088-speckit-visualization/test-evidence/us5-efficiency-element.txt` — [blockedBy: T070] [green: ' + E + 'C-65] [covers: FR-023, FR-024]'),
 ('T073',
  ' Measure the read-only property over both reads: take a per-file digest of `.specify/memory/exec-quant/` (legacy stream files included) plus a listing of it, run the element\'s read and the measure report against it, take the same digest and listing again, and store all four verbatim with the comparison verdict into `.specify/specs/088-speckit-visualization/test-evidence/us5-readonly-store.txt` — every file equal and no path created is the reading, not the assertion — [blockedBy: T072] [green: ' + E + 'C-69] [covers: FR-024, FR-025]'),
 ('T074',
  ' Record this slice\'s success-criterion evidence into `.specify/specs/088-speckit-visualization/test-evidence/success-criteria.txt` as a dated second section: for SC-011 the two-surface captures plus the marker and absent-store readings, for SC-012 the before/after store digests and listing, for SC-013 the populated-store run with its hand-computed expectation table and the empty-store run with its exit status, for SC-014 the two byte-identical runs with their diff plus the changed-file scan — naming the capture file and the producing command per row, and marking any criterion whose evidence is a green check without a captured reading `not-measured` rather than `pass` — [blockedBy: T071,T073] [green: ' + O + 'C-52] [covers: FR-023, FR-026, FR-029]'),
 ('T075',
  ' Judge the new command and script against the zero-new-machinery boundary by AST-level scan rather than prose: `git diff --name-only 56f3f881..HEAD` against `feature-ref.md` § Delivered paths #29–#40, a spawn / thread / scheduler / network import-and-call scan over `scripts/python/measure.py` and the edited `scripts/python/status-digest.py`, a `pyproject.toml` dependency pin against its pre-change values, a confirmation-gate count against the recorded 27, and a static assertion that neither file carries a second record-format parser or a second store engine — every reading into `.specify/specs/088-speckit-visualization/test-evidence/cl-01-closure.txt` as an appended dated section — [blockedBy: T074] [green: ' + M + 'C-60] [covers: FR-026, FR-029]'),
]

s = open(P).read()
lines = s.split('\n')
start = None
end = None
for i, l in enumerate(lines):
    if re.match(r'^- \[x\] T062 ', l):
        start = i
    if re.match(r'^- \[x\] T072 ', l):
        end = i
assert start is not None and end is not None, (start, end)
new = ['- [x] ' + tid + desc for tid, desc in ROWS]
lines[start:end + 1] = new
s = '\n'.join(lines)
s = s.replace(' **Checkpoint**: Both visibility surfaces', ' **Checkpoint**: Both visibility surfaces')
open(P, 'w').write(s)
print('rows written:', len(new), 'ids', ROWS[0][0], '->', ROWS[-1][0])
