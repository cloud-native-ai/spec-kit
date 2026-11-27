# 通用最佳实践 (General Best Practices)

> 本模块是 **Spec Kit** 框架的**日常开发经典最佳实践**库:记录那些反复出现、值得沉淀的工程经验。它是**渐进积累**的内容,而非一次性清单——每条最佳实践都来自一次真实的开发摩擦/教训,经复核后沉淀到对应模块。
>
> 归属 Feature 111(General Best Practices);积累机制按指针抵达既有引擎,不新建机制。

## 四个模块(封闭集)

| 模块 | 文件 | 内容 |
|------|------|------|
| **编程语言** | [programming-languages.md](programming-languages.md) | 语言级惯用法、类型/并发/内存模型陷阱 |
| **系统接口** | [system-interfaces.md](system-interfaces.md) | 操作系统 / 进程 / 网络 / 文件系统的接口约定 |
| **编程框架** | [programming-frameworks.md](programming-frameworks.md) | 框架级结构与流程的可靠做法 |
| **编程工具** | [programming-tools.md](programming-tools.md) | 工具(CLI / 构建 / 版本控制 / 调试)的正确用法与默认口径 |

模块集合是**封闭集**:新增模块 MUST 只经修订本 README + 建立对应 owner 文件 + 更新守卫 `tests/contract/test_general_best_practices.py`。

## 条目形态

每个模块的 owner 文件按统一条目形态逐条积累:

- **标题** —— 一句话的实践名;
- **实践** —— 可操作的正确做法(默认口径 + 例外);
- **反例 / 证据** —— 触发的真实缺陷或偏差(带路径/命令/观察),说明这条为何成立;
- **延伸**(可选) —— 边界情形下的处置口径。

条目形态的契约面见 `.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md`(三元 = 标题 + 实践 + 反例/证据,可选 延伸)。

## 逐步积累机制(progressive accumulation)

最佳实践**经既有的 feedback 引擎逐步积累**,本模块不新建第二引擎、第二存储、第二渲染器或索引:

1. **观察**:开发中遇到一次真实摩擦/教训时,经 `.specify/scripts/python/feedback-utils.py --action record` 落一条观察——`[best-practice]` 标记与四类之一的 owner 文件 stem(`programming-languages` / `system-interfaces` / `programming-frameworks` / `programming-tools`,不带 `.md`)写入该记录的 `--review` 文本;记录形态、其余参数与存储处置归该引擎的 `--help`,本模块不新增字段、动作或存储。
   - **身份约定**:摩擦发生在框架命令/技能运行内时,用该运行的 unit id 与类型(`/speckit.<command>` + `command`,或 `skill:<name>` + `skill`)并以该 run id 作 `--run-id`;无此类运行承载的 ad-hoc 观察用 `--unit-id custom:best-practices/observation --unit-type custom-unit --run-id bp-<yyyy-mm-dd>-<slug>`;装载 probe 注册表的工作区须先按 probe 系统为该 custom 单元建立外部 probe(`probe-utils.py --action probe-inject`,义务归 probe 系统)。观察本身不写入本模块。
2. **复核(晋升)**:一条观察只有在被证明**通用**时才成为条目——判据 = **反复出现**,或**一次明确的用户纠正**。本节**拥有**该晋升程序与通用判据:满足判据时,按本程序把观察沉淀为条目,落到观察 `--review` 文本所命名的 owner 文件,并遵守「条目形态」节;晋升不改写既有观察记录、不新增 feedback 状态、不建立并行的晋升台账。
3. **留痕**:每条晋升条目 MUST 携带 `**来源**` 项目符号,至少给出以下之一——feedback 条目 ID / 提交号(hex,≥7 位)/ 会话原话引用——并写明「通用」判定依据(反复出现或一次明确的用户纠正),使条目可回溯到其实证。首条种子豁免来源行。
4. **知识记录义务**:晋升沉淀之外的知识记录义务与强调升级按指针归 `.specify/shared/guidelines/knowledge-promotion.md`,本节只引用、不复述其取值。
5. **红线**:干净运行 MUST NOT 追加空洞条目;MUST NOT 编造数值或证据;存量模块由 `scripts/python/sync-mirrors.py` 镜像到 `.specify/shared/best-practices/`,MUST 保持字节一致。

本模块只承载**内容**;观察的记录按指针复用既有 feedback 引擎,知识记录义务按指针归既有 owner,晋升程序与通用判据为本节自有规则——不新建存储或渲染器。

## 首条(种子)

- [programming-tools.md](programming-tools.md) § **Git clone 的默认协议**:默认用 HTTPS 作 clone URL;特殊仓库需要 HTTP 时必须显式提示;反例 = 此前 `~/.git-credentials` 记录了 HTTP 认证信息而 install 用 HTTPS clone 造成的认知偏差。