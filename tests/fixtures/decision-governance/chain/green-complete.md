# Chain snapshot — complete three-segment chain (record → dispatch attempt → receipt)

- **snapshot_kind**: chain

## Record

- **decision_id**: D-001
- **carrier_pointer**: tests/fixtures/decision-governance/chain/carriers/round-trip.md

## Dispatch Attempt

- **attempt_id**: implement-executor-a
- **parent_identity**: root
- **child_label**: implement-executor-a
- **decision_id**: D-001

## Receipt

- **decision_id**: D-001
- **implementation_summary**: plan-a implemented within the stated constraints
- **evidence**: tests/fixtures/decision-governance/chain/carriers/round-trip.md
- **divergence**: none
