# Yul 介绍

## 为什么要用 Yul？

Solidity 编译器已经很智能了，但它就像一个“自动挡”汽车，方便但有时不够经济。Yul 则是“手动挡”，它能让你：

1\.  **绕过编译器检查**：例如，执行没有溢出检查的数学运算，节省 Gas。

2\.  **直接操作内存和堆栈**：避免不必要的内存变量和复制，实现更高效的数据流。

3\.  **访问底层 EVM 操作码**：使用一些 Solidity 语言层面没有直接暴露的、但非常省 Gas 的操作。

**核心思想**：把 Yul 当作一把手术刀，对合约中消耗 Gas 最多的“热点”代码进行精准优化。



## EVM 的核心部件

在开始之前，我们必须了解 EVM 的四个核心工作区域：

1\.  **堆栈 \(Stack\)**：临时的“计算台”，后进先出。所有计算都在这里进行。操作堆栈本身几乎不消耗 Gas。

2\.  **内存 \(Memory\)**：临时的“草稿纸”，用于存储临时数据，交易结束时清空。**扩展内存的成本是按其大小的平方增长的，非常昂贵。**

3\.  **Calldata**：只读的“收件箱”，存放交易的输入数据。**访问 Calldata 非常便宜。**

4\.  **存储 \(Storage\)**：永久的“硬盘”，数据会永久保存在链上。**读写存储是 EVM 中最昂贵的操作。**

**Gas 优化第一定律：** 尽可能在**堆栈**上完成计算，多从 **Calldata** 读取数据，谨慎使用**内存**，极度审慎地操作**存储**。



## Yul 基础语法

Yul 的代码都写在 `assembly { ... }` 块中。

### 1. 注释

和 JavaScript 一样，使用 `//` 和 `/* ... */`。

```Plain Text
// 单行注释

/*
  多行注释
*/
```

### 2. 变量声明与赋值

- 使用 `let` 关键字声明变量。

- 使用 `:=` 进行赋值。

- Yul 变量存储在**堆栈**上，这使得访问非常高效。

```Plain Text
assembly {
    // 声明变量 x 并赋值为 10
    let x := 10

    // 声明变量 y，默认为 0
    let y

    // 给 y 赋值
    y := add(x, 5) // y 现在是 15
}
```



### 3. 作用域

使用花括号 `{}` 创建新的作用域，作用域内的变量在外部不可访问。这有助于管理堆栈，避免“堆栈太深”的错误。

```Plain Text
assembly {
    let x := 1
    {
        let y := 2
        x := add(x, y) // x = 3
    }
    // 在这里访问 y 会导致编译错误
}
```



### 4. if 语句 (条件分支)

`if` 语句用于条件判断，它**没有 **`else`。如果需要 `else` 的逻辑，需要结合 `if` 和 `jump `来实现。

```Plain Text
assembly {
    let x := 10
    if eq(x, 10) {
        // 如果 x 等于 10，执行这里的代码
        let y := 20
    }
}
```



### 5. switch 语句 (多重分支)

`switch` 语句用于匹配多个条件。它会计算一个表达式，然后与多个 `case` 进行比较。

- `case` 后面必须是字面量（不能是变量）。

- `default` 是可选的，当所有 `case` 都不匹配时执行。

```Plain Text
assembly {
    let x := 2
    switch x
    case 1 {
        // x 是 1
    }
    case 2 {
        // x 是 2，代码会从这里执行
    }
    default {
        // x 不是 1 也不是 2
    }
}
```



### 6. for 循环

`for` 循环包含三个部分：初始化、条件判断和后处理。

- **初始化 \(**`for { let i := 0 } ...`**\)**: 在循环开始前执行一次。

- **条件判断 \(**`... lt(i, 10) ...`**\)**: 每次循环开始前检查，如果为假 \(0\)，则退出循环。

- **后处理 \(**`... { i := add(i, 1) }`**\)**: 每次循环结束后执行。

```Plain Text
assembly {
    for { let i := 0 } lt(i, 5) { i := add(i, 1) } {
        // 循环体，会执行 5 次 (i = 0, 1, 2, 3, 4)
        let x := mul(i, 2)
    }
}
```



### 7. 函数 (Functions)

Yul 中可以定义自己的函数，这有助于代码复用和组织。

- 函数可以有参数和返回值。

- 返回值通过 `->` 符号指定。

```Plain Text
assembly {
    // 定义一个函数 my_add，接收两个参数 a, b，返回一个值
    function my_add(a, b) -> result {
        result := add(a, b)
    }

    // 调用函数
    let sum := my_add(10, 5) // sum 会是 15
}
```



## Yul 核心语汇 —— EVM 指令详解

