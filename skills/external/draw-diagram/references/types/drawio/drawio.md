# drawio

## Goal

把**已经定好的**图表语义兑现为 draw.io / mxGraph 产物（`.drawio`，未压缩 mxGraph XML），并按需导出 SVG/PNG/PDF。本技能是 draw.io / mxGraph 的**实现层**：产物格式、XML 结构、渲染与导出。它不做语义判断、不选图类、不选引擎。

## Ownership Boundary（只给指针，不复写）

本技能 MUST NOT 内联任何语义层内容。「这张图该表达什么、该是什么结构、该长什么样、该由哪个引擎画」一律回下列 owner：

| 问题 | Owner（打开它；不要从这里复制） |
|------|--------------------------------|
| 语义模型（实体、层级、结构、关联；SDS/LDM schema） | `skills/external/draw-diagram/references/semantic-model.md`（**现存**） |
| **引擎选择**——含本引擎与他引擎的取舍、`drawio` ↔ `excalidraw` 可判优先序、独占登记、tie-break、反路由红线 | `skills/external/draw-diagram/references/routing-matrix.md`（**现存**：§0 能力轴层 / §1 独占 / §2 图类矩阵 / §3 tie-break / §4 红线） |
| 语义分析、图类选择、版面规划、样式配色、内容措辞、类专属约定 | 前门 `skills/external/draw-diagram/SKILL.md`（**现存**）。这些问题的**专章参考文件**（`references/howto/*`、`references/guide/*`、`references/document/*`）由 stage S1d 规划、**尚未落盘**——今日该 `references/` 树下只有上两行那两个文件。故此处**不预建具体路径**；在专章落盘前一律回前门 `SKILL.md`，不在本技能内自答 |

> **本技能不含任何路由叙事。** 「何时该选我而不选别的引擎」属引擎选择策略，owner 是 `routing-matrix.md`。绕开前门直接调用本技能不在其职责范围内。

## SDS 实现与强弱落地

本技能是绘图技能族的**语法层**：只拥有 draw.io / mxGraph 引擎语法（XML 结构、样式串）、SDS 实现与渲染导出。语义层——逻辑模型、geometry（canvas/box/anchor）、`weight_plan` 档位、typography 层级——归 draw-diagram，schema 见 [../draw-diagram/references/semantic-model.md](../../semantic-model.md)，此处不复述。

**输入契约**：draw-diagram 委派传入 **SDS 文件路径**。**MUST NOT 改写语义**——不增删元素/关系、不挪 box、不改档位次序；兑不了（如 label 装不进 box）→ 量化回报，不擅自修。无 SDS 的直接调用属越界（见上「不含路由叙事」），如仍被执行则 MUST 显式声明自规划的假设。

**强弱实现**（tier → `strokeWidth`；相对线宽语义与档位定义 owner = `semantic-model.md`，此处只落实绝对值。`strokeWidth` 缺省为 `1`）：

| 档位（语义角色） | strokeWidth | 落实要点 |
|------|------|------|
| T1 大模块/分区边界 | 3 | 实线；分区用容器（`swimlane`，见 `./references/mxgraph-format.md` §5） |
| T2 小模块/组件边界 | 2 | 实线 |
| T3 数据流/关系箭头 | 1.5 | edge 的 `strokeWidth`；若某渲染路径不接受小数宽度，钳位为 2 并把 T2>T3 的层级转移到**深浅通道**（`strokeColor` 更浅），与 excalidraw 同法 |
| T4 注释/副标题 | 1 | 独立 text 形状或细线 |

- zone 边界虚实：`dashed=1`（缺省 `0` = 实线）；仅当 `style_intent` 要求手绘观感时才用 `sketch=1`——**手绘美学是 excalidraw 的独占**，本引擎默认不启用。
- 关键路径仅色相抬升，线宽封顶 = T2；typography 落实（`fontSize`，缺省 `12`）：zone/图标题 18 > 元素标签 12 > 注释 10。
- **颜色取值不在本文件**：`fillColor` / `strokeColor` / `fontColor` 的**具体色值**是配色决策，owner 是前门的样式指引（尚未落盘）；本技能只负责把档位差落实为可辨的粗细与深浅。

