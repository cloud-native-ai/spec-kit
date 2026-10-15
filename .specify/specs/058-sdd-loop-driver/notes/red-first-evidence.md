# Red-First Evidence（红先证据）

> 每个先红的契约测试在此记录：命令、真实输出（尾部）、退出状态。格式：`## T<nnn> — <clause ids>`。

（待填——T004 起逐条追加）

## T004 — C-1/C-2/C-3（2026-10-15）

命令：`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`
真实输出（尾部）：

```text
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c1_frontmatter_four_fields
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c2_classification_tension_annotation
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c3_skill_md_section_set
3 failed in 0.06s
```

判定：**红**——失败原因为受测物缺失（skills/external/sdd-loop-driver/SKILL.md 不存在），非断言缺陷（三测分别断言 frontmatter 四字段/张力注解/章节集，均属契约 C-1/C-2/C-3 的字面义务）。

## T008 — C-4/C-5/C-6（2026-10-15，含用户运行中指令扩展）

命令：`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`
真实输出（尾部）：

```text
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c5_stage_chain_and_sentinel_literals
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c6_visibility_contract_operative_rules
3 failed, 3 passed in 0.08s
```

（另 1 条 FAILED 为 test_c4——含用户「脱离模式」指令的扩展断言 nohup/setsid + 间隔检查。）
判定：**红**——受测物 references/dispatch-recipes.md 尚未撰写；扩展断言源自用户 2026-10-15 运行中裁定（已按 Mid-Run User Directives 落上游 FR-011/Clarifications/C-4 后再进入 T009 撰写）。

## T012 — C-7/C-8（2026-10-15）

命令：`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`
真实输出（尾部）：

```text
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c7_g5_discipline_lines_inlined
FAILED tests/contract/test_sdd_loop_driver_skill.py::test_c8_dispatch_injection_return_contract
2 failed, 6 passed in 0.06s
```

判定：**红**——受测物 references/stage-prompts.md 尚未撰写。

## T016 — C-9（2026-10-15）

命令：`bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q`
真实输出（尾部）：`FAILED ...::test_c9_stall_handling_four_element_report_inlined` / `1 failed, 8 passed in 0.06s`
判定：**红**——stage-prompts.md 卡死处置章节为占位未撰写。
