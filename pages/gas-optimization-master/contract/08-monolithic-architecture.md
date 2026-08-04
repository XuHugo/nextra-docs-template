# 使用单体架构

## 分析

在 Solidity 中，默认的做法可能是将代码模块化，分解成多个相互交互的合约。虽然这有利于维护和解耦，但由于合约调用的开销，可能会导致 Gas 成本增加。通过设计单体架构，将大部分逻辑集中在一个合约中，可以降低 Gas 成本。

合约调用非常昂贵，节省 Gas 的最佳方法是完全不使用它们。这其中自然存在权衡，但多个合约相互通信有时会增加 Gas 和复杂性，而不是管理 Gas。



**单体架构的优势**

- **降低 Gas 成本**：消除合约调用的开销，从而节省大量 Gas。

- **简化的 Gas 管理**：当所有逻辑都位于单个合同中时，更容易估算和管理 Gas 消耗。

**权衡**

- **复杂性增加**：合同可能会变得更加复杂和更难维护。

- **模块化降低**：在其他合同或项目中重用组件更加困难。



## 测试

**文件位置：**

```Bash
src/contract/Monolithic.sol
test/contract/Monolithic.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_monolithic_ -vvv --optimize
```



![使用单体架构图示](/images/gas-optimization-master/contract/08-monolithic-architecture-01.png)



## 总结

将逻辑整合到更少的合约中，以减少合约间调用开销。尽可能在单个合约中实现大部分功能。但您需要仔细评估可维护性和 Gas 成本之间的权衡。

## 对应源码

- [`src/contract/Monolithic.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Monolithic.sol)
- [`test/contract/Monolithic.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Monolithic.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
