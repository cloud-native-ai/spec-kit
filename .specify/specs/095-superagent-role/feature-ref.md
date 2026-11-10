# Feature Reference — 095-superagent-role

- **Feature ID**: 095
- **Feature Name**: Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）
- **Feature detail**: `.specify/features/095-superagent-role.md`
- **Feature index row**: `.specify/features.md` (§ Features, row `095`)
- **Spec**: `.specify/specs/095-superagent-role/requirements.md`
- **Status transition owned by this plan**: `Draft → Planned` (the `Implemented` transition is owned by `/speckit.implement`)

## How this plan maps to the Feature

| Feature detail item | Plan coverage |
|---------------------|---------------|
| 1. New owner `shared/definitions/superagent-definitions.md` ([[STR-004]]) | Plan D-1; Work Package P1; `contracts/harness-landing.contract.md` § C-2 |
| 2. Read-only role-edge judgement engine | Plan D-2…D-7; P2; `contracts/role-edge-engine.contract.md` |
| 3. `status-digest.py` role-edge view | Plan D-8; P4; `contracts/status-digest-role-view.contract.md` |
| 4. Dispatch surfaces add fields only | Plan D-9/D-14; P3; `contracts/role-transition-payload.contract.md` |
| 5. Harness landing + instruction budget | Plan D-10; P5; `contracts/harness-landing.contract.md` § C-1 |
| 6. 080–094 mechanism observation appendix | Plan D-12; P6; `observation-appendix.md` at implement close-out |

**No new Feature is introduced or deprecated by this plan**; the functional/non-functional classification (framework capability: role model + judgement + projection) is unchanged. Related-neighbour cross-references (027 / 085 / 093) live only in the feature detail file, per the clarify wrap-up correction.
