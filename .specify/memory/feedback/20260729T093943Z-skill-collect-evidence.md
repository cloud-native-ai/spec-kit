---
id: "20260729T093943Z-skill-collect-evidence"
unit_id: "skill:collect-evidence"
unit_type: "skill"
run_id: "dogfood-project-20260729"
scope: "local"
feature: "034-evidence-infra"
partial: false
created: "2026-07-29T09:39:43Z"
summary: "对 spec-kit 自身完成首次真实 dogfood 证据闭环:采集(ev-093344)→分拣冻结唯一缺陷候选(assets 泳道计数缺陷)→最小修复+回归钉点→台账→第二轮采集+compare(lintFindings 3→16)→verdict=Outcome-supported(机制首个正向判定)。红线全守:Unobserved 只记录、计数不产生发现、冻结外发现(上游 SKILL_HO"
---

## Review
对 spec-kit 自身完成首次真实 dogfood 证据闭环:采集(ev-093344)→分拣冻结唯一缺陷候选(assets 泳道计数缺陷)→最小修复+回归钉点→台账→第二轮采集+compare(lintFindings 3→16)→verdict=Outcome-supported(机制首个正向判定)。红线全守:Unobserved 只记录、计数不产生发现、冻结外发现(上游 SKILL_HOME 误报、draw-echarts 镜像残留)只记录待人工。

## Optimization Points
- 证据机制首次对宿主项目自转即抓到自身缺陷(lintFindings 数信封字典恒为 3),且 compare 给出首个 Outcome-supported 判定——纵向闭环全链路在真实场景走通;建议把"泳道 envelope 结构断言"(信封 dict vs list)扩展为对全部 Node 泳道映射函数的合同测试,而非仅 lint 一处。
- 上游 lint 不解析 ${SKILL_HOME} 路径变量产生 4 条误报——这是采集子集对 spec-kit 资产约定的首个适配缺口,应按 UPSTREAM.md 修改纪律做本地 resolver 注入(候选回馈上游),否则 assets 泳道信号长期带噪。
