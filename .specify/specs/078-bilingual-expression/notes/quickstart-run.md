# quickstart S1–S8 实跑留档 — 078 双语表述（Bilingual Expression）

**实跑阶段**：implement（T018 收口；本文件头部先列场景与判据）
**权威场景源**：`.specify/specs/078-bilingual-expression/quickstart.md` S1–S8（MUST NOT 改写）

## 场景清单与各自判据

| 场景 | 内容 | 判据 | 状态 |
|------|------|------|------|
| S1 | 约定核对（读者面，无命令） | 四步核对可自判合规（信号 / 方向 / 形态 / 豁免） | pending |
| S2 | 检查器形态判定 ×3（合规 / 全角 / 同向） | 退出码 0/1 与 finding 码、行号定位形态 | pending |
| S3 | 覆盖面核验 | `coverage` 不接受 `--path`；覆盖面清单只读 owner 文档 | pending |
| S4 | 下游 instructions 生成（pilot 管道） | 产物含逐字 ambient 标题、四组枚举关键词零命中、含 [[STR-001]] 指针；pilot 拆除 | pending |
| S5 | 镜像零新增漂移 | 本特性三对相对 `plan-sync-mirrors-baseline.txt` 无新增 DIFF | pending |
| S6 | 结构面零新增 | `docs-utils.py --action validate` violations 相对基线 4 零新增 | pending |
| S7 | SC-001 关键词扫描 | 程序派生关键词表；排除 owner 自身与指针行后命中数 0 | pending |
| S8 | census（SC-005） | 退出码 0；中文侧逐字比对；100% census | pending |

## S1 实跑

（待 T018 填写）

## S2 实跑

（待 T018 填写）

## S3 实跑

（待 T018 填写）

## S4 实跑

（待 T018 填写；含拆卸步骤与 `git status --ignored` 核查）

## S5 实跑

（待 T018 填写）

## S6 实跑

（待 T018 填写）

## S7 实跑

（待 T018 填写）

## S8 实跑

（待 T018 填写；含拆卸步骤）
