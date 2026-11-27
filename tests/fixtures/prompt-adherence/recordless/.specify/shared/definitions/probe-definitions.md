# Probe definitions — prompt-adherence fixture registry (recordless variant)

Ships like a fresh `specify init` does: the probe registry is a declaration, not a
record, so this row reads `Wired` while every record-bearing row stays absent.

## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| fixture-wrapup | internal | fixture class for the prompt-adherence store | commands | record→review | wrap-up |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| fixture-plan | fixture-wrapup | /speckit.plan | wrap-up |