# 待验证：无符号整数使用 != 0 代替 > 0

## 分析

- **Gas 成本变化**：在对无符号整数进行比较时，比较运算符的选择会影响 Gas 成本。具体来说，在优化条件下，`!= 0`比`> 0`语句略微节省 Gas 。

- **优化器效率**：启用优化器后，在语句`!= 0`中使用 for 比较`require`与使用相比，每次操作可节省约 6 个 gas `> 0`。

## 测试

**文件位置：**

```Bash
src/compiler/Uint.sol
test/compiler/Uint.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_uint_ -vvv --optimize
```

未加\-\-optimize时，确实有一些差距

加\-\-optimize之后，优化之后，一样的；

![待验证：无符号整数使用 != 0 代替 > 0图示](/images/gas-optimization-master/compiler/03-nonzero-comparison-01.png)

## 总结

编译已经优化。

：[https ://](https://twitter.com/gzeon/status/1485428085885640706)[twitter\.com/gzeon/status/1485428085885640706](https://twitter.com/gzeon/status/1485428085885640706)

## 对应源码

- [`src/compiler/Uint.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Uint.sol)
- [`test/compiler/Uint.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Uint.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
