# 预编译合约

## 分析

1. **什么是预编译合约？**

    预编译合约是一组位于固定地址的特殊合约。它们的功能不是由 EVM 字节码实现的，而是直接用客户端（如 Geth、Nethermind）的本地代码（如Go、Rust）编写。这使得它们在执行特定任务时，远比在 EVM 中运行等效代码要快得多，也便宜得多。你可以将它们视为以太坊协议内置的、高效的“原生函数库”。

- 常见示例：

    - ecrecover \(地址 0x1\)：用于从签名中恢复公钥，是验证数字签名的核心。

    - sha256 \(地址 0x2\)：计算 SHA2\-256 哈希。

    - modexp \(地址 0x5\)：处理大数模幂运算，是某些密码学应用的基础。

        你可以在 EVM Codes \(https://www\.evm\.codes/precompiles\) 网站上查看完整的预编译合约列表。

2. **为何使用预编译合约能节省 Gas？**

核心原因在于绕过 EVM。 EVM 是一个通用的计算环境，执行每一条指令都需要付费。对于密码学哈希、大数运算这类计算密集型任务，用 Solidity 在 EVM 中实现会非常昂贵。

预编译合约将这些繁重的计算任务从 EVM转移到运行节点的本地机器上执行，其效率提升了几个数量级。因此，以太坊协议可以为这些操作设定一个远低于等效 EVM 计算的固定 Gas 价格。

简而言之：用更少的 Gas，完成更复杂的计算。

## 测试

**文件位置：**

```Bash
src/compiler/Precompiles.sol
test/compiler/Precompiles.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_precompile_ -vvv --optimize
```

## 总结

- 何时使用： 当你的合约需要执行计算密集型操作（特别是加密、哈希或大数运算）时，优先考虑使用预编译合约。

- 核心优势： 大幅降低特定操作的 Gas 成本，提升合约效率。

- 核心权衡： 使用预编译合约是在 “Gas 效率” 和 “跨链可移植性” 之间做出的选择。

- 最终建议： 如果你的应用主要针对以太坊主网，并且 Gas 节省效果显著，那么预编译合约是一个极佳的优化工具。但如果你的目标是多链部署，请谨慎使用，并仔细验证目标链是否支持你所依赖的预编译合约。

## 对应源码

- [`src/compiler/Precompiles.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Precompiles.sol)
- [`test/compiler/Precompiles.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Precompiles.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
