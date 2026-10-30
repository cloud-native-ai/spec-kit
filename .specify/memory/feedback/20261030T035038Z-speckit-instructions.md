---
id: "20261030T035038Z-speckit-instructions"
unit_id: "/speckit.instructions"
unit_type: "command"
run_id: "20261030T115000Z-instructions-size"
scope: "local"
probe: "speckit-instructions-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-30T03:50:38Z"
summary: "指令体积收敛：模板与 live 同步精简，静态不变量全绿；契约测试未执行（项目 .venv 缺 pytest，替代解释器运行被拒）。"
---

## Review
指令体积收敛：模板与 live 同步精简，静态不变量全绿；契约测试未执行（项目 .venv 缺 pytest，替代解释器运行被拒）。

## Optimization Points
- 模板 36471->27940 B；live 43439->32259 B（余量 509 B）；T=M 镜像字节一致；30/31 节标题；gate 27 / violations 0；pytest 未执行