**几何**：mxGraph 是**绝对坐标**引擎（`semantic-model.md` Deviation Declaration 第 1 类）→ **MUST 精确兑现 SDS box**（`x/y/width/height`、zone box、relation anchor+gap 照抄），容器内子元素按 SDS box 换算为**相对父容器**坐标。**预期零偏离**，不适用「逼近声明」豁免；未声明偏离按 semantic-fidelity 扣分。

> **布局授权与冻结**：按 `semantic-model.md`「布局授权」消费独立 `layout_policy`；优化不得改变 `reproduction` 语义。最终 SDS box 冻结后精确兑现，不在导出时移动 vertex。需重布局时先经前门授权与最终几何回读；ELK/libavoid 只有实际执行面支持才可调用，不能据官方文档假定当前 HTTP 后端可用（见 `./references/render-and-export.md` §3.5）。本地固定几何编译器入口见下节。

**细节**：XML 结构与样式串语法 → [./references/mxgraph-format.md](references/mxgraph-format.md)；渲染、导出与布局 pass → [./references/render-and-export.md](references/render-and-export.md)。

> **与其它五家的一处形差（如实记录）**：五个既有引擎各有独立的 `references/sds-realization.md` 承载几何映射表与复刻覆盖规则；本技能暂无该文件，SDS 落地细则全部内联于本节 + 上述两份 references。若本节继续增长，再按 `improve-skills` 拆出同名文件与套件对齐。

## 本地编译与回读校验

资源：`scripts/architecture.py`（Python ≥3.8 标准库）及 `scripts/tests/test_architecture.py`。输入契约归 [semantic-model.md](../../semantic-model.md)「固定几何架构 JSON」；不是渲染器，不依赖也不冒充 ELK/libavoid。

```bash
python3 "${SKILL_HOME}/references/types/drawio/scripts/architecture.py" compile --input architecture.json --output architecture.drawio --report compile-report.json
python3 "${SKILL_HOME}/references/types/drawio/scripts/architecture.py" validate --input architecture.json --diagram architecture.drawio --report validate-report.json
```

