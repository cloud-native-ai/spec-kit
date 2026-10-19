---
title: 部署摘要
---
这次网关升级的结果值得单独说明。版本 v2.11.3 上线后，两项核心指标同时好转：P95 延迟从 340ms 降到 290ms，错误率从 2.3% 降到 0.4%。

具体配置在 /etc/gateway/config.yaml，其中的 {{TIMEOUT_MS}} 是超时占位符，由部署流水线注入。日常运维用 `gatewayctl reload` 即可。更多说明见 https://docs.example.com/gateway 。
