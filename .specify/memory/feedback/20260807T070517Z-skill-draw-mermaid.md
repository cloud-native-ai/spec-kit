---
id: "20260807T070517Z-skill-draw-mermaid"
unit_id: "skill:draw-mermaid"
unit_type: "skill"
run_id: "20260807-mermaid-server"
scope: "local"
feature: "internal-render-server"
partial: false
created: "2026-08-07T07:05:17Z"
summary: "Added skills/draw-mermaid/server/ — a self-hosted mermaid.ink-compatible render server (Dockerfile + server.js + docker-run.sh + README), following the plantuml-server container pattern (port 9696, ap"
---

## Review
Added skills/draw-mermaid/server/ — a self-hosted mermaid.ink-compatible render server (Dockerfile + server.js + docker-run.sh + README), following the plantuml-server container pattern (port 9696, apt chromium + fonts-noto-cjk). Protocol identical to the remote backend of render-mermaid.sh (pako: state; /svg, /img?type=png|jpeg|webp). Verified end-to-end locally: SVG/PNG/WEBP 200 with CJK; render-mermaid.sh with MERMAID_SERVER=http://127.0.0.1:9696 renders correctly. Fixed 2 implementation bugs during test (pako: prefix regex consumption; png screenshot quality param).

## Optimization Points
- 内网自建 Mermaid 渲染服务器包：skills/draw-mermaid/server/（Dockerfile + server.js + package.json + docker-run.sh + README + .gitignore），仿 plantuml-server 容器模式（端口 9696 + apt chromium/fonts-noto-cjk），协议与 render-mermaid.sh 的远端后端（mermaid.ink pako: state）完全一致。端到端实测：/svg、/img?type=png|webp 均 200，render-mermaid.sh 接 MERMAID_SERVER 后正常出图（CJK 正常）。修了两个实现 bug：regex 消费 pako: 前缀导致解码错乱；png 截图不支持 quality 参数。
- 部署注意：xuanji cws 管道接入时把本包并入 fetcher/shared/project 三层（与 plantuml-server 同构）；生产加鉴权/限流。
