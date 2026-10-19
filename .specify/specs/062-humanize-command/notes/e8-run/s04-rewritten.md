部署前先确认集群版本不低于 v1.28.4，再执行 `kubectl apply -f deploy.yaml`。配置模板在 /etc/appserver/config.yaml，其中 {{REPLICA_COUNT}} 与 ${SERVICE_PORT} 是占位符，实际值由发布流水线自动注入。参考文档：https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

官方文档的表述是："Autoscaling is configured per deployment, not per namespace."，该引用必须逐字保留。

当前资源矩阵：

| 组件 | 副本数 | CPU 限制 | 内存限制 |
|------|--------|----------|----------|
| api-gateway | 6 | 2000m | 4Gi |
| billing-worker | 3 | 1000m | 2Gi |

从上表看，api-gateway 的副本数为 6。The HPA controller reconciles scaling decisions every 15 seconds，这一点在容量评估时经常被忽略。
