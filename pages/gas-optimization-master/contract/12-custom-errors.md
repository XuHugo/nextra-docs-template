# 使用自定义错误

## 分析

由于自定义错误的处理方式，自定义错误比带有字符串的 require 语句更便宜。Solidity 仅存储错误签名哈希值的前 4 个字节并仅返回该字节。这意味着在还原期间，只需在内存中存储 4 个字节。对于 require 语句中的字符串消息，Solidity 必须至少在内存中存储 64 个字节并使用它们进行还原。下面是一个例子。

```Solidity
// SPDX-License-Identifier: MIT
 pragma solidity 0.8.23;
contract CustomError {
    error InvalidAmount();
function withdraw(uint256 _amount) external pure {
        if (_amount > 10 ether) revert InvalidAmount();
    }
 }
// This uses more gas than the above contract
 contract NoCustomError {
    function withdraw(uint256 _amount) external pure {
        require(_amount <= 10 ether, "Error: Pass in a valid amount");
    }
 }
```

- **返回 payload 更小：**

    - 自定义错误只返回 **4 字节 selector**，比如 `ErrorName()` 的前 4 个字节，比如 `0x82b42900` 等，回退时只需在内存中存储这 4 个字节。

    - 而 `require(..., "error message")` 则返回的是完整的字符串格式：Error\(string\)，包括函数选择器 \+ string 长度 \+ 数据等，至少几十个字节（比如一个 12 \+ 字符的字符串也要约 68 字节）。

- **更小的内存操作：**

    - 在 Yul 层面的实现中，自定义错误只需 `mstore(free_mem_ptr, selector)`，然后 `revert(ptr, 4)`。仅一个 `mstore` 操作与很少字节数 。

    - 但普通 error string（`revert("Unauthorized")`）需要多个 `mstore` 写入 selector、偏移、长度、字符串内容等，整体写入长度可能超过 100 字节，大量操作成本高 。

- **合约体积更小（部署节省 gas）：**

    - 合约字节码中不再嵌入完整错误字符串，减少 bytecode 大小。数据显示仅一个自定义错误就可节省约 0\.13 KiB 的部署大小，对于大合约而言更明显。



## 测试

**文件位置：**

```Bash
src/contract/CustomErr.sol
test/contract/CustomErr.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_customError_ -vvv --optimize
```



![使用自定义错误图示](/images/gas-optimization-master/contract/12-custom-errors-01.png)



## 总结

**自定义错误只存储并返回错误选择器的前 4 个字节**，而 `require` 携带字符串消息时，需要存储并返回更多的字节（通常几十字节），导致回退时需要占用更多内存和 gas。因此，自定义错误整体上比 `require(string)` 更加高效，既节省回退时的 gas，也缩减合约部署体积。

## 对应源码

- [`src/contract/CustomErr.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/CustomErr.sol)
- [`test/contract/CustomErr.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/CustomErr.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
