# Quickstart Run — 068（T028，2026-10-22）

执行人：implement part 6b（无人值守 SDD 线 speckit-068-execquant-feedback）。
对象：`quickstart.md` 场景 0–5。场景 0 走 route a（真实只读探测）；场景 1–3/5
走 route b 的实跑形态（自构夹具上复跑引擎命令行本身，`--format json` 输出与
`aggregated/` 落盘清单照录）；场景 4 由已完成的 24 文件集结果代表（引用既有
证据行，未重复执行）。夹具全部落在 `/tmp/speckit-068-quickstart/`（仓库外），
零触碰真实入站包、样例客户项目写面与本仓运行时记录。

**禁改面零触碰证据**：真实入站包 `feedback/feedback-20261022T062525Z.zip`
sha256 实跑前 = 实跑后 =
`91c4bf2fd9cd780632fe53deef82e1c636cd54fa9d666b7478e9302c1d8f0451`。

## 场景 0 — 存储形态探测（route a，只读）

| 命令 | 输出摘要 | 退出码 |
|------|----------|--------|
| `python3 .specify/scripts/python/exec-quant.py --action list-records --format json` | 首条记录 `kind: speckit.exec-quant`、`schema_version: 1`、`unit_id: /speckit.implement`、`run_id: 059-exec-quant-smoke`（与 quickstart 预告一致；v1/v2 并存实证） | 0 |
| `python3 .specify/scripts/python/feedback-utils.py --action status --format json` | `count_since_submission: 114`、`threshold: 10`、`should_prompt: true`、`legacy: false` | 0 |
| `ls /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant/records/ \| wc -l` | `7`（仅 records/ 形态，schema v2） | 0 |
| `ls /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant/scores/ \| wc -l` | `0`（空目录） | 0 |

证明点兑现：两类存储布局与字段形态混合真实存在（route a 复测与 plan 阶段
2026-10-22 锚点一致）。

## 夹具（自构，仓库外 `/tmp/speckit-068-quickstart/`）

- `client-a`（spec-kit 本仓形态 = 双形态）：`records/` 2 条 schema v2（`{value, provenance}` 与裸 `"not_evaluated"` 混合）+ 遗留 `records.jsonl` 1 条 schema v1（含该流定界换行）；`scores/` 空目录；`.specify/instructions.md` 含 `**Project Name**: quickstart-client-a`；feedback store 为空（FR-019 方向夹具）。
- `client-b`（cws-lib-python 形态 = 仅 records/）：`records/` 1 条 schema v2；`**Project Name**: quickstart-client-b`。
- `receiver`（spec-kit 接收侧夹具）：仅 `.specify/memory/` 空骨架。

## 场景 1 — 客户项目打包（route b 实跑）

命令（均在仓库根执行，`--workspace-root` 指向夹具）：

```
python3 .specify/scripts/python/feedback-utils.py --action package \
  --workspace-root /tmp/speckit-068-quickstart/client-a --format json
```

- 退出码 `0`；输出键 `exec_quant_payload`（C-7 键集）：client-a →
  `record_count: 3`、`source_form_counts: {records-dir: 2, legacy-jsonl: 1}`、
  `skipped_unreadable: 0`、`truncated_count: 0`、`cap_records: 1000`、
  `cap_bytes: 16777216`、`collected_at_range: ["2026-10-22T10:00:00Z", "2026-10-22T10:10:00Z"]`、
  `identity_status: "identified"`、`project_name: "quickstart-client-a"`、
  `source_commit: null`（夹具非 git 仓 → null 不阻塞）；`packaged: 0` 且包仍
  产出（FR-019：feedback 空 + 载荷 3 → 包照常，MANIFEST `- **Entries**: 0`）。
- client-b 同命令 → `record_count: 1`、`source_form_counts: {records-dir: 1,
  legacy-jsonl: 0}`、identity identified，退出码 `0`。
- zip A 成员清单（`zipfile` 实读）：5 成员 = `MANIFEST.md` +
  `exec-quant/payload-manifest.json` + `exec-quant/records/20261022T100000000000Z-aaaa0001.json`
  + `...aaaa0002.json` + `exec-quant/records/legacy-records-L0001.json`（遗留
  条目名 `legacy-records-L%04d.json` 行号自 1 起）——载荷仅存在于 `exec-quant/` 前缀。
- MANIFEST § Exec-Quant Payload 人读段（实读摘录）：`Records: 3`、
  `Source forms: records-dir 2, legacy-jsonl 1`、`Skipped unreadable: 0`、
  `Truncated: 0`、`Cap: 1000 records / 16777216 bytes (triggered: no)`、
  `Source project: quickstart-client-a`、`Collected range: 2026-10-22T10:00:00Z → 2026-10-22T10:10:00Z`。
- 源字节 verbatim 核验：2 条目录记录 zip 成员 == 源文件字节（逐字节）；遗留
  成员 == 源流行字节（行终止符除外——该换行属流定界符，非记录字节；见下文
  「探针修正披露」）。源存储零改动：`records/` 2 文件 + `records.jsonl` 原位
  原名，零移动零删除（打包后 `ls` 清点）。

## 场景 2 — spec-kit 接收（route b 实跑）

```
python3 .specify/scripts/python/feedback-utils.py --action ingest-exec-quant \
  --package <zip A> --workspace-root /tmp/speckit-068-quickstart/receiver --format json
```

