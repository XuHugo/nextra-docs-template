# 仅使用一次的内部函数可以内联

## 分析

内部函数是可以的，但是它们会在字节码中引入额外的跳转标签。因此，如果只有一个函数使用它，最好将内部函数的逻辑内联到正在使用的函数中。这样可以避免在函数执行期间跳转，从而节省一些 gas。

1. **函数调用开销**：每个函数调用，即使是`internal`一次调用，都会在 EVM 中带来一些开销。

2. **内联**：这是一种编译器优化技术，其中函数的代码在原地扩展而不是被调用，从而节省与函数调用相关的开销。

*问题*`internal`：合约中有一个函数只调用一次。*解决方案*：与其将其保留为单独的函数，不如将其逻辑直接放置（或“内联”）在调用的位置。

## 测试

**文件位置：**

```Bash
src/contract/Payable.sol
test/contract/Payable.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_payable_ -vvv --optimize
```

## 总结

1. **可重用性**：如果该函数有可能`internal`在未来版本中或从其继承的其他合约中被更多地使用，请考虑保留它。

2. **可读性**：有时，即使某个`internal`函数只调用一次，也能提高合约的可读性。在这种情况下，请考虑在 Gas 效率和清晰度之间进行权衡。

## 对应源码

- [`src/contract/Payable.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Payable.sol)
- [`test/contract/Payable.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Payable.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
