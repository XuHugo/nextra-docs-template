# 使用位图替换大量 bool

## 分析

这是一种常见的模式，尤其是在空投中，在领取空投或 NFT 铸币时将地址标记为“已使用”。然而，由于存储此信息仅需 1 位，而每个存储槽有 256 位，这意味着一个存储槽可以存储 256 个标志/布尔值。

BitMaps（位图）是一种使用位（bit）来存储布尔值（true/false）的数据结构，在以太坊智能合约中常用于批量标记、授权、白名单等场景。它相较于常规的 mapping\(uint256 =\> bool\) 结构，有以下优势，尤其体现在 gas 成本的优化上。

1. 存储层面的优势

- 节省存储空间

    - mapping\(uint256 =\> bool\) 每个布尔值都单独占用一个存储槽（slot），即 256 位（32 字节）。

    - BitMaps 则可以把 256 个布尔值压缩在同一个存储槽（slot）中。每个位代表一个布尔值。

2. 其它优势

- 批量操作：可以用位运算一次性处理一组标志，提升效率。

- 可组合性：适合大规模布尔集合，如 NFT 空投/资格列表等。



## 测试

**文件位置：**

```Bash
src/storage/BitMaps.sol
test/storage/BitMaps.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_bitmap_ -vvv --optimize
```



Gas 成本对比，批量标记 10 个 NFT 已被领取。

A\. 传统 mapping 方案

```Solidity
mapping(uint256 => bool) public claimed;
function batchClaim(uint256[] memory ids) public {
    for (uint i = 0; i < ids.length; i++) {
        require(!claimed[ids[i]], "Already claimed");
        claimed[ids[i]] = true;
    }
 }
```

- 每次 claimed\[ids\[i\]\] = true; 都会单独写入一个 slot，10 次就是 10 个 slot。

- 写入新 slot 的 gas：\~20,000 gas/slot（首次写入）。

B\. BitMaps 方案

使用 OpenZeppelin BitMaps 库：

```Solidity
import "@openzeppelin/contracts/utils/structs/BitMaps.sol";
BitMaps.BitMap private claimed;
function batchClaim(uint256[] memory ids) public {
    for (uint i = 0; i < ids.length; i++) {
        require(!BitMaps.get(claimed, ids[i]), "Already claimed");
        BitMaps.set(claimed, ids[i]);
    }
 }
```

- 10 个 id 实际中，可能只涉及 1个 slot（如果 id 连续）。

- 每修改一个 slot 只产生一次 SSTORE，极大减少 gas 消耗。

![使用位图替换大量 bool图示](/images/gas-optimization-master/storage/08-bitmaps-01.png)

实际 gas 取决于 id 分布，但 BitMaps 优势明显。

## 总结

BitMaps 通过将布尔数组压缩进单一存储槽，极大地减少了 SSTORE 次数，从而降低了写入 gas 成本。适用于大规模、稠密的布尔型状态管理场景，是智能合约 gas 优化的重要技术之一。

## 对应源码

- [`src/storage/BitMaps.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/BitMaps.sol)
- [`test/storage/BitMaps.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/BitMaps.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
