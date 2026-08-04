# 始终使用命名返回

## 分析

在 Solidity 中定义函数时，可以为返回变量命名。这可以增强可读性并减少代码冗余。如果函数具有命名的返回变量并且还包含显式`return`语句，则可能导致冗余和额外的 gas 成本。

```Solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;
contract NameReturns1 {
    function calls(uint256 *x*, uint256 *y*) external pure returns (uint256 *z*) {
       require(x > 0);
       require(y > 0);

        z = x * y;
    }
}

contract NameReturns2 {
    function calls(uint256 *x*, uint256 *y*) external pure returns (uint256 *z*) {
        require(x > 0);
        require(y > 0);
        z = x * y;
        return z;
    }
}

contract Returns {
    function calls(uint256 *x*, uint256 *y*) external pure returns (uint256) {
        require(x > 0);
        require(y > 0);
        return x * y;
    }
}
```

## 测试



**文件位置：**

```Bash
src/compiler/NameReturn.sol
test/compiler/NameReturn.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_return_ -vvv --optimize
```



![始终使用命名返回图示](/images/gas-optimization-master/compiler/20-named-returns-01.png)

## 总结

## 对应源码

- [`src/compiler/NameReturn.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/NameReturn.sol)
- [`test/compiler/NameReturn.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/NameReturn.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
