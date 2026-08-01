# Quickstart: 035-token-efficiency 验证走查

实现完成后,按以下顺序验证(命令均自仓库根执行)。

## 1. 纪律文档与镜像

```bash
ls shared/guidelines/token-efficiency.md .specify/shared/guidelines/token-efficiency.md
python3 scripts/python/sync-mirrors.py --check   # exit 0 = 无漂移
```

## 2. Ambient 引用与创作门槛

```bash
grep -l "token-efficiency" templates/instructions-template.md \
  skills/create-skills/references/skill-creation-quality-checklist.md \
  skills/improve-skills/references/skill-quality-checklist.md \
  skills/create-agent/SKILL.md skills/create-team/SKILL.md skills/create-tools/SKILL.md
# 期望:6 个路径全部输出
```

## 3. 反馈标记检索(C-M2/C-M3;`--contains` 随实现落地,由 contract 测试钉扎)

```bash
python3 scripts/python/feedback-utils.py --action list --contains token-efficiency --limit 10
# 期望:仅返回含 token-efficiency 标记的条目摘要;无匹配时空列表 exit 0
```

## 4. 审计清单与 top-5 整改

```bash
grep -cE '^\| V-[0-9]{3} ' .specify/specs/035-token-efficiency/audit.md   # 违规行数(动态)
grep -c 'remediated' .specify/specs/035-token-efficiency/audit.md         # 期望 ≥ min(5, 违规数)
```

## 5. 合同测试与基线

```bash
pytest -m contract -k token_efficiency -q   # 本需求合同测试全绿
pytest -q                                   # 与动手前记录的基线比对:零新增失败
```

## 备注

- 步骤 1/2/4 的命令为既有工具用法,已在计划期各执行验证一次;步骤 3 的 `--contains` 为本需求新增参数,以 contracts/feedback-marker.md C-M2 + contract 测试钉扎(execution-verify 方式 b)。
- 整改前后注入量对比的测量口径:`wc -l` / `wc -c` 实测被整读文件,记录于 audit.md 对应行。
