# 数学运算:偶奇校验

## 分析

检查一个数是奇数还是偶数的常规方法是执行 ，x % 2 == 0其中 x 是待检查的数。您也可以改为检查x \& uint256\(1\) == 0。其中 x 假设为 uint256 类型。按位执行和比模操作码更便宜。在二进制中，最右边的位表示“1”，而 的所有位都是 2 的倍数，也就是偶数。将 1 加到偶数上会使它变成奇数。

## 测试

**文件位置：**

```Bash
src/assembly/MathOpt.sol
test/assembly/MathOpt.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_isOdd_ -vvv --optimize
```

![数学运算:偶奇校验图示](/images/gas-optimization-master/assembly/10-even-odd-01.png)



## 总结

## 对应源码

- [`src/assembly/MathOpt.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MathOpt.sol)
- [`test/assembly/MathOpt.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MathOpt.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
