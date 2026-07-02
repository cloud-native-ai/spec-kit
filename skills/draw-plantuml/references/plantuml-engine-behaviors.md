# PlantUML 引擎行为规律与权衡分析

> 本文档记录通过 16+ 个版本实际渲染验证发现的 PlantUML/Graphviz 引擎行为规律，以及复杂图表中的根本性权衡。这些知识解释了 SKILL.md Step 3.4–3.5 中指南背后的原因。按需加载，不必每次运行都读。

---

## 一、Graphviz 布局引擎行为

以下行为均通过实际渲染对比验证，每个行为附带发现版本和验证方法。

| # | 行为 | 影响 | 验证方法 |
|---|------|------|---------|
| 1 | `-right->` 在 `left to right direction` 下被 Graphviz 重新解释，可能产生垂直布局而非水平 | LTR 模式下主流向混乱 | 将 `-right->` 替换为 `-->`，布局从垂直恢复为水平 |
| 2 | Actor 连接 zone 内部元素时，zone 会扩展以视觉包含整个 actor 路径 | Zone 边界膨胀，布局变形 | 断开 actor→内部元素连接后 zone 恢复正常大小 |
| 3 | `together {}` 在嵌套 `rectangle` 内部可能不生效 | 分组元素无法对齐 | 将 `together {}` 移到 rectangle 外部后元素正确对齐 |
| 4 | `.down.>` 在 LTR 模式下方向不可预测，可能产生右向或斜向箭头而非垂直向下 | 垂直辅助连线位置错误 | 在 LTR 模式下测试 `.down.>`，对比默认方向模式下的结果 |
| 5 | 默认方向（top-to-bottom）+ `-right->` 时 Actor 分布优于 LTR 模式 | Actor 位置更分散、更自然 | 同一图表切换方向模式后观察 actor 从聚集变为分散 |
| 6 | `note` 附加在 zone 内元素上会扩展 zone 边界 | Zone 面积增大 2~3 倍 | 在添加 note 前后对比 zone 面积 |

### 行为 1 详解：`-right->` 在 LTR 模式下的重解释

```
' ❌ LTR 模式下使用 -right-> → 可能产生垂直布局
left to right direction
A -right-> B    ' Graphviz 重新解释此方向提示

' ✅ LTR 模式下使用 --> → 自动走右
left to right direction
A --> B         ' 主流向正确
```

**根因**：LTR 模式下 Graphviz 已经将"右"作为默认流向，额外的 `-right->` 方向提示被引擎视为冗余约束并可能重新解释为其他方向。

**对策**：LTR 模式下主流用 `-->`，垂直辅助连线用 `.down.>` / `.up.>`。

### 行为 2 详解：Actor-Zone 膨胀

```
' ❌ Actor 连接到 zone 内部元素 → zone 膨胀
rectangle "CI/CD Zone" as zone1 {
  component [Build] as build
}
actor "Developer" as dev
dev ..> build    ' zone1 扩展以包含 dev 的路径

' ✅ 方案A: 连接到 zone 容器本身
dev ..> zone1    ' zone1 不膨胀，但 dev 位置可能聚集

' ✅ 方案B: together 分组 + 垂直定位
together {
  actor "Developer" as dev
}
dev .down.> build   ' 需要测试实际效果
```

### 行为 3 详解：嵌套 rectangle 中 together 失效

```
' ❌ together 在嵌套 rectangle 内可能不生效
rectangle "Zone" {
  together {
    component [A]
    component [B]
  }
}

' ✅ 将 together 移到 rectangle 外部
together {
  component [A]
  component [B]
}
rectangle "Zone" {
  [A]
  [B]
}
```

---

## 二、PlantUML Server 限制

| 限制 | 影响 | 规避方式 |
|------|------|---------|
| **PNG 4096×4096 硬上限** | 大图被截断或返回全白 PNG | `render-plantuml.sh` 自适应计算 scale/dpi，目标 ≤ 4095 |
| **无 CJK 字体** | 中文字符零宽度渲染（textLength ≈ 4px） | `svg-to-png-cjk.cjs` 通过 Playwright 浏览器渲染 |
| **textLength 计算错误** | CJK 文字被压缩到几像素宽度 | 后处理移除 SVG 中的 `textLength` 和 `lengthAdjust` 属性 |
| **`note over X,Y` 仅限时序图** | 矩形图/组件图中报语法错误 | 使用 `note top/bottom/right/left of X` 替代 |

