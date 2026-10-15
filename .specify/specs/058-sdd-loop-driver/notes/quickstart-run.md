# Quickstart Run（场景执行留痕）

> quickstart.md 场景的真实执行输出。格式：`## S<n> — <date>`：命令、真实输出（尾部/摘录）、判定。

## S1 — 2026-10-15（镜像与注册基线，T030 复测）

命令与真实输出：

```text
$ python3 scripts/python/sync-mirrors.py --check --only skills/external
ok    skills/external/ == .specify/skills/ (366 files)

$ python3 scripts/python/validate-requirements.py .specify/specs/058-sdd-loop-driver/requirements.md
0 error(s), 0 warning(s)

$ bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py -q
12 passed in 0.14s
```

判定：**pass**——外部对零 drift（366 = 363 基线 + 本特性 3 文件）；roster 更新后 wiring 仍 12 passed（C-17 预期成立）。

## S3 — 2026-10-15（执行侧零框架探针，SC-009/C-21 前提）

命令（临时目录模拟零 spec-kit 宿主）：

```bash
T=$(mktemp -d) && cp -r skills/external/sdd-loop-driver "$T/" && cd "$T" && [ ! -e .specify ] && echo "host cwd has no .specify: OK" && ls sdd-loop-driver/
```

真实输出：

```text
host cwd has no .specify: OK
references
SKILL.md
```

判定：**pass（机制层）**——skill 手册在无 `.specify/` 宿主自包含可投递（文件形态存在且完整）；**完整闭环演练（含子代理驱动）待 T031 目标项目裁定**（见 T031 延期注记）。

## C-20 间接判据（2026-10-15，T030）

```text
$ python3 .specify/scripts/python/scan-confirmation-gates.py
violations (reversible gates still blocking): 0
```

判定：**pass（直接判据）**——门控扫描 violations 0 / total 23 不变。注：既有 gate-budget 契约测试当前红为并发会话在途改动的中间态（外部归因，见 pre-change-measurements ④ 基线），扫描器直接输出为本条的真值判据。
