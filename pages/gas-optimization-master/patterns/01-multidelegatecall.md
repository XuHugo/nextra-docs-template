# 使用 Multidelegatecall 批量处理交易

## 分析

通常合约中需要多次调用本合约逻辑函数时，会消耗多次交易打包费和基础 Gas 开销。使用 `multi-delegatecall`，可以在一笔交易中依次调用多个函数，只消耗一次交易基础费与 calldata 成本，显著降低整体 Gas 支出。与 Multicall（使用 `.call()`）不同，delegatecall 保留上下文（如 `msg.sender`、`msg.value`、storage 指针），允许内部调用更灵活复杂。



- **批量调用优势**：通过单笔交易执行多个函数调用，仅需支付一次基础费用 \(base fee\)，显著节省 Gas。

- **保留上下文**：`Multicall` 使用 `delegatecall` 调用合约自身的函数，保留 `msg.sender`、`msg.value` 和 storage 上下文。

- **减少 calldata 重复**：编码多个函数调用合并为更紧凑的 calldata，减少重复开销。



## 测试



**文件位置：**

```Bash
src/patterns/Multicalls.sol
test/patterns/Multicalls.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_multicalls_ -vvv --optimize
```



![使用 Multidelegatecall 批量处理交易图示](/images/gas-optimization-master/patterns/01-multidelegatecall-01.png)



![使用 Multidelegatecall 批量处理交易图示 2](/images/gas-optimization-master/patterns/01-multidelegatecall-02.png)



## 总结

- **适用场景**：多个合约函数需顺序执行（如设置状态、转账、授权等）；

- **Gas 优势**：一笔交易替代多笔，节省 base fee、calldata、重入 gas；

- **安全控制**：设计时要考虑 delegatecall 的上下文影响，确保不会泄露或污染状态；

- **使用方式**：按需继承 `Multicall` abstract 合约；运行时传入调用数据数组；

- **兼容性**：可配合 UUPS 或治理合约使用，弥补高频函数调用场景效率不足。

## 对应源码

- [`src/patterns/Multicalls.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/patterns/Multicalls.sol)
- [`test/patterns/Multicalls.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/patterns/Multicalls.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
