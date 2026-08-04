# 使用 Calldata 替换 Memory

## 分析

对于外部函数中的只读数据，`calldata`事实证明，这是一种更高效的选择，因为它避免了`memory`不必要的数据复制，并且 Gas 成本更低。

- **内存成本**`memory`：由于数据复制和内存空间分配，使用函数参数会产生额外的 gas 成本。

- **Calldata 效率**：`calldata`是一个保存函数参数的不可变数据区域。它更节省 gas，因为它不涉及数据复制，并且利用了函数参数已存储的不可修改、非持久化空间。

## 测试

**文件位置：**

```Bash
src/storage/Calldata.sol
test/storage/Calldata.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_calldata_ -vvv --optimize
```

![使用 Calldata 替换 Memory图示](/images/gas-optimization-master/storage/11-calldata-over-memory-01.png)



## 总结

- **识别内存参数**：通过智能合约来识别使用`memory`的只读参数的外部函数。

- **替换为 Calldata**：将这些参数的数据位置从 切换`memory`为`calldata`以节省 gas。

- **测试**：严格测试，确保数据位置的切换不会影响合约的预期功能，同时节省交易的 gas。

## 对应源码

- [`src/storage/Calldata.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Calldata.sol)
- [`test/storage/Calldata.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Calldata.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
