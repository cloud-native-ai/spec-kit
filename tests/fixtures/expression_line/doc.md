# 表达类夹具线的交付文档

**Readers**: 第一次接手这条夹具线的维护者，需要在十分钟内判断门禁是否真的跑过。
**Reading scenario**: 复跑集成测试之前，对照本文核对命令与期望。

## 概览

这条夹具线被声明为表达类（证据：实测，as-of 2026-10-30，source: `flow-class-check.py --action lookup --unit-id spec:777-expression-line-pilot`）。

## 判定

四面门禁与结构子步各跑一次；退出码为 0 时本阶段放行，任何一个面为 `not-evaluated` 都不算通过。
