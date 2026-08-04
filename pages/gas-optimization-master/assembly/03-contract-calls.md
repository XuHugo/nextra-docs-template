# 内存优化：调用合约

### 分析

当从合约 A 调用合约 B 上的函数时，最方便的方式是使用接口，创建一个带有地址的 B 实例，然后调用我们想要调用的函数。这种方法效果很好，但由于 Solidity 编译代码的方式，它会将要发送给合约 B 的数据存储在新的内存位置，从而扩展内存，有时这种扩展是不必要的。使用内联汇编，我们可以更好地优化代码，并通过使用以前使用过但不再需要的内存位置，或者（如果合约 B 预期的调用数据小于 64 字节）在临时空间中存储调用数据来节省一些 gas。以下是比较两者的示例：

```Solidity
/// 30570
function set(address addr, uint256 num) external {
        Callme(addr).setNum(num);
}

/// 30350
function set(address addr, uint256 num) external {
        assembly {
            mstore(0x00, hex"cd16ecbf")
            mstore(0x04, num)
if iszero(extcodesize(addr)) {
                revert(0x00, 0x00) // revert if address has no code deployed to it
            }
let success := call(gas(), addr, 0x00, 0x00, 0x24, 0x00, 0x00)
            
            if iszero(success) {
                revert(0x00, 0x00)
            }
        }
    }
contract Callme {
    uint256 num = 1;
function setNum(uint256 a) external {
        num = a;
    }
 }
```

我们可以看到，汇编使用的Gas更少。请注意，使用内联汇编进行外部调用时，务必检查调用的地址是否已部署代码，extcodesize\(addr\)如果返回 0，则进行回滚。这一点很重要，因为调用未部署代码的地址总是返回 true，这在大多数情况下会对我们的合约逻辑造成毁灭性打击。 

### 测试

**文件位置：**

```Bash
src/assembly/MemoryExp.sol
test/assembly/MemoryExp.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_memexp_set_ -vvv --optimize
```



![内存优化：调用合约图示](/images/gas-optimization-master/assembly/03-contract-calls-01.png)



### 总结

略

## 对应源码

- [`src/assembly/MemoryExp.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MemoryExp.sol)
- [`test/assembly/MemoryExp.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MemoryExp.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
