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

## 首条(种子)

- [programming-tools.md](programming-tools.md) § **Git clone 的默认协议**:默认用 HTTPS 作 clone URL;特殊仓库需要 HTTP 时必须显式提示;反例 = 此前 `~/.git-credentials` 记录了 HTTP 认证信息而 install 用 HTTPS clone 造成的认知偏差。