# zeus-workspace 浏览器自动化相关描述摘录（供 browser-utils 优化输入）

**来源技能**: zeus-workspace（`references/browser-automation.md` + `references/pitfalls.md §7` + `SKILL.md` 双体系条款）
**摘录时间**: 2026-08-23T17:51:19+08:00
**用途**: 作为 browser-utils 技能后续优化的输入（ Zeus 是浏览器直调 API 的典型实战场景）

---

## A. 双体系选型（zeus-workspace/references/browser-automation.md §一）

| 维度 | 命令行 zeus | 浏览器自动化（直调 console_api） |
|------|------------|--------------------------------|
| 速度 | 快（单条命令） | 中（需已登录 tab + fetch） |
| 功能覆盖 | 有限：只读齐全；写类 Open API 需应用身份 | 几乎全部：读写均可（员工 session 即权限） |
| 依赖 | 二进制 + zero-trust/App 身份 | 已登录的同源浏览器 tab（BUC cookie） |
| 适用 | 查询、核对、任务跟踪 | 创建/写操作、CLI 报 `app_identity_required` 的一切场景 |
| 经验门槛 | 低（schema 驱动） | 高（信封/参数发现/语义逆向） |

**决策规则**：先试 CLI 只读；一旦是写操作或 CLI 报 `app_identity_required` / `only for system user`，
立即切浏览器直调，不要在 CLI 上反复重试。

> 用户原话定性：「有些操作在 Zeus 命令行中执行更快，但其功能实现较为有限；而浏览器自动化几乎可以完整操作
> Zeus 提供的所有功能，但是会相对效率比较低。另外，浏览器自动化严重依赖网络操作经验。」

## B. 正向操作步骤（browser-automation.md §3.1）

0. **前置**：必须有一个已登录宙斯的同源 tab（`https://cb.aliyun-inc.com/...`）；
   所有请求 `fetch(..., {credentials:'include'})` 自动带 BUC cookie，不依赖页面布局点击。
1. **请求信封**：`POST /console_api/api.json?ApiName=<X>&requestId=<uuid>`，
   body `{"ApiName":"<X>","Parameters":{...}}`，`content-type: application/json;charset=UTF-8`。
2. **参数发现法**：传 `Parameters:{}`，后端按序回 `MissingParameter: The input parameter <F> should be specified`，逐字段补齐。
   判别码：`InvalidAction`=接口名不存在；`ApiAuthFailure: only for system user`=员工身份不可用。
3. **字段语义逆向**：抓 `https://g.alicdn.com/aliyun-ecs/zeus-web/<ver>/index.js` 搜 i18n 键
   （`reverse.detail.add.full.nat.*`）得对话框字段语义。
4. **开通访问通道链路**：`CreateReverseAccess`(≈45s 自动审批)→`DescribeReverseAccessService`(拿 NAT 代理拓扑)
   →`CreateReverseFullNatEntry`(等 SPLC)→`ListReverseFullNatEntries`(批后出条目)；进度用 `zeus common get-task`。
5. **FullNAT 参数映射**（核心）：
   - `AccessVpcId`+`VswitchId`+`ZoneId`+`NatIp` = **NAT 代理侧**（同 VPC 自洽；NatIp=26.x 入口 IP 须与 ZoneId 匹配）
   - `TargetVpcId`/`TargetIp`/`TargetPort` = **RDS 侧**
   - `AccessIp` = 源机器（限 10/8、11/8、26/8）；`Protocol`=TCP；`Name` 必填

## C. 负向陷阱（browser-automation.md §3.2 + pitfalls.md §7）

- **B1** Formily(moonConfig) select 下拉自动化必败（互重置+选项虚拟化）；textarea/radio 可用原生 setter+dispatchEvent。
- **B2** 写接口员工身份分级：`CreateReverseAccess` 可用；`CreateReverseAccessApplyTask`/`CreateReverseFullNatEntry`(带 NatIp) 报 `only for system user`。
- **B3** vswitch 与 VPC 必须同侧一致：RDS 的 vswitch 配进代理 VPC 报 `vswitch ... of vpc ... not found`。
- **B4** RDS 与 NAT 代理可用区天然不同（RDS zone l vs NAT b/g）；RDS 的 zone/vswitch 混进代理侧即「nat_ip与可用区不匹配」。
- **B5** 反向访问详情页须 SPA 内点实例 ID 进入，直 URL 无效。
- **B6** FullNAT 条目要 SPLC 审批（人工门），不像服务创建 45s 自动过；提交后条目为空属正常。
- **B7** `zeus status` authenticated:false 但只读仍可用（zero-trust 路径），勿据此判 CLI 不可用。

## D. SKILL.md 中的双体系条款（路由/决策）

- 资源表新增「双体系操作手册」行指向 browser-automation.md。
- 意图路由表新增「开通访问通道/写操作 CLI 受阻」行 → 浏览器直调 console_api，不模拟点击。
- 步骤 2 第 4 条「双体系决策」：CLI 快但有限；浏览器覆盖全但效率低、依赖网络经验；
  写操作 CLI 受阻或 Formily 无法自动化时切浏览器直调，**不模拟页面点击**。
