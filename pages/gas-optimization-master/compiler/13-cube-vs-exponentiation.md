# n * n * n替换n 3

## 分析

机制原理：MUL vs EXP Opcodes

1. 乘法 \(`*`\): 当你写 n \* n 时，Solidity 编译器会将其转换为 EVM 的 MUL 操作码。MUL是一个非常基础和廉价的操作，它的 Gas 消耗是固定的，非常低（5 Gas）。因此，n\*n\*n 会被编译成两次 MUL操作，总成本大约是 10 Gas。

2. 指数 \(`**`\): 当你写 n3 时，编译器会使用 `EXP` 操作码。`EXP`设计用于处理任意的指数运算（a\*\*b），因此它的实现要复杂得多，Gas 成本也高昂得多。`EXP` 的 Gas 成本是动态的，由一个基础费用和一个与指数大小相关的附加费用组成。对于像 n\*\*3 这样的小指数，其 Gas 成本大约是60 Gas（10 Gas 基础费 \+ 50 Gas 附加费）。

## 测试

**文件位置：**

```Bash
src/compiler/Exponentiation.sol
test/compiler/Exponentiation.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_expo_ -vvv --optimize
```

![n * n * n替换n 3图示](/images/gas-optimization-master/compiler/13-cube-vs-exponentiation-01.png)

## 总结

优先使用乘法: 当你需要计算一个数的平方、立方等固定的、小的幂时，总是直接写乘法（n\*n, n\*n\*n），而不是使用 \*\*运算符。

## 对应源码

- [`src/compiler/Exponentiation.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Exponentiation.sol)
- [`test/compiler/Exponentiation.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Exponentiation.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
