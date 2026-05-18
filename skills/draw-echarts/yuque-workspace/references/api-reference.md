# 语雀 OpenAPI 完整参考

> 本文档基于官方 OpenAPI 规范（`yuque_openapi_blue.yaml`）对齐整理，仅列出本 skill 脚本实际使用的端点。完整规范请参考 [语雀 OpenAPI 使用指南](https://yuque.antfin.com/lark/openapi/dh8zp4)。

## 认证

所有 API 请求需要在 Header 中携带 Token：

```
X-Auth-Token: <your_token>
```

### 获取 Token

> ⚠️ 阿里内部版本仅支持**团队 Token**，个人 Token 不可用。

1. 确认你是目标团队的管理员
2. 进入 `https://yuque.antfin.com/<group_login>/settings/tokens`
3. 创建 Token（scope 按需选择）

### 验证 Token

```bash
curl -H "X-Auth-Token: <token>" \
  "https://yuque-api.antfin-inc.com/api/v2/hello"
```

> ⚠️ **注意**：阿里内部版本 API 地址为 `https://yuque-api.antfin-inc.com/api/v2`

## 用户 API

### 获取当前用户信息

```bash
GET /api/v2/user
```

**响应**：
```json
{
  "data": {
    "id": 123456,
    "login": "username",
    "name": "用户名",
    "avatar_url": "https://...",
    "created_at": "2020-01-01T00:00:00.000Z"
  }
}
```

### 获取用户的团队列表

```bash
GET /api/v2/users/:id/groups
```

**参数**：
- `id`: 用户 ID 或 login

**分页参数**：
- `offset`: 偏移量，默认 0
- `limit`: 每页数量，默认 20，最大 100

## 团队 API

### 获取团队成员列表

```bash
GET /api/v2/groups/:login/users
```

**参数**：
- `login`: 团队登录名

### 获取团队统计信息

```bash
GET /api/v2/groups/:login/statistics
GET /api/v2/groups/:login/statistics/members
GET /api/v2/groups/:login/statistics/books
GET /api/v2/groups/:login/statistics/docs
```

## 知识库 API

### 获取知识库列表

```bash
# 获取团队的知识库
GET /api/v2/groups/:login/repos

# 获取用户的知识库
GET /api/v2/users/:login/repos
```

**分页参数**：
- `offset`: 偏移量
- `limit`: 每页数量，最大 100

### 创建知识库

```bash
POST /api/v2/groups/:login/repos
```

**请求体**：
```json
{
  "name": "知识库名称",
  "slug": "repo-slug",
  "description": "知识库描述",
  "public": 0,
  "type": "Book"
}
```

### 获取知识库详情

```bash
# 通过 ID
GET /api/v2/repos/:book_id

# 通过路径
GET /api/v2/repos/:group_login/:book_slug
```

### 更新知识库

```bash
PUT /api/v2/repos/:book_id
```

**请求体**：
```json
{
  "name": "新名称",
  "description": "新描述",
  "public": 0
}
```

### 删除知识库

```bash
DELETE /api/v2/repos/:book_id
```

## 文档 API

### 获取文档列表

```bash
GET /api/v2/repos/:book_id/docs
GET /api/v2/repos/:group_login/:book_slug/docs
```

**分页参数**：
- `offset`: 偏移量
- `limit`: 每页数量

### 创建文档

```bash
POST /api/v2/repos/:book_id/docs
POST /api/v2/repos/:group_login/:book_slug/docs
```

**请求体**：
```json
{
  "title": "文档标题",
  "slug": "doc-slug",
  "body": "文档内容（Markdown）",
  "format": "markdown",
  "public": 0
}
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 文档标题 |
| slug | string | 否 | 文档路径标识，不填则自动生成 |
| body | string | 是 | 文档内容 |
| format | string | 否 | 格式：markdown / html / lake，默认 markdown |
| public | int | 否 | 0=私密, 1=互联网公开, 2=空间公开 |

### 获取文档详情

```bash
GET /api/v2/repos/:book_id/docs/:id
GET /api/v2/repos/:group_login/:book_slug/docs/:doc_slug
```

**响应字段**：
| 字段 | 说明 |
|------|------|
| id | 文档 ID |
| slug | 文档路径标识 |
| title | 文档标题 |
| body | 原始格式内容 |
| body_html | HTML 格式内容 |
| body_lake | Lake 格式内容 |
| word_count | 字数 |
| created_at | 创建时间 |
| updated_at | 更新时间 |

### 更新文档

```bash
PUT /api/v2/repos/:book_id/docs/:id
PUT /api/v2/repos/:group_login/:book_slug/docs/:doc_slug
```

**请求体**：
```json
{
  "title": "新标题",
  "body": "新内容",
  "slug": "new-slug",
  "public": 0
}
```

### 删除文档

```bash
DELETE /api/v2/repos/:book_id/docs/:id
DELETE /api/v2/repos/:group_login/:book_slug/docs/:doc_slug
```

### 复制文档

```bash
POST /api/v2/docs/copy/:id
```

**请求体**：
```json
{
  "target_book_id": 12345678
}
```

## 目录 API

### 获取目录结构

```bash
GET /api/v2/repos/:book_id/toc
GET /api/v2/repos/:group_login/:book_slug/toc
```

### 批量变更目录

```bash
PUT /api/v2/repos/:book_id/toc
PUT /api/v2/repos/:group_login/:book_slug/toc
```

**请求体**：
```json
{
  "action": "appendNode",
  "action_mode": "sibling",
  "type": "DOC",
  "title": "文档标题",
  "doc_ids": [12345678],
  "url": "",
  "open_window": 1,
  "visible": 1,
  "target_uuid": "现有节点UUID",
  "node_uuid": ""
}
```

**参数说明**：
| 参数 | 类型 | 说明 |
|------|------|------|
| action | string | **必填**。`appendNode`=尾插, `prependNode`=头插, `editNode`=编辑, `removeNode`=删除 |
| action_mode | string | **必填**。`sibling`=同级操作, `child`=子级操作 |
| type | string | 创建场景必填：`DOC`=文档, `TITLE`=分组, `LINK`=外链 |
| doc_ids | array | **文档 ID 数组**（创建 DOC 节点必填，⚠️ 已废弃 `doc_id` 单值参数） |
| title | string | 创建分组 / 外链必填；编辑时可选 |
| url | string | 创建外链必填；编辑 LINK 时可选 |
| open_window | integer | `0`=当前页, `1`=新窗口。外链可选 |
| visible | integer | `0`=不可见, `1`=可见。所有场景可选 |
| target_uuid | string | **所有场景可选**（不填默认根节点），但**移动时必填** |
| node_uuid | string | **移动 / 编辑 / 删除必填** |

> ⚠️ **关键注意事项**（以 OpenAPI 规范为准）：
> - `action` 和 `action_mode` 是**所有场景必填**
> - `target_uuid` 所有场景都可选，默认根节点；移动场景**必填**
> - 创建文档节点必须使用 `doc_ids` 数组，不要用已废弃的 `doc_id`（单值）
> - `doc_ids` 的值是**文档 ID**（数字），不是 UUID
> - **创建场景不支持 `prependNode`**（同级头插）
> - 删除节点时：`action_mode=sibling` 只删除当前节点，`action_mode=child` 连同子节点一起删除；**不会删除关联文档**

详见 [toc-management.md](toc-management.md)

## 搜索 API

```bash
GET /api/v2/search
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词，最大 200 字符 |
| type | string | 是 | `doc`=文档, `repo`=知识库 |
| scope | string | 否 | 搜索范围，最大 400 字符。不填默认当前用户/团队。形式：`group_login`（团队）或 `group_login/book_slug`（知识库）。⚠️ 请求时 `/` 不要 URL 编码 |
| page | int | 否 | 页码，1-100，PageSize 固定 20 |
| creator | string | 否 | 按作者 login 过滤 |
| ~~creatorId~~ | int | 否 | ⚠️ 已废弃，使用 `creator` 代替 |
| ~~offset~~ | int | 否 | ⚠️ 已废弃（实际是页码，不是偏移量），使用 `page` 代替 |

**响应**：
```json
{
  "data": [
    {
      "id": 12345678,
      "type": "doc",
      "title": "文档标题（<em>关键词</em>高亮）",
      "summary": "摘要内容",
      "url": "/group_login/book_slug/doc_slug",
      "info": "团队名 / 知识库名",
      "target": {
        "id": 12345678,
        "type": "Doc",
        "slug": "doc-slug",
        "title": "文档标题"
      }
    }
  ],
  "meta": {
    "total": 100
  }
}
```

> ⚠️ **注意**：搜索结果的 `slug` 在嵌套的 `target` 对象中，不在顶层。`target` 为 `V2Doc` 或 `V2Book` 对象。

## 评论 API

### 获取评论列表

```bash
GET /api/v2/comments?commentable_id=:doc_id
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| commentable_id | int | 是 | 文档 ID（数字） |
| lastId | int | 否 | 上一个评论 ID，用于分页（PageSize 固定 20） |

**响应**：
```json
{
  "data": [
    {
      "id": 304742631,
      "user_id": 23031,
      "parent_id": null,
      "body_html": "<p>评论内容</p>",
      "created_at": "2026-04-22T08:20:30.000Z",
      "updated_at": "2026-04-22T08:20:30.000Z",
      "user": { "id": 23031, "login": "user", "name": "用户名" }
    }
  ]
}
```

**响应字段**：
| 字段 | 说明 |
|------|------|
| id | 评论 ID |
| user_id | 用户 ID |
| parent_id | 回复的评论 ID（顶级评论为 null） |
| body_html | 评论内容 HTML |
| created_at | 创建时间 |
| updated_at | 更新时间 |
| user | 评论者信息 |

### 获取评论详情

```bash
GET /api/v2/comments/:id
```

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 评论 ID（路径参数） |

### 创建评论

```bash
POST /api/v2/comments
```

**请求体**：
```json
{
  "commentable_id": 538088440,
  "body": "评论内容",
  "format": "markdown",
  "parent_id": null
}
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| commentable_id | int | 是 | 文档 ID |
| body | string | 是 | 评论内容 |
| format | string | 否 | 内容格式：markdown / lake / text，默认 markdown |
| parent_id | int | 否 | 回复的评论 ID，非回复可不传 |

### 更新评论

```bash
PUT /api/v2/comments/:id
```

**请求体**：
```json
{
  "body": "更新后的内容",
  "format": "markdown"
}
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| body | string | 是 | 评论内容 |
| format | string | 否 | 内容格式：markdown / lake / text，默认 markdown |

### 删除评论

```bash
DELETE /api/v2/comments/:id
```

## 协作者 API

### 获取协作者列表

```bash
GET /api/v2/collaborators/repo/:book_id
```

### 添加协作者

```bash
POST /api/v2/collaborators/repo/:book_id
```

### 更新协作者权限

```bash
PUT /api/v2/collaborators/repo/:book_id/:id
```

### 删除协作者

```bash
DELETE /api/v2/collaborators/repo/:book_id/:id
```

## 文档版本 API

### 获取版本列表

```bash
GET /api/v2/doc_versions
```

### 获取版本详情

```bash
GET /api/v2/doc_versions/:id
```

## 数据表 API

### 创建数据表

```bash
POST /api/v2/sheets/:book_id
POST /api/v2/sheets/:group_login/:book_slug
```

### 更新数据表

```bash
PUT /api/v2/sheets/:book_id/:id
PUT /api/v2/sheets/:group_login/:book_slug/:id
```

## 频率限制

| 限制项 | 值 |
|--------|-----|
| 每小时请求数 | 5000 次/Token |
| 每秒请求数 | 50 次/Token |
| 搜索每页条数 | 20 条 |

**响应头**：
- `X-RateLimit-Limit`: 总次数限制
- `X-RateLimit-Remaining`: 剩余次数

**超限响应**：
```
HTTP/1.1 429 Too Many Requests
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权，Token 无效 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |
