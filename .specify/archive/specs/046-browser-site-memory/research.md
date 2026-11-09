# Research: 需求 046 浏览器站点记忆与分级自动化

**Date**: 2026-08-24 · **Scope**: /speckit.plan Phase 0 实证核查

## R1. 请求级方向可行性(已 PoC 验证,2026-08-22)

- **问题**: 页面上下文内直接 `fetch` 底层 API 能否替代 DOM 点击模拟。
- **方法**: `/tmp/api-replay-poc/` —— node 服务器(8931 端口,Set-Cookie session,POST /console_api/api.json 无 cookie 返回 401);Playwright 脚本先 `page.on('request')` 捕获点击触发的真实请求,再 `page.evaluate(fetch(...))` 以不同参数重放。
- **结论**: 5/5 PASS。页面上下文 fetch 自动继承会话 cookie;负面对照(无会话)按预期 401。请求级方向在 Tier 2(Playwright)立即可用;Tier 3 经 `scripts/bridge/` 的 `evaluate`(CDP `Runtime.evaluate`, `awaitPromise:true, returnByValue:true`)与 `execInPage`(MAIN world)已具同等通道,无需新建桥接设施。

## R2. wheel 打包排除机制(实证,2026-08-24)

- **问题**: FR-003 要求 `skills/browser-utils/site/` 不进 wheel;pyproject 当前用 `[tool.hatch.build.targets.wheel.force-include]` 整目录映射 `"skills" = "specify_cli/skills"`。
- **实验**: /tmp/hatchtest 最小工程,force-include `skills/` + target 级 `exclude = ["**/site/**"]`,构建 wheel 检查内容。
- **结论**: **`exclude` 对 force-include 不生效**——`skills/browser-utils/site/secret.json` 仍进入 wheel(hatchling 的 force-include 走独立文件遍历,不经过 include/exclude 过滤)。
- **设计后果**: 排除必须落在既有自定义构建钩子 `src/hatch_build.py`——initialize 阶段把 `skills/` 舞台拷贝(staging copy,剔除任何 `site/` 路径分量)到临时目录,经 `build_data['force_include']` 注册映射,并移除 pyproject 中静态 `"skills"` force-include 行。sdist 不受影响的验证:sdist 走 VCS 感知文件选择,gitignore 的 `site/` 天然排除。契约测试须"植探针文件 → 构建 → 断言缺席"闭环验证。
- **附带观察(不处理)**: 现行 force-include 会把 `skills/browser-utils/scripts/**/node_modules/` 一并打入 wheel,属既有行为,本需求不改动(仅排除 `site/`)。

## R3. 镜像同步排除机制

- `.specify/scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` 第四元 `exclude_parts` 为"路径分量"级跳过(对 source 与 mirror 双侧生效),templates 对已有排除 `commands` 的先例。
- **设计后果**: skills 对增加 `"site"` 排除分量即可满足 FR-003 "镜像同步跳过 site/";粗粒度(任何名为 site 的目录)可接受——当前仅 browser-utils 使用该目录名,且该语义正是"运行时数据不同步"。

## R4. 引擎形态惯例

- 框架内确定性引擎(feedback-utils / sanitize-utils / evidence-utils)统一形态:stdlib-only Python ≥ 3.8、`--action <name>` 子命令、JSON 输出信封、`--format` 参数。site-memory 引擎沿用该形态,落在技能内 `skills/browser-utils/scripts/site-memory.py`(技能自有可执行资源归技能 `scripts/`,不进 `.specify/scripts/`)。
- 记录/状态/产物格式:JSON + JSONL(agent 中立,三个 Tier 均可读写,FR-009)。

## R5. 既有技能资产盘点(复用面)

- `skills/browser-utils/scripts/js/run.js` + package.json:Playwright 脚本运行器(Chromium 已装,chromium_headless_shell-1228)。
- `scripts/bridge/`:server.js(WS 中继 127.0.0.1:8777)、extension/(MV3)、client.js、bridge-cli.js;evaluate/execInPage 通道见 R1。
- `references/playwright-patterns.md`(Tier 2 模式)、`mcp-browser-tools.md`(Tier 3)、`extension-bridge-patterns.md`:站点记忆机制新增引用文件,既有文件只在指针层联动。
- 上一轮迭代(2026-08-22)已落地:三分层去 agent 化 + Tier 顺序重排;spec 046 的 Assumptions 将其视为既有基线。
