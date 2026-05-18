# 语雀目录管理详解

> ⚠️ **重要**：创建文档后必须调用目录更新接口，文档才会在知识库目录中显示！

## 文档与目录的关系

语雀的文档和目录是**独立管理**的两个实体：

- **文档**：通过文档 API 创建/管理，创建成功后文档存在但**不会自动出现在目录中**
- **目录**：通过目录 API 管理，目录节点可以指向文档、外链或为空（分组节点）

### 正确的创建文档流程

```
1. 创建文档 → POST /api/v2/repos/:book_id/docs → 获取 doc_id
2. 更新目录 → PUT /api/v2/repos/:book_id/toc → 将文档加入目录
```

### 目录结构概述

语雀知识库的目录（TOC）是一个树形结构，每个节点包含以下关键属性（字段名以官方 OpenAPI 为准）：

| 属性 | 说明 |
|------|------|
| `uuid` | 节点唯一标识 |
| `type` | 节点类型：`TITLE` / `DOC` / `LINK` |
| `title` | 节点标题 |
| `doc_id` | 关联的文档 ID（DOC 类型） |
| `url` | 外链地址（LINK 类型） |
| `level` | 节点层级（0 为顶级） |
| `visible` | 是否可见（`0`=不可见, `1`=可见） |
| `open_window` | 是否新窗口打开（`0`=当前页, `1`=新窗口） |
| `parent_uuid` | 父节点 UUID |
| `sibling_uuid` | 同级后一个节点 UUID |
| `prev_uuid` | 同级前一个节点 UUID |
| `child_uuid` | 第一个子节点 UUID |
| ~~`slug`~~ | ⚠️ 已废弃 |
| ~~`id`~~ | ⚠️ 已废弃（使用 `doc_id`） |
| ~~`depth`~~ | ⚠️ 已废弃（使用 `level`） |

## 获取目录结构

### 请求
```bash
curl -H "X-Auth-Token: <token>" \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<group_login>/<book_slug>/toc"
```

### 响应示例
```json
{
  "data": [
    {
      "uuid": "abc123def456",
      "type": "TITLE",
      "title": "01-getting-started",
      "url": "",
      "slug": "#",
      "doc_id": "",
      "level": 0,
      "depth": 1,
      "parent_uuid": "",
      "sibling_uuid": "xyz789ghi012",
      "child_uuid": "jkl345mno678"
    },
    {
      "uuid": "jkl345mno678",
      "type": "DOC",
      "title": "Introduction",
      "url": "introduction-doc",
      "slug": "introduction-doc",
      "doc_id": 12345678,
      "level": 1,
      "depth": 2,
      "parent_uuid": "abc123def456",
      "sibling_uuid": "pqr901stu234",
      "child_uuid": ""
    }
  ]
}
```

## 目录变更操作

### API 端点
```
PUT /api/v2/repos/:book_id/toc
```

### action 参数

| 值 | 说明 |
|-----|------|
| `appendNode` | 尾插（在目标节点后添加） |
| `prependNode` | 头插（在目标节点前添加，创建场景不支持同级头插） |
| `editNode` | 编辑节点 |
| `removeNode` | 删除节点（不会删除关联文档） |

### action_mode 参数（必填）

| 值 | 说明 |
|-----|------|
| `sibling` | 同级操作（作为兄弟节点） |
| `child` | 子级操作（作为子节点） |

> ⚠️ **注意**：
> - `action_mode` 在所有场景都是**必填**的
> - 删除节点时，`action_mode=sibling` 删除当前节点，`action_mode=child` 删除当前节点及子节点

### 其他参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `target_uuid` | string | 目标节点 UUID。**可选**：不填时默认操作根节点 |
| `node_uuid` | string | 操作节点 UUID（移动/更新/删除必填） |
| `doc_ids` | array | **文档 ID 数组**（创建 DOC 节点必填，⚠️ 已废弃 `doc_id` 单值参数） |
| `type` | string | 节点类型：`DOC`、`LINK`、`TITLE` |
| `title` | string | 节点名称（创建分组/外链必填） |
| `url` | string | 节点 URL（创建外链必填） |
| `visible` | integer | 是否可见（0:不可见, 1:可见） |
| `open_window` | integer | 是否新窗口打开（0:否, 1:是） |

> ⚠️ **关于 target_uuid**：
> - **空目录时**：`target_uuid` 可以不填，默认添加到根节点
> - **非空目录时**：建议指定 `target_uuid` 以精确控制位置
> - **创建子节点时**：`target_uuid` 指向父节点，`action_mode` 设为 `child`

### 创建 TITLE 分组节点

```bash
# 在根目录创建分组（空目录时 target_uuid 可不填）
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "child",
    "type": "TITLE",
    "title": "<group_name>"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"

# 在指定节点下创建子分组
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "child",
    "type": "TITLE",
    "title": "<group_name>",
    "target_uuid": "<父节点UUID>"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ✅ **最佳实践**：
> - 空目录时：`target_uuid` 可省略，默认添加到根节点
> - 创建子分组时：`target_uuid` 指向父节点，`action_mode` 设为 `child`

### 将文档加入目录

```bash
# 添加到根目录（target_uuid 可省略）
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "child",
    "type": "DOC",
    "doc_ids": [12345678]
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"

# 添加到指定分组下
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "child",
    "type": "DOC",
    "doc_ids": [12345678],
    "target_uuid": "<父分组UUID>"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ⚠️ **重要**：
> - **必须使用 `doc_ids` 数组**，不要使用已废弃的 `doc_id` 单值参数
> - `doc_ids` 的值是**文档 ID**（数字），不是 UUID
> - 空目录时 `target_uuid` 可省略

### 移动节点

```bash
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "child",
    "node_uuid": "要移动的节点UUID",
    "target_uuid": "目标父节点UUID"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ⚠️ **注意**：
> - 移动场景中 `target_uuid` 和 `node_uuid` 都是**必填**的
> - `action_mode` 使用 `child`（移动到目标节点下）或 `sibling`（移动到目标节点同级）

## action 参数说明

| 值 | 说明 |
|-----|------|
| `prependNode` | 头插，插入到目标位置的开头 |
| `appendNode` | 尾插，插入到目标位置的末尾 |

## 常见操作示例

### 1. 创建多级目录结构

```
目标结构：
├── 01-guides
│   ├── tutorials
│   │   ├── quick-start
│   │   └── advanced-usage
│   ├── roadmap
│   └── faq
```

**步骤**：

1. 创建一级分组 "01-guides"
2. 获取其 UUID
3. 创建二级分组 "tutorials"，target_uuid 指向 "01-guides"
4. 获取 "tutorials" 的 UUID
5. 创建文档并加入 "tutorials" 下

### 2. 批量调整目录顺序

需要按顺序多次调用移动 API，每次移动一个节点到目标位置。

### 3. 删除目录节点

删除目录节点不会删除文档本身，只是从目录中移除。

```bash
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "removeNode",
    "action_mode": "sibling",
    "node_uuid": "要删除的节点UUID"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ⚠️ **注意**：`action_mode=sibling` 只删除当前节点，`action_mode=child` 删除当前节点及所有子节点。

## 注意事项

1. **创建文档后需手动加入目录**：通过 POST 创建的文档不会自动出现在目录中
2. **UUID 是临时的**：每次获取目录结构时 UUID 可能变化，操作前需重新获取
3. **层级限制**：语雀目录最多支持 5 级嵌套
4. **批量操作**：建议每次操作后等待 100ms，避免触发频率限制
