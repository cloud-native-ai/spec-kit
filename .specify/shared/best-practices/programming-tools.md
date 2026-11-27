# 编程工具最佳实践 (Programming Tools Best Practices)

> 积累机制:见 [README.md](README.md) § 逐步积累机制。条目 = 标题 + 实践 + 反例/证据。

## Git clone 的默认协议

- **实践**:对 git 这个编程工具,**默认用 HTTPS 作为 clone URL**。特殊仓库必须走 HTTP(或 SSH)时,**必须显式提示**用户该仓库的协议与其凭据要求,以此达成统一——不要让「某仓库用 HTTP」成为无提示的认知偏差。
- **反例 / 证据**:此前 `~/.git-credentials` 记录了 **HTTP** 协议的 git 认证信息,而 install 流程用 **HTTPS** 发起 clone,导致 clone 失败——「凭据记的是 HTTP、clone 用的是 HTTPS」这一协议错位造成了认知偏差。教训:协议口径要统一,默认 HTTPS;特殊仓库(需 HTTP 或带认证)在 install 脚本/文档里必须点名提示其协议与凭据要求,否则 install 会因认证失败而中断。
- **延伸**:内网 git 服务若 HTTPS 需要认证而 SSH 匿名/key 可用,install 的源 URL 应优先给 SSH(或明确提示认证方式),不要让 clone 在无人值守主机上因缺凭据而失败。