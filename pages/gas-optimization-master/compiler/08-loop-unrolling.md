# 展开循环

## 分析

for 循环内置了跳转指令，因此您可能需要考虑[展开循环](https://en.wikipedia.org/wiki/Loop_unrolling)以节省 Gas。循环不必完全展开。例如，您可以一次执行两个循环，并将跳转指令的数量减半。

## 测试

**文件位置：**

```Bash
src/compiler/UnRoll.sol
test/compiler/UnRoll.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_unroll_ -vvv --optimize
```



![展开循环图示](/images/gas-optimization-master/compiler/08-loop-unrolling-01.png)

根据测试结果，普通的展开循环，其实并没有gas优化；

但是如果我们把切换到汇编模式，即展开和未展开都使用汇编编写，此时展开循环就会有gas优化。

## 总结

这是一种非常极端的优化，但应该注意，条件跳转和循环会引入开销略大的操作码。

## 对应源码

- [`src/compiler/UnRoll.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/UnRoll.sol)
- [`test/compiler/UnRoll.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/UnRoll.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
