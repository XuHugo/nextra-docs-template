# 通过哈希比较数组和字符串

## 分析

如果要测试数组和字符串是否相等，则通过哈希值来比较它们是否相等。这是一个你很少会使用的技巧，因为循环遍历数组或字符串比对它们进行散列并比较散列要昂贵得多。

## 测试

**文件位置：**

```Bash
src/compiler/CompareHash.sol
test/compiler/CompareHash.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_hash_ -vvv --optimize
```

比较字符串“a”的时候，hash的gas消耗还是稍高一些的。

![通过哈希比较数组和字符串图示](/images/gas-optimization-master/compiler/10-hash-array-string-comparison-01.png)

比较字符串“aa”的时候，这个时候使用hash已经优于普通的遍历了。

![通过哈希比较数组和字符串图示 2](/images/gas-optimization-master/compiler/10-hash-array-string-comparison-02.png)



## 总结

- **最常用、最高效**：`keccak256(a) == keccak256(b)`（优先带长度检查）

- 只在少量短字符串中，才用迭代比较法

- 此方式适用于各种动态字节类型（`string`, `bytes`, 动态数组）

## 对应源码

- [`src/compiler/CompareHash.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/CompareHash.sol)
- [`test/compiler/CompareHash.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/CompareHash.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
