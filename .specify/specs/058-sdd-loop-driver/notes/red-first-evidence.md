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