- 所有路径由调用方指定，父目录必须已存在，输出必须为新文件；拒绝覆盖输入、已有产物、符号链接及同名 report。退出 `0` 为通过、`1` 为输入/几何/走线验收失败、`2` 为参数或输出 I/O 错误；失败不生成伪安全直线。先检查报告，再导出。
- `optimize` 只整理走线，不移动 box。按稳定 ID 排序，使用稀疏正交可见网格与带方向 Dijkstra，成本含长度、弯折、交叉、共线及过近平行段；避开节点、无关分区与所有分区标题。算法是确定性逐边贪心，不保证全图最优或零交叉；无可用路由、资源上限或端口空间不足时明确失败。
- 贪心结束后运行**有界冲突修复**（最多 2 轮）：对端点互不相同的两条关系，若其简化路线存在共线重叠，则以 8× 共线代价重路由较晚的一条；仅当全图共线总长严格下降、交叉数增加不超过 1（以一次交叉换掉一段共享线，且每轮至多一次）、近平行长度不变差时采纳，否则保留原路线。修复只换走线，不移动 box；仍无法避免的共线/交叉照实报告，不冒充已消除。
- side 缺省按中心主方向确定；同侧端口按边 ID 等分，平行端口预留间距。容器左右端口避开标题。`preserve` 必须逐边提供两个 side 与完整 `via`（允许空数组表示直连），原样检查，不自动绕障；其端口仍按该确定性分配规则生成，不能表达任意实测端口比例。`optimize` 的 via 为必须经过的绝对锚点。
- `style` 只接受 `clearance`、`edgeSpacing`、`bendPenalty`、`crossingPenalty`、`collinearPenalty`、`fontFamily`；默认值以脚本 `DEFAULTS` 为准。均须正值，字体不能携带样式分隔符。矩形元素与水平标题容器是唯一形状子集；标题高度由 `title_height()` 决定，不提供自动文本测量。
- 边标签固定为水平 16px、白底与 4px 留白；按路段长度、节点/标题/分区边框/全部路线/已放标签的估算边界确定性择位（除垂直偏移外也枚举沿路线位移，短段无法容纳时仍可把标签整体移出边框），写入原生 `mxGeometry x/y` 与 `mxPoint as="offset"`，不增加节点或边。**分区边框（任一 zone 外框线穿过标签内部）同属冲突**：自动择位不得跨越，显式位置跨越即失败。自动无安全位置保留文字并报告 `label_unresolved`，不冒称视觉通过。可选 `relations[].label_position:{x,offset:{x,y}}`：x 是沿路径的归一化位置（-1..1），offset 是画布像素位移向量，不是父容器坐标；显式位置碰撞或读回偏离即失败。
- 原生 `jumpStyle=arc;jumpSize=6;jumpLayers=1` 来自官方 style-reference §4.4；仍报告原交叉/共线及线段内部 `proper_crossings`，不把接触或共线当作已解决的跨线。导出后可在 validate 命令追加 `--rendered-svg <existing.svg>`，只读核对 SVG 的 data-cell-id、实际字号、祖先 transform、白底留白和位置/碰撞。支持原生 SVG text/rect、平移及正轴缩放；HTML/栅格标签或不支持的变换明确失败。SVG 检查与曲线路径数量都不等于完整视觉验收或每一处跨线已验证；本工具不渲染。
- 编译结果是未压缩原生 XML，节点/容器位置与边方向不增删；父坐标换算按 `mxgraph-format.md` §5。validate 只验本编译器的单页、直接 mxCell 子集，不是任意 draw.io 文件/XSD 校验器。报告含期望/实际三类计数、语义差异、重叠/包含/标题/正交/穿框错误，以及交叉和共线长度 warning；warning 不等于消除。
- 自环、非正交保留路线、无法避开的标题端口、未知字段与无效引用均失败；最多 500 个节点/分区、1000 条关系；坐标绝对值及画布尺寸上限为一百万，路由网格上限见 `MAX_GRID`。`visual_validation=not_performed` 始终保留：中文、标题裁切、箭头观感与边标签遮挡需用同一 XML 实际导出后另验。

## 原生回读与渲染核对（native-readback.py）

资源：`scripts/native-readback.py`（Python ≥3.8 标准库）。独立读取**实际产物**（不是输入副本），并在给出 `--svg` 时核对实际渲染。

```bash
python3 "${SKILL_HOME}/references/types/drawio/scripts/native-readback.py" \
  --source architecture.drawio --semantics shared-semantics.json \
  [--svg architecture.svg] --output readback-report.json
```

- 原生侧：从 mxGraph cell 读出实际 elements/zones/edges、parent（分区成员）、source/target（方向）、value（标签）、strokeColor/fillColor 与几何，与权威语义逐项对照 id、成员、方向、标签与颜色。**任何多出的 cell（含携带文字的隐藏图例）都作为硬差异列出**——期望语义没有的图形内容即未被授权。
- 渲染侧（`--svg`）：先由实际顶点 rect 标定画布映射，再核对分区外框 path、边 body path 的起点/箭头落点/是否偏离原生路线、标签文本与白底位置，以及**标签是否跨越分区边框**；交叉与不相关关系的共线重叠从实际渲染折线测量并单列（测量口径，不是硬失败）。
- 退出码：`0` 通过；`1` 硬差异或 partial（partial 不算通过）；`2` 参数/输入输出错误；`3` 不支持的原生或 SVG 结构（显式报告，不伪造覆盖）。
- 明确限制：曲线命令（跳线弧）区间不参与几何计算；文本宽度为声明性字符估算而非字体测量；旋转/反射变换不支持；不做交互验证，不替代视觉验收。

**已知限制与返修判据（引擎事实；某次运行的具体量化值归该次 manifest 与验收记录，不写进本文件当通用门槛）**：

