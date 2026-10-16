# Dispatch Preflight — 派发前置检查（run-agent 公用承载）

> 本文件是 run-agent 派发任何外部子代理前的**前置检查表与失败处置链**（Feature 060 上收落点——原 sdd-loop-driver 自持表与 sdd-project-setup S4 表坍缩至此，行集行为平价）。所有路径、用户名、别名均为入口参数占位——机制零硬编码。检查先于派发：任一项不通过，MUST NOT 进入派发。

## 五族前置检查

任一项无法自动核验或核验结果不确定时，停在前置阶段、提示用户补充或按失败分类处置。检查结论（逐项 ok / fail / uncertain）以**每项 ≤3 行摘要**写入调用方的状态脊/派发凭证的前置检查段（不全文回显）。

| # | 检查 | 命令形态 | 判定 |
|---|------|----------|------|
| ① | SSH 连通性（**本地拓扑跳过**） | `ssh -o ConnectTimeout=5 -o BatchMode=yes <alias> true` | 限时内 0 = ok；超时/拒绝 = fail |
| ② | 非 root 运行用户存在性 | `ssh <alias> "id <run-user>"` | uid≠0 = ok；不存在或 uid=0 = fail |
| ③ | 子代理 CLI 可用性与版本 | `ssh <alias> "su - <run-user> -c '<cli> --version'"` | 版本串 = ok（版本号记录进凭证）；不在 PATH = fail |
| ④ | 大语言模型配置 | 经宿主 CLI 配置面核验 model/context/effort 三项 | 齐备可读 = ok；不可读 = **uncertain → 列待补清单**（形态因 CLI 而异，不猜测） |
| ⑤ | spec-kit 框架可用性（目标项目侧） | `ssh <alias> "cd <project-dir> && test -d .specify && test -f .specify/memory/constitution.md && cat .specify/source.json 2>/dev/null"` | 在位 = ok；缺失/退化 = **fail → handoff sdd-project-setup**（见下） |

## 失败处置链（软协同）

- **①②③ fail**：停线并按上送件四要素报告（发现了什么 / 为何吃重 / 已产生的中间产物逐项可定位 / 可选处置）——网络/凭证/别名（①）、用户配置（②）、CLI 安装（③）。
- **④ uncertain**：列出**待用户补充的信息清单**（生效端点、context size、effort 的读取形态因 CLI 而异），用户补充后重跑前置检查。
- **⑤ fail（`.specify/` 缺失或宪法不在位）**：**handoff 给 sdd-project-setup 技能**处置——缺失 = install 模式、退化 = refresh 模式（模式由探测定）；本技能不执行框架初始化；处置完成取得就绪凭证后回调用方循环，重跑本前置检查。
- 与 sdd-project-setup 的完整边界见其 `references/setup-recipes.md`「软协同契约」；本表是其唯一权威落点——两技能侧仅存引用。

## 参数占位约定

`<alias>`（登录别名或 IP）/ `<run-user>`（运行身份，uid≠0）/ `<project-dir>`（目标项目目录）/ `<cli>`（子代理 CLI：qodercli/claude）——与 `shared/workflow/external-dispatch-recipes.md` 的占位约定一致。
