# Contract: 打包腿布局与行为（Package Leg）

**Feature**: 068 Exec-Quant Feedback Channel | **File scope**: `scripts/python/feedback-utils.py`
(+ mirror) | **FR served**: FR-001 ~ FR-005, FR-019 | **引擎动作**: `--action package`（扩展）

- **C-1** 载荷采集（read-only sweep）

打包流程 MUST 扫描 `<workspace>/.specify/memory/exec-quant/`：

- `records/*.json` 逐条文件 + 遗留 `records.jsonl` 逐行条目，两类并存时**全部**纳入
  （全量包含，FR-001）。
- 每条 MUST 可 `json.loads` 为 object 且 `kind == [[STR-001]]`；不可解析条目跳过并
  计入 `skipped_unreadable`（FR-005）。
- 遗留流条目名 `legacy-records-L%04d.json`（行号自 1 起）；来源形态分别计入
  `source_form_counts.records-dir / .legacy-jsonl`。
- 源存储零改动、零移动、零删除（FR-002）；扫描窗口 = 动作发起时刻快照，扫描期间
  新写入不纳入（与 A3 自省既有快照语义一致）。

- **C-2** 排序与封顶

- 排序键 `(collected_at 升序, 源文件名升序)`，确定性、跨机可复现。
- 上限：`MAX_PAYLOAD_RECORDS = 1000` 条、`MAX_PAYLOAD_BYTES = 16 MiB`（模块常量）。
- 触顶即截断：余下条目计入 `truncated_count`，不静默丢弃、不无界膨胀（FR-005）。
- 上限值 MUST 写入 `payload-manifest.json` 的 `cap_records` / `cap_bytes`（取证）。

- **C-3** 包内布局

```text
<zip root>/exec-quant/payload-manifest.json
<zip root>/exec-quant/records/<name>.json     # 原样字节拷贝
```

- 载荷 MUST 只存在于 `exec-quant/` 目录（一等载荷、显式声明，FR-001）；MUST NOT
  以临时附加文件等未声明形态混入 zip 其他位置。
- 记录文件内容 = 源文件字节原样拷贝（byte-verbatim）；MUST NOT 重排、重编码、
  过滤字段。
- feedback 条目、`introspection/`、`SUBMISSION-NOTES.md`、`MANIFEST.md` 既有布局
  与命名零变化。

- **C-4** payload-manifest.json

`exec-quant/payload-manifest.json` 字段与校验见 data-model.md § E4；MUST 与
MANIFEST.md § Exec-Quant Payload 人读段由同一渲染函数产出（内容同源）。

- **C-5** 包级源项目身份

- `project_name`：读 `.specify/instructions.md` 的 `**Project Name**:` 行；失败回退
  workspace 目录基名；再失败置空 + `identity_status: "unknown-project"`（D3）。
- `source_commit`：`git rev-parse HEAD`（仓库内）；失败置 null，不重试不阻塞。
- MUST NOT 以文件系统绝对路径作身份载体；MUST NOT 新增凭据面（FR-003）。
- 身份写入 E2 / E4，接收侧以此归因；记录级 `agent.cwd` 仅佐证（FR-003）。

- **C-6** MANIFEST.md § Exec-Quant Payload 段

- 空载荷时该段 MUST 存在并声明「无量化数据」（显式降级，FR-005）。
- 非空时 MUST 声明：条数、`source_form_counts`、`skipped_unreadable`、
  `truncated_count`、`project_name`（或 unknown-project）、封顶触发与否。

- **C-7** 打包输出报告

`--action package` 的输出（text 与 `--format json` 双面）MUST 可见载荷纳入情况：
条数、降级计数（FR-004）——用户手动投递前对包内数据范围知情。

- **C-8** FR-019 行为修订

- `write_package` 早退条件由「feedback 条目为空」修订为「feedback 条目与载荷记录
  双空」（D9）。
- feedback 条目空 + 载荷 ≥1 → 照常产包：`Entries: 0` 显式入 MANIFEST，载荷照常。
- 双空 → 不产包，输出显式说明（既有非零包为成功语义不变）。
- external 排除（`kind: external`）、时间过滤、`--all`、`--include-introspection`
  语义零变化。
- 引用组：(FR-019)

- **C-9** 非阻塞与零网络

- 载荷采集任何降级（空存储/目录缺失、部分不可解析、截断、身份缺失）MUST NOT 使
  打包流程失败（FR-005）。
- 打包腿零网络操作（FR-016 / SC-005）。
