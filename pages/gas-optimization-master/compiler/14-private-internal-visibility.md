# 合理使用 private 和 internal

## 分析

在 Solidity 中，`public`变量具有自动生成的 getter 函数，虽然很有用，但在合约部署期间会产生额外的 Gas 成本\(公共函数会增加跳转表的大小\)。如果常量不需要在合约或派生合约之外访问，则更改其可见性可以节省 Gas。请记住，私有变量并非私有的，使用web3\.js提取变量值并不困难。对于那些旨在供人类而非智能合约读取的常量来说尤其如此。

部署包含大量常量的合约`public`可能会因为新增的 getter 函数而增加不必要的部署 Gas 成本。此外，每次访问这些常量时都会消耗额外的 Gas。

## 测试



**文件位置：**

```Bash
src/compiler/Visibility.sol
test/compiler/Visibility.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_visibility_ -vvv --optimize
```



![合理使用 private 和 internal图示](/images/gas-optimization-master/compiler/14-private-internal-visibility-01.png)





## 总结

1. **审查常量**：检查合同中的`public`常量。

2. **调整可见性**：如果一个常量不需要在合约外部或派生合约中访问，可以考虑将其可见性更改为`internal`。如果它也不需要被派生合约访问，可以考虑将其设置为`private`。

3. **测试合同**：确保您的合同在进行可见性调整后仍能按预期运行。

## 对应源码

- [`src/compiler/Visibility.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Visibility.sol)
- [`test/compiler/Visibility.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Visibility.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
