# Solidity 0.8+ 不再需要 SafeMath

## 分析

`SafeMath`用于防止整数上溢和下溢的库。自 Solidity 0\.8 以来，这些检查已内置到编译器中，从而消除了`SafeMath`冗余，并可移除，以优化 Gas 性能。

- **SafeMath 开销**：以前，该`SafeMath`库对于安全地进行算术运算至关重要。然而，由于它执行的外部库调用和检查，它会产生额外的 Gas 成本。

- **编译器级检查**：从 Solidity 0\.8 开始，编译器包含对整数溢出和下溢的内置检查，从而无需对`SafeMath`涉及算术运算的每个交易进行检查，从而节省 gas。

## 测试

**文件位置：**

```Bash
src/contract/SafeMath.sol
test/contract/SafeMath.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_safemath_ -vvv --optimize
```

## 总结

从使用 Solidity 0\.8 及以上版本编译的智能合约中,移除该`SafeMath`库是一种简单有效的降低 Gas 消耗的优化方法。虽然每笔交易节省的 Gas 消耗看似不多，但考虑到长期处理的交易量，这笔节省的 Gas 消耗总量可能相当可观。请务必在优化后对合约进行全面测试，以验证其行为和实际节省的 Gas 消耗。

## 对应源码

- [`src/contract/SafeMath.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/SafeMath.sol)
- [`test/contract/SafeMath.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/SafeMath.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
