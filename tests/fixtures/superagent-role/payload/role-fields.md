# Downlink role fields block

Every governed dispatch payload carries these seven fields. The shape and the value domains
are owned by `.specify/shared/definitions/superagent-definitions.md` § The super↔sub
Protocol; this block is the fixture copy the payload contract test reads.

| Field | Content |
|-------|---------|
| `parent_identity` | the dispatching executor's identity |
| `child_label` | this dispatch's label |
| `role_declaration` | `subagent` \| `superagent` — the role claim for this edge (`dual-role` never appears here) |
| `dispatch_duty` | `granted` \| `not-granted` — the grant fact, declared independently of the role claim |
| `depth_position` | the child's declared depth (integer) |
| `authority_ref` | pointer to the authorization basis (`sdd-route.py --action authorize` record, team territory, or `none`) |
| `return_channel` | the declared return path (structured return + evidence pointer channel) |
