# Gas 常量：EVM 操作成本

`文件首先定义了一系列常量，它们是所有 Gas 计算的基础。让我们分类来看一些重要的常量。`

## 基础与算术操作

|常量|值|描述|
|---|---|---|
|`GAS_JUMPDEST`|1|`JUMPDEST` 指令的成本。它是唯一有效的跳转目标。|
|`GAS_BASE`|2|一些最简单的指令，如 `ADDRESS`, `CALLER`。|
|`GAS_VERY_LOW`|3|常见的算术运算，如 `ADD`, `SUB`, `NOT`, `AND`。|
|`GAS_LOW`|5|稍复杂的运算，如 `MUL`, `DIV`。|
|`GAS_MID`|8|更复杂的运算，如 `ADDMOD`, `MULMOD`。|
|`GAS_HIGH`|10|`SIGNEXTEND` 指令。|

**`示例`**`: `a + b` 的操作大致会消耗 `GAS_VERY_LOW` (3 Gas)。`

## 存储操作 (SSTORE)

`这是最昂贵的操作之一，因为它改变了区块链的永久状态。`

|常量|值|描述|
|---|---|---|
|`GAS_STORAGE_SET`|20,000|**创建**一个新的存储槽（从 0 \-\> 非 0）。|
|`GAS_STORAGE_UPDATE`|5,000|**更新**一个已存在的非 0 存储槽。|
|`GAS_STORAGE_CLEAR_REFUND`|4,800|**清理**一个存储槽（从非 0 \-\> 0）时获得的**退款**。|
|`GAS_COLD_SLOAD`|2,100|**冷访问**：交易中首次读取一个存储槽。|
|`GAS_WARM_ACCESS`|100|**热访问**：再次读取一个已访问过的存储槽。|

**`示例`**`: `myVar = 123;``

- `如果 myVar 之前是 0 (冷访问): 成本约为 GAS_COLD_SLOAD + GAS_STORAGE_SET = 22,100 Gas。`

- `如果 myVar 之前是 456 (热访问): 成本约为 GAS_WARM_ACCESS + GAS_STORAGE_UPDATE = 5,100 Gas。`

## 内存操作 (MLOAD, MSTORE)

`内存操作的基础成本很低，但其动态成本是关键。`

|常量|值|描述|
|---|---|---|
|`GAS_MEMORY`|3|内存扩展成本的线性部分系数。|
|`GAS_COPY`|3|`MCOPY` 指令每复制一个 word \(32字节\) 的成本。|

**`关键点`**`: 内存的主要成本来自于`**`扩展`**`，我们将在下一节详细分析。`

## 合约调用与创建

|常量|值|描述|
|---|---|---|
|`GAS_CREATE`|32,000|`CREATE` 指令的基础成本。|
|`GAS_NEW_ACCOUNT`|25,000|当 `CALL` 或 `CREATE` 创建一个新账户时产生的额外成本。|
|`GAS_CALL_VALUE`|9,000|当 `CALL` 转移 ETH \(value \> 0\) 时的额外成本。|
|`GAS_CALL_STIPEND`|2,300|当 `CALL` 转移 ETH 时，给予子调用的一笔“津贴”，确保其有足够 Gas 执行。|

## 对应源码

- [Gas Optimization Master 配套代码](https://github.com/XuHugo/gas_optimization_master/tree/8960383)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
