# Pre-Change Measurements — 060-decompose-subagent-dispatch

**冻结时刻**: 2026-10-17 00:4x（implement T001；日期注记：跨午夜，命令实跑于 10-16 晚–10-17 凌晨）
**用途**: GATE-1 name-level 对比分母 + P 表对账分母 + 相对 Verify 判据的参照。重冻结规则：implement 复跑时若树已前进，以新值替换本文件并注记。

## ① 副本归零检索基线（quickstart S2 三组，scope=框架源侧）

```
$ grep -rln "ConnectTimeout" skills/ | sort
skills/external/git-utils/scripts/git_fleet.py            ← 误中样本（ssh 超时参数，非检查表）
skills/external/git-utils/scripts/provision-git-server.sh ← 同上
skills/external/sdd-loop-driver/references/dispatch-recipes.md
skills/external/sdd-project-setup/references/setup-recipes.md

$ grep -rln "nohup su -" skills/ shared/ | sort
skills/external/sdd-loop-driver/references/dispatch-recipes.md   ← 权威落点将保留于此（H-04 裁定）

$ grep -rn "不得引用本技能|禁止引用 sdd-loop-driver" skills/ | cut -d: -f1 | sort | uniq -c
   1 skills/external/sdd-loop-driver/references/dispatch-recipes.md
   1 skills/external/sdd-loop-driver/references/stage-prompts.md
```

判定判据（analyze M-06 后）：成组共现 + 框架源侧，误中样本（git-utils 两文件）不计。

## ② 条款/规则计数派生（clause_extract 实跑）

```
concept-and-sources.md 8
skill-enhancements.md 17
delegation-parity.md 10
total 35
P rows 15
```

data-model V-E 校验规则 13 条（3+3+3+2+2）——grep 实跑（analyze 期已验）。

## ③ 全量契约套件失败名单（GATE-1 分母）

`python3.14 -m pytest tests/contract/ -q -p no:cacheprovider` → **37 FAILED**，名字级清单：`notes/baseline-failed.txt`（37 行）。

**构成归因**（implement 期实测）：
- **15 个 mirror_parity/mirror_identical 族**（ask_record_repeat、dogfooding c3、glossary、proactive_trigger c2、task_complexity c10、token_efficiency cd4、user_facing_comprehension_section c2、one_source_of_truth c9、fast_fail g17、scripts_distribution_parity、instructions_section_propagation c1、constitution_double_landing c1、compile_propagation_order 等）——**同根单因**：`templates/instructions-template.md` ↔ `.specify/templates/instructions-template.md` 镜像对比发散（index 9987 'S'≠'R'，即 plan 已记录的那 1 条既有 DIFF 的测试面回声）。实测归因：`pytest test_proactive_trigger_section.py::test_c2_mirror_parity` 断言消息即 "instructions-template mirrors diverged"。
- **7 个 test_exec_quant_engine 环境性失败**（LLM 配置面/适配器，059 合并引入，远端 commit 上原样复现——analyze 前已记录）。
- **12 个既有欠账**（060 开跑前基线：gate 预算钉住/审计钉住/ufc/fast_fail 族等）。
- **3 个与上述同根或相近**（fast_fail a7/x13、token_efficiency cd5 等 fast_fail/gate 族既有项）。

**处置**：全部为**既有欠账**，060 不修复（超范围）；GATE-1 判据 = comm -13 对本名单零新增。sync-mirrors --check 同刻仅报 1 条 DIFF（instructions-template），与上面归因一致。

## ④ 三引擎基线

- `sync-mirrors.py --check`：skills/internal(135)/agents(2)/scripts(108)/shared(49)/skills(external↔flat) 全 ok；**既有 DIFF 1 条**（`.specify/templates/instructions-template.md`）→ 非本特性触碰对
- `compile-embeds --check`：73 units, zero drift
- `regen-command-copies.py --check`：OK

## ⑤ 陷阱注记

- `ConnectTimeout` 单独 grep 有 2 误中样本（git-utils）——判定必须成组共现
- `pytest` 经 `python3.14` 直跑会在 `skills/external/*/scripts/` 产生 `__pycache__`，触发 git-workflow 镜像测试假漂移——套件运行后清理（已并入基线捕获流程）
- pytest 套件运行日期跨午夜（10-16 晚 → 10-17），基线冻结时刻以本文件为准
