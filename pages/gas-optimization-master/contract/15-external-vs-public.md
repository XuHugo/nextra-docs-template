# external 与 public

## 分析

Solidity 提供了各种函数可见性说明符，包括`public`和`external`。虽然两者都可以从合约外部访问，但在某些情况下从`external` 切换到`public`可以节省 Gas，并提高智能合约的效率。

**`public`**** 函数**

可以在合约内部、继承的合约中以及合约外部调用。



**`external`**** 函数**

只能从合约外部调用（包括其他合约或外部账户），不能在合约内部直接调用。如果需要在合约内部调用 `external` 函数，必须使用 `this.functionName()` 语法，这将是一个新的外部消息调用，会消耗更多 Gas。



## 测试

**文件位置：**

```Bash
src/contract/External.sol
test/contract/External.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_external_com -vvv --optimize
```



![external 与 public图示](/images/gas-optimization-master/contract/15-external-vs-public-01.png)



## 总结

- **选择 ****`external`**** 的时机：**如果一个函数**只会被外部账户或外部合约调用**，并且**不需要**被当前合约内部的其他函数直接调用，那么应该优先使用 `external`。

- **选择 ****`public`**** 的时机：**如果一个函数**需要在合约内部被其他函数直接调用**，那么它必须是 `public`（或 `internal`）。

## 对应源码

- [`src/contract/External.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/External.sol)
- [`test/contract/External.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/External.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
