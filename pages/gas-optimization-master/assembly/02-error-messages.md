# 内存优化：错误消息

## 分析

在 Solidity 代码中执行回滚操作时，通常使用 require 或 revert 语句来回滚执行并返回错误信息。大多数情况下，可以使用汇编代码回滚并返回错误信息来进一步优化。以下是示例：

```Solidity
/// calling restrictedAction(2) with a non-owner address: 24042
 contract SolidityRevert {
    address owner;
    uint256 specialNumber = 1;
    constructor() {
        owner = msg.sender;
    }
    function calls(uint256 num)  external {
        require(owner == msg.sender, "caller is not owner");
        specialNumber = num;
     }
 }
/// calling restrictedAction(2) with a non-owner address: 23734
contract AssemblyRevert {
    address owner;
    uint256 specialNumber = 1;
    constructor() {
        owner = msg.sender;
    }
    function calls(uint256 num)  external {
        assembly {
            if sub(caller(), sload(owner.slot)) {
                mstore(0x00, 0x20) // store offset to where length of revert message is stored
                mstore(0x20, 0x13) // store length (19)
                mstore(0x40, 0x63616c6c6572206973206e6f74206f776e657200000000000000000000000000) // store hex representation of message
                revert(0x00, 0x60) // revert with data
            }
        }
        specialNumber = num;
    }
 }
```

从上面的例子中我们可以看到，使用汇编语言进行同样的错误信息恢复比使用 Solidity 语言恢复节省了超过 300 Gas。这部分 Gas 节省来自于内存扩展成本以及 Solidity 编译器在后台执行的额外类型检查。  

## 测试

**文件位置：**

```Bash
src/assembly/AssemblyErr.sol
test/assembly/AssemblyErr.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_revert_ -vvv --optimize
```



![内存优化：错误消息图示](/images/gas-optimization-master/assembly/02-error-messages-01.png)



## 总结



- 更高效：可以直接操作存储槽、内存、calldata，省去 Solidity 运行时的各种边界检查和中间变量消耗，节省 gas。

- 自定义编码：允许你用自己的方式打包数据（如本例中自己决定如何编码字符串和长度）。

- 极限优化：可以省略一些安全检查和冗余操作，做到极致紧凑。

## 对应源码

- [`src/assembly/AssemblyErr.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/AssemblyErr.sol)
- [`test/assembly/AssemblyErr.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/AssemblyErr.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