### CJK 渲染问题详解

**根因链**：
```
.puml → Graphviz → SVG（textLength 由字体 metrics 计算）
                         ↓
              server 无 CJK 字体 → fallback 字体返回近零宽度
                         ↓
              textLength ≈ 4px（应 ≈ 56px/4字）
                         ↓
              浏览器按 textLength 压缩文字 → 中文不可读
```

**五步修复管道**（`svg-to-png-cjk.cjs` 实现）：

| 步骤 | 操作 | 原因 |
|------|------|------|
| 1 | `sed` 移除 `textLength` 和 `lengthAdjust` 属性 | 错误的 textLength 强制浏览器压缩文字 |
| 2 | viewBox 宽度 ×2.5，高度 ×1.5 | CJK 文本正确渲染后宽度远超 server 预留 |
| 3 | 包装 HTML + CJK 字体栈 CSS | 通过 `!important` 覆盖 SVG 内嵌字体声明 |
| 4 | Playwright headless Chromium screenshot | 利用系统 CJK 字体正确计算排版 |
| 5 | JavaScript 计算所有 SVG 元素 bounding box → clip | 去除 viewBox 扩展后的空白区域 |

**CJK 字体栈**（覆盖主流平台）：
```css
svg text {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
               "Noto Sans CJK SC", "WenQuanYi Micro Hei",
               Arial, Helvetica, sans-serif !important;
}
```

---

## 三、复杂图表的根本性三方权衡

通过 16 个版本的迭代验证，发现 PlantUML 中存在一个**根本性的三方权衡**：

```
          Zone 边框（虚线分组区域）
          /      \
         /        \
   Actor 分布 ---- 注释完整性
```

**三者无法在 PlantUML 中同时完美实现**：

| 策略 | Zone 边框 | Actor 分布 | 注释完整 | 典型得分 |
|------|----------|-----------|---------|---------|
| LTR + zones + actor→zone | ✅ 有 | ❌ 聚集 | ❌ 不全 | ~51/100 |
| LTR + zones + actor→内部 | ⚠️ 膨胀 | ⚠️ 受限 | ❌ 不全 | N/A |
| 默认方向 + zones + actor→内部 | ⚠️ 膨胀 | ⚠️ 混乱 | ✅ 全 | N/A |
| **默认方向 + 无zone + actor→元素** | ❌ 无 | ✅ 好 | ✅ 全 | **~70/100** |
| LTR + 无zone + actor→元素 | ❌ 无 | ⚠️ 一般 | ❌ 不全 | ~52/100 |

### 当前最优策略（70/100）

当需要同时处理多区域分组、Actor 定位和丰富注释时：

1. **使用默认方向**（top-to-bottom）+ `-right->` 实现水平主流向
2. **不使用 zone 虚线边框**，改用 `note` 标签或 `package` 替代视觉分组
3. **Actor 通过 `.down.>` / `.up.>` 精确定位**在管道上下方
4. **包含全部注释**，短标签用箭头标签 (`: text`)，长说明用 `note` 元素

### 何时可以突破权衡

如果图表**不需要**同时满足三个条件，可以适当放松：
- **不需要 zone 边框** → 可以用 LTR + actor→元素，actor 分布尚可
- **不需要 actor** → 可以用 LTR + zones，zone 边框完整
- **不需要丰富注释** → 任何策略都能工作

> **理论上限**（估计 ~85/100）：如果 PlantUML/Graphviz 未来支持"Actor 穿越 zone 边界而不影响布局"的特性，可以同时实现三者。目前受引擎限制无法突破。

---

## 四、版本演进关键转折点

以下转折点对理解引擎行为最有价值：

| 版本 | 转折 | 关键发现 |
|------|------|---------|
| v1→v2 | 全英文标签 → 中文化 | 发现 CJK 零宽度渲染问题 |
| v3 | 修复 `-right->` → `-->` | 发现 LTR 模式下方向提示被重解释 |
| v4→v5 | 无zone → 有zone | 发现 actor→内部元素导致 zone 膨胀 |
| v7 | LTR → 默认方向 | Actor 分布显著改善 |
| v10 | 回退到 LTR + zones | 评分从 59 退步到 51（actor 聚集 + 注释不全） |
| v12 | 回退到默认方向 + 无zone | 70/100 — 最完整的注释覆盖和最佳 actor 分布 |
