# 内存优化：Hash

### 分析

使用汇编对最多 96 个字节的数据进行哈希处理

```Solidity
contract ExpensiveHasher {
    bytes32 public hash;
    struct Values {
        uint256 a;
        uint256 b;
        uint256 c;
    }
    Values values;
    // cost: 113155function setOnchainHash(Values calldata _values) external {
        hash = keccak256(abi.encode(_values));
        values = _values;
    }
 }
contract CheapHasher {
    bytes32 public hash;
    struct Values {
        uint256 a;
        uint256 b;
        uint256 c;
    }
    Values values;
    // cost: 112107
    function setOnchainHash(Values calldata _values) external {
        assembly {
            // cache the free memory pointer because we are about to override it 
            let fmp := mload(0x40)
            
            // use 0x00 to 0x60
            calldatacopy(0x00, 0x04, 0x60)
            sstore(hash.slot, keccak256(0x00, 0x60))
            // restore the cache value of free memory pointer
            mstore(0x40, fmp)
        }
        values = _values;
    }
 }
```

在上面的例子中，与第一个类似，我们使用汇编将值存储在内存的前 96 个字节中，这节省了 1,000 多 gas。另请注意，在本例中，由于我们仍然要分解回 Solidity 代码，因此我们在汇编代码块的开头和结尾缓存并更新了可用内存指针。这是为了确保 Solidity 编译器对内存存储内容的假设仍然兼容。

### 测试



**文件位置：**

```Bash
src/assembly/MemoryExp.sol
test/assembly/MemoryExp.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_memexp_hasher_ -vvv --optimize
```



![内存优化：Hash图示](/images/gas-optimization-master/assembly/07-hashing-01.png)



### 总结

## 对应源码

- [`src/assembly/MemoryExp.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MemoryExp.sol)
- [`test/assembly/MemoryExp.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MemoryExp.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
