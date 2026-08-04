# 待验证：冗余操作

## 分析

- **冗余初始化成本**：将变量初始化为其默认值，例如将`bool`变量设置为`false`或`uint256`将变量设置为`0`，会引入不必要的操作，从而消耗额外的 gas。

- **默认值**：在 Solidity 中，未初始化的`bool`变量默认为`false`，`uint256`变量默认为`0`。了解这些默认值可以使代码更简洁、更省油。

- **其他冗余操作**：重复的赋值、未使用的函数等；

## 测试

**文件位置：**

```Bash
src/storage/InitDefault.sol
test/storage/InitDefault.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_init_ -vvv --optimize
```



![待验证：冗余操作图示](/images/gas-optimization-master/storage/12-remove-redundant-operations-01.png)

**结果显而易见，编译器已经足够优秀了。**

## 总结

1. **识别冗余初始化**：扫描智能合约，查找初始化为默认值的变量。

2. **删除冗余初始化**：当您打算将变量设置为默认值时，请省略变量的显式初始化。

3. **测试**：进行严格的测试，以确保删除显式初始化不会影响合约的预期行为，同时有助于节省少量 gas。

## 对应源码

- [`src/storage/InitDefault.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/InitDefault.sol)
- [`test/storage/InitDefault.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/InitDefault.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
