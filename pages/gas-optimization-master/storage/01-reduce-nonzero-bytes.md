# 减少非零字节

Calldata 是随交易一起发送到合约的数据，例如函数参数。它的 Gas 成本是按字节计算的。

- 零字节 \(Zero Byte\): 消耗 4 Gas。

- 非零字节 \(Non\-Zero Byte\): 消耗 16 Gas。

    **场景:**

    假设你调用一个函数 doSomething\(uint256 amount\)。

- 调用 doSomething\(0\): amount 参数是 0，在 calldata 中会被编码为32个零字节。成本是 32 \* 4 = 128 Gas。

- 调用 doSomething\(1\): amount 参数是 1，编码后包含31个零字节和1个非零字节。成本是 31 \* 4 \+ 1 \* 16 = 140 Gas。

    

    虽然单个参数的差异不大，但如果函数参数包含大量数据（如数组），或者在 Layer 2 的 Rollup场景下，这种差异会变得非常显著，因为所有数据都要提交到主网。

## 避免在calldata中使用有符号整数

### 分析

一种经常被忽视的优化技巧是尽可能避免在调用数据中使用有符号整数。这种方法可以节省 Gas，尤其是在处理较小的负数时。

Solidity 使用二进制补码（two's complement）来表示有符号整数。
对于一个小的负数，比如 \-1，在补码表示中通常是 `0xFF...FF`，也就是全是非零字节，导致 calldata 里几乎没有零字节——这会增加 gas 消耗。

而如果你能用无符号整数（uint）来替代（比如业务上负数其实没有意义），那么小的正数一般编码后会带很多前导零字节，比如 `0x0000...01`，这样 gas 费用会大大降低。

**要点：**

- Solidity 使用二进制补码来表示有符号整数。

- 二进制补码形式的小负数主要由非零字节组成。

- 在calldata中使用无符号整数可以产生更多的零字节，从而降低gas成本。

**例如：** 该数字以二进制补码形式（256 位）`-1`表示。`0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff`

二进制补码是一种用于以二进制表示有符号整数的数学运算。在该系统中，负数的表示方法是将正数的所有位取反，然后加 1。

让我们比较一下在 calldata 中使用有符号整数和无符号整数的 gas 成本：



### 测试

**文件位置：**

```Bash
src/storage/ByteZero.sol
test/storage/ByteZero.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_bytezero_ -vvv --optimize
```

![减少非零字节图示](/images/gas-optimization-master/storage/01-reduce-nonzero-bytes-01.png)





### 总结

- 尽可能使用无符号整数（`uint`）而不是有符号整数（`int` ）。

- 如果需要负值，请考虑使用偏移方法，其中使用无符号整数表示值的范围并在合约逻辑中应用偏移量。

- 请注意权衡：虽然这种优化可以节省 gas，但它可能会使您的合约使用起来不那么直观，并且需要额外的文档。

## 多0地址

### 分析

使用以零开头的靓号地址更便宜，这节省了调用数据的 gas 成本。一个很好的例子是具有以下地址的 OpenSea [Seaport 合约](https://etherscan.io/address/0x00000000000000adc04c56bf30ac9d3c0aaf14dc#code)0x00000000000000ADc04C56Bf30aC9d3c0aAF14dC： 。直接调用该地址时不会节省 gas。但是，如果该合约的地址用作函数的参数，则由于调用数据中包含更多零，该函数调用将花费更少的 gas。将包含大量零的 EOA 作为函数参数传递也是如此 \- 由于同样的原因，它可以节省 gas。请注意，存在使用随机性不足的私钥为钱包生成靓号地址的[黑客行为](https://www.halborn.com/blog/post/explained-the-profanity-address-generator-hack-september-2022)。这不是针对通过为 create2 查找盐创建的智能合约靓号地址的音乐会，因为智能合约没有私钥。  



- 地址占 20 字节，如果有多位 **0x00 前导零**，传递该地址时这些字节变为 zeros

- **直接发起交易** 给该地址：不会影响 calldata，因为‘to’ 字段不在 calldata 内

- **将其作为参数传入函数**：参数部分包含 zeros，calldata 变更，gas 减少 

- 无论是 EOA 还是合约地址都有此优化——但 EOA 如果为 vanity 地址则需强随机私钥，存在风险

### 测试

`无`



### 总结

**为何节省**： calldata 每个 zero 收费仅 4 gas，非零为 16 gas

**怎么用**：把 vanity 地址当作参数传入函数以增加零字节

**风险与应用场景**：

- 合约地址的 vanity 用 `CREATE2` 安全；

- EOA vanity 地址需警惕私钥安全；

- 调用结构中频繁出现该地址参数的函数更划算

## 对应源码

- [`src/storage/ByteZero.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/ByteZero.sol)
- [`test/storage/ByteZero.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/ByteZero.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
