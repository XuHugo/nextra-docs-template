# 退款

## 分析

当不再需要某个存储槽时，将其值设置为零（本质上是将变量“清零”）可以返还 Gas。务必策略性地确定合约中哪些存储变量可以安全地清零。在不再需要该变量时立即执行此操作，不仅可以清理合约状态，还可以恢复存储值所消耗的部分 Gas。

单笔交易的 Gas 退款上限为已用 Gas 的 **20%**。这意味着你不可能通过清除存储来获得超过你实际消耗 Gas 量 20% 的退款。

- **目的：** 主要为了减少以太坊的状态大小，降低链上存储成本。

- **实践：** 当你的合约中的数据结构（如映射）中的某个条目不再需要时，如果它是一个非零值，将其显式地设置为零 \(`delete myMapping[key];` 或 `myVariable = 0;`\) 仍然会为你带来一小笔 Gas 退款。虽然这笔退款不足以覆盖写入零的成本，但它会比不清除获得更低的净成本。

- **适用场景：** 用户注销、数据过期、一次性使用的数据等。

## 测试

**文件位置：**

```Bash
src/storage/GasRefund.sol
test/storage/GasRefund.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_refund_ -vvv --optimize
```

## 总结

当链上状态数据不再需要时，显式地将其设置为零，可以获得少量的 Gas 节约，并有助于以太坊网络的整体健康。为了优化长期成本和网络效率。

## 对应源码

- [`src/storage/GasRefund.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/GasRefund.sol)
- [`test/storage/GasRefund.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/GasRefund.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
