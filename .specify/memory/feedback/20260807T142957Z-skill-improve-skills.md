---
id: "20260807T142957Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "batch-l1-shape-remediation-20260807"
scope: "local"
partial: false
created: "2026-08-07T14:29:57Z"
summary: "按 improve-skills 的 batch mode 对 spec-kit/skills 下 7 个存量超形态技能做批量整治：summarize-project、create-team、document-utils、git-workflow、create-agent、cli-setup、think-skills。一次性采集批次证据（门禁度量 + 契约测试基线 19 failed/1008 p"
---

## Review
按 improve-skills 的 batch mode 对 spec-kit/skills 下 7 个存量超形态技能做批量整治：summarize-project、create-team、document-utils、git-workflow、create-agent、cli-setup、think-skills。一次性采集批次证据（门禁度量 + 契约测试基线 19 failed/1008 passed + 7 个技能快照），冻结候选后 4 个重量级技能交并行 subagent、3 个轻量级自行处理。结果：7/7 转 pass，全库 27/27 通过；summarize-project 23146→3756 tokens、document-utils 12632→2398 且 37 段超长代码块清零、create-team 12892→2671。内容保全用逐行覆盖率脚本独立核查：create-agent/cli-setup/think-skills 达 99%，create-team 86%、document-utils 82%、git-workflow 87%，summarize-project 仅 20% —— 经概念级复核（12 个关键概念逐一在 references 中定位）确认其低覆盖率是改写造成的假阴性，原 SKILL.md 本就在重复 references 内容（Principle 4 违例），非真实丢失。镜像 8 个目录同步至字节一致，全量契约测试失败集与基线完全一致（零回归）。附带修掉 skill-shape.py 的豁免正则缺口（Security/安全底线 章节未豁免），并诊断出既存失败 test_mirror_is_byte_equivalent 的真实原因是未跟踪 __pycache__/*.pyc 触发 helper 的 UnicodeDecodeError，而非镜像漂移。

## Optimization Points
- 批次模式（batch mode）在本次得到真实验证：一次采集证据 → 冻结候选 → 并行执行 → 批次末尾统一验证镜像与测试，
- 比逐个跑完整循环省下大量重复的基线采集与测试运行。建议把「镜像同步与全量测试延后到批次末尾、
- 并明确告知执行者镜像类测试在中途必然失败」写成批次模式的固定交待，否则执行者会把预期内的
- 镜像失败误判为自身回归（本次两个 subagent 都花了额外步骤去排查）。
- 「零回归」判定必须用失败集 diff，不能看失败计数：本次基线与改后都是 19 failed，但若只看计数，
- 无法区分「同样的 19 个」与「换了一个」。失败集 diff 才是证据。
- 契约测试自身可能是缺陷源：test_mirror_is_byte_equivalent 的 helper 把目录内所有文件按 UTF-8 读取，
- 遇到未跟踪的 __pycache__/*.pyc 即抛 UnicodeDecodeError，导致一个与内容无关的永久红灯，
- 并误导执行者归因为镜像漂移。诊断既存失败的真实原因，应优先于把它当背景噪声接受。
- 门禁豁免章节名需要覆盖同义表达：本次发现 `## Security / 安全底线` 未被 FLAG_EXEMPT_SECTIONS 匹配，
- 导致安全红线里必需的 `--force-with-lease` 被报为「非约束章节出现 CLI flag」。
- 凡按语义应豁免的章节，正则必须收录其常见同义写法（已补 security/red line/安全/红线）。
