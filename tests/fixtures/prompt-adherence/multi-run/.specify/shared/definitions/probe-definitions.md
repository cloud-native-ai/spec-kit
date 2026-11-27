# Probe definitions — prompt-adherence fixture registry

A minimal structurally valid registry so `probe-utils.py load_probe_registry` reads
`available: true` with one declaration object and no validation errors.

## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| fixture-wrapup | internal | fixture class for the prompt-adherence store | commands | record→review | wrap-up |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| fixture-plan | fixture-wrapup | /speckit.plan | wrap-up |