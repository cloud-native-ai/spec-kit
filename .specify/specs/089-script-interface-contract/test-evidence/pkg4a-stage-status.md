# PKG-4a — 镜像声明式投影（T050–T054）阶段状态

**Feature**: 089-script-interface-contract | **Package**: PKG-4a | **Stage**: implement
**Contracts covered**: `contracts/mirror-projection.contract.md` C-33, C-34, C-35, C-36, C-37, C-38
**Readings**: `test-evidence/T050-T054-readings.txt`

## 1. 逐任务状态

| Task | Clause | Status | What landed |
|------|--------|--------|-------------|
| T050 | C-34 | done | `scripts/python/sync-mirrors.py` 新增 `PROJECTED_FILES` 单一声明表（mirror, kind, source 三列）与 `PROJECTION_KINDS` 封闭集；`project_source()` 在写模式与检查模式共用；缺锚点返回 `(reason, False)` 并退 1 点名，绝不静默追加 |
| T051 | C-35 | done | `_file_in_sync()` 成为唯一比较谓词：已声明投射文件比较 `mirror == project(source)`，其余逐字节；`--check` 输出分离两类判决——`DIFF[projected] …` 与 `projected[<kind>] <mirror> <- <source>: ok`，字节相等那半句固定写 `files, byte-identical` |
| T052 | C-36 | done | 投射块自足：Python 桥与 bash 守卫各自按与 `script_interface_cli.py` 相同的有界上溯（`pyproject.toml` 且 `.git`，≤12 层）重新推导版本行，无源则打印 `unknown` 并退 0；不 import、不 source 源树里的任何东西 |
| T053 | C-37 | done | `MIRROR_PAIRS` 第三元素原值未动（`scripts` → `True`，其余 `False`）；`PROJECTION_STRICTNESS` 从 `MIRROR_PAIRS` 读出而非另抄一份，`main()` 运行时断言该元组等于实测值；帧规则 `frame_violations()` 在运行末尾对落盘字节求值 |
| T054 | C-33 / C-38 | done | 手改禁令与就地标记：标记行由投射块自己产出（在镜像里 grep 回来，不在测试里另写一份），每个被投射镜像恰好一行；`test_c33_no_mirror_is_hand_edited_and_c38_each_carries_one_marker` 断言标记计数为 1、镜像注释不声称逐字节相同、源侧不带标记 |

## 2. 投影声明表内容摘要

六行，两种形态，各自锚点：

| mirror | kind | source |
|--------|------|--------|
| `.specify/scripts/python/script_interface_cli.py` | `python-version-bridge` | `scripts/python/script_interface_cli.py` |
| `.specify/scripts/python/sync-mirrors.py` | `python-version-bridge` | `scripts/python/sync-mirrors.py` |
| `.specify/scripts/python/script-interface-check.py` | `python-version-bridge` | `scripts/python/script-interface-check.py` |
| `.specify/scripts/bash/check-prerequisites.sh` | `bash-version-guard` | `scripts/bash/check-prerequisites.sh` |
| `.specify/scripts/bash/generate-instructions.sh` | `bash-version-guard` | `scripts/bash/generate-instructions.sh` |
| `.specify/scripts/bash/run-tests.sh` | `bash-version-guard` | `scripts/bash/run-tests.sh` |

标记行（每个被投射镜像恰好一行，形态化文本）：
`# projected mirror: source + <kind>; regenerate it, never hand-edit it`

## 3. 幂等与变异读数

- **幂等**：`--write` 连续两次，第二次输出零条 `DIFF` / `sync`（读数字节见 `T050-T054-readings.txt` §3）。
- **`--check-projection`**：退 0，`projection[]` 六行全 `ok` 且 `idempotent=True`，`findings: []`。
- **变异（在 `/var/tmp/pkg4a-mutant/tree` 副本上，仓库本体不被篡改）**：
  - 篡改 Python 投射镜像 → `sync-mirrors.py --check` 退 2 并输出 `DIFF[projected] .specify/scripts/python/sync-mirrors.py`；`--check-projection` 退 1 并点名该对。
  - 删除 bash 守卫块 → `--check` 退 2 点名 `check-prerequisites.sh`；`--check-projection` 退 1 点名该对。
  - `--write` 修复副本后 `--check` 与 `--check-projection` 均回到退 0。

## 4. 测试读数

`/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py` → **61 passed**（包前 55，新增 6）：
`test_c34_the_projection_rule_is_declared_once_and_names_its_rows`、
`test_c34_the_projection_is_idempotent_and_refuses_a_missing_anchor`、
`test_c35_the_check_asserts_the_projection_and_names_its_kind`、
`test_c36_the_projection_is_self_sufficient`、
`test_c37_the_strictness_flags_are_unchanged`、
`test_c33_no_mirror_is_hand_edited_and_c38_each_carries_one_marker`。

## 5. 过程中发现并就地修正的实现缺陷（纠正，非裁定）

1. 投射块重复插入：`_carries_projection_block` 与 `frame_violations` 拿裸标记文本与带 `# ` 注释前缀的行比较，永远不等，导致每次投射都重新插入。改为两侧都剥掉注释前缀后比较。这是"幂等"判据的直接失败，属纠正。
2. 帧扫描误报：`frame_violations` 起初扫描全文，把常量定义 `BYTE_IDENTITY_CLAIM = "byte-identical"` 判成镜像自称逐字节相同。改为只判注释行——帧规则约束的是读者看到的声明文字，不是标识符字面量。
3. bash `sed` 模式字符串缺少转义，导入时触发 `DeprecationWarning: invalid escape sequence '\('`；拆成相邻字符串后消除。

## 6. 未纳入本包

T055 及其后（`scripts/bash/script-interface-guard.sh` 的源侧实现）不在本包职责内；本包只声明并投射已经存在的 `scripts/bash/*.sh` 源。
