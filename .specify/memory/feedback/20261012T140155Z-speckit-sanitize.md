---
id: "20261012T140155Z-speckit-sanitize"
unit_id: "/speckit.sanitize"
unit_type: "skill"
run_id: "20261012-migration-residue"
scope: "local"
probe: "speckit-sanitize-wrapup"
kind: "internal"
slice: "commands"
disposition: "ignored"
partial: false
created: "2026-10-12T14:01:55Z"
summary: "本次为 sanitize 增加 init 迁移残留检测(C-22/23/24 + C-10 扩链):过程中发现系统性盲区——tests/contract/ 多个文件无 @pytest.mark.contract 装饰器,-m contract 门从未选中它们,S3 的 123 项归因修复漏掉了 sanitize_template ×5 / confirmation_gates_sweep ×10 "
disposition_reason: "introspection-20261013T155006Z#excluded — ALREADY-FIXED: C-12/C-22 double-report boundary implemented+contracted+pinned (sanitize-utils.py:670-677, 045 contracts :36,44, test_sanitize_checks_migration.py:73,97)"
---

## Review
本次为 sanitize 增加 init 迁移残留检测(C-22/23/24 + C-10 扩链):过程中发现系统性盲区——tests/contract/ 多个文件无 @pytest.mark.contract 装饰器,-m contract 门从未选中它们,S3 的 123 项归因修复漏掉了 sanitize_template ×5 / confirmation_gates_sweep ×10 / fast_fail ×6 等共 21+2 条同残留,本次已全部收口并给 sanitize_template 补标记;建议后续专项:为 tests/contract 下全部无装饰器文件补标记(逐文件裁决),否则 A/B 门存在持续漏检面

## Optimization Points
- engine-design:同目标双报要防——mirror-drift(C-12)与迁移残留(C-22)在框架仓/客户仓分别管辖,以 skills/external 源侧存在性为分界
