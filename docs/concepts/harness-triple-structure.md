# Harness Triple Structure (Three Layers)

A harness step used to live in **two layers**: prose that said what to do, and a script that did it.
The value a script decided with — a threshold, a closed set, an ordered operator table, a mapping, a
record schema — then existed twice: once in the prose, once as a tuple constant in the engine. Two
copies, two tests, and no mechanism that could notice they disagree. Neither copy was wrong on its
own; together they were.

The triple structure splits that into **three layers with one owner each**:

- **markdown** keeps the *reasoning* — the obligation, the judgement order, the boundary narrative,
  what a reader needs in order to decide which case they are in.
- **yaml** owns the *machine-readable value*: one file per fact, path as identity, so changing the
  value is changing one file.
- **script** keeps deterministic execution and the verdict, and reads the value from the yaml layer
  instead of carrying a second copy.

The discipline therefore has three properties worth stating up front, because each one is what a
copy-based layout cannot give you: a value has exactly one place to change; a disagreement between
layers becomes a program reading rather than a reviewer's memory; and "the yaml file exists" is
never accepted as evidence that anything reads it.

## Where the detail lives

This page states *what* the layer is and *why* it exists. Everything normative is owned elsewhere —
the discipline itself, the tests that decide whether a piece of content belongs in yaml, the screen
that recomputes which units are candidates, the meaning of each out-of-scope reason, the authority
order to follow when two faces have already drifted, and the explicit non-goals:

→ [`shared/definitions/harness-triple-definitions.md`](../../shared/definitions/harness-triple-definitions.md)

That document reaches every value-domain question — the closed sets, the exit codes, the required
keys, the call sites — by `<path>#/<key>` into `shared/declarations/contract.yaml`. No value domain
is restated on this page, and none should be added here: this is a pointer, and a pointer that grew a
table of values would be the second copy the whole arrangement exists to remove.

The judgement engine (`scripts/python/harness-triple-check.py`) is the machine surface of the
discipline: it reports how each candidate unit is disposed of and whether a unit's three layers are
actually complete. It is wired into an existing gate host behind an opt-in flag rather than as a new
gate stage — turning it on by default would move a closed set another accepted feature pinned.

## Reading it as a contributor

If you are adding or changing a harness unit, the question you need answered is narrow: does my unit
own a value a deterministic program decides with? If yes, that value belongs in the yaml layer and
your prose gets a pointer to it. If no, your unit owes one exclusion record naming *why* — a reason
from the closed set plus a location a reader can follow — and nothing else about it changes.
