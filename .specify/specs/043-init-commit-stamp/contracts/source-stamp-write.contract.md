# Contract: 落章写入与 init 集成(write_source_stamp)

**Spec**: [requirements.md](../requirements.md) FR-001, FR-002, FR-003, FR-005, FR-006, FR-007  
**Surface**: `src/specify_cli/__init__.py`(`write_source_stamp` + `init()` 调用点)  
**Authority**: 解析语义见 source-stamp-resolution 契约;本契约定义落盘载荷与 init 编排

## C-1 载荷 schema(目标项目文件)

路径恒为 `<project>/.specify/source.json`([[STR-001]]),JSON/UTF-8/indent 2:

```json
{
  "framework": "spec-kit",
  "commit": "<40-hex> | \"unavailable\"",
  "reason": "<仅 commit=unavailable 时出现>",
  "stamped_at": "20260817T075305Z"
}
```

- `framework` 恒为 [[STR-003]] 字面量;`commit` 取值域 = 40-hex 或 [[STR-002]],无第三种;
- `reason` 键在 commit 有效时**不存在**(而非空串/null);
- `stamped_at` 复用 `_utc_compact_stamp()`(UTC ISO-8601 basic);
- pyproject version **不得**成为任何字段的值来源(FR-002:commit 是唯一标识)。

## C-2 覆写语义(刷新)

- 每次写入为**整体覆写**:以本合约 C-1 的完整载荷替换文件原有内容,不合并旧字段;
- 升级 init 后旧 commit 在文件中零残留(grep 旧 id 0 命中,FR-006/SC-004);
- 目标 `.specify/` 目录不存在时创建后写入(init 流程内恒已存在,防御性兜底)。

## C-3 非阻塞(落章是附随信息,不是门禁)

- `write_source_stamp` 捕获自身一切 `OSError`/序列化异常:失败 → Rich 黄色告警一行(沿 init 既有 warn-but-continue 模式),返回 `False`;**不抛出、不改变 init 退出语义**;
- 成功 → 静默落盘(文件即记录,不加成功噪音);
- 函数签名 `write_source_stamp(project_path: Path) -> bool`(可测)。

## C-4 init 集成点

- `init()` 在打印 `Project ready.` 之前调用一次 `write_source_stamp(project_path)`——fresh init 与再次 init(升级路径)都必经此点,覆写语义由 C-2 保证;
- 不新增 CLI 选项/flag(零交互面,Assumptions);不触碰 agents manifest(正交);
- 本需求不修改 init 的任何既有输出步骤顺序与文案(落章插在收尾区,不改前置流程)。

## 验证

- `tests/contract/test_source_stamp.py` 写入组——monkeypatch 解析结果:有效 commit → 载荷逐字段断言(reason 键不存在);unavailable → STR-002 + reason;先写 A 再写 B → 文件含 B 且 grep A 为 0;monkeypatch `Path.write_text` 抛 OSError → 返回 False 且不抛;
- `tests/integration/test_init_source_stamp.py`——conftest 最小资源夹具 + `RUNNER.invoke(app, ["init", <tmp 项目>, "--ai", "qoder", "--no-git", ...])`:断言 `<项目>/.specify/source.json` 存在且 commit 为当前 checkout 的 HEAD(或测试注入的期望值);再次 invoke → 刷新断言。
