# 使用 ERC20 Permit 合并授权与转账

## 分析

**ERC20Permit它允许用户在不支付 Gas** 的情况下，通过链下签名来授权另一个地址（通常是去中心化应用或服务，DApp）转移其 ERC\-20 代币。然后，被授权的 DApp 可以将这个授权（`permit` 交易）和实际的代币转账操作**合并到一笔链上交易中执行**，并且由 DApp 或接收方支付 Gas 费用。



**传统流程**：ERC\-20 Token 一般需要两笔交易：

- 用户调用 `approve(spender, amount)`：支付 gas，授权合约；

- 再调用 `transferFrom(owner, recipient, amount)`：再次支付 gas。

**ERC20Permit 优化**：支持 EIP‑2612 的 Token（如 DAI、UNI、COMP 等）允许用户离线签名一条 `permit(owner, spender, amount, deadline, v, r, s)`：

- `approve` 通过签名认证，无需用户支付 gas；

- 后续由执行者提交 `permit` 与 `transferFrom` 两步，**合并为单笔 on\-chain 调用** 。

## 测试

**文件位置：**

```Bash
src/patterns/Permit.sol
test/patterns/Permit.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_permit_ -vvv --optimize
```



```Solidity
// EIP-712 规范的完整消息哈希是 keccak256("\x19\x01" || domainSeparator || structHash)

    // 构造 permit 签名
    *bytes32* permitHash = keccak256(
        abi.encodePacked(
            "\x19\x01",
            permitToken.DOMAIN_SEPARATOR(),
            keccak256(abi.encode(
                keccak256("Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)"),
                owner,
                spender,
                value,
                nonce,
                deadline
            ))
        )
    );
    (*uint8* v, *bytes32* r, *bytes32* s) = vm.sign(ownerPk, permitHash);
```



一个标准的 ERC\-20 Permit 消息（通常基于 EIP\-2612）包含以下几个关键部分：

1. **`domain`****（域分隔符）：**

    - 这是一个识别消息来源和其适用范围的结构化数据。它确保一个签名不能在不同链、不同合约或不同版本中重放。

    - **必需字段：**

        - `name`: 代币合约的名称（例如："Uniswap V2" 或 "Dai Stablecoin"）。

        - `version`: Permit 规范的版本（通常是 "1"）。

        - `chainId`: 当前网络的链 ID（例如：Ethereum 主网是 1，Sepolia 是 11155111）。

        - `verifyingContract`: 代币合约的地址。

    - **可选字段：** `salt`（不常用）。

2. **`types`****（类型定义）：**

    - 定义了所有在签名过程中用到的自定义数据结构。

    - **必需包含：**

        - `EIP712Domain`: `domain` 结构的定义。

        - `Permit`: `permit` 消息本身的结构定义。

3. **`message`****（实际消息内容）：**

    - 这是用户真正要签名的数据，包含授权的具体信息。

    - **必需字段：**

        - `owner`: 授权人（代币持有者）的地址。

        - `spender`: 被授权人（将花费代币的地址，例如路由器合约）的地址。

        - `value`: 授权金额（`uint256` 类型）。

        - `nonce`: 一个防止重放攻击的随机数，通常是 `owner` 在代币合约中的 `nonces` 计数器的值。每次 `permit` 签名后，`nonces` 会增加。

        - `deadline`: 授权的截止时间（Unix 时间戳）。超过此时间，签名将失效。



## 总结

- **用户体验大幅提升：** 用户无需提前授权，只需一次签名操作即可完成整个流程。

- **Gas 成本优化：** 用户无需支付 Gas，由 DApp 或服务商承担。对于新用户或 Gas 费用敏感的用户来说，这大大降低了进入门槛。

- **流程简化：** 将两笔交易合并为一笔，减少了链上拥堵和用户的等待时间。

- **原子性：** 授权和转账在同一笔交易中完成，保证了操作的原子性。

## 对应源码

- [`src/patterns/Permit.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/patterns/Permit.sol)
- [`test/patterns/Permit.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/patterns/Permit.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
