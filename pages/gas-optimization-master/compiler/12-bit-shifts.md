# 使用位移替换乘除运算

## 分析

在 Solidity 中，对 2 的幂数进行移位乘除运算通常比直接使用乘法或除法运算符更节省 Gas。例如，以下两个表达式是等价的

```Solidity
10 * 2
10 << 1 # shift 10 left by 1
```

这也等同于

```Solidity
8 / 4
8 >> 2 # shift 8 right by 2
```

在二进制算术中，将数字右移一位相当于将其除以 2。同样，左移相当于将其乘以 2。Solidity 提供了`>>`按位右移的运算符。用右移运算代替除以 2 的操作，我们实现了两个主要优点：
**Gas 效率：** EVM 的`DIV`操作码消耗 5 Gas。相比之下，`SHR`（右移）操作码仅需 3 Gas，因此该操作的 Gas 消耗量减少了 40%。

**绕过额外检查： Solidity 对 shr 和 shl 操作不进行上溢/下溢或除法检查**。使用按位移位时，我们可以绕过此检查，从而节省额外的 Gas。

## 测试



**文件位置：**

```Bash
src/compiler/MulDiv.sol
test/compiler/MulDiv.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_shift_ -vvv --optimize
```



![使用位移替换乘除运算图示](/images/gas-optimization-master/compiler/12-bit-shifts-01.png)



## 总结

1. 确定代码中使用除以 2 的区域。

2. 用按位右移代替除法运算。

3. 确保上下文和逻辑在更改后仍然有意义，尤其是在处理负值或精度至关重要时。

## 对应源码

- [`src/compiler/MulDiv.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/MulDiv.sol)
- [`test/compiler/MulDiv.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/MulDiv.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
