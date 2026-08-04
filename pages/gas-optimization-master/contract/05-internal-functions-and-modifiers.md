# 内部函数和修饰符

## 分析

**修改器**会将其实现字节码直接注入到使用位置，这可以减少运行时 gas 成本，但由于代码重复，会增加部署大小。**内部函数**会跳转到函数的实现，这可以减少部署大小，但会略微增加运行时 gas 成本。这给两种选择带来了一定的权衡。

- 多次使用修饰符会导致重复执行并增加运行时代码的大小，但由于无需跳转到内部函数执行偏移量并跳转回继续执行，因此可以降低 Gas 成本。这意味着，如果您最关心运行时 Gas 成本，那么修饰符应该是您的选择；但如果部署 Gas 成本和/或减少创建代码的大小对您最重要，那么使用内部函数将是最佳选择。

- 然而，修饰符的缺点是它们只能在函数的开头或结尾执行。这意味着在函数中间执行修饰符是不可能的，至少在没有内部函数的情况下是不行的，因为内部函数违背了修饰符的初衷。这影响了修饰符的灵活性。然而，内部函数可以在函数的任何位置调用。



## 测试

**文件位置：**

```Bash
src/contract/Modifier.sol
test/contract/Modifier.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_modifier_ -vvv --optimize
```



![内部函数和修饰符图示](/images/gas-optimization-master/contract/05-internal-functions-and-modifiers-01.png)

从上面的例子我们可以看出：

- 由于`onlyOwner`在函数中重复了功能，使用修饰符的合约产生的部署 gas 成本比使用内部函数的合约更高。



## 总结

- 如果您主要关心的是运行时 gas 成本，并且您不介意增加部署规模，那么修饰符是一个不错的选择。它们通过避免跳转到内部函数来降低函数调用期间的 gas 成本。

- 如果最小化部署 gas 成本并减少创建代码的大小更重要，那么内部函数是更好的选择。它们提供了更大的灵活性，因为它们可以在函数中的任何位置调用，而不仅仅是在开始或结束时。

## 对应源码

- [`src/contract/Modifier.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Modifier.sol)
- [`test/contract/Modifier.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Modifier.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
