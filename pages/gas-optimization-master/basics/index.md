# 基础知识

理解 Gas 费用、EVM 数据区、Yul 与 Foundry 测试方法。

以太坊中的 Gas 是驱动智能合约执行和交易的“燃料”。它是衡量执行操作所需计算量的单位。以太坊网络上的每个操作，从简单的转账到复杂的合约交互，都需要 Gas。因此，Gas 是一种防止计算无限运行并破坏网络的机制。

Gas也是一种奖励高效开发的机制。两个智能合约可能实现相同的目标，但执行复杂度较低的合约将获得更低的 Gas 费用。这种经济模型激励开发者磨练 Solidity 技能，编写既实用又高效的代码。在这个区块链生态系统中，Gas 优化是成功的关键，它确保你的智能合约不仅高效，而且对开发者和用户都具有经济可行性。

## 文章目录

1. [Gas Fee 计算方法](./01-gas-fee)
2. [Gas 常量：EVM 操作成本](./02-opcode-gas-costs)
3. [Storage 与 Transient Storage](./03-storage-and-transient-storage)
4. [Memory](./04-evm-memory)
5. [Calldata](./05-calldata)
6. [Yul 介绍](./06-yul)
7. [Foundry 介绍](./07-foundry)
