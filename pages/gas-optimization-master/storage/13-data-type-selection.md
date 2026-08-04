# 数据类型的选择

## 分析

1. **关键策略：打包（Packing）小类型变量**

    当多个小于 32 字节的变量在 struct 中或作为合约状态变量被连续声明时，Solidity编译器会尝试将它们“打包”进同一个 32 字节的存储槽中。

    - 如何工作：例如，两个 uint128 变量、或者一个 uint128 和两个 uint64 变量，可以被打包进一个存储槽。

    - 巨大优势：这显著减少了昂贵的 SSTORE 和 SLOAD 操作次数。访问两个打包好的 uint128 变量只需要一次SLOAD，而不是两次。这是节省存储 Gas 的最有效方法之一。

    - 实际应用：时间戳（uint48）和区块号（uint64）就是绝佳的例子。当它们可以和地址（address，20字节）或其他小整数一起打包时，选择这些精确的小类型就能极大提升 Gas 效率。

    

2. **常见陷阱：孤立的小类型**

    如果一个小于 32 字节的类型（如 uint8）无法与其他变量打包，它不仅无法节省 Gas，反而会导致更高的成本。

    - 双重惩罚：

        1. 空间浪费：这个 uint8 变量仍然会独占一个完整的 32 字节存储槽。

        2. 额外计算成本：当对它进行读写或运算时，EVM 需要执行额外的位操作（masking 和 shifting）来将其从 32字节的字中分离出来或确保其范围正确，这会消耗额外的 Gas。

    - 结论：如果一个变量不能被打包，请直接使用 uint256，以避免不必要的计算开销。

        

3. **固定大小 vs\. 动态大小：确定性优于一切**

    在任何可能的情况下，都应优先使用固定大小的变量，因为它们的 Gas 成本更低且更可预测。

    - 字符串：如果文本长度已知且不超过 32 字节，永远选择 `bytes32` 而不是 `string` 或 `bytes`。bytes32被当作值类型处理，仅占用一个存储槽，操作非常便宜。而 string 和 bytes是复杂的引用类型，管理它们的长度和数据位置会产生显著的开销。

    - 数组：如果数组的长度是固定的，请使用固定大小的数组（如uint256\[8\]）而不是动态数组（uint256\[\]）。对固定大小的存储数组进行读写比操作动态数组更高效。

    - 动态数组操作：您关于数组扩展的观察很敏锐。对于动态存储数组：

        - 扩展：在末尾添加元素 \(\.push\(\)\) 的 Gas 成本相对固定。

        - 缩减：缩减数组（例如，修改 \.length 或使用 \.pop\(\)）则更为复杂。虽然清空存储槽会带来 Gas 返还（refund），但操作本身的成本可能很高，尤其是当数组非常大时。因此，应谨慎设计避免频繁缩减存储数组的逻辑。



## 测试

src/storage/Types\.t\.sol

**文件位置：**

```Bash
src/storage/Types.sol
test/storage/Types.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_types_ -vvv --optimize
```

![数据类型的选择图示](/images/gas-optimization-master/storage/13-data-type-selection-01.png)



## 总结

- **EVM 只关心 32 字节 slot，单独小整数会自动扩展为 256 位，反而可能更贵。**

- **正确打包小整数（struct/连续变量）能显著节省合约存储和 gas。**

- **写合约前需评估数据结构，合理选择类型和布局，避免“省小损大”。**

## 对应源码

- [`src/storage/Types.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Types.sol)
- [`test/storage/Types.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Types.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
