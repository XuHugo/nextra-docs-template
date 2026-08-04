# x = x + y 与 x += y

## 分析

在 Solidity 中，复合赋值操作`x += y`是`x = x + y`的语法糖。然而，前者的 Gas 成本往往会略高一些。额外的成本源于复合赋值操作本身带来的开销。因此，直接使用`x = x + y`可能是一种更节省 Gas 的方法。

1. **复合分配：**复合分配操作（`+=`、`-=`等）的额外开销会导致 gas 消耗略有增加。

2. **交易累积：**在具有大量交易的合约或广泛使用的协议中，使用复合任务产生的额外 gas 会大量累积，从而影响整体效率。

## 测试

**文件位置：**

```Bash
src/compiler/Add.sol
test/compiler/Add.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_add_ -vvv --optimize
```



![x = x + y 与 x += y图示](/images/gas-optimization-master/compiler/15-compound-assignment-01.png)



## 总结

- 检查您的合同以确定复合算术作业的出现，例如`+=`或`-=`。

- 用它们的直接分配等价物替换它们，如有必要，调整任何相关逻辑。

- 彻底测试修改后的合同，以确保没有引入任何意外行为。

## 对应源码

- [`src/compiler/Add.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Add.sol)
- [`test/compiler/Add.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Add.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
