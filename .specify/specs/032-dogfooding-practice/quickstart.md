# Quickstart: Dogfooding Practice (Revised)

**Feature**: Feature 036 | **Spec**: [requirements.md](requirements.md)

全部场景仅使用**既有**机制——本特性不新增任何动作或步骤。

## 场景 1：Loop A —— 下游项目反馈回流框架

```bash
# 1. 真实使用中遇到摩擦点，记录（既有 record 动作；unit-id 须为 /speckit.<cmd> 或 skill:<name>）
python3 .specify/scripts/python/feedback-utils.py --action record \
  --unit-id "/speckit.implement" --unit-type command \
  --run-id "dogfood-demo-001" \
  --review "实现阶段镜像同步提示不明显，漏改一次运行时副本" \
  --points "在收尾清单中显式列出镜像清单"

# 2. 查看累计与阈值状态（既有 status 动作）
python3 .specify/scripts/python/feedback-utils.py --action status

# 3. 达阈值提示后，打包待提交条目（既有 package 动作；提交是手动的，零自动传输）
python3 .specify/scripts/python/feedback-utils.py --action package
```

## 场景 2：Loop B —— 为自己的产品建反馈循环（复用同一引擎）

```bash
# 用 skill:<自定义场景名> 标识本产品的真实使用场景（引擎仅接受 /speckit.<cmd> 或 skill:<name> 两种格式）
python3 .specify/scripts/python/feedback-utils.py --action record \
  --unit-id "skill:my-product-checkout-flow" --unit-type skill \
  --run-id "dogfood-own-001" \
  --review "结账页在低速网络下超时无提示" \
  --points "增加超时兜底文案"
# 沉淀与复盘：memory-record / /speckit.history / /speckit.review（均为既有能力）
```

## 场景 3：下游项目获得指引

- 新项目：`specify init` 后 `.specify/instructions.md` 含 `## Dogfooding Practice` 节。
- 既有项目：运行 `/speckit.instructions` 刷新即并入，用户自定义内容保留。

## 场景 4：无新机器自检（SC-004）

```bash
python3 .specify/scripts/python/feedback-utils.py --action nonexistent 2>&1 | head -2
# argparse 报错中的 choices 集合应仍为 7 个既有动作
```

## 验证入口

```bash
pytest tests/contract/test_dogfooding_practice.py
```
