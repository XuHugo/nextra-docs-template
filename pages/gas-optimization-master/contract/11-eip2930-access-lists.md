# 使用 EIP2930 预热存储槽

## 分析

**ERC\-2930** （EIP\-2930）是一种以太坊交易类型，允许你在发起交易时声明会访问哪些合约地址和存储槽。这被称为“访问列表交易”。这样做的主要好处是预先支付并锁定部分 Gas 费用，使访问这些“预热”过的地址和槽的成本更低。

- **EVM 设计**：首次访问新合约地址或存储槽，EVM 需加载其状态，消耗高额 gas。后续访问则视为“热”，gas 低。

- **Access List**：通过访问列表声明，将这些地址和槽标记为“热”，避免冷启动高额费用。

- **优化点**：如果你知道交易会涉及哪些外部地址/槽，提前在 access list 里声明，整体 gas 显著降低。

- 

**使用场景：**

- **跨合约调用**：如 A 调用 B（或 delegatecall 代理合约），涉及新合约地址的首次访问，默认是冷启动，gas 高。

- **克隆/代理合约**：经常用 delegatecall，需要频繁跨合约访问。

- **批量存储操作**：一次性访问多个新槽。



## 测试

**文件位置：**

```Bash
src/contract/AccessList.sol
test/contract/AccessList.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_accesslist_proxy_good(no) -vvv --optimize
```



![使用 EIP2930 预热存储槽图示](/images/gas-optimization-master/contract/11-eip2930-access-lists-01.png)



## 总结

- **EIP\-2930 访问列表**能有效降低跨合约调用和首次状态访问的 gas 开销，适合所有涉及代理、克隆、批量存储的业务场景。

- **操作很简单**：只需在发起交易时声明 accessList，无需更改合约逻辑。

- **实际优化**：充分利用 ethers\.js、web3\.js 等工具，将易变地址和槽打包声明，享受 gas 折扣。

- **建议开发者**：养成分析交易访问模式，并据此合理设置访问列表的习惯。

-

## 对应源码

- [`src/contract/AccessList.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/AccessList.sol)
- [`test/contract/AccessList.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/AccessList.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
