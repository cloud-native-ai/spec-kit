# Feature Reference: spec 034 → Feature 038

**Requirement**: `034-evidence-infra`(`.specify/specs/034-evidence-infra/requirements.md`)  
**Bound Feature**: Feature 038 — Evidence Infrastructure(`.specify/memory/features/038.md`,Status: Draft → Planned by this plan)

## 映射

| Feature 038 关键面 | 本 plan 落点 |
|--------------------|--------------|
| D1 引擎源码托管 | `scripts/js/better-harness/`(+ 镜像)+ UPSTREAM.md/LICENSE;contracts/engine-subset-boundary.md |
| 证据合同与编排 | evidence-utils.py(五 action)+ `.specify/memory/evidence/` 存储;contracts/{findings-contract,evidence-utils-cli}.md |
| D3 自有泳道 | runs/feedback 纯 Python 泳道(C-E9/C-E10) |
| 公共技能与约定 | skills/collect-evidence + shared/workflow/evidence-step.md |
| 消费层改造 | improve-skills/agent/team 三技能接入证据步骤 |
| 纵向验证 | intervention.json + compare verdict(C-E7/C-F14) |
| D2 平台扩展 | 本 spec 边界内仅 doctor 探测报告与定序建议(Clarify Q3) |

## 关联 Feature(非归属)

- 028 Feedback Mechanism:feedback 泳道数据源;evidence-step 与 feedback-step 对偶。
- 027 Team Management:runs 泳道数据源;improve-team 为消费方。
- 013 Skills Command:collect-evidence 技能载体与注册表。
