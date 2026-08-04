# 使用枚举而不是字符串

与其他数据类型相比，字符串的 Gas 消耗更高。如果可能，请考虑使用枚举代替字符串来表示有限的选项集。枚举提供了一种紧凑高效的方式来处理预定义的值列表。使用枚举可以降低与字符串操作和存储相关的 Gas 成本。

### 存储成本

- **字符串存储：**字符串是动态数据类型，需要额外的长度信息；短字符串（≤31字节）：打包存储，但仍需长度标记；长字符串（\>31字节）：分别存储长度和数据，消耗多个存储槽

- **枚举存储：**枚举本质上是 uint8（最多256个选项）；固定大小，直接存储在一个存储槽中；无需额外的长度信息

### 比较操作成本

- 比较两个字符串时（如 `if (str1 == str2)`），编译器会展开为字节数组逐字节比较，在 EVM 层面通常涉及 `keccak256` 或内联循环比较，**gas 昂贵**。

- 枚举比较实际上就是比较整数（`uint8`），非常便宜（\~3 gas）。



## 测试

**文件位置：**

```Bash
src/compiler/Enums.sol
test/compiler/Enums.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_enums_ -vvv --optimize
```



![使用枚举而不是字符串图示](/images/gas-optimization-master/compiler/16-enums-over-strings-01.png)



## 总结

**在需要表示固定选项集的场景中，使用枚举代替字符串能显著降低 gas 成本**，因为它能减少存储槽占用和运行时操作复杂度，是 Solidity 编码中的推荐实践之一。

## 对应源码

- [`src/compiler/Enums.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Enums.sol)
- [`test/compiler/Enums.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Enums.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
