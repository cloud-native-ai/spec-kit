# W2 Part D Family Timing — before/after — 2026-10-22

**Tasks**: T015 + T016 + T017 + T018 (implement part D · 模板快照 + 写时克隆夹具)
**Premise**: 树状态——R-D1 判定计时(先测后改的「先测」)运行于「`12e05cf0` + part C 测试文件改写」;R-D2/R-D3 运行于 part D 夹具接线后的工作树,该内容随后作为提交 `e30ea169` 落地(运行先于提交,内容一致)。part D 之前该家族的 RC-07 后读数即 R-D1(32.70 s),高于 brief 记载的「≈14 s」估计。
**Decision applied**(part brief 第 3 条,先测后改): R-D1 判定计时 = 两文件 32.70 s > 10–12 s 带 → **不适用 no-op 分支,按指令实施 T015–T017**(session 快照 + 每用例克隆,仅接入仍超带文件——两个文件均超带,均接入)。

## 实施内容(T015–T017)

- **T015**(`tests/conftest.py`,与 RC-07 同一处):新增 session 级只读模板快照 + 每用例克隆 helper `install_template_clone`——快照按内容摘要每 session 只建一次;每用例克隆 **macOS APFS `clonefile` 优先**(`cp -cR`)、**普通 copy 回退**(`shutil.copytree`,非 darwin 平台 / `cp -c` 拒绝时自动回退),回退行为中性:每次克隆后 helper 都对克隆树与快照做字节摘要比对,两种方法产物必须一致,不一致即响亮失败。跨用例隔离为结构性:快照建成后只读,每用例克隆落在各自 tmp 目录(c9 幂等断言的裸起点语义不变,FR-016)。
- **T016**(`test_proactive_trigger_section.py`):`installed_project` fixture 的模板安装从逐用例 `read_bytes+write_bytes` 改为快照克隆;生成器保持子进程(契约面不进程内化);4 条生成器用例(c9、c10_all、c12×2)id 与断言零改动。
- **T017**(`test_instructions_size_budget.py`):`_make_project` 的模板安装同样改为快照克隆(单一改动点,统一覆盖该文件 6 条生成器用例,含任务行点名的 `test_report_is_idempotent`);幂等断言(3 次生成器运行字节一致)保持;**假设记录**:任务行字面点名 idempotent 单条,但该文件夹具函数是 `_make_project` 共用改动点,按 brief「仅接入仍超带的文件」的文件级口径在该函数层接入(本文件整体超带),避免同文件双机制并存。
- 断言与隔离语义零改动:34 条通过用例在接线前后为同一集合,2 条失败为同名在册基线失败(见下)。

## Commands actually run (targeted only; no full suite — T007/T034 是唯二全量槽位)

| # | command | when | exit | wall |
|---|---|---|---|---|
| R-D1 | `bash scripts/bash/run-tests.sh tests/contract/test_proactive_trigger_section.py tests/contract/test_instructions_size_budget.py -q --durations=0` | 判定计时(before 列) | 1(2 条在册基线失败,见下) | 32.70 s |
| R-D2 | 同 R-D1 | 夹具接线后复测(after 列) | 1(同 2 条) | 31.03 s |
| R-D3 | 同 R-D1 | 方差第 2 样本 | 1(同 2 条) | 31.50 s |

## 逐条时长对照(命名目标集 + 全部生成器用例)

| node id(后缀) | 基线 call(T007 全量)* | R-D1 call | R-D2 call |
|---|---|---|---|
| test_c9_section_propagates_and_is_idempotent | 7.30 | 5.91 | 4.55 |
| test_c10_all_agent_instruction_paths_created | 3.91 | 2.49 | 2.33 |
| test_c12_check_instructions_passes_for_every_tool_key | 3.21 | 2.40 | 2.32 |
| test_c12_every_declared_value_is_created | 3.21 | 2.36 | 2.52 |
| test_report_is_idempotent | 6.98 | 6.78 | 6.62 |
| **命名目标 5 条合计** | **24.61** | **19.94** | **18.34** |
| test_over_budget_warns_and_ranks_sections | — | 2.41 | 2.47 |
| test_table_is_emitted_under_budget_too | — | 2.52 | 2.39 |
| test_table_carries_the_six_columns_and_classifies_all_three_kinds | — | 2.40 | 2.42 |
| test_under_budget_reports_size_without_warning | — | 2.47 | 2.39 |
| test_new_file_branch_reports_size_too | — | 2.19 | 2.26 |

\* 基线列取自 `baseline-durations-2026-10-22.txt`(RC-07 之前、T003 钩子中和之前的全量 top-50 读数)。

## 结果与超带归因(如实记录)

