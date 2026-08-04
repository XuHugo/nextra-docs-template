# 使用 ECDSA 签名实现白名单和空投

## 分析

在区块链项目中，常见的白名单（whitelist）和空投（airdrop）场景一般采用 Merkle 树结构来存储用户地址和分发凭证。这种方式通过在链上存储 Merkle 根节点、在链下生成 Merkle 证明来实现批量验证和节省 gas。但是，随着 EIP\-712 等签名标准的普及，也可以用 ECDSA（椭圆曲线数字签名算法）签名来代替 Merkle 树实现相似的功能。

**Merkle 树做白名单与空投**

- **原理**：将所有用户地址（及其分配额度等信息）构建为一棵 Merkle 树，链上只存储 Merkle 根节点。

- **流程**：

    1. 项目方生成 Merkle 树，并公开 Merkle 根。

    2. 用户领取空投时，提交自己的地址、分配额度、以及 Merkle 证明（proof）。

    3. 合约通过 proof 验证该用户确实在白名单里，允许领取。

- **优点**：链上存储少，批量验证高效。

- **缺点**：每个用户都需要生成和上传 proof，操作复杂，proof 数据量较大（影响 gas）。

    

**ECDSA 签名做白名单与空投**

- **原理**：项目方为每个白名单用户生成一份独立的签名（如 EIP\-712），链上通过公钥验证签名真伪。

- **流程**：

    1. 项目方用私钥对每个用户的地址（和分配信息）签名。

    2. 用户领取时上传自己的签名和相关信息。

    3. 合约通过公钥（或 recover）验证签名是否由项目方生成。

- **优点**：用户上传的数据更小，验证简单、gas 较低；不需要 proof。

- **缺点**：每个用户都要获取项目方签名，不能批量验证；如果私钥泄漏，所有签名失效。

## 测试

src/patterns/AirDrops\.sol

**文件位置：**

```Bash
src/patterns/AirDrops.sol
test/patterns/AirDrops.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_ad_ -vvv --optimize
```



![使用 ECDSA 签名实现白名单和空投图示](/images/gas-optimization-master/patterns/02-ecdsa-whitelist-airdrop-01.png)



- **Merkle 树方案**：验证 proof 需要多次哈希，proof 长度随白名单人数增长，gas 逐步上升。

- **ECDSA 签名方案**：只需一次 `ecrecover`，且上传数据量固定，gas 更低。

- **实际测试**：当人数超过512之后，也就树的高度达到10之后，基本就是ecdsa的方式gas消耗更低了。

## 总结

规模变大之后，ECDSA的gas消耗更少，但是ECDSA 需要为每个用户生成一个独立的签名文件，并确保分发到每个用户手中。对于 100,000 个用户，这是管理和分发上的噩梦。而 Merkle 树只需计算一个 Root，然后用户可以自己根据公共的白名单列表和开源工具生成 Proof。实际项目可结合两种方案，按需选择。

## 对应源码

- [`src/patterns/AirDrops.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/patterns/AirDrops.sol)
- [`test/patterns/AirDrops.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/patterns/AirDrops.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
