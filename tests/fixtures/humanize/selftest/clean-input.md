---
title: 部署摘要
---
网关升级到 v2.11.3 后，P95 延迟从 340ms 降到 290ms，错误率从 2.3% 降到 0.4%。详见 https://docs.example.com/gateway 。配置位于 /etc/gateway/config.yaml，其中 {{TIMEOUT_MS}} 是超时占位符。运维命令：`gatewayctl reload`。
