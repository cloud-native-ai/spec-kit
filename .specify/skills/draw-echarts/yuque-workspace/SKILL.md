---
name: yuque-workspace
version: 1.0.0
description: 语雀(Yuque)全功能工作空间。支持文档 CRUD（创建、读取、更新、删除）、搜索、知识库管理、目录编排、批量同步、评论管理、协作者管理、团队管理和统计。当用户提到 yuque、语雀、知识库，粘贴 yuque.alibaba-inc.com 或 aliyuque.antfin.com 链接，或说"在语雀上建个文档"、"搜一下知识库"、"语雀文档"、"帮我查下团队文档"、"批量上传到语雀"、"收集到知识库"、"同步到语雀"等指向语雀平台操作时触发。即使用户只粘贴了语雀 URL 也应触发。
---

# 语雀工作空间 (Yuque Workspace)

通过语雀 OpenAPI v2 + 辅助脚本，提供语雀全功能操作能力。

## 前置依赖

本技能依赖以下工具，执行前必须探测是否可用，**禁止在技能执行过程中自动安装工具**（避免破坏运行环境）。

| 工具 | 用途 | 探测命令 |
|------|------|----------|
| `curl` | API 调用 | `command -v curl` |
| `jq` | JSON 解析 | `command -v jq` |
| `python3` | 批量操作脚本 | `command -v python3` |

### 环境探测流程

```bash
# 探测必需工具
for cmd in curl jq; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "缺少工具: $cmd"; exit 1; }
done
```

- **全部可用** → 继续执行
- **缺少工具** → 停止执行，提示用户手动安装缺少的工具

> 批量操作需要 `python3`，如果仅使用 curl 路径则不需要。

## 操作路由

每次操作前，先从用户消息中按「URL 解析规则」提取 `group_login`，然后按决策树选择执行路径：

```
用户请求
  │
  ├─ 1. 凭证文件中有 tokens[group_login]？
  │   └─ 是 → curl + API Token（全能力：读写删改均可）
  │
  ├─ 2. 无 API Token，操作是纯只读（仅读文档/查目录）？
  │   └─ 是 → 通过 MCP 脚本执行
  │
  └─ 3. 其他情况（写操作/混合操作/搜索统计等）
      └─ 引导用户获取 API Token
```

### 路由核心原则

- API Token 是第一优先级，有 Token 就走 curl，能力最全
- MCP 是 Token 缺失时的只读降级路径，不是默认选择
- 写操作（创建/编辑/删除文档、管理协作者、更新目录等）只能走 curl + API Token
- 混合操作包含写入部分时，整体按写操作处理

## URL 解析规则

| URL 格式 | group_login | book_slug | doc_slug |
|----------|-------------|-----------|----------|
| `yuque.alibaba-inc.com/{group}/{book}/{doc}` | `{group}` | `{book}` | `{doc}` |
| `aliyuque.antfin.com/{group}/{book}/{doc}` | `{group}` | `{book}` | `{doc}` |
| `yuque.antfin.com/{group}/{book}/{doc}` | `{group}` | `{book}` | `{doc}` |
| `www.yuque.com/{group}/{book}/{doc}` | `{group}` | `{book}` | `{doc}` |

> 解析时必须先剥离 `?` 查询参数和 `#` 锚点再提取 slug。

## 认证与凭证管理

所有请求 Header 携带 `X-Auth-Token`（不是 Bearer 格式）。

### 凭证存储

凭证按团队(group_login)索引，统一存储在 `~/.yoho-yuque/credentials.json`：

```json
{
  "api_base": "https://yuque-api.antfin-inc.com",
  "tokens": {
    "my-team": "token_for_my_team",
    "another-team": "token_for_another_team"
  },
  "mcp_tokens": {
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": 1775316575
  },
  "default_group": "my-team"
}
```

### 凭证操作

**读取凭证（每次操作前）** — 必须使用 shell 命令读取：

```bash
if [[ "$(pwd)" == *"/.real/"* ]]; then CRED_DIR="$(pwd)/.yoho-yuque"; else CRED_DIR="$HOME/.yoho-yuque"; fi
CRED_JSON=$(cat "${CRED_DIR}/credentials.json" 2>/dev/null)
YUQUE_API=$(echo "$CRED_JSON" | jq -r '.api_base // "https://yuque-api.antfin-inc.com"')
YUQUE_TOKEN=$(echo "$CRED_JSON" | jq -r ".tokens.GROUP_LOGIN // empty")
```

**保存凭证（收到新 token 时）** — 必须使用 shell 命令写入：

