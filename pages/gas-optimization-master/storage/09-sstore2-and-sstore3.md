# 使用 SSTORE2 或 SSTORE3 存储大量数据

## 分析

当需要在 EVM 上存储大量数据时，直接使用合约 `storage` 会十分昂贵，所以其实不推荐链上存储大量的数据。如果必须要存储，可以使用`SSTORE2`和`SSTORE3`库，它们提供了一种使用“代码即存储”的新方法，可以在链上高效地存储和检索大量数据。 `SSTORE3`相对于`SSTORE2`，在于它允许更小的指针大小，让您可以更轻松地将数据指针与其他存储变量打包在一起，从而节省更多 Gas。

**SSTORE**

SSTORE 是 EVM 的一个操作码，允许我们基于键值对存储持久数据。与 EVM 中的所有内容一样，键和值都是 32 字节的值。写入（SSTORE）和读取（SLOAD）的成本非常高昂，具体来说，需要消耗非常多的Gas。例如写入 32 字节需要 22,100 Gas，相当于每字节约 690 Gas。而写入智能合约的字节码则需要每字节 200 Gas。

**SSTORE2**

SSTORE2 的独特之处在于它使用合约的字节码来写入和存储数据。为了实现这一点，我们利用了字节码固有的不可变性。SSTORE2 的一些特性：

- 工作原理: SSTORE2 的模式是一个非常聪明的技巧。它不是将数据保存到存储槽中，而是：

    1. 构建一个非常小的、新的合约，这个新合约的运行时字节码 \(runtime bytecode\) *就是*

    你想要存储的数据本身。

    2. 它使用 CREATE 操作码部署这个新的“数据合约”。

    3. 它返回这个新创建合约的地址（sstore2Pointer）。

    4. 当需要读取数据时，它对该地址使用 EXTCODECOPY 操作码，这个操作码比从存储中读取（SLOAD）要便宜得多。

- 表达的含义: 这展示了一种巨大的 Gas 节省模式。你用一个相对便宜的 CREATE 调用，替换了许多次极其昂贵的

SSTORE 调用。在你的主合约中，唯一的存储成本就是用一次 SSTORE 来保存 sstore2Pointer 这个地址。



**SSTORE3**

为了理解SSTORE3，首先让我们回顾一下SSTORE2的一个重要属性，新部署的地址取决于我们想要存储的数据。 而SSTORE3 库，它在 SSTORE2 的基础上做了进一步改进。

写入数据 SSTORE3实现了一种设计，使得新部署的地址独立于我们提供的数据。它先通过 CREATE2 部署代理合约，然后通过代理合约把数据（或代码）存储到一个新合约中，最终返回新合约的地址。这种设计选择使我们能够仅通过提供盐（可以少于 20 个字节）即可有效地计算数据的指针地址。从而使我们能够将指针与其他变量打包在一起，从而降低存储成本。

- 工作原理: 它与 SSTORE2 非常相似（将数据存储为字节码），但有一个关键区别：它使用 CREATE3

来部署数据合约。

- CREATE3 允许你根据你提供的一个 salt（盐值），将合约部署到一个可预测的、确定性的地址。

- 因为地址是可预测的，你甚至不再需要在你的合约存储中保存指针地址了！

- write 函数：将数据合约部署到一个确定性的地址。

- read 函数：它使用相同的 salt 在运行时动态地重新计算出地址，然后直接从那个地址读取字节码。

- 这是三种方法中最节省 Gas 的。它拥有 SSTORE2 的所有优点，并且还额外节省了一次 SSTORE

操作（因为指针地址无需保存），这使得 write 操作的成本更低。

## 测试

**文件位置：**

```Bash
src/storage/Sstore.sol
test/storage/Sstore.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_sstore_w -vvv --optimize
```

![使用 SSTORE2 或 SSTORE3 存储大量数据图示](/images/gas-optimization-master/storage/09-sstore2-and-sstore3-01.png)



## 总结

- `Sstore`: 昂贵、最直观的方式。

- `Sstore2`: 通过改变数据存储的介质（字节码 vs\. 存储槽），实现了巨大的进步。需要额外的空间存储address；

- `Sstore3`: 借助确定性地址生成，连指针都无需存储，是这项技术的顶峰。需要额外的步骤计算地址；

***也可以减少 SSTORE2 指针大小，对SSTORE2进行优化。***

*通过利用 CREATE2 确定性 SSTORE2 部署，SSTORE2 的指针大小实际上可以从完整的 20 字节地址减少最多 6 个字节到 14 字节指针，但是这需要您为每次更新挖掘一个盐，从而导致地址以 X 为前导零（其中 **`X`**是您将指针缩小的字节数）。*

## 对应源码

- [`src/storage/Sstore.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Sstore.sol)
- [`test/storage/Sstore.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Sstore.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
