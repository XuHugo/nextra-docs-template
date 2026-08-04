# 使用 ++i 替换 i++

## 分析

在Solidity中，前置自增\(`++i`\)和后置自增\(`i++`\)在某些情况下会产生不同的字节码，特别是在循环和复杂表达式中。理解这些差异有助于编写更高效的代码。

**后增（****`i++`****）：**

使用`i++`时，它是一个后增操作。这意味着先使用`i`的值，然后再进行递增。这涉及在`i`的原始值递增之前临时存储它，以便操作可以使用或返回它。这意味着无论您是否要使用，堆栈上都会存储两个值以供使用。

以下是具体内容：

- `j = i;`此步骤涉及将 的当前值赋给`i`临时变量`j`。这是一个额外的操作，会消耗 gas。

- `i = i + 1;`这会增加`i`的值。

- `return j;`最后，返回的原始值`i`（现在存储在`j`中）。

由于额外的步骤和临时变量的使用，后增量往往会消耗更多的 gas。

**预增量（****`++i`****）：**

另一方面，`++i`是预增操作。它先增加`i`的值，然后使用它或返回它，这更直接，步骤更少。这意味着只需要在堆栈上存储一个项。

以下是具体内容：

- `i = i + 1;`此步骤会增加`i`的值。

- `return i;`此步骤返回新的增量值。

**合理的：**

关键区别在于后置增量（`i++`）中使用的临时变量和额外的赋值操作。EVM 会为每个计算步骤收取 Gas 费用，由于后置增量涉及更多步骤，因此 Gas 成本往往更高。在以太坊智能合约中，优化 Gas 至关重要，以确保其运行经济。因此，尽可能选择预增量 \( `++i`\) 而不是后增量 \( `i++`\) 是 Gas 优化的更好做法。

## 测试

**文件位置：**

```Bash
src/compiler/Increment.sol
test/compiler/Increment.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_increment_ -vvv --optimize
```



![使用 ++i 替换 i++图示](/images/gas-optimization-master/compiler/11-prefix-increment-01.png)



## 总结

- **识别循环增量**：检查智能合约中计数器变量增加的循环结构。

- **使用预增量**：在循环中更改`i++`为`++i`在每次迭代中节省gas。

- **测试**：通过进行彻底的测试确保更改不会影响合同的功能。

## 对应源码

- [`src/compiler/Increment.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Increment.sol)
- [`test/compiler/Increment.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Increment.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
