# 变量打包

## 分析

在 Solidity 中，将多个变量打包到同一个存储槽（storage slot）中是优化 Gas 成本的有效策略。这种打包可以通过两种方式实现：手动打包和 EVM 自动打包。选择哪种方式取决于具体的使用场景和对 Gas 成本的敏感程度。我们先看evm自动打包的两个例子

```Solidity

contract Packgood {
    uint256 public a;
    uint256 public b;
    uint80 public c;
    uint80 public d;
    address public e;
    function setPackgood() public {
        c = 12;
        d = 34;
        e = address(0x1234567890);
    }
}
```

当 solidity 编译器遇到连续的多个占据位数较少的变量声明时，solidity 编译器会选择打包这些变量。比如此处的c 和 d 各占据 80 bit, e是 address 类型实际占用 160 bit，这三个声明时紧邻的变量位数之和为 320 bit，所以 solidity 编译器则会选择将c,d打包起来一起存储，e单独存储；即对c、d 的赋值只进行了一次存储槽写入。

如果你觉得还不够，其实还可以深入的优化一次；手动打包。我们模仿solidity的行为，将原来的c、d,使用一个类型为uint160的变量存储和检索，它只占用一个存储槽，并且在单笔交易中存储或读取单个值时成本更低。

```Solidity
contract Packbest {
    uint256 public a;
    uint256 public b;
    uint160 public cd;
    address public e;
    function setPackbest() public {
        pack(12, 34);
        e = address(0x1234567890);
    }
    function pack(uint80 x, uint80 y) private {
        cd= (uint160(x) << 80) | uint160(y);
    }
    function unpack() external view returns (uint80, uint80) {
        uint80 x = uint80(cd>> 80);
        uint80 y = uint80(cd);
        return (x, y);
    }
}
```



||**手动打包**<br>|**EVM 自动打包**|
|---|---|---|
|原理|开发者使用位移（bit\-shifting）和按位或（bitwise OR）等位运算，将多个小于 256 位的变量合并存储到一个 uint256 类型的变量中。|Solidity 编译器会自动将连续声明的、大小小于 256 位的状态变量打包到同一个存储槽中，以节省存储空间。|
|优点|- **更低的 Gas 成本：      **由于只需一次 SSTORE 操作即可写入所有打包的变量，减少了写入操作的次数，从而降低了 Gas 成本。<br>- **更高的控制性：      **开发者可以精确控制每个变量在存储槽中的位置，优化存储布局。|- **开发便利：      **无需手动编写位运算逻辑，代码更简洁。<br>|
|缺点|- **代码复杂度增加：      **需要手动编写位运算逻辑，增加了代码的复杂性和出错的可能性。|- **较高的 Gas 成本：      **尽管变量被打包到同一个存储槽中，但每个变量的读写操作仍然需要单独的 SLOAD 或 SSTORE 操作。<br>- **EVM 自动处理位移：** EVM 在读取或写入部分存储槽时，需要执行掩码和位移操作，增加了额外的 Gas 成本。|

## 测试



**文件位置：**

```Bash
src/storage/Pack.sol
test/storage/Pack.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_pack_ -vvv --optimize
```

![变量打包图示](/images/gas-optimization-master/storage/04-variable-packing-01.png)

不打包和编译器自动打包的gas消耗差距很小，但是我们手动打包gas优化就比较明显了。实际开发时需要进行测试对比，在安全、维护、性能等各方面考虑下决定使用哪种方式。

## 总结

如果你的合约对 Gas 成本非常敏感，且愿意承担额外的开发复杂度，手动打包是更优的选择。它可以显著减少存储操作的次数，从而降低 Gas 成本。然而，如果您的合约对 Gas 成本要求不高，或者优先考虑开发效率和代码可读性，EVM 自动打包可能更适合您。

在实际开发中，您可以根据具体需求选择合适的打包方式，甚至在同一个合约中混合使用两种方式，以达到最佳的性能和可维护性。

打包结构体项（例如打包相关状态变量）有助于节省 Gas。（需要注意的是，在 Solidity 中，结构体成员按顺序存储在合约存储中，从它们初始化的 slot 位置开始）。

## 对应源码

- [`src/storage/Pack.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Pack.sol)
- [`test/storage/Pack.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Pack.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
