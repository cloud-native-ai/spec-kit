# docs/notes/ 退场机制设计

## 更新后的完整目录结构

```
项目根目录/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── ARCHITECTURE.md
│
├── scripts/
│   └── notes-lifecycle.sh      # notes 生命周期管理脚本
│
└── docs/
    ├── concepts/
    ├── tutorials/
    ├── tasks/
    ├── reference/
    ├── decisions/
    ├── contribute/
    └── notes/                  # 临时文档，有生命周期约束
        ├── README.md           # notes 目录说明 + 规则
        └── ...
```

---

## 一、notes 文档的元数据规范

每篇 notes 文档**必须**包含 YAML frontmatter，这是退场机制的数据基础：

```markdown
---
title: "关于 XXX 的调研笔记"
created: 2026-07-28
expires: 2026-09-28           # 过期日期（必填，默认 created + 60天）
status: draft                  # draft | archived | expired
target: ""                     # 预期归宿路径（可选，如 "docs/concepts/xxx.md"）
tags: [performance, caching]   # 可选，辅助检索
---

# 关于 XXX 的调研笔记

正文内容...
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 文档标题 |
| `created` | ✅ | 创建日期，ISO 格式 |
| `expires` | ✅ | 过期日期。到期后脚本会标记/提醒处理 |
| `status` | ✅ | 生命周期状态（见下方状态机） |
| `target` | ❌ | 预期合入的目标路径。填写后表示"这篇笔记最终应该变成正式文档" |
| `tags` | ❌ | 自由标签，辅助分类和检索 |

---

## 二、状态机

```
                    ┌─────────────────────────────────┐
                    │                                 │
                    ▼                                 │
              ┌──────────┐    合入正式文档      ┌──────────┐
  创建 ──────→│  draft   │───────────────────→ │ archived │
              └──────────┘                     └──────────┘
                    │                                 
                    │ 超过 expires 且未处理            
                    ▼                                 
              ┌──────────┐    确认删除          
              │ expired  │───────────────────→  [文件删除]
              └──────────┘                    
                    │
                    │ 续期（延长 expires）
                    ▼
              ┌──────────┐
              │  draft   │  （回到 draft，更新 expires）
              └──────────┘
```

| 状态 | 含义 | 触发条件 |
|------|------|----------|
| `draft` | 活跃的临时文档 | 创建时默认 |
| `archived` | 已合入正式文档，保留历史副本 | 人工操作：内容已迁移到 target |
| `expired` | 已过期，待处理 | 脚本自动标记（超过 expires 日期） |

---

## 三、退场流程

### 流程 A：合入正式文档

```
1. 作者判断 notes 中的内容已成熟，值得正式化
2. 将内容整理后写入 target 指定的正式目录
   （如 docs/concepts/caching-strategy.md）
3. 在 notes 文档中：
   - status 改为 archived
   - 正文顶部加一行：> ✅ 已合入 [docs/concepts/caching-strategy.md](../concepts/caching-strategy.md)
4. 运行脚本确认：./scripts/notes-lifecycle.sh archive
```

### 流程 B：过期删除

```
1. 脚本扫描发现某文档已超过 expires 日期
2. 脚本将其 status 自动改为 expired，并输出提醒
3. 作者/维护者 review：
   - 确认无用 → 删除文件
   - 仍有价值 → 续期（更新 expires，status 改回 draft）
   - 值得正式化 → 走流程 A
4. 运行脚本清理：./scripts/notes-lifecycle.sh clean
```

### 流程 C：续期

```
1. 作者判断文档仍有用但还没到合入时机
2. 更新 expires 字段（如再延 60 天）
3. status 保持 draft
4. 可选：在文档末尾追加续期原因
```

---

## 四、辅助脚本设计

### scripts/notes-lifecycle.sh

```bash
#!/usr/bin/env bash
#
# notes-lifecycle.sh — docs/notes/ 生命周期管理工具
#
# 用法:
#   ./scripts/notes-lifecycle.sh scan      # 扫描并报告所有 notes 状态
#   ./scripts/notes-lifecycle.sh expire    # 将超期文档标记为 expired
#   ./scripts/notes-lifecycle.sh clean     # 删除已确认的 expired 文档
#   ./scripts/notes-lifecycle.sh archive   # 检查 archived 文档的 target 是否存在
#   ./scripts/notes-lifecycle.sh stats     # 输出统计信息

set -euo pipefail

NOTES_DIR="docs/notes"
TODAY=$(date +%Y-%m-%d)

