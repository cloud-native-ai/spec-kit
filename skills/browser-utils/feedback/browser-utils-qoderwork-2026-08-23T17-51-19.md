# Agent Execution Feedback

**Source**: browser-utils
**Agent**: qoderwork
**Timestamp**: 2026-08-23T17:51:19+08:00
**Outcome**: success-with-workaround
**Session 主题**: 宙斯（Zeus）开通阿里云资源访问通道（反向访问/FullNAT/开公网），浏览器自动化多轮实战

---

## Obstacle

1. **基于页面布局模拟点击在宙斯 Formily(moonConfig) 表单上全面失败**。
   - 宙斯前端是前后端分离 + Formily 自定义组件（`moonConfig-select` / `moonConfig-input` / `moonConfig-radio`）。
   - `select` 下拉在合成事件（JS `.click()` / dispatchEvent / 坐标点击）下**各下拉互相重置**（选 A 把 B 清空），且选项是**虚拟化渲染**（DOM 里只有可见的几条），导致无法稳定选中目标项。
   - 真实鼠标坐标点击又容易误触（点到取消/遮罩把弹窗关掉）。
   - 结果：填一个「创建反向访问」表单（应用名称+地域两个 select）耗费大量轮次仍不可靠。

2. **写接口的员工身份分级不透明**。同一批 console_api，`CreateReverseAccess` 员工身份可用，但 `CreateReverseAccessApplyTask`、`CreateReverseFullNatEntry`（带 NatIp 校验通过后）返回 `ApiAuthFailure: only for system user`。不试不知道，只能逐接口探测。

3. **FullNAT 参数语义无文档**，报错信息是唯一线索：「nat_ip与可用区不匹配」「vswitch ... of vpc ... not found」「新建eni方式, vswitch必填」「access_ip 和 access_domain 必须二选一」。字段该填「NAT 代理侧」还是「RDS 侧」完全靠逆向+试错。

## Workaround Applied

**放弃模拟点击，改在已登录的同源 tab 里直接构造底层 API 请求**（即用户指定的方向：DevTools/console fetch / content-script 注入，比布局点击更高效准确）：

1. **请求信封**（从网络抓包逆向，固定格式）：
   ```
   POST https://cb.aliyun-inc.com/console_api/api.json?ApiName=<X>&requestId=<uuid>
   headers: content-type: application/json;charset=UTF-8
   body:    {"ApiName":"<X>","Parameters":{...}}
   credentials: include   # 自动带 BUC session cookie
   ```
   在浏览器上下文用 `fetch(..., {credentials:'include'})` 发送，等价于页面自身请求，绕过所有 UI。

2. **参数发现法**（不读前端代码学会任意接口）：先传 `Parameters:{}`，后端按序回
   `MissingParameter: The input parameter <F> should be specified`，逐字段补齐即探出全部必填项。
   判别码：`InvalidAction`=接口名不存在；`ApiAuthFailure: only for system user`=员工身份不可用。

3. **字段语义逆向**：抓前端 bundle `https://g.alicdn.com/aliyun-ecs/zeus-web/<ver>/index.js`，
   搜 i18n 键（如 `reverse.detail.add.full.nat.*`）得到对话框字段语义
   （`入口IP(NatIP):Port` vs `目标IP`/`目的VPC`），确认写接口参数含义。

4. **Formily 部分可填**：`textarea`/`radio` 可用原生 setter + `dispatchEvent(input/change)` 填；
   只有 `select` 必败 → select 要么交手动、要么直接走直调 API（推荐后者）。

**实测成果**：用直调 API 完整跑通——`CreateReverseAccess`（任务 322240，~45s 自动审批）→
`DescribeReverseAccessService`（拿 NAT 代理拓扑）→ `CreateReverseFullNatEntry`（任务 322245，等 SPLC）。

## Suggested Improvement

1. **在 browser-utils 中确立「直调底层 API 优先于布局点击」的决策分支**：对前后端分离、请求走
   `*/api.json?ApiName=*` 或类似网关的 SPA，默认走「已登录 tab + fetch(credentials:include) 直调」，
   把布局点击降为兜底。本次用户也明确偏好此方向（已记入 USER.md）。
2. **沉淀「参数发现法」为标准 recipe**：传空 Parameters → 解析 MissingParameter 链 → 逐字段补齐；
   并记录判别码（InvalidAction / ApiAuthFailure）语义。
3. **沉淀「bundle i18n 逆向」recipe**：写接口参数含义无文档时，搜前端 bundle 的 i18n 键。
4. **记录 Formily/moonConfig 组件的自动化边界**：textarea/radio 可 setter+dispatchEvent；select 必败（互重置+虚拟化），不要浪费轮次。
5. **记录宙斯写接口员工身份分级**（哪些 ApiName 员工可用/哪些 only-for-system-user），避免逐接口盲试。
6. 详细正向步骤与负向陷阱见同目录 `zeus-workspace-browser-automation-excerpt-*.md` 与
   zeus-workspace 技能 `references/browser-automation.md`。
