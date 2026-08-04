# 转账时使用 fallback 或 receive

## 分析

在 Solidity 智能合约中，任何状态更改或交互都需要消耗 gas。通常，用户通过调用合约的 `payable` 函数（如 `deposit()`）进行 Ether 存款操作。然而，如果你的合约允许直接转账 Ether（即不调用任何特定函数，仅向合约地址发送 ETH），你可以利用 Solidity 的 `receive()` 和 `fallback()` 特性，进一步节省 gas 并提升用户体验。



**receive\(\) 和 fallback\(\) 区别**

- `receive()`：当合约被“直接”发送 ETH（无 calldata）时自动调用。gas 开销极低，代码短小精悍。

- `fallback()`：当调用合约且未找到匹配函数签名时自动调用，可携带 calldata。适合逻辑分发和参数解析。



1. **用户通常通过如下函数存款：**

```Solidity
function deposit() external payable {
    // ...如将 ETH 存入 AAVE 或转换为 WETH
}
```

- 需要 ABI 编码、函数选择器、参数解析等步骤，gas 较高。

    

2. **使用 receive\(\) 简化存款**

允许用户直接向合约地址转账 ETH，合约在 `receive()` 中自动处理逻辑：

- 省略了 ABI 编码、函数查找等步骤，gas 更低。

- 用户体验更好：直接转账即可，无需调用特定函数。

    

3. **使用 fallback\(\) 解析自定义参数**

如果需要携带细粒度参数，可以让用户通过 fallback 传递 ABI 编码的数据，例如 `abi.encode(user, refCode)`，合约解析后完成复杂操作。这样无需多余显式方法，节省接口和管理成本。



## 测试

**文件位置：**

```Bash
src/contract/Deposit.sol
test/contract/Deposit.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_deposit_ -vvv --optimize
```



![转账时使用 fallback 或 receive图示](/images/gas-optimization-master/contract/10-fallback-and-receive-01.png)



汇编

![转账时使用 fallback 或 receive图示 2](/images/gas-optimization-master/contract/10-fallback-and-receive-02.png)



- `receive()` 是专门为“只收 ETH”设计的入口，最简洁，理论上 gas 最低。

- `fallback()` 是“兜底”入口，EVM 需把 calldata 传进来（即使为空）。Solidity 编译器会为 fallback 加上一些必要的 ABI 解包逻辑，即使你没用到 `msg.data`。

- 普通 `payable` 函数（如 `deposit()`）有函数选择器和参数解码（但如果没有参数，解码非常简单）。



## 总结

- **节省 gas**：使用 `receive()` 让用户直接转账 ETH，省去编码/查找等步骤，显著降低 gas。

- **灵活参数支持**：通过 `fallback()` 支持携带复杂参数，提升合约灵活性，无需大量接口。

- **提升体验**：用户操作更自然、界面更简洁，尤其适合 DeFi、NFT、钱包等场景。

- **安全性注意**：需防止 fallback 被恶意利用，参数解析需严格校验，合理分配权限。

- **在设计常用的接收 ETH 场景时，优先考虑 receive/fallback 的 gas 优化与用户体验提升方案，结合实际业务逻辑灵活使用。**

## 对应源码

- [`src/contract/Deposit.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Deposit.sol)
- [`test/contract/Deposit.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Deposit.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