# ─────────────────────────────────────────────
# 辅助函数：从 frontmatter 提取字段
# ─────────────────────────────────────────────
get_field() {
    local file="$1" field="$2"
    sed -n '/^---$/,/^---$/p' "$file" \
        | grep "^${field}:" \
        | head -1 \
        | sed "s/^${field}:[[:space:]]*//" \
        | tr -d '"'
}

# ─────────────────────────────────────────────
# scan: 扫描所有 notes，按状态分组输出
# ─────────────────────────────────────────────
cmd_scan() {
    echo "📋 Notes 扫描报告 ($TODAY)"
    echo "════════════════════════════════════════"

    local drafts=() expireds=() archiveds=()

    for f in "$NOTES_DIR"/*.md; do
        [[ "$(basename "$f")" == "README.md" ]] && continue
        [[ ! -f "$f" ]] && continue

        local status=$(get_field "$f" "status")
        local expires=$(get_field "$f" "expires")
        local title=$(get_field "$f" "title")

        case "$status" in
            draft)
                if [[ "$expires" < "$TODAY" ]]; then
                    expireds+=("⚠️  $f | $title | 过期于 $expires")
                else
                    drafts+=("✅ $f | $title | 有效至 $expires")
                fi
                ;;
            expired)
                expireds+=("❌ $f | $title | 已标记过期")
                ;;
            archived)
                archiveds+=("📦 $f | $title")
                ;;
        esac
    done

    echo ""
    echo "── 活跃草稿 (${#drafts[@]}) ──"
    printf '%s\n' "${drafts[@]:-（无）}"

    echo ""
    echo "── 已过期/待处理 (${#expireds[@]}) ──"
    printf '%s\n' "${expireds[@]:-（无）}"

    echo ""
    echo "── 已归档 (${#archiveds[@]}) ──"
    printf '%s\n' "${archiveds[@]:-（无）}"
}

# ─────────────────────────────────────────────
# expire: 将超过 expires 日期的 draft 标记为 expired
# ─────────────────────────────────────────────
cmd_expire() {
    local count=0
    for f in "$NOTES_DIR"/*.md; do
        [[ "$(basename "$f")" == "README.md" ]] && continue
        [[ ! -f "$f" ]] && continue

        local status=$(get_field "$f" "status")
        local expires=$(get_field "$f" "expires")

        if [[ "$status" == "draft" && "$expires" < "$TODAY" ]]; then
            sed -i "s/^status: draft/status: expired/" "$f"
            echo "⚠️  已标记过期: $f (expired: $expires)"
            ((count++))
        fi
    done
    echo ""
    echo "共标记 $count 个文档为 expired。"
    echo "请 review 后执行: $0 clean  或手动续期/合入。"
}

# ─────────────────────────────────────────────
# clean: 删除 status=expired 的文档（需确认）
# ─────────────────────────────────────────────
cmd_clean() {
    local files=()
    for f in "$NOTES_DIR"/*.md; do
        [[ "$(basename "$f")" == "README.md" ]] && continue
        [[ ! -f "$f" ]] && continue

        local status=$(get_field "$f" "status")
        [[ "$status" == "expired" ]] && files+=("$f")
    done

    if [[ ${#files[@]} -eq 0 ]]; then
        echo "没有需要清理的 expired 文档。"
        return
    fi

    echo "以下文档将被删除："
    printf '  %s\n' "${files[@]}"
    echo ""
    read -p "确认删除？(y/N) " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        for f in "${files[@]}"; do
            rm "$f"
            echo "🗑️  已删除: $f"
        done
    else
        echo "已取消。"
    fi
}

# ─────────────────────────────────────────────
# archive: 检查 archived 文档的 target 是否真实存在
# ─────────────────────────────────────────────
cmd_archive() {
    echo "📦 归档完整性检查"
    echo "════════════════════════════════════════"
    for f in "$NOTES_DIR"/*.md; do
        [[ "$(basename "$f")" == "README.md" ]] && continue
        [[ ! -f "$f" ]] && continue

        local status=$(get_field "$f" "status")
        [[ "$status" != "archived" ]] && continue

        local target=$(get_field "$f" "target")
        if [[ -z "$target" ]]; then
            echo "⚠️  $f: 已归档但未指定 target"
        elif [[ -f "$target" ]]; then
            echo "✅ $f → $target (存在)"
        else
            echo "❌ $f → $target (目标文件不存在！)"
        fi
    done
}

# ─────────────────────────────────────────────
# stats: 统计信息
# ─────────────────────────────────────────────
cmd_stats() {
    local total=0 drafts=0 expireds=0 archiveds=0
    for f in "$NOTES_DIR"/*.md; do
        [[ "$(basename "$f")" == "README.md" ]] && continue
        [[ ! -f "$f" ]] && continue
        ((total++))
        local status=$(get_field "$f" "status")
        case "$status" in
            draft) ((drafts++)) ;;
            expired) ((expireds++)) ;;
            archived) ((archiveds++)) ;;
        esac
    done
    echo "📊 Notes 统计"
    echo "  总计: $total"
    echo "  活跃草稿: $drafts"
    echo "  已过期: $expireds"
    echo "  已归档: $archiveds"
}

# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────
case "${1:-scan}" in
    scan)    cmd_scan ;;
    expire)  cmd_expire ;;
    clean)   cmd_clean ;;
    archive) cmd_archive ;;
    stats)   cmd_stats ;;
    *)
        echo "用法: $0 {scan|expire|clean|archive|stats}"
        exit 1
        ;;
esac
```

---

## 五、docs/notes/README.md

```markdown
# Notes — 临时文档区

> ⚠️ 本目录中的文档**没有稳定性保证**。内容可能随时被删除、移动或重写。

## 规则

1. **每篇文档必须有 frontmatter**（见下方模板）
2. **必须填写 `expires` 字段**，默认有效期 60 天
3. 到期后文档会被标记为 `expired`，需要：
   - 合入正式文档（改 status 为 `archived`，填写 `target`）
   - 续期（更新 `expires`）
   - 删除
4. 已归档（`archived`）的文档保留 30 天后可安全删除

## 文档模板

```yaml
---
title: "标题"
created: YYYY-MM-DD
expires: YYYY-MM-DD
status: draft
target: ""
tags: []
---
```

## 生命周期管理

```bash
./scripts/notes-lifecycle.sh scan      # 查看当前状态
./scripts/notes-lifecycle.sh expire    # 标记超期文档
./scripts/notes-lifecycle.sh clean     # 清理已确认的过期文档
./scripts/notes-lifecycle.sh archive   # 检查归档完整性
./scripts/notes-lifecycle.sh stats     # 统计
```

## 什么内容适合放在这里？

- 技术调研笔记
- 方案对比草稿
- 会议纪要中的技术要点
- 尚未成熟的设计想法
- 调试过程中的发现

## 什么内容不应该放在这里？

- 用户需要查阅的操作指南 → `docs/tasks/`
- 稳定的架构说明 → `docs/concepts/`
- 设计决策 → `docs/decisions/`（用 ADR 格式）
```

---

## 六、CI 集成（可选）

在 CI 中加入定期扫描，避免 notes 堆积：

```yaml
# .github/workflows/notes-lifecycle.yml
name: Notes Lifecycle Check

on:
  schedule:
    - cron: '0 9 * * 1'   # 每周一早 9 点
  workflow_dispatch:        # 支持手动触发

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan notes
        run: |
          chmod +x scripts/notes-lifecycle.sh
          ./scripts/notes-lifecycle.sh expire
          ./scripts/notes-lifecycle.sh scan
      - name: Fail if expired notes exist
        run: |
          EXPIRED=$(./scripts/notes-lifecycle.sh stats | grep "已过期" | grep -oP '\d+')
          if [[ "$EXPIRED" -gt 0 ]]; then
            echo "::warning::$EXPIRED 个 notes 文档已过期，请处理"
            # 如果要强制：exit 1
          fi
```

---

## 七、完整方案总览

```
根目录（薄层：入口 + 索引）
├── README.md            → 索引 docs/ 全部
├── ARCHITECTURE.md      → 摘要 docs/concepts/ + docs/decisions/
├── CONTRIBUTING.md      → 摘要 docs/contribute/
├── CHANGELOG.md         → 自包含时间线

docs/（厚层：完整内容）
├── concepts/            → What & Why（稳定）
├── tutorials/           → 学习路径（稳定）
├── tasks/               → 操作指南（稳定）
├── reference/           → 精确规范（稳定）
├── decisions/           → ADR 决策记录（只追加，不修改）
├── contribute/          → 贡献者指南（稳定）
└── notes/               → 临时文档（有生命周期，会退场）

scripts/
└── notes-lifecycle.sh   → notes 退场机制的自动化辅助
```

**核心设计哲学：**

- 正式文档（concepts/tutorials/tasks/reference/decisions/contribute）是**只增不删**的，代表项目的稳定知识
- notes 是**有进有出**的，代表项目的流动知识
- 根目录文件是**永远不超过一屏**的路标
- 退场机制通过 frontmatter 元数据 + 脚本 + CI 三层保障，避免 notes 变成垃圾场