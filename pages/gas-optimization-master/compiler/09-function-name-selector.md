# 频繁使用的函数名

## 分析

在合约中，所有函数都被组织成一个数组，并根据其 MethodID（每个函数的唯一标识符）进行系统排序。这种组织方式不仅简化了函数调用的管理，还通过强制执行结构化顺序来促进快速访问，以便在函数执行期间进行高效搜索。

当一个函数被调用时，系统并不会立即执行该函数，而是开始在函数数组中顺序搜索。它使用 MethodID 来准确定位并执行所需的函数。在此搜索过程中，每次比较 MethodID 都会产生 22 个单位的 Gas 成本。此成本与以太坊虚拟机 \(EVM\) 读取和比较 MethodID 所需的计算工作量相关。

为了优化 Gas 的使用，尤其是在包含大量函数的合约中，开发者可以按照函数的调用频率进行排序。将最常调用的函数放在数组的开头，可以减少大多数调用所需的迭代次数，从而降低整体 Gas 成本并提高合约的效率。

同时优化函数名称，增加 MethodId 中 0 字节的数量可以降低 Gas 成本。这种优化对于频繁调用的函数尤其有效，因为它直接影响合约交互的整体 Gas 效率。



```Solidity
// SPDX-License-Identifier: MIT
 pragma solidity 0.8.20;
contract MethodID {
    uint256 counter=0;
    *//0x371303c0*
    function inc() external {
       ++counter;
    }
}

contract MethodIDOpt {
    uint256 counter=0;
    *//0x00000011*
    function inc_C2A2FA() external {
        ++counter;
    }
}

```

此外，我们还有一个用 Rust 构建的实用工具 Solidity Zero Finder，可以帮助开发人员实现这一目标。

## 测试



**文件位置：**

```Bash
src/compiler/MethodID.sol
test/compiler/MethodID.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_methodid_ -vvv --optimize
```



![频繁使用的函数名图示](/images/gas-optimization-master/compiler/09-function-name-selector-01.png)



## 总结

- 通过根据调用频率对函数进行排序，并将调用最多的函数放在数组顶部，我们可以降低 gas 成本，特别是对于高频操作。

- 通过优化函数名称，最大限度地提高 MethodId 中 0 字节的出现频率，我们可以降低 Gas 消耗。（需要注意的是，这种方法会在一定程度上影响代码的可读性。）

## 对应源码

- [`src/compiler/MethodID.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/MethodID.sol)
- [`test/compiler/MethodID.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/MethodID.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
