# 条件优化：使用 ! 代替 == 判断

## 分析

布尔值本质上表示`true`或`false`。直接将它们与`true`或`false`进行比较是多余的，而且稍微浪费 Gas。与其使用`if (booleanValue == true)`，不如直接使用`if (booleanValue)`。对于错误检查，可以使用`if (!booleanValue)`而不是`if (booleanValue == false)`。

优点包括：

1. **气体效率：**避免直接比较可以节省一些气体，因为在 EVM 中执行的操作码更少。

2. **代码清晰度：**直接使用布尔值通常会产生更易读、更简洁的代码。



## 测试

**文件位置：**

```Bash
src/compiler/Not.sol
test/compiler/Not.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_not_ -vvv --optimize
```



![条件优化：使用 ! 代替 == 判断图示](/images/gas-optimization-master/compiler/02-not-vs-eq-01.png)



## 总结

1. **识别布尔比较**：检查您的智能合约以使用布尔比较来定位`== false`。

2. **使用逻辑非**：用`!true`代替`== false`比较，以在每次操作中节省少量气体。

3. **测试**：实施彻底的测试，以确保变更在节省 gas 的同时保持预期的合同行为。

## 对应源码

- [`src/compiler/Not.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Not.sol)
- [`test/compiler/Not.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Not.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
