# 查找表

## 分析

在 EVM 中，CPU 计算（尤其是在循环或复杂数学运算中）的成本极高，而读取存储（SLOAD）的成本相对固定且较低。查找表（Lookup Table）正是利用这一成本差异的经典优化策略，其核心思想是 “用存储换计算”。如果您需要计算底数或幂为分数的对数或幂，则最好预先计算一个表格（如果底数或幂是固定的）。以[Bancor 公式](https://github.com/AragonBlack/fundraising/blob/master/apps/bancor-formula/contracts/BancorFormula.sol#L293)和[Uniswap V3 Tick Math](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol#L23)为例。

1. **工作原理**

- 预计算 \(Pre\-computation\): 在合约部署时或通过一个专门的初始化函数，提前计算出一系列可能用到的结果。

- 存储 \(Storage\): 将这些预计算的结果存入一个状态变量中，通常是数组或映射（mapping）。为了进一步优化，如果数据是固定的，可以将其声明为immutable，这样在部署时直接写入合约字节码，运行时读取成本更低。

- 查找 \(Lookup\): 在合约运行时，当需要某个值时，不再进行实时计算，而是直接从存储中读取预先计算好的结果。这通常只涉及一次廉价的 SLOAD操作。

2. **经典案例：Uniswap V3 的 TickMath**

这是一个完美的实战案例。Uniswap V3 需要根据 tick（价格区间的离散单位）来计算 sqrt\(P\)，即sqrt\(1\.0001^tick\)。

- 问题： 在运行时实时计算幂函数（尤其是带小数的底数）会消耗大量 Gas。

- 解决方案： Uniswap V3 的 TickMath\.sol 库预先计算了一系列 tick 对应的 sqrt\(P\) 值，并将它们存储在一个公共的、不可变的查找表中。

- 效果： 当需要某个 tick 对应的价格时，合约只需从表中读取该值，将昂贵的幂运算替换为一次廉价的 SLOAD，极大地节省了 Gas。

## 测试

**文件位置：**

```Bash
src/compiler/LookupTableMath.sol
test/compiler/LookupTableMath.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_table_ -vvv --optimize
```

## 总结

请记住，向状态变量写入数据（SSTORE）是 EVM 中最昂贵的操作之一。因此，查找表策略的初始部署成本较高。只有当 节省的计算 Gas 总和能够超过这个初始存储成本时，这种优化才有意义。

- 核心原则： 用一次性的高存储成本（SSTORE）换取未来无数次的低计算成本（SLOAD）。

- 最大优势： 将昂贵的、重复的数学运算转变为廉价的存储读取。

- 主要成本： 部署合约时写入查找表所需的高昂 Gas。

- 最佳实践： 最适合用于 高频调用的、具有有限输入范围的复杂计算，是 DeFi 核心协议的必备优化技巧。

## 对应源码

- [`src/compiler/LookupTableMath.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/LookupTableMath.sol)
- [`test/compiler/LookupTableMath.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/LookupTableMath.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
