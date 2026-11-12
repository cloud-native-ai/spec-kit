---
status: active
created: 2026-11-06
updated: 2026-11-06
binding:
  owner: human
  owner_id: human
  origin: 089-script-interface-contract
---

# Anchor: 脚本接口契约（Script Interface Contract）

## Objective

让所有可直接执行的 *.sh / *.py 脚本默认声明自身接口：-h/--help 与 --version 零副作用、未知选项非零拒绝；并把该规则作为框架级通用原则分发到下游项目。

## Success Criteria

1. 适用脚本的 -h/--help/--version 全部成功退出、输出非空，执行前后工作树零差异（SC-001/SC-002）
2. 契约检查对全部候选给出判定，违规计数为 0，豁免成员逐条带机械判据证据（SC-003）
3. 干净下游项目经初始化后，宪法含该原则、instructions.md 含对应常驻段落（SC-004/SC-006）

## Boundaries

- 不改造纯库文件（被 source/import 的模块）
- 不替换脚本内部实现或统一 CLI 库
- 不改 src/specify_cli 的 Typer CLI

## History

- 2026-11-06 — created.
