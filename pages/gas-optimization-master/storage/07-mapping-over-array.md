# 使用 mapping 避免数组长度检查

## 分析

当你希望存储一个列表或一组项目，并希望它们按特定顺序组织，并使用固定的键/索引进行提取时，通常的做法是使用数组数据结构。这种方法效果很好，但你是否知道，可以使用mapping来实现一个技巧，在每次读取时节省很多 Gas？请参阅下面的示例。

```Solidity
/// get(0) gas cost: 4860 
 contract Array {
    uint256[] a;
constructor() {
        a.push() = 1;
        a.push() = 2;
        a.push() = 3;
    }
function get(uint256 index) external view returns(uint256) {
        return a[index];
    }
 }
/// get(0) gas cost: 2758
 contract Mapping {
    mapping(uint256 => uint256) a;
constructor() {
        a[0] = 1;
        a[1] = 2;
        a[2] = 3;
    }
function get(uint256 index) external view returns(uint256) {
        return a[index];
    }
 }
```

仅通过使用映射，我们就可以节省 2102 gas。为什么？当您读取数组索引的值时，solidity 会在底层添加字节码来检查您是否从有效索引（即严格小于数组长度的索引）读取，否则它会以恐慌错误（Panic\(0x32\)准确地说）恢复。这可以防止它读取未分配或更糟的已分配存储/内存位置。由于映射的方式（仅仅是一个键 =\> 值对），不存在这样的检查，我们能够直接从存储槽读取。重要的是要注意，当以这种方式使用映射时，您的代码应该确保您没有读取规范数组的超出范围的索引。

除了使用映射来避免 Solidity 在读取数组时进行的长度检查（同时仍然使用数组）之外，还有一种替代方法是使用 Openzeppelin [Arrays\.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Arrays.sol)库中的 unsafeAccess 函数。这允许开发人员直接访问数组中任何给定索引的值，同时跳过长度溢出检查。但仍然重要的是，仅当您确保解析到函数中的索引不能超过解析数组的长度时才使用此方法。

unsafeAccess 是 OpenZeppelin 的 Arrays 库中的一组内部函数，用于以“非安全”方式访问 Solidity 动态数组的元素。这里的“非安全”是指跳过了 Solidity 的下标越界检查，直接通过底层 slot 计算访问存储（storage）中的数组元素。

```Solidity
using Arrays for uint256[];
 
uint256[] private myArray;
 
function getElement(uint256 idx) public view returns (uint256) {
    // 传统写法（有边界检查）：
    // return myArray[idx];
 
    // unsafeAccess 写法（无边界检查，效率更高）：
    return Arrays.unsafeAccess(myArray, idx).value;
}
```

***注意***：*调用者必须确保 idx \< myArray\.length，否则会读到非法存储甚至导致安全隐患！*



## 测试

**文件位置：**

```Bash
src/storage/Maps.sol
test/storage/Maps.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_map_ -vvv --optimize
```

![使用 mapping 避免数组长度检查图示](/images/gas-optimization-master/storage/07-mapping-over-array-01.png)

实际测试情况，使用mapping的消耗gas最少，

## 总结

- 在 Solidity 中，使用 mapping 进行键值查找通常比在动态数组中按索引查找更节省 Gas。

- 可以使用像 Arrays\.unsafeAccess 这样的库函数来进一步优化数组访问的 Gas 成本，但需要开发者自己承担保证索引有效的责任。

- 省略边界检查：Solidity 默认会对数组下标进行范围检查，防止越界。unsafeAccess 直接通过 slot 计算，省去了一次 SLOAD 以及条件判断，从而节省 gas。mapping也是如此。

- 低层原生操作：使用 assembly 和 Storage Slot 操作访问存储，比标准数组读写更直接、指令更少。

- 适合高频或已知安全的场景：比如在手写的二分查找、排序等算法内部，已经逻辑上保证不会越界时，使用 unsafeAccess 可以进一步压榨 gas。

## 对应源码

- [`src/storage/Maps.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Maps.sol)
- [`test/storage/Maps.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Maps.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
