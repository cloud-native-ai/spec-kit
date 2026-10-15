---
id: "20261014T160808Z-skill-memory-recall"
unit_id: "skill:memory-recall"
unit_type: "skill"
run_id: "20261015T000511Z-instructions-shared-docs"
scope: "local"
probe: "skill-memory-recall-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-14T16:08:08Z"
summary: "定向部分更新（用户请求=区分 shared/docs 文档面）：两处编辑，其余章节逐字节未动；24 行路径核验全过；标题集合双向零丢失；制品提交 5ca10ec6。"
---

## Review
定向部分更新（用户请求=区分 shared/docs 文档面）：两处编辑，其余章节逐字节未动；24 行路径核验全过；标题集合双向零丢失；制品提交 5ca10ec6。

## Optimization Points
- wrap-up 引擎调用链需多轮参数发现（run-id → complexity → review → points 各报一个错误），命令模板 Wrap-up 嵌入未载明必填参数全集，4 个受调单元 ×3 轮重试放大 token 消耗；建议嵌入处列全必填参数或引擎提供一次校验全部必填项的模式。
- instructions 尺寸 33898 B 超 32768 B 预算 1130 B，且 R1/R2 均无合法候选（正 delta 行全部 placeholder=yes 项目填充型；唯一 project-owned 章节 787 B 未达 4 KB 阈值）——预算收敛机制对"项目填充型大章节"无解，需用户裁定预算值或章节拆分。
