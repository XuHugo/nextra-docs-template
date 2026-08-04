# 使用现有的 create2 工厂

## 分析

建议在需要 deterministic address（确定性地址）时，不要自己部署一个 CREATE2 工厂合约，而是复用社区已有的、已部署好的 CREATE2 工厂合约。

**为什么“使用现有的 CREATE2 工厂”更好：**

- **部署成本更低**
你无需部署工厂合约本身，只需调用现有工厂即可使用 CREATE2 创建子合约，节省了部署该工厂的 gas 与维护成本，这对于多次部署相同用户或团队非常划算。

- **地址统一且可信**
如果你自建了工厂，不同网络工厂地址可能不同，导致跨链支持不一致。而知名的“Deterministic Deployment Proxy”或 OpenZeppelin 等社区标准工厂，在多个网络上部署到了相同地址，使用它保证部署的子合约地址在各链保持一致 。

- **更低的前置风险**
若你公开了自建工厂地址和代码，其他人可能使用相同 salt 和 bytecode 提前部署架子合约（front\-run），占用目标地址。使用社区标准工厂，项目对部署者和盐值控制更成熟，风险更小。

## 测试

**文件位置：**

```Bash
script/Create2.s.sol
```

现在我们利用anvil启动一个本地节点，然后使用create2工厂，创建一个以0xabc开头的合约；create2工厂使用0x4e59b44847b379578588920ca78fbf26c0b4956c，这是一个主网上存在的create2工厂；anvil本身就集成了，所以我们不需要自行部署了。

- **启动本地节点**

```Bash
anvil
```

- **查找合适的 Salt**

使用 `cast create2` 命令查找能生成以 "abc" 开头地址的 salt，可以执行脚本`./geerate_salt.sh`，内容大致如下：

```Bash
# 获取合约字节码
BYTECODE=$(forge inspect src/contract/SimpleContract.sol:SimpleContract bytecode)

# 添加构造函数参数
CONSTRUCTOR_ARGS=$(cast abi-encode "constructor(string)" "Hello from CREATE2!")
INIT_CODE="${BYTECODE}${CONSTRUCTOR_ARGS:2}"

# 查找以 abc 开头的地址
cast create2 --starts-with abc --deployer 0x4e59b44847b379578588920cA78FbF26c0B4956C --init-code $INIT_CODE
```

**示例输出**:

```Plain Text
Address: 0xaBc6b437f83764AB543AECAa7cf440a01a184cA4
Salt: 0x0931f671a3b3ed03a02a11e2cfe2cf64ba9842fd881fee6d892e8e0e75a8959a
```

- **运行部署脚本（脚本中也包括了测试）**

```Bash
forge script script/Create2.s.sol:Create2FScript \
  --rpc-url http://localhost:8545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
  --broadcast
```

- **验证部署结果（其实不需要了，可以当作练习）**

    - **检查合约代码**

    ```Bash
    cast code 0xaBc6b437f83764AB543AECAa7cf440a01a184cA4 --rpc-url http://localhost:8545
    ```

    - **调用合约函数**

    ```Bash
    # 调用 getMessage 函数
    cast call 0xaBc6b437f83764AB543AECAa7cf440a01a184cA4 "getMessage()" --rpc-url http://localhost:8545
    
    # 解码返回值
    cast --to-ascii <返回的十六进制值>
    ```

    

## 总结

- 优先使用社区标准工厂（如 Deterministic Deployment Proxy、OpenZeppelin CLI 带的 CREATE2 部署工具），不要为了每个项目单独部署 CREATE2 工厂。

- **一致使用相同 salt 和 bytecode**，确保跨链部署地址一致。

- 在生产使用中，避免子合约能够 self‑destruct 后存在重复部署风险；或者对代码 hash 做校验验证，确认合约逻辑安全。

- 如果你确实有特殊需求（如工厂参数化、权限控制），可以自己部署，并在开发文档中提醒调用方注意跨链一致性的使用方式。

## 对应源码

- [`script/Create2.s.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/script/Create2.s.sol)
- [`src/contract/SimpleContract.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/SimpleContract.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
