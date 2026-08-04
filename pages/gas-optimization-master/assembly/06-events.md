# 内存优化：事件

### 分析

使用汇编记录最多 96 个字节的未索引数据

```Solidity
contract ExpensiveLogger {
    event BlockData(uint256 blockTimestamp, uint256 blockNumber, uint256 blockGasLimit);
    // cost: 26145
    function returnBlockData() external {
        emit BlockData(block.timestamp, block.number, block.gaslimit);
    }
 }
contract CheapLogger {
    event BlockData(uint256 blockTimestamp, uint256 blockNumber, uint256 blockGasLimit);
    // cost: 22790
    function returnBlockData() external {
        assembly {
            mstore(0x00, timestamp())
            mstore(0x20, number())
            mstore(0x40, gaslimit())
            log1(0x00, 
                0x60,
                0x9ae98f1999f57fc58c1850d34a78f15d31bee81788521909bea49d7f53ed270b // event hash of BlockData
            )
        }
    }
 }
```

上面的示例展示了如何通过使用内存来存储我们希望在BlockData事件中发出的数据，从而节省近 2,000 Gas。这里无需更新可用内存指针，因为执行在事件发出后立即结束，并且我们无需返回 Solidity 代码。让我们再举一个例子，其中我们需要更新可用内存指针

### 测试

**文件位置：**

```Bash
src/assembly/MemoryExp.sol
test/assembly/MemoryExp.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_memexp_logger_ -vvv --optimize
```



![内存优化：事件图示](/images/gas-optimization-master/assembly/06-events-01.png)



### 总结

## 对应源码

- [`src/assembly/MemoryExp.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MemoryExp.sol)
- [`test/assembly/MemoryExp.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MemoryExp.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
