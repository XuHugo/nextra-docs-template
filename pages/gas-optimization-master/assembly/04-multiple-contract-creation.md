# 内存优化：创建多个合约

### 分析

Solidity 将合约创建视为类似外部调用，返回 32 个字节（即，返回已创建合约的地址，如果合约创建失败则返回地址 \(0\)）。优化此操作的一种方法是将返回的地址存储在临时空间中，避免扩展内存。请参阅下面的类似示例；

```Solidity

    // cost: 261032
    function call() external returns (Called, Called) {
        Called called1 = new Called();
        Called called2 = new Called();
        return (called1, called2);
    }


    // cost: 260210
    function call() external returns(Called, Called) {
        bytes memory creationCode = type(Called).creationCode;
        assembly {
            let called1 := create(0x00, add(0x20, creationCode), mload(creationCode))
            let called2 := create(0x00, add(0x20, creationCode), mload(creationCode))
// revert if either called1 or called2 returned address(0)
            if iszero(and(called1, called2)) {
                revert(0x00, 0x00)
            }
            mstore(0x00, called1)
            mstore(0x20, called2)
            return(0x00, 0x40)
        }
    }

contract Callme1 {
    function add(uint256 a, uint256 b) external pure returns(uint256) {
        return a + b;
    }
 }
```

通过使用内联汇编，节省了gas。注意：在部署两个合约不相同的场景下，第二个合约的创建代码需要使用内联汇编手动存储，而不是赋值给 Solidity 中的变量，以避免内存膨胀。  

### 测试

**文件位置：**

```Bash
src/assembly/MemoryExp.sol
test/assembly/MemoryExp.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_memexp_deploy_ -vvv --optimize
```



![内存优化：创建多个合约图示](/images/gas-optimization-master/assembly/04-multiple-contract-creation-01.png)



### 总结

## 对应源码

- [`src/assembly/MemoryExp.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MemoryExp.sol)
- [`test/assembly/MemoryExp.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MemoryExp.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
