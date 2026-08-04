# 选择 Gas 优化库

## 分析

虽然 OpenZeppelin 是一个广泛使用且备受推崇的智能合约库，但也有一些替代库可以提高 Gas 效率。Solmate和**Solady就是两个值得注意的例子。这些库都**经过测试，并因其对 Gas 优化的关注而受到开发者的推荐。

[OpenZeppelin](https://www.openzeppelin.com/contracts)是一个用于安全智能合约开发的库。它提供了 ERC20 和 ERC721 等标准的实现，您可以按原样部署或根据需要进行扩展，同时还提供 Solidity 组件，用于构建自定义合约和更复杂的去中心化系统。



[Solmate](https://github.com/transmissions11/solmate)是由 Rari Capital 创建的 Gas 优化智能合约库。它为以太坊开发中的常见用例提供高度优化的合约实现，注重极简主义和 Gas 效率。



[Solady](https://github.com/Vectorized/solady)是一个 Gas 优化的 Solidity 库，优先使用汇编语言进行核心操作。它专为需要极致 Gas 优化且愿意牺牲部分可读性来换取效率的项目而设计。

## 主要区别

- **OpenZeppelin**：全面、审核良好，但由于额外的安全检查，可能需要更高的 gas 成本。

- **Solmate**：专注于常见智能合约模式的高效 gas 实现。

- **Solady**：强调极端的气体优化，通常利用组装来实现核心功能。

## 测试

src/contract/Libs\.t\.sol

**文件位置：**

```Bash
src/contract/Libs.sol
test/contract/Libs.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_libs_ -vvv --optimize
```

![选择 Gas 优化库图示](/images/gas-optimization-master/contract/09-gas-optimized-libraries-01.png)

Solady 在所有操作中始终消耗最少的 gas，与 OpenZeppelin 相比，Solmate 节省了大量的 gas，但不如 Solady 那么多，部署成本显示出最显著的差异，Solady 的部署成本比 OpenZeppelin 便宜约 66%。

注意：这些 gas 估算值是近似值，可能会根据特定的 Solidity 编译器版本、优化设置和确切的实施细节而有所不同。

## 总结

对于大容量或对gas敏感的应用，请考虑使用 Solmate 或 Solady 代替 OpenZeppelin。虽然这些替代方案可以节省 Gas，但请确保您了解并考虑到它们可能遗漏的任何安全检查。

## 对应源码

- [`src/contract/Libs.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Libs.sol)
- [`test/contract/Libs.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Libs.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
