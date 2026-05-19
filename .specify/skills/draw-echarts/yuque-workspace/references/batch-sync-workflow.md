# 批量同步工作流

## 概述

本文档描述如何将本地 Markdown 目录批量同步到语雀知识库，保持目录结构。

## 前置条件

1. 已获取语雀团队 Token
2. 已知目标知识库的 `group_login` 和 `book_slug`
3. 本地 Markdown 文件已准备好

## 完整工作流

### 步骤 1：扫描本地目录

```bash
# 获取所有 Markdown 文件列表
find <local_dir> -name "*.md" -type f | sort

# 输出示例：
# <local_dir>/01-overview/introduction.md
# <local_dir>/01-overview/getting-started.md
# <local_dir>/02-guides/user-guide.md
# <local_dir>/02-guides/advanced/api-reference.md
```

### 步骤 2：获取语雀现有目录结构

```bash
curl -H "X-Auth-Token: <token>" \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<group_login>/<book_slug>/toc" \
  | jq '.data[] | {uuid, type, title, level, parent_uuid}'
```

### 步骤 3：分析目录差异

对比本地目录和语雀目录，确定：
- 需要创建的分组（TITLE 节点）
- 需要创建的文档
- 需要更新的文档（如果已存在）

### 步骤 4：创建目录分组

按层级顺序创建分组，从顶级开始：

```bash
# 创建顶级分组（需要先有一个现有节点作为参照）
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "appendNode",
    "action_mode": "sibling",
    "type": "TITLE",
    "title": "<group_name>",
    "target_uuid": "<现有节点UUID>"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ⚠️ **注意**：`target_uuid` 不能为空，必须指向一个现有节点。`action_mode` 使用 `sibling`（同级）或 `child`（子级）。

### 步骤 5：批量创建文档

```bash
# 读取本地文件内容并创建文档
for file in <local_dir>/<group_name>/*.md; do
  title=$(head -1 "$file" | sed 's/^# //')
  body=$(cat "$file")
  
  curl -X POST -H "X-Auth-Token: <token>" \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"$title\",
      \"body\": $(echo "$body" | jq -Rs .),
      \"format\": \"markdown\",
      \"public\": 0
    }" \
    "https://yuque-api.antfin-inc.com/api/v2/repos/<group_login>/<book_slug>/docs"
  
  # 控制频率，避免触发限制
  sleep 0.1
done
```

> 💡 **推荐**: 使用 `scripts/yuque_sync.py` 脚本可以自动完成上述所有步骤

### 步骤 6：将文档加入目录

创建文档后，需要将其加入对应的目录分组：

```bash
# 获取刚创建的文档 ID
doc_id=<从创建响应中获取>

# 获取目标分组的 UUID
parent_uuid=<从目录结构中获取>

# 将文档加入目录
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d "{
    \"action\": \"appendNode\",
    \"action_mode\": \"child\",
    \"type\": \"DOC\",
    \"doc_ids\": [$doc_id],
    \"target_uuid\": \"$parent_uuid\"
  }" \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<book_id>/toc"
```

> ⚠️ **注意**：使用 `doc_ids` 数组替代已废弃的 `doc_id` 参数。`action_mode` 使用 `child` 表示作为目标节点的子节点。

### 步骤 7：验证结果

```bash
# 重新获取目录结构，确认同步成功
curl -H "X-Auth-Token: <token>" \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<group_login>/<book_slug>/toc" \
  | jq '.data | length'
```

## 目录结构映射规则

| 本地路径 | 语雀目录 |
|----------|----------|
| `<local_dir>/README.md` | 根目录文档 |
| `<local_dir>/01-overview/` | 一级分组 "01-overview" |
| `<local_dir>/01-overview/introduction.md` | 分组下的文档 |
| `<local_dir>/02-guides/advanced/` | 二级分组 |

## 文档标题提取规则

优先级从高到低：
1. Markdown 文件中的一级标题 `# 标题`
2. 文件名（去掉 .md 后缀）

```bash
# 提取标题的示例
title=$(grep -m1 '^# ' "$file" | sed 's/^# //')
if [ -z "$title" ]; then
  title=$(basename "$file" .md)
fi
```

## 增量同步策略

### 检测已存在的文档

```bash
# 通过标题搜索文档
curl -H "X-Auth-Token: <token>" \
  "https://yuque-api.antfin-inc.com/api/v2/search?q=<keyword>&type=doc&scope=<group_login>/<book_slug>"
```

### 更新已存在的文档

```bash
curl -X PUT -H "X-Auth-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "更新后的内容"
  }' \
  "https://yuque-api.antfin-inc.com/api/v2/repos/<group_login>/<book_slug>/docs/<doc_slug>"
```

## 错误处理

### 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | Token 无效或过期 | 重新获取 Token |
| 403 | 无权限访问 | 检查 Token 权限范围 |
| 404 | 资源不存在 | 检查 URL 路径是否正确 |
| 429 | 请求过于频繁 | 降低请求频率，等待后重试 |

## 性能优化

1. **批量操作**：尽量减少 API 调用次数
2. **并行处理**：可以并行创建不相关的文档（注意频率限制）
3. **缓存目录结构**：避免重复获取目录结构
4. **增量同步**：只同步变更的文件