- **报告是确定性检查，warning 不等于消除**：交叉/共线与穿框错误以 `compile/validate` 报告为准；返修 = 改生成源（`architecture.json` 的 box/via/side）后重新 compile + validate，并对比前后报告，不得以单次渲染结果声称零交叉。
- **重排会转移而不是消除缺陷**：调整布局常把共线/交叉从一处挪到另一处；验收看报告前后差量与未解决清单，单点改善不算修好。
- **标签与路径的认知限制**：SVG 组件/分区标签为 foreignObject + 图片后备，边端点语义以原生 `source`/`target` 为准，最终路径不独立反推；`validate --rendered-svg` 只核对原生 text/rect 子集，不等于完整视觉验收。

四轴验收与 manifest 判据见 [quality-gate.md](../../quality-gate.md)；结果写入 manifest 的 `crossings`（测量口径随本次运行声明）与 `unresolved`。

## 本技能自有内容

两份引擎知识参考与上述可执行资源：

- [`./references/mxgraph-format.md`](references/mxgraph-format.md) — 产物格式与必备 XML 结构：两种可接受形态、两根结构 cell、`parent` 规则、`mxGeometry as="geometry"`、vertex/edge 属性、标签与元数据载体、样式串语法、最小骨架、生成硬性规则与自检清单。
- [`./references/render-and-export.md`](references/render-and-export.md) — 渲染与导出：CLI 导出命令与 `--layout` 开关、查看/嵌入路径、**布局与走线的事实**（默认内建 router 无避障；布局 pass 为可选）、分平台二进制定位。

两份都只承载实现细节，不得复写语义层指引。

## 生成契约（摘要 — 详见 `./references/mxgraph-format.md`）

1. **形态二选一**：完整形 `mxfile > diagram > mxGraphModel > root`，或**简化形**只给 `mxGraphModel`（draw.io 打开时自动补齐外层；官方推荐 AI 生成用简化形，需多页时才用完整形）。
2. **两根结构 cell 必备**：`<mxCell id="0"/>`（根容器，无 parent）与 `<mxCell id="1" parent="0"/>`（默认图层）。
3. **vertex 与 edge 都必须带 `parent`**（通常为 `"1"`，或所属 group/layer 的 id）。只有 `id="0"` 可以没有 parent。
4. `vertex="1"` 与 `edge="1"` **互斥**；`id` 在同一 diagram 内唯一，任意字符串皆可。
5. `mxGeometry` 必须带 **`as="geometry"`** 才被识别为该 cell 的几何。
6. **一律未压缩 XML**：绝不生成 `compressed="true"`，绝不生成 Base64/deflate 负载。
7. **绝不输出 XML 注释** `<!-- -->`：官方明令禁止（浪费 token、可能引发解析错误、对图形无语义）。
8. 样式是 cell 上的**字符串属性** `style`，`key=value` 以 `;` 连接，可含裸 token（形状名 / 样式类名）。
9. 标签走 `value`；自定义元数据走 `UserObject` / `object` 的 `label`（此时**嵌套的 mxCell 不带自己的 id**）。
10. 普通边可由引擎走线；固定几何编译路径必须生成显式 waypoint 与固定 exit/entry 端口，禁用默认再路由；坐标归属见 `mxgraph-format.md` §5。
11. **非矩形形状必须配匹配的 `perimeter=`**（否则连接点计算错位）。已确证的取值只有两个：`rectanglePerimeter`（默认）与 `ellipsePerimeter`（配 `ellipse`）；其余取值目录 owner 是官方 `style-reference.md` §6，本技能不复制、也不按命名长相推断。

> **验证状态（必读）**：结构条款引据官方 XSD/参考文档；第 10 条的固定几何编译路径由本技能提供并以脚本回读校验，不把历史样本的 XSD 通过当作本次产物或导出通过。真实导出与视觉验收须单独执行（见 `./references/mxgraph-format.md` §9）。

## 渲染与导出（摘要 — 详见 `./references/render-and-export.md`）

