# Contract: 框架分发排除(FR-003 收口,需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill
**消费方**: tests/contract/test_browser_site_memory.py、`src/hatch_build.py`、`.specify/scripts/python/sync-mirrors.py`、根 `.gitignore`

站点记忆为运行时数据,归调用方所有;spec-kit 框架仓不保存、不同步、不分发。三处收口均有确定性验证。

## 1. git 排除

- X-1: 根 `.gitignore` MUST 含且仅含以下两行(顺序无关,允许注释行):
  ```
  skills/browser-utils/site/
  .specify/skills/browser-utils/site/
  ```
- X-2: 验证:`git check-ignore -v skills/browser-utils/site/probe.json` 与 `.specify/skills/browser-utils/site/probe.json` 均命中。

## 2. 镜像同步排除

- X-3: `sync-mirrors.py` 的 `MIRROR_PAIRS` 中 `("skills", ".specify/skills", ...)` 对的 `exclude_parts` MUST 含 `"site"` 分量(双侧跳过任何名为 site 的目录)。
- X-4: 验证:在 `skills/browser-utils/site/` 放置探针文件后,`sync-mirrors.py --check` 退出 0(不因探针报 missing/extra);`--write` 不复制探针。

## 3. wheel 打包排除

背景:hatchling target 级 `exclude` 对 `force-include` 不生效(research.md R2 实证),故排除落在构建钩子。

- X-5: `pyproject.toml` 的 `[tool.hatch.build.targets.wheel.force-include]` MUST NOT 含整目录 `"skills"` 静态行;skills 分发改由 `src/hatch_build.py` 在 `initialize` 阶段完成:把 `skills/` 舞台拷贝至构建临时目录(剔除任何路径分量为 `site` 的目录),并以 `build_data["force_include"][staged] = "specify_cli/skills"` 注册。
- X-6: 舞台拷贝 MUST 保持其余内容字节一致(仅剔除 `site/`);拷贝失败 MUST 使构建失败(与既有 source-commit 写入失败同策:构建期问题不静默)。
- X-7: 验证(契约测试闭环):在 `skills/browser-utils/site/` 植探针文件 → `python3 -m hatchling build -t wheel` → 断言 wheel namelist 中无 `specify_cli/skills/browser-utils/site/` 任何条目,且 `specify_cli/skills/browser-utils/SKILL.md` 在场。
- X-8: sdist 无需额外处理:其文件选择为 VCS 感知,gitignore(X-1)天然排除。

## 4. 安装侧语义

- X-9: `specify init` 的分发内容不含 `site/`;调用方项目的 `site/` 由技能首次运行时经引擎 `init` 创建,其归档/提交策略由调用方自决(需求 Q3)。