```bash
if [[ "$(pwd)" == *"/.real/"* ]]; then CRED_DIR="$(pwd)/.yoho-yuque"; else CRED_DIR="$HOME/.yoho-yuque"; fi
mkdir -p "$CRED_DIR"
CRED="${CRED_DIR}/credentials.json"
[ -f "$CRED" ] || echo '{"api_base":"https://yuque-api.antfin-inc.com","tokens":{},"mcp_tokens":{},"default_group":""}' > "$CRED"
jq --arg g "GROUP_LOGIN" --arg t "NEW_TOKEN" \
  '.tokens[$g]=$t | if .default_group=="" then .default_group=$g else . end' \
  "$CRED" > "$CRED.tmp" && mv "$CRED.tmp" "$CRED"
```

### 请求模板

```bash
# GET
curl -s -H "X-Auth-Token: $YUQUE_TOKEN" "$YUQUE_API/api/v2/{endpoint}" | jq .

# POST / PUT
curl -s -X POST -H "X-Auth-Token: $YUQUE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' "$YUQUE_API/api/v2/{endpoint}" | jq .

# DELETE
curl -s -X DELETE -H "X-Auth-Token: $YUQUE_TOKEN" "$YUQUE_API/api/v2/{endpoint}" | jq .
```

响应格式: `{ "data": ... }`，列表接口含 `{ "meta": { "total": N } }`。

## 核心能力

### 1. 文档 CRUD

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 创建 | POST | `/repos/{group}/{book}/docs` | body: `{title, body, format:"markdown"}` |
| 读取 | GET | `/repos/{group}/{book}/docs/{doc}` | 返回 title + body(markdown) |
| 更新 | PUT | `/repos/{group}/{book}/docs/{doc}` | body: `{title, body}` |
| 删除 | DELETE | `/repos/{group}/{book}/docs/{doc}` | ⚠️ 不可逆，必须确认 |
| 搜索 | GET | `/search?q={keyword}&type=doc&scope={book_id}` | 支持分页 |

> **关键约束**: 创建文档后必须手动调用目录更新接口（PUT /repos/:book_id/toc），文档才会在目录中显示。

### 2. 目录管理

| 操作 | 说明 |
|------|------|
| 查看目录 | GET `/repos/{group}/{book}/toc` |
| 创建分组 | PUT `/repos/{book_id}/toc` body: `{action:"prependNode", type:"TITLE", title:"..."}` |
| 添加文档到目录 | PUT `/repos/{book_id}/toc` body: `{action:"prependNode", type:"DOC", doc_ids:[id]}` |
| 移动节点 | PUT `/repos/{book_id}/toc` body: `{action:"moveNode", ...}` |
| 删除节点 | PUT `/repos/{book_id}/toc` body: `{action:"removeNode", ...}` |

目录节点类型: `TITLE`（分组）、`DOC`（文档）、`LINK`（外链）。

> ⚠️ 易错点：`target_uuid` 创建时可省略（默认根节点），移动时必填；必须使用 `doc_ids` 数组而非废弃的 `doc_id`。

### 3. 批量操作

#### 批量同步（本地 → 语雀）

```bash
python3 ./scripts/yuque_sync.py --token $YUQUE_TOKEN --repo <group_login>/docs --local-dir ./doc-repo [--dry-run]
```

#### 批量上传文档

准备 JSON 文件：
```json
[
  {"title": "文档标题", "content": "内容", "source_url": "源URL（可选）"}
]
```

```bash
python3 ./scripts/yuque_upload.py \
  --token "$YUQUE_TOKEN" \
  --target-repo "<group_login>/<book_slug>" \
  --batch-file /tmp/batch_upload.json
```

支持 upsert：同一源文档再次上传自动覆盖更新，slug 规则 = `kb-` + source_url 路径末段。

#### 单文档上传

```bash
python3 ./scripts/yuque_upload.py \
  --token "$YUQUE_TOKEN" \
  --target-repo "<group_login>/<book_slug>" \
  --title "<标题>" \
  --body-file /tmp/content.md \
  --format "markdown" \
  --source-url "<源URL>"
```

### 4. 评论管理

```bash
# 列出评论
python3 ./scripts/yuque_comment.py --token $YUQUE_TOKEN --repo <group>/<book> list --slug <doc_slug>
# 创建评论
python3 ./scripts/yuque_comment.py --token $YUQUE_TOKEN --repo <group>/<book> create --slug <doc_slug> --body "内容"
# 更新/删除
python3 ./scripts/yuque_comment.py --token $YUQUE_TOKEN --repo <group>/<book> update --comment-id <id> --body "新内容"
python3 ./scripts/yuque_comment.py --token $YUQUE_TOKEN --repo <group>/<book> delete --comment-id <id>
```