- **最短可运行链路**：`architecture.json` → `architecture.py compile --report` → `validate`（可加 `--rendered-svg` 核对既有导出）→ 共享契约的 `POST /svg`、`POST /png`（body = `<mxfile>` XML）或 `drawio -x` CLI → `native-readback.py`（原生 + 实际 SVG 独立回读）；**同一份 XML** 导出后回读。端口与请求 shape 的 owner 是 `../../self-deploy-render-service.md`，此处不复述。
- **CLI 导出**：`drawio -x -f svg|png|pdf -o <out> <in>`；无图形环境的 Linux 以 `xvfb-run -a` 包裹。这是官方文档确证的既有成熟路径；**本机尚未实测**，且 drawio-desktop 官方 README 无 CLI 章节，故完整开关表仍属未决项。
- **`--layout` 开关**：可在创建后跑一次布局 pass，取值为预设名（`verticalFlow` / `horizontalFlow` / `verticalTree` / `horizontalTree` / `radialTree` / `organic`）或自定义 layout JSON 数组。
- **几何事实**：`.drawio` 格式自身**不做任何布局计算**——vertex 必须携带显式 `x/y/width/height`。但布局与走线 pass 是**可选叠加**的：默认内建 router 很基础（直线或简单直角，**无避障**，连线会直接穿过中间的形状）。
- **三个 pass 的调用面尚未确证**：`routing=libavoid` / `postLayout=elk` / `applyLayouts` 在官方文档中是 **MCP server `create_diagram` 的参数名**；其在 Desktop CLI 上的等价开关**只确证了 `--layout`**。首次真实出图前不得把这三者当作 CLI 开关直接调用——详见 `./references/render-and-export.md` §4 未决项 9。

> **轴②「渲染位置」不在本技能内声明。** 渲染方式（本地 / 远端 / 共享渲染服务）正在另一条流程中重新裁定；本文件与其 references 只登记**引擎能力事实**，不声明本套件采用哪条渲染路径。选路判据的 owner 是 `skills/external/draw-diagram/references/routing-matrix.md` §0。

## 交付形态（Delivery）

规则 owner = [../draw-diagram/references/delivery-contract.md](../../delivery-contract.md)（D1–D6，七技能统一）。本节只写 **draw.io 侧的机械落地**，不复写规则。

**同目录三件套**（缺 HTML 即不合格）：

| 产物 | 说明 |
|------|------|
| `<name>.drawio` | **源文件**，未压缩 mxGraph XML；保留以供未来在 draw.io 中继续编辑 |
| `<name>.svg`（+ 按需 `.png` / `.pdf`） | 经 CLI 导出的**渲染图**，与 HTML 同目录 |
| `<name>.html` | **用户直接双击打开的入口**，相对路径引用同目录的图 |

- **HTML 由 Agent 组装**（本技能不带脚本）：页面主体是 `<img src="<name>.svg">`（相对路径，MUST NOT 写绝对路径），离线可看；`<html lang>` 与页面文字语言跟用户一致。
- **复现性附录**：可折叠 `<details>` 块内放 `.drawio` 源码 + 实际用的导出命令；附录源码 MUST 与磁盘上那份 `.drawio` **逐字节一致**（直接从磁盘复制，不凭记忆重写）。
- **文字规则在本引擎的落点**：图内标签走 `mxCell` 的 `value=`，HTML 说明文字走页面正文——**两者都**受契约 D3–D5 约束（条文与示例见契约，本节不复写）。
- **未导出成功的兜底**：若本机无 draw.io CLI 导致无法导出图片，MUST 如实说明「只交付了 `.drawio` 源文件与一个引用它的 HTML，图需在 draw.io 中打开」，**不得**假装已交付可直接查看的图。

## 参考文档（外部权威源）

本技能不复写 draw.io 的样式目录与形状库——它们的 owner 是官方文档：

- 生成与校验总纲：https://www.drawio.com/docs/reference/diagram-generation/
- 样式与形状完整参考（官方，供 AI 生成用）：https://github.com/jgraph/drawio-mcp/blob/main/shared/style-reference.md
- 规范 XML 生成参考（官方 MCP 各 prompt 的唯一真源）：https://github.com/jgraph/drawio-mcp/blob/main/shared/xml-reference.md
- 结构校验 XSD：https://github.com/jgraph/drawio-mcp/blob/main/shared/mxfile.xsd
