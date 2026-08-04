# 适当使用unchecked

## 分析

Solidity 0\.8 及更高版本引入了自动检查算术溢出和下溢的功能。虽然这些检查可以防止意外行为，从而增强安全性，但每次操作也会消耗额外的 Gas。如果由于合约逻辑导致溢出或下溢无法实现，这些自动检查就变成了不必要的 Gas 消耗。Solidity`unchecked`中的指令允许开发者绕过这些检查，从而节省 Gas。

## 测试

**文件位置：**

```Bash
src/compiler/UnChecked.sol
test/compiler/UnChecked.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_unchecked_ -vvv --optimize
```



![适当使用unchecked图示](/images/gas-optimization-master/compiler/06-unchecked-01.png)



## 总结

1. **识别安全操作**：识别不会发生溢出/下溢的算术运算。

2. **实施****`unchecked`**：用块包围这些安全操作`unchecked`。

3. **彻底测试**：进行严格的测试，以确保所识别的操作真正不会出现溢出和下溢。

## 对应源码

- [`src/compiler/UnChecked.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/UnChecked.sol)
- [`test/compiler/UnChecked.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/UnChecked.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
