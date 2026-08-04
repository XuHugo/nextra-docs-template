# 待验证：selfbalance 与 address(this).balance

## 分析

address\(this\)\.balance有时可以使用 yul 中的函数更有效地完成 solidity 代码selfbalance\(\)?

理论上：

- selfbalance\(\) \(Yul/Assembly\): 直接调用 EVM 操作码，成本约 5 gas

- address\(this\)\.balance \(Solidity\): 需要额外的操作来获取地址，然后查询余额

但请注意，编译器有时足够智能，可以在后台使用这个技巧，因此请两种方式都进行测试。  

## 测试

**文件位置：**

```Bash
src/assembly/Balance.sol
test/assembly/Balance.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_balance_ -vvv --optimize
```

![待验证：selfbalance 与 address(this).balance图示](/images/gas-optimization-master/assembly/11-selfbalance-01.png)

编译器很智能：即使你写的是 address\(this\)\.balance，Solidity 编译器（0\.8\.30）足够智能，会自动优化为 selfbalance 操作码！

Gas 成本相同：方法1和方法2生成了几乎相同的汇编代码，都使用 selfbalance 操作码。

手动 assembly 的优势：只有在你需要更复杂的逻辑或者想要确保使用特定操作码时，手动 assembly 才有意义。

真正的差异：只有方法3（balance\(address\(\)\)）才会产生额外的 address 操作码调用。

## 总结

- 现代 Solidity：直接使用 address\(this\)\.balance，编译器会自动优化

- 明确控制：如果你想要明确控制或者处理更复杂的逻辑，使用 assembly selfbalance\(\)

- 避免：避免在 assembly 中使用 balance\(address\(\)\)，因为这确实会产生额外的 gas 成本sd

## 对应源码

- [`src/assembly/Balance.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/Balance.sol)
- [`test/assembly/Balance.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/Balance.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
