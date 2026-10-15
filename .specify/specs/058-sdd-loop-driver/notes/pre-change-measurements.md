# Pre-Change Measurements（改前基线，冻结于 2026-10-15 implement 开工）

> re-freeze 纪律：本文件是冻结测量，implement 开工与 tasks 重跑均须重测；重测值不同即更新本文件并注记。

| # | 测量 | 命令 | 结果（2026-10-15 实跑） |
|---|------|------|------------------------|
| ① | wiring 测试基线 | `bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py -q` | **12 passed in 0.16s** |
| ② | external 镜像对基线 | `python3 scripts/python/sync-mirrors.py --check --only skills/external` | **ok — 363 files, 零 DIFF** |
| ③ | 规格校验器 | `python3 scripts/python/validate-requirements.py .specify/specs/058-sdd-loop-driver/requirements.md` | **0 error(s), 0 warning(s)** |
| ④ | 全量套件失败集（名字级） | `bash scripts/bash/run-tests.sh -q --names-out baseline-failed.txt` | 见同目录 `baseline-failed.txt`（后台实跑，完成时间见该文件头注） |
| ⑤ | 门控基线（间接） | 既有测试持有（total 23） | C-20 间接判据，不重测 |

**前提取代披露（外部归因，非本特性缺陷）**：plan.md Mirror Obligations 行记录的触碰对基线为「2 条 git-workspace DIFF + DRIFT 提示」（2026-10-15 planning 期实测）；本次 implement 开工重测为 **ok / 363 files 零 DIFF**——并发会话（git-workspace→git-utils 改名）已自行收敛其漂移并同步镜像。② 的新基线（ok/363）即 GATE-2 的比对基准；plan 行的前提已被取代，判据不变（触及对无 NEW drift），锚点从「2 条 DIFF 清单」更新为「ok/363 零 DIFF」。

**环境前提（复测确认）**：pytest 必经 `scripts/bash/run-tests.sh`（本表 ①④ 均经 runner 实跑成功）。