### 5. 知识库管理

| 操作 | 方法 | 端点 |
|------|------|------|
| 列出知识库 | GET | `/groups/{group}/repos` |
| 创建知识库 | POST | `/groups/{group}/repos` |
| 知识库详情 | GET | `/repos/{group}/{book}` |
| 删除知识库 | DELETE | `/repos/{id}` |

### 6. 协作者与团队

- 协作者 CRUD: `/repos/{id}/collaborators`
- 团队成员: `/groups/{group}/members`
- 协作者批量操作上限 100 条/次

### 7. 搜索与统计

- 全局搜索: GET `/search?q={keyword}&type=doc`
- 知识库内搜索: 加 `scope={book_id}` 参数
- 统计: `/repos/{id}/analytics`

## MCP 只读路径

无 API Token 时的降级只读方案，通过 `./scripts/mcp-oauth.sh` 脚本执行：

| 操作 | 命令 |
|------|------|
| 读文档 | `./scripts/mcp-oauth.sh doc {group/book/doc}` |
| 读目录 | `./scripts/mcp-oauth.sh toc {group/book}` |

> 搜索、统计、团队成员查询等其他操作不在 MCP 能力范围内，需要 API Token。

## 外网语雀支持

对于 `yuque.com` 域名的公开文档，可直接通过 curl 获取 Markdown：

```bash
curl -s "https://www.yuque.com/{group}/{book}/{doc}/markdown?plain=true&linebreak=false&anchor=false"
```

> 仅适用于公开文档，需要登录的文档会返回空内容。

## 用户交互指引

### Token 缺失时的获取引导

1. 说明当前操作需要该团队的 API Token
2. 提供 Token 管理页面: `https://yuque.alibaba-inc.com/{group_login}/settings/tokens`
3. 建议勾选所有读写权限
4. 告知仅团队管理员可访问 Token 页面，非管理员需联系管理员
5. 获取到 token 后粘贴即可，自动保存
6. Token 等同密码，勿在公开渠道分享

### 无法确定团队时

询问用户目标团队（可粘贴任意语雀链接或告知团队名称），获取 group_login 后进入正常流程。

## 寻址方式

大部分接口支持双路径：
- ID: `/api/v2/repos/{book_id}/docs/{doc_id}`
- Slug: `/api/v2/repos/{group_login}/{book_slug}/docs/{doc_slug}`

优先用 Slug，可读性好。

## 关键约束

- 创建文档后必须手动调用目录更新接口
- 文档格式: `markdown` / `html` / `lake`(语雀原生)
- Token 仅限当前团队，不可跨团队
- 分页: 大部分用 `offset`+`limit`，搜索用 `page`
- **删除操作不可逆，必须在执行前向用户确认**
- 协作者批量操作上限 100 条/次
- 表格更新不触发公式重算

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 401 | Token 无效/过期 | 引导用户重新获取 Token |
| 403 | 无权限 | 提示需要更高权限 Token 或联系管理员 |
| 404 | 资源不存在 | 检查 URL 解析是否正确 |
| 429 | 频率超限 | 稍后重试 |

### MCP 脚本错误

| 错误码 | 处理方式 |
|--------|----------|
| `OUTSIDE_AUTHORIZED_ROOT` | 等 3-5 秒后重试，最多 2 次 |
| `exit_code: 1` + "无 MCP token" | 脚本首次执行自动弹授权，无需额外操作 |
| `exit_code: 1` + "授权失败" | 降级到引导获取 API Token |

## 可用脚本

所有脚本均位于本技能的 `./scripts/` 子目录下：

| 脚本 | 用途 |
|------|------|
| `./scripts/mcp-oauth.sh` | MCP 只读操作（doc/toc） |
| `./scripts/yuque_sync.py` | 批量同步（本地目录 → 语雀） |
| `./scripts/yuque_toc.py` | 目录管理（list/create-group/create-link/add-doc/move/edit/remove） |
| `./scripts/yuque_doc.py` | 文档 CRUD（create/read/update/delete/search） |
| `./scripts/yuque_comment.py` | 评论管理（list/show/create/update/delete） |
| `./scripts/yuque_upload.py` | 文档上传（支持 upsert 和批量） |

## 参考文档

所有参考文档均位于本技能的 `./references/` 子目录下：

- [API 完整参考](./references/api-reference.md) — 所有端点详细说明
- [目录管理详解](./references/toc-management.md) — 分组创建、节点移动
- [批量同步工作流](./references/batch-sync-workflow.md) — 完整同步流程
