# 使用汇编检查Address(0)

## 分析

使用内联汇编编写合约通常被认为是 Gas 优化的。这样我们就可以直接操作内存，使用更少的操作码，而不必将其交给 Solidity 编译器。身份验证机制就是一个使用内联汇编的良好示例，例如实现地址零校验。以下是一个例子：

```Solidity
require(addr != address(0), "zero address");

assembly {
    if iszero(addr) {
        // revert or return
    }
}
```

- 编译后会涉及类型检查、错误字符串引用等，虽然编译器优化优秀，但还是有额外开销。

- `iszero(addr)` 只是一条EVM指令，没有类型转换，也不需要构造错误字符串。

- 更进一步，如果你只是需要跳过零地址，可以直接用`iszero`配合`jump`或`revert`。



## 测试

**文件位置：**

```Bash
src/assembly/Address0.sol
test/assembly/Address0.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_address0_ -vvv --optimize
```



![使用汇编检查Address(0)图示](/images/gas-optimization-master/assembly/08-address-zero-check-01.png)



## 总结

- 你极致追求gas优化（如ERC20、批量操作、低层库）。

- 错误信息不重要，或用全局 revert selector。

- 你的代码review团队熟悉Yul。

## 对应源码

- [`src/assembly/Address0.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/Address0.sol)
- [`test/assembly/Address0.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/Address0.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
