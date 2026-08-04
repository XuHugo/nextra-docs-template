# 待验证：修改器中使用内部视图函数

## 分析

建议将修饰符 require 语句移至 中。这可以减少使用修饰符的已编译合约的大小。将 require 语句放在内部函数中，可以在多次使用修饰符时减少合约大小。与和函数`internal virtual function`相比，部署 gas 成本没有差异。`privateinternal`

这个优化建议的核心是：将修饰符中的 require 语句提取到内部函数中，可以减少合约的字节码大小。



背景机制：

- 修饰符复制机制：每次使用修饰符时，Solidity 编译器会将修饰符的代码复制到使用它的函数中

- 代码重复问题：如果多个函数使用同一个修饰符，require 语句会被重复多次

- 内部函数优化：将 require 逻辑放在内部函数中，修饰符只调用这个函数，避免代码重复



编译器行为

- 未优化：修饰符代码在每个使用点都被内联展开

- 优化后：修饰符只包含函数调用，require 逻辑只存在一份



## 测试

**文件位置：**

```Bash
src/contract/Payable.sol
test/contract/Payable.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_payable_ -vvv --optimize
```



## 总结

**第一种写法 \(独立辅助函数，通过 ****`jump`**** 调用\)：**

- **优点：** 代码模块化，减少部署时的合约大小（如果修饰符被多处复用）。

- **缺点：** 运行时 Gas 消耗较高，因为每次修饰符检查都涉及额外的 `JUMP` 操作。

**第二种写法 \(内联修饰符逻辑\)：**

- **优点：** 运行时 Gas 消耗较低，因为它减少了 `JUMP` 操作，使得代码执行路径更直接。

- **缺点：** 如果修饰符在多个函数中被使用，会导致编译后的合约代码重复，增加合约部署 Gas 成本和合约大小。

-

## 对应源码

- [`src/contract/Payable.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Payable.sol)
- [`test/contract/Payable.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Payable.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
