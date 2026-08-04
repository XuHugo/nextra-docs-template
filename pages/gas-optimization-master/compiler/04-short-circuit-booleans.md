# 条件优化：短路布尔值

## 分析

在 Solidity 中，当你评估一个布尔表达式（例如\|\|逻辑或或\&\&逻辑与运算符）时，只有当\|\|第一个表达式的计算结果为假时，才会评估第二个表达式；只有当\&\&第一个表达式的计算结果为真时，才会评估第二个表达式。这称为短路。

例如，require\(msg\.sender == owner \|\| msg\.sender == manager\)如果第一个表达式的msg\.sender == owner计算结果为真，则表达式将通过。第二个表达式msg\.sender == manager将根本不被评估。但是，如果第一个表达式的msg\.sender == owner计算结果为假，则将评估第二个表达式msg\.sender == manager以确定整个表达式是真还是假。

在这里，通过首先检查最有可能通过的条件，我们可以避免检查第二个条件，从而在大多数成功的调用中节省 Gas。这对于表达式类似require\(msg\.sender == owner \&\& msg\.sender == manager\)。如果第一个表达式的msg\.sender == owner计算结果为假，则不会评估第二个表达式，msg\.sender == manager因为整个表达式不可能为真。为了使整个语句为真，表达式的两边都必须评估为真。

短路很有用，建议将开销较小的表达式放在最前面，因为开销较大的表达式可能会被绕过。如果第二个表达式比第一个表达式更重要，则可能需要颠倒它们的顺序，以便先执行开销较小的表达式。  

## 测试

**文件位置：**

```Bash
src/compiler/Short.sol
test/compiler/Short.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_short_ -vvv --optimize
```



![条件优化：短路布尔值图示](/images/gas-optimization-master/compiler/04-short-circuit-booleans-01.png)



## 总结

- 利用**短路**来防止不必要的函数调用或计算。

- 在逻辑运算中，将可能成功（或消耗较少 gas）的函数或条件放在其他函数或条件**之前。**

- 了解操作的 gas 成本，并构建代码以尽可能地降低这些成本。

## 对应源码

- [`src/compiler/Short.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Short.sol)
- [`test/compiler/Short.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Short.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