### 1. 算术与逻辑运算 (Arithmetic & Logic Operations)

这些指令在堆栈上对数据进行计算，是所有复杂逻辑的基础。

|指令|描述与参数|示例 \(Yul\)|
|---|---|---|
|`add(x, y)`|`x + y`|`let sum := add(a, b)`|
|`sub(x, y)`|`x - y`|`let diff := sub(a, b)`|
|`mul(x, y)`|`x * y`|`let prod := mul(a, b)`|
|`div(x, y)`|`x / y` \(整数除法\)|`let ratio := div(a, b)`|
|`mod(x, y)`|`x % y` \(取模\)|`let rem := mod(a, b)`|
|`exp(x, y)`|`x` 的 `y` 次方|`let power := exp(base, exponent)`|
|`iszero(x)`|判断 `x` 是否为零 \(`x == 0`\)|`if iszero(value) { revert(0, 0) }`|
|`eq(x, y)`|判断 `x` 是否等于 `y`|`if eq(caller(), owner) { ... }`|
|`lt(x, y)`|判断 `x` 是否小于 `y`|`for {} lt(i, 10) {}`|
|`gt(x, y)`|判断 `x` 是否大于 `y`|`if gt(balance, 100) { ... }`|
|`and(x, y)`|按位与|`let masked := and(data, 0xFF)`|
|`or(x, y)`|按位或|`let combined := or(flags1, flags2)`|
|`xor(x, y)`|按位异或|`let toggled := xor(bits, mask)`|
|`not(x)`|按位取反|`let inverted := not(value)`|

**Gas 优化技巧**:

- Yul 中的算术运算默认是 `unchecked` 的，没有溢出检查，因此比 Solidity 的标准算术运算 Gas 成本更低。请确保在逻辑上不会发生溢出时才使用。

- 使用 `iszero` 判断是否为零比 `eq(x, 0)` 更便宜。



### 2. EVM 环境与状态信息 (Environment & State Information)

这些指令用于获取当前交易和区块链状态的信息。

|指令|描述|示例 \(Yul\)|
|---|---|---|
|`address()`|获取当前执行合约的地址 \(`this`\)。|`let self := address()`|
|`balance(addr)`|获取地址 `addr` 的 ETH 余额。|`let bal := balance(caller())`|
|`caller()`|获取直接调用者的地址 \(`msg.sender`\)。|`if eq(caller(), owner) { ... }`|
|`callvalue()`|获取随调用发送的 ETH 数量 \(`msg.value`\)。|`if gt(callvalue(), 1) { ... }`|
|`origin()`|获取交易的发起者地址 \(`tx.origin`\)。|`let tx_sender := origin()`|
|`gasprice()`|获取交易的 Gas 价格 \(`tx.gasprice`\)。|`let price := gasprice()`|
|`blockhash(b)`|获取区块号 `b` 的哈希值。|`let hash := blockhash(sub(number(), 1))`|
|`coinbase()`|获取当前区块的矿工地址。|`let miner := coinbase()`|
|`timestamp()`|获取当前区块的时间戳。|`let now_time := timestamp()`|
|`number()`|获取当前区块的区块号。|`let block_num := number()`|
|`difficulty()`|获取当前区块的难度。|`let diff := difficulty()`|
|`gaslimit()`|获取当前区块的 Gas 限制。|`let limit := gaslimit()`|
|`chainid()`|获取当前链的 ID。|`let id := chainid()`|
|`selfbalance()`|获取当前合约的 ETH 余额。|`let my_bal := selfbalance()`|





### 3. 内存与存储操作 (Memory & Storage)

|指令|描述|示例 \(Yul\)|
|---|---|---|
|`mload(p)`|从内存地址 `p` 加载 32 字节。|`let data := mload(0x80)`|
|`mstore(p, v)`|将 32 字节的 `v` 存储到内存地址 `p`。|`mstore(0x80, 42)`|
|`mstore8(p, v)`|将 `v` 的最低一个字节存储到内存地址 `p`。|`mstore8(0x80, 'c')`|
|`msize()`|返回当前已分配的内存大小（字节）。|`let current_size := msize()`|
|`sload(p)`|从存储槽 `p` 加载 32 字节。|`let owner := sload(0)`|
|`sstore(p, v)`|将 32 字节的 `v` 存储到存储槽 `p`。|`sstore(0, caller())`|
|`calldataload(p)`|从 Calldata 的 `p` 位置加载 32 字节。|`let arg1 := calldataload(4)`|
|`calldatasize()`|返回 Calldata 的总字节大小。|`let size := calldatasize()`|
|`calldatacopy(t, f, s)`|将 Calldata 的数据复制到内存。|`calldatacopy(0x80, 0, calldatasize())`|



