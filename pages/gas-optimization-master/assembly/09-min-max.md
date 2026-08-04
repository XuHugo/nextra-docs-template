# 数学运算:min 和 max

## 分析

在优化以太坊智能合约的 Gas 使用时，可以使用汇编语言来提高常见的数学运算效率。虽然 Solidity 提供了高级数学运算，但使用汇编语言实现可以显著节省 Gas。

```Solidity
function max(uint256 x, uint256 y) public pure returns (uint256 z) {
    z = x > y ? x : y;
 }
优化
function max(uint256 x, uint256 y) public pure returns (uint256 z) {
    /// @solidity memory-safe-assembly
    assembly {
        z := xor(x, mul(xor(x, y), gt(y, x)))
    }
 }
```

上面的代码取自[Solady 库](https://github.com/Vectorized/solady/blob/main/src/utils/FixedPointMathLib.sol)的数学部分，更多数学运算可在此处找到。值得探索一下该库，看看有哪些可用的 Gas 高效运算。上面的示例之所以 Gas 效率更高，是因为三元运算符（以及通常包含条件语句的代码）在操作码中包含条件跳转，而这些条件跳转的开销更大。



1. **更少的操作**：与高级实现相比，汇编实现通常使用更少的 EVM 操作。

2. **无条件跳转**：汇编实现可以避免耗费大量气体的条件跳转（JUMPI 操作）。

3. **直接内存访问**：汇编允许直接操作值而无需额外的开销。



## 测试

src/assembly/Mathopt\.t\.sol

**文件位置：**

```Bash
src/assembly/MathOpt.sol
test/assembly/MathOpt.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_max_ -vvv --optimize
```

![数学运算:min 和 max图示](/images/gas-optimization-master/assembly/09-min-max-01.png)

这里可以看到只优化了30多gas。这里有一个需要注意的点，如果优化的gas比较少的时候，一定要注意测试方法，必须两个合约，保证测试的函数名字一样，否则就会出现误差；如果是两个不同的函数名，就到函数id不同。

## 总结

考虑在您的智能合约中使用这些汇编实现来执行经常调用的数学运算

汇编代码会绕过 Solidity 的安全特性。请确保在部署前进行彻底的测试和审核。

## 对应源码

- [`src/assembly/MathOpt.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MathOpt.sol)
- [`test/assembly/MathOpt.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MathOpt.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
