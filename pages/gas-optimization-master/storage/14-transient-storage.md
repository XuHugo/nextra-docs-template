# 使用瞬态存储

## 分析

**瞬态**存储是除内存、存储、调用数据（以及返回数据和代码）之外的另一个数据位置，它与其各自的操作码一起由 EIP\-1153 引入 `TSTORE`。[这个](https://eips.ethereum.org/EIPS/eip-1153)`TLOAD`新的数据位置的行为类似于存储的键值存储，主要区别在于**瞬态**存储中的数据不是永久的，而是仅限于当前交易，超过当前交易范围后将被重置为零。由于**瞬态**存储内容的生命周期和大小非常有限，因此它不需要作为状态的一部分永久存储，并且相关的 gas 成本远低于存储。要使用瞬态存储，需要 EVM 1\.1 或更高版本。



- **可组合性风险（Composability）**：由于 transient 数据跨函数调用共享，但在交易结束时统一清除，可能导致复杂组成调用中状态不一致的 bug [Solidity Programming Language\+1cyfrin\.io\+1](https://soliditylang.org/blog/2024/01/26/transient-storage/?utm_source=chatgpt.com)。

- **未手动清除可能阻塞后续调用**：如果不正确重置锁变量，某些函数只能在交易内被调用一次，导致不可重入或 DOS 风险。

- **尚无高阶语言全面支持**：早期只能在 assembly 操作，直到 Solidity 0\.8\.27/0\.8\.28 才开始支持 `transient` 关键字，但目前语法仅限 value types，引用类型（struct/array/mapping）尚不支持



## 测试

**文件位置：**

```Bash
src/storage/transient.sol
test/storage/transient.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_transient_ -vvv --optimize
```



![使用瞬态存储图示](/images/gas-optimization-master/storage/14-transient-storage-01.png)



## 总结

总之，**transient storage 正在逐步成为 Solidity 开发中提高效率、降低 gas 的重要利器**，尤其在安全模式（如重入锁）、回调或复杂跨调用逻辑、以及 DeFi 协议部署优化等场景中非常实用。随着 Solidity 高层语法的完善和更多实践案例落地，它的应用将日益广泛。

## 对应源码

- [`src/storage/transient.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/transient.sol)
- [`test/storage/transient.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/transient.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