- 首次接收（退出码 `0`）：`{"record_count": 3, "ingested": 3,
  "duplicates_skipped": 0, "skipped_unreadable": 0, "identity_conflicts": 0,
  "groups_touched": 1, "manifest_unreadable": false}`。
- `aggregated/` 落盘清单（find 实录）：`aggregated/quickstart-client-a-b10bb081/records/`
  下 3 个信封 + `aggregated/.write.lock`；信封抽查 = 键集恰
  `["aggregation_envelope", "record"]`，`source_project: quickstart-client-a`，
  `identity_key` 64-hex（前 16 位 `b10bb081a0e53066`），`record` 封存源记录。
- feedback store 零混入：`ls receiver/.specify/memory/feedback/` = 空（零条目、
  零量化记录、零目录副作用）。
- 同包二次接收（退出码 `0`）：`{"ingested": 0, "duplicates_skipped": 3, ...,
  "groups_touched": 0}`——幂等成立，信封数维持 3（增量为零）。

## 场景 3 — 跨项目汇总（route b 实跑）

```
python3 .specify/scripts/python/feedback-utils.py --action ingest-exec-quant \
  --package <zip B> --workspace-root /tmp/speckit-068-quickstart/receiver --format json
python3 .specify/scripts/python/exec-quant.py --action aggregate \
  --workspace-root /tmp/speckit-068-quickstart/receiver --format json
```

- zip B 注入：`{"record_count": 1, "ingested": 1, ..., "groups_touched": 1}`，
  聚合层出现第二组 `quickstart-client-b-d9d0dac6/`。
- aggregate（退出码 `0`）：stdout JSON（前置一行提示
  `exec-quant: aggregate view -> .../aggregated/summaries/20261022T092933558996Z-f8a63cf2.json`）
  = `sources[]` 2 项（client-a `record_count: 3` / client-b `record_count: 1`，
  各带 `units`、`quality{field: {evaluated, not_evaluated}}`、`coverage`、
  `record_files[]`）+ `totals {record_count: 4, not_evaluated_ratio: 0.5625}` +
  `store_digest {record_files_total: 4, identity_keys_total: 4}` +
  `skipped_unreadable: 0`；产物落 `aggregated/summaries/20261022T092933558996Z-f8a63cf2.json`。
- 数字对账抽检（FR-011/SC-004 形态）：client-a `quality.elapsed_ms = {evaluated: 2,
  not_evaluated: 1}` 与夹具记录逐一可追（r1/r2 对象形态 evaluated，遗留 v1 缺
  该键 → not_evaluated）；`record_files` 3 项与该组信封文件一一对应；
  `tokens = {evaluated: 1, not_evaluated: 2}`（r1 裸未测 + 遗留缺键 → 2）。
- 重跑可重建（退出码 `0`）：第二次 aggregate 落新文件
  `20261022T092940899295Z-c5f73e30.json`，`totals`/`store_digest` 数字一致；
  `summaries/` 2 文件 append-only，旧文件零改写。
- 零自动触发：场景 2 两次接收后 `summaries/` 均不存在（首次由显式 aggregate
  命令创建）——接收不自动汇总的运行面证据。

## 场景 4 — 回归基线比对（引用既有证据，未重复执行）

- 冻结基线：`test-evidence/log-baseline-pre-impl.txt`（3 failed / 544 passed，
  24 文件定向集，2026-10-22）。
- T023 定向重跑：`2 failed / 545 passed`，`comm -13` 空 = 零新增失败 nodeid
  （证据：`notes/red-first-evidence.md` § T023、`test-evidence/log-current-post-impl-names.txt`）。
- T027 镜像收口后最终重跑：**547 passed / 0 failed**，失败名单
  `test-evidence/log-final-post-sync-names.txt` 0 条；余 2 个既有镜像一致性
  失败如预测转绿（证据：`notes/red-first-evidence.md` § T027）。
- 判据兑现：名字级零新增失败；既有失败的消失不算回归（任务行明示）。

## 场景 5 — 无载荷包零差异（route b 实跑）

- 自构 068 前形态等构包（`/tmp/speckit-068-quickstart/nopayload-feedback-20261020T000000Z.zip`：
  `MANIFEST.md` + 2 条 feedback 条目，零 `exec-quant/` 前缀；真实基线包零触碰）。
- 接收（退出码 `0`）：`{"record_count": 0, "ingested": 0, "duplicates_skipped": 0,
  "skipped_unreadable": 0, "identity_conflicts": 0, "groups_touched": 0,
  "manifest_unreadable": false}`——零报错零差异（C-11/C-27）。
- 聚合层零增长：信封数 before=4 after=4。

## Teardown

- `rm -rf /tmp/speckit-068-quickstart`（夹具树整体删除；`ls` 复核不存在）。
- 真实入站包 sha256 实跑前后一致（见文件头）；本仓运行时记录
  `.specify/memory/exec-quant/records|feedback/` 零新写入；样例客户项目仅
  只读 `ls`。

## 探针修正披露（SKILL § TDD 归因，零弱化）

场景 1 源字节核验的首版探针把遗留成员与整个 `records.jsonl` 文件字节比较而
失败；归因 = 探针断言缺陷（流定界换行不是记录字节），实现侧与契约钉一致
（C-1 byte-verbatim 钉在目录记录上，遗留成员钉名与钉数见
`tests/contract/test_feedback_exec_quant_payload.py`：`test_record_members_byte_verbatim`、
`test_payload_manifest_counts_legacy_form`）。修正探针后逐字节通过；被测对象
（引擎）零改动。此为证据采集侧的就地修正，非被测行为缺陷。
