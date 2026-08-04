# 使用克隆合约

## 分析

我们经常需要创建多个子合约，有三种常见的方法可以做到这一点：

- 使用`new`关键字通过现有合约创建，允许直接通过现有合约的代码库实例化子合约。此方法需要将子合约的字节码合并到创建合约本身中，因此需要同时部署子合约。这种方法简单直观，但需要谨慎管理，以避免原合约臃肿，尤其是在以太坊网络合约大小受限的情况下。

- 使用`create2`创建代码创建，此方法需要在任何子合约之前将创建代码加载到创建合约中。create2 的一个显著优势是其合约地址生成的可预测性，可以在实际合约部署之前预先确定，从而方便实现更复杂的部署方案和交互。

- 克隆技术用于`clone`克隆现有合约，利用 EIP1167 中规定的最小代理概念来复制已部署的合约。通过克隆现有合约，开发者可以显著降低部署大量合约实例所需的 Gas 成本。此方法需要预先部署子合约的副本，克隆合约将基于此副本创建，这些合约拥有各自的状态，但共享相同的代码库。

[EIP\-1167：最小代理标准](https://www.rareskills.io/post/eip-1167-minimal-proxy-standard-with-initialization-clone-pattern)

[EIP\-3448 Metaproxy 克隆](https://www.rareskills.io/post/erc-3448-metaproxy-clone)

## 测试

**文件位置：**

```Bash
src/contract/Clone.sol
test/contract/Clone.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_clone_ -vvv --optimize
```

![使用克隆合约图示](/images/gas-optimization-master/contract/07-clones-01.png)



## 总结

部署多个类似的智能合约时，Gas 成本可能会很高。为了降低这些成本，您可以使用最小克隆或元代理，它们将实现合约的地址存储在字节码中，并作为代理与其交互。然而，克隆的运行时成本和部署成本之间存在权衡。由于使用委托调用，克隆的交互成本比普通合约更高，因此仅在不需要频繁交互时使用它们。

## 对应源码

- [`src/contract/Clone.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Clone.sol)
- [`test/contract/Clone.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Clone.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
