# 使用 UUPS 降低代理部署成本

## 分析

**透明代理（Transparent Proxy）**

- 在透明代理模式中，代理合约每次接收调用（包括普通用户调用 logic 函数）时，都会执行一条逻辑：检查 `msg.sender == admin`？

- 该检查涉及一次 **SLOAD（加载存储 slot）** 操作，用于读取 admin 地址，并与调用者进行比较。这条分支判断每次调用都要执行。

- 虽然仅一条分支比较，但每次调用都会导致额外的写费与执行分支路径，累积下来会浪费不少 Gas。

**UUPS 模式**

- UUPS 模式下，代理合约仅做最低限度的 `delegatecall` 转发功能，没有判断 `msg.sender` 是否是 admin，也没有判断是不是管理操作。

- 所有的升级逻辑（如 `upgradeTo`）被内置到逻辑合约中。在升级调用时，逻辑合约才执行 `msg.sender == owner` 等权限检查。

- 因此，大多数用户的普通交互调用无需额外的 admin 检查，从而省下一次 SLOAD 和条件判断，节省 Gas。

## 测试



**文件位置：**

```Bash
src/patterns/UUPS.sol
test/patterns/UUPS.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_uups_ -vvv --optimize
```



![使用 UUPS 降低代理部署成本图示](/images/gas-optimization-master/patterns/03-uups-01.png)



## 总结

- 若你的项目主要为用户提供频繁的功能调用（例如 ERC20 转账、Mint、查询等日常操作），使用 **UUPS 模式**会使大多数交易更轻量、更低 Gas 成本。

- 透明可升级代理虽然安全性更好（权限分离明确），但是在调用 Gas 上存在持续开销，尤其当用户并非 admin 时仍被触发。

- 安全上，UUPS 升级逻辑在逻辑合约中，开发者需注意实现好 `_authorizeUpgrade` 等访问控制机制。

## 对应源码

- [`src/patterns/UUPS.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/patterns/UUPS.sol)
- [`test/patterns/UUPS.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/patterns/UUPS.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
