# Concurrency contracts — index

**Owner of the clause bodies**: the five files below. This index carries no clause body; it exists so a reader
reaches the right file without scanning them all.

| File | Clauses | Binds |
|---|---|---|
| `declaration-facts.contract.md` | C-001…C-018 | The declaration layer: fact files, kinds, registration, scope and enumeration roots |
| `judgement-engine.contract.md` | C-019…C-040 | `scripts/python/concurrency-check.py`: interface, five actions, exit taxonomy, JSON envelope |
| `executor-obligations.contract.md` | C-041…C-062 | The three-part obligation, class obligation text, serial reason codes, shared strings, declaration-equals-execution |
| `high-order-executors.contract.md` | C-063…C-078, C-093…C-094 | Goal, team, loop grains, coordinator dispatch, sub-agent inheritance; the analyze wave and the fork mechanism |
| `existing-semantics-disposal.contract.md` | C-079…C-092 | Disposition of every pre-existing restatement; adjacent features left untouched |

**Clause gateway**: 94 clauses in total. `[[STR-001]]`…`[[STR-011]]` are the shared strings from requirements.md
and appear in these files as pointers, never as redefinitions. `C-060` is the red-first clause: every other clause
that is machine-decidable names the module that goes red when it is violated.

**Reading order for an implementer**: C-001…C-018 (what the facts are) → C-019…C-040 (how they are judged) →
C-041…C-062 (what a body must do) → C-063…C-078 (how the grains comply) → C-079…C-092 (what to do with what is
already written) → C-093…C-094 (the analyze wave and the mechanism that carries it).
