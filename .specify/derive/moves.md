# Reasoning Move Library

Project-level accumulation of inference patterns extracted by `/speckit.derive`.
Concept authority: `shared/definitions/derivation-definitions.md` §Reasoning Move.

<!-- engine-written: derive-utils.py --action moves-add is the only writer; hand edits are DETECTED by validate, never silently accepted -->

| move_id | name | inference_form | prevents | applies_when | anchor | status |
|---------|------|----------------|----------|--------------|--------|--------|
| M-001 | Locate-the-binding-constraint | Given a system `S` believed to be limited by factor `F`, identify the resource `R` whose per-unit cost actually grows with load; the binding constraint is `R`, not `F`, so designs must be evaluated by their consumption of `R`. | designing against the bottleneck that was true in a previous era, and treating a capacity claim as an architectural justification | a scaling, capacity or performance claim is being used to justify a structural choice AND a measurable per-unit resource cost can be named; NOT licensed when no resource curve is observable, or when the constraint is social or organizational rather than physical | rest-architecture.S-004 | active |
