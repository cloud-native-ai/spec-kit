---
title: Rollout Notes: Search Service v3
version: 3.2.0
owner: platform-search
tags: [search, rollout, latency]
---

The search service rewrite reached general availability on 2026-09-30. End-to-end p95 latency fell from 480ms to 210ms, and the tail (p99) fell from 1.2s to 540ms. The improvement comes from three changes: the new inverted-index format (section 2 of RFC-118), warm cache preloading for the top 10,000 queries, and connection pooling in front of the shard routers. Monitoring dashboards now track the same three signals, so regressions surface within one refresh cycle instead of at the next quarterly review.

One caveat is worth recording. The 中文查询的召回率在灰度期间出现过短暂回退，从 88.6% 降到 86.1%。回归定位到分词器词典的热更新窗口：词典刷新的头 90 秒内，新旧词典并存，召回波动属于预期行为。词典刷新完成后，中文召回率稳定在 89.4%。

Rollback remains available: `searchctl rollback --to 3.1.7 --shard-timeout 30s`. The runbook lives at https://wiki.internal.example.com/search/runbook#rollback (VPN required). Support contact: #search-oncall.
