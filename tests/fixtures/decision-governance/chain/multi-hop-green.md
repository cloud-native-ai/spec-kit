# Chain snapshot — multi-hop chain, every hop carries the block and every receipt keeps D-001

- **snapshot_kind**: chain

## Record

- **decision_id**: D-001
- **carrier_pointer**: tests/fixtures/decision-governance/chain/carriers/round-trip.md

## Dispatch Attempt

- **attempt_id**: coordinator-hop-1
- **parent_identity**: root
- **child_label**: coordinator-hop-1
- **decision_id**: D-001

## Receipt

- **decision_id**: D-001
- **implementation_summary**: hop 1 accepted the block and forwarded it unchanged
- **evidence**: tests/fixtures/decision-governance/chain/carriers/round-trip.md
- **divergence**: none

## Dispatch Attempt

- **attempt_id**: implement-executor-hop-2
- **parent_identity**: coordinator-hop-1
- **child_label**: implement-executor-hop-2
- **decision_id**: D-001

## Receipt

- **decision_id**: D-001
- **implementation_summary**: hop 2 implemented plan-a within the stated constraints
- **evidence**: tests/fixtures/decision-governance/chain/carriers/round-trip.md
- **divergence**: none