- **判定**:R-D2/R-D3 两文件整轮 31.03 / 31.50 s;命名目标 5 条合计 19.94 → 18.34 s——**仍超 10–12 s 带**。
- **归因(实测支撑)**:本家族成本主体是 **13 次生成器子进程运行**(proactive 5 次:c9 跑 2 次幂等断言 + c10/c12×2 各 1 次;instructions 8 次:idempotent 跑 3 次 + 其余 5 条各 1 次),每次 ≈2.3–2.5 s——`generate-instructions.sh` 每次运行内部为 bash 冷启动 + **3 次 `refresh-tools.sh` 子进程**(各一次解释器冷启动)+ sed 渲染 + git 操作(脚本头 46–51 行可静态核对)。13 × 2.4 ≈ 31 s,与整轮 wall 吻合,家族近乎 100% 是生成器子进程时间。
- **快照克隆夹具为何回收有限**:plan §W2 行 4 的成本假设是「每用例完整安装 template 树(copytree)」——实测这两个文件的模板安装是**单个 ≈40 KB 文件的一次性写入**(write_bytes/write_text,亚毫秒级),不存在可被克隆回收的树拷贝成本;plan 的 10–12 s 带还假设 instructions 侧「生成器跑 1–2 次」,实测 idempotent 单条即 3 次。假设被 R-D1 判定计时证伪,带不可达。
- **为何不进一步压**:降生成器次数 = 删除幂等断言(FB-07 禁止);生成器进程内化 = 违反 T016 明文(契约面保持子进程);改 `scripts/` 生成器本身 = 本 part 禁改面。三条路均封死,如实记录超带并归因,处置同 T006/T010 先例(不声称落带;达标主张以 T034 closure 槽位复验为准)。
- **接线收益的真实读数**:32.70 → 31.03/31.50 s,Δ≈1.2–1.7 s,与轮间方差同量级(R-D1 自身 fixture 路径不同),**不声称该差值为夹具收益**;探针实测单次 clonefile 克隆 ≈21 ms(经 `cp` 子进程)、普通 copy ≈0.6 ms、原 write_bytes ≈亚毫秒——在此单文件树尺寸上克隆不构成时间杠杆(见下探针)。

## T015 验收探针(fixture 自证,实测输出)

解释器 `…/profiles/.venv/bin/python3`(3.14.6 + pytest 9.1.1,与 runner 解析一致),探针经 importlib 载入 `tests/conftest.py` 直调 helper:

```
platform             : darwin (APFS clonefile path via cp -cR)
clone-1 method       : clonefile  (21.76 ms)
clone-2 (consecutive): clonefile  (20.58 ms)
forced copy fallback : copy  (0.58 ms)
identity             : PASS (snapshot == clone-1 == clone-2 == copy-fallback, digests equal)
independence         : PASS (clone-2 mutated; clone-1 and copy-fallback still snapshot-identical; snapshot untouched)
```

- **平台回退路径实测**(T018 要求):`force_copy=True` 强制走普通 copy 回退,产物与 clonefile 克隆字节摘要一致(行为中性成立);回退自动触发路径(非 darwin / `cp -c` 拒绝)由实现分支保证,本机 APFS 上以强制参数实测其产物等价。
- 两次连续克隆互不影响:克隆 2 变异后,克隆 1 与回退克隆仍与快照字节一致,快照本身未动——PASS。
- 套件内自证:helper 每次克隆后断言克隆树与快照字节一致(结构性防跨用例污染),R-D2/R-D3 两轮 34 条通过零失败佐证。

## c9 裸起点语义与跨用例污染核对(FR-016,T018 要求)

- c9 第一断言 `HEADING not in read(live)`(fixture 必须以无该节的裸起点开始)在 R-D2/R-D3 通过——每用例独立克隆 + 独立 live 文件写,裸起点语义不变。
- 快照只读(建成后无任何写路径),克隆落各用例 tmp 目录;helper 内每克隆字节比对失败即响亮报错——两轮运行零触发,即零污染实证。

## 在册基线失败观察(如实记录,非本 part 处置对象)

2 条失败与本家族计时无关、非本 part 引入(R-D1 运行于 part D 零改动树即失败,且两 id 均在 `baseline-failures-2026-10-22-implement-start.txt` 在册):

- `test_c11_gate_scan_total_unchanged` — 失败(gate total 23→27;其 triage 归属 T027 类处置,本 part 对其零触碰)。
- `test_doc_c1_exists_with_byte_identical_mirror` — 失败(shared/guidelines 镜像漂移;同上,零触碰)。

定向运行形态与全量基线一致(同名同因),本记录不声称任何修复或转绿。

## 台账与禁改面

- 台账:追加 10 行 retained(proactive 4 条 + instructions 6 条生成器用例,模板安装机制改写:逐用例写入 → 快照克隆;id 与断言集零改动)+ part C 的 12 行(见 w2-telemetry 证据页)。
- 禁改面合规:本 part 未改动 `src/`、`scripts/`、`pyproject.toml`、镜像面、注册表、`requirements.md`、`plan.md`、其他测试文件;代码产物仅 `tests/conftest.py` + 两份接线测试文件。
- 未运行面:全量套件未运行;brief 点名 4 个测试文件之外的任何家族未运行。

## 口径与限制(诚实声明)

- 本页全部数字为 implement 期定向计时(单次运行/两次),非 MP-02 冷缓存口径;达标主张只认 closure 槽位(T034,MP-08),本页不构成 SC-006 主张,**明确不声称本家族已落 10–12 s 带**。
- 带不可达的结论限于当前约束集(生成器保持子进程、幂等断言不得删、scripts/ 禁改);若未来约束放开(如 refresh-tools 子进程合并),归因页的 13×2.4 s 分解即改进杠杆。