### 4. 流程控制 (Control Flow)

|指令|描述|示例 \(Yul\)|
|---|---|---|
|`jump(label)`|无条件跳转到 `label` 标记的位置。|`jump(loop_start)`|
|`jumpi(label, cond)`|如果 `cond` 不为零 \(true\)，则跳转。|`jumpi(error_handler, iszero(success))`|
|`pc()`|获取当前程序计数器的位置。|`let current_pc := pc()`|
|`gas()`|获取剩余的 Gas 量。|`let remaining_gas := gas()`|
|`return(p, s)`|成功停止执行，并返回内存中从 `p` 开始的 `s` 字节数据。|`return(0x80, 32)`|
|`revert(p, s)`|回滚状态，并返回内存中从 `p` 开始的 `s` 字节错误信息。|`revert(0, 0)`|
|`stop()`|成功停止执行，不返回数据。|`stop()`|
|`invalid()`|无效指令，导致交易失败并消耗所有 Gas。|`invalid()`|



### 5. 合约交互 (Contract Interaction)

|指令|描述与参数|返回值|
|---|---|---|
|`call(...)`|调用另一个合约。|`1` \(成功\) / `0` \(失败\)|
|`delegatecall(...)`|在当前合约上下文中执行另一个合约的代码。|`1` \(成功\) / `0` \(失败\)|
|`staticcall(...)`|对另一个合约进行只读调用。|`1` \(成功\) / `0` \(失败\)|
|`create(val, p, s)`|创建新合约。|新合约地址 / `0` \(失败\)|
|`create2(val, p, s, salt)`|使用 `salt` 创建地址确定的新合约。|新合约地址 / `0` \(失败\)|
|`returndatasize()`|获取上一次外部调用返回的数据大小。|`let size := returndatasize()`|
|`returndatacopy(t, f, s)`|将上一次外部调用返回的数据复制到内存。|`returndatacopy(0x80, 0, returndatasize())`|



`call` 示例:

```Plain Text
// 调用 otherContract.someFunction(123)
// 假设函数选择器和参数已写入内存 0x00 处
let success := call(
    gas(),          // gas: 传递所有剩余 gas
    otherContract,  // to: 目标合约地址
    0,              // value: 不发送 ETH
    0x00,           // argsOffset: 输入数据在内存中的起始位置
    36,             // argsSize: 输入数据大小 (4-byte selector + 32-byte argument)
    0x00,           // retOffset: 用于存储返回数据的内存起始位置
    32              // retSize: 期望返回数据的最大字节大小
)
if iszero(success) { revert(0, 0) }
let result := mload(0x00)
```



## 实战演练

### 场景一：高效的 ETH 转账

Solidity 的 `.transfer()` 和 `.send()` 有 2300 Gas 的硬编码限制，如果接收方是一个有复杂 fallback 函数的合约，可能会导致转账失败。使用 `call` 可以更灵活地控制 Gas。

```Solidity
*function* transferEth(*address* *payable* *recipient*, *uint256* *amount*) *public* {
    assembly {
        // call(gas, to, value, in, insize, out, outsize)
        // 我们不发送任何数据 (in, insize = 0, 0)
        // 也不期望任何返回数据 (out, outsize = 0, 0)
        *let* success := call(gas(), recipient, amount, 0, 0, 0, 0)

        // 必须检查 call 的返回值！
        if iszero(success) {
            revert(0, 0)
        }
    }
}
```



### 场景二：更便宜的require

使用 `iszero` 和 `revert(0, 0)` 可以实现比 `require(condition, "error message")` 更省 Gas 的检查。

```Solidity
// 常规 Solidity
// require(owner == msg.sender, "Not owner");

// Yul 优化
assembly {
    // sload(0) 假设 owner 存储在 slot 0
    // eq(caller(), sload(0)) 比较调用者和 owner
    // iszero(...) 如果不相等（eq 返回 0），iszero 返回 1
    if iszero(eq(caller(), sload(0))) {
        // revert(0, 0) 表示不返回任何错误数据，这是最便宜的回滚方式
        revert(0, 0)
    }
}
```



## 总结

1\.  Yul 是性能优化的利器，但也会增加代码的复杂性和风险。

2\.  始终以可读性和安全性为先，只在关键的性能瓶颈处进行优化。

3\.  利用 `calldataload` 减少内存拷贝，利用 `revert(0,0)` 降低错误处理成本。 

4\.  使用 `call` 系列指令时，务必检查返回值。 

****

## 对应源码

- [Gas Optimization Master 配套代码](https://github.com/XuHugo/gas_optimization_master/tree/8960383)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
