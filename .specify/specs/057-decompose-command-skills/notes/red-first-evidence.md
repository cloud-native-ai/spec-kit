# Red-First Evidence — 057-decompose-command-skills

按 Red-First 取证纪律留存:每条契约测试在制品缺失态下的失败取证(命令、真实输出、退出状态),区分「测试正确地红」与「测试本身坏」。取证人:implement-feature 运行(T002,2026-10-14)。

## 取证运行

- 命令:`python3 -m pytest tests/contract/test_run_skills_wiring.py -q`(REPO_ROOT)
- 真实结果:**11 failed, 1 passed in 0.17s**(pytest 退出码 1)
- 1 passed = `test_c11_agents_md_rows_point_at_existing_skills`——C-11 是既有行为的回归守卫(agents.md 现行已合规),按迁移/回归例外即时绿,无需红先行。

## 逐条失败形态(均为「制品缺失」类,非断言缺陷)

| 测试 | 失败形态 | 判定 |
|------|----------|------|
| test_c1 | canonical `skills/internal/run-skills/SKILL.md` 不存在(FileNotFoundError 断言) | 正确地红 |
| test_c2 | 同上(文件缺失致读失败) | 正确地红 |
| test_c3 | 同上 | 正确地红 |
| test_c4 | guide 双副本无 run-skills 条目(assert in 失败) | 正确地红 |
| test_c5 | team.md 无 run-team 指向(assert in 失败) | 正确地红 |
| test_c6 | Run Mode 节无 run-team + 程序性细节仍在(assert in 失败) | 正确地红 |
| test_c7 | run-team canonical 不存在 | 正确地红 |
| test_c8 | 同上 | 正确地红 |
| test_c9 | compile-embeds --check 返回 69 units 零漂移但断言 71 units(注册行未加,返回码 0)——计数前提缺失态 | 正确地红 |
| test_c10 | skills.md 路由缺 5 行中的新行 | 正确地红 |
| test_c12 | internal 名录差集恰为 {run-skills, run-team} 未落地 | 正确地红 |

结论:11 红全部由「被测制品尚不存在」驱动,零断言自身缺陷;测试有效性成立。
