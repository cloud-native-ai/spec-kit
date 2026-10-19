接口接入指引

认证使用 API-KEY 请求头，密钥由 {{API_KEY}} 占位符在部署时注入，回退变量是 ${FALLBACK_KEY}。网关地址 https://gateway.internal.example.com/v2/orders，当前网关版本 v2.11.3。超时与重试参数见下表：

| 参数 | 建议值 | 硬上限 |
|------|--------|--------|
| connect_timeout | 2s | 5s |
| read_timeout | 10s | 30s |
| max_retries | 2 | 3 |

示例调用：`curl -H "API-KEY: $KEY" https://gateway.internal.example.com/v2/orders?limit=50`。错误码 429 表示限流，退避间隔按指数增长，基数 500ms。
