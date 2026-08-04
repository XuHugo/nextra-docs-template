# 内存优化：多个外部调用

### 分析

还有一个导致 solidity 编译器扩展内存的操作是进行外部调用。进行外部调用时，编译器必须将它希望在外部合约上调用的函数的函数签名与其参数一起编码到内存中。众所周知，solidity 不会清除或重用内存，因此它必须将这些数据存储在下一个可用内存指针中，这会进一步扩展内存。使用内联汇编，如果函数参数在内存中占用的字节数不超过 96 个，我们可以使用临时空间和可用内存指针偏移量来存储此数据（如上所述）。更好的是，如果我们进行多个外部调用，我们可以重用与第一个调用相同的内存空间来在内存中存储新参数，而无需不必要地扩展内存。在这种情况下，Solidity 会将内存扩展至返回数据的长度。这是因为返回的数据存储在内存中（大多数情况下）。如果返回数据小于 96 个字节，我们可以使用临时空间来存储它以防止扩展内存。请参见下面的示例；



```Solidity
contract Called {
    function add(uint256 a, uint256 b) external pure returns(uint256) {
        return a + b;
    }
 }
contract Solidity {
    // cost: 7262
    function call(address calledAddress) external pure returns(uint256) {
        Called called = Called(calledAddress);
        uint256 res1 = called.add(1, 2);
        uint256 res2 = called.add(3, 4);
        uint256 res = res1 + res2;
        return res;
    }
 }
contract Assembly {
    // cost: 5281
    function call(address calledAddress) external view returns(uint256) {
        assembly {
            // check that calledAddress has code deployed to it
            if iszero(extcodesize(calledAddress)) {
                revert(0x00, 0x00)
            }
            // first call
            mstore(0x00, hex"771602f7")
            mstore(0x04, 0x01)
            mstore(0x24, 0x02)
            let success := staticcall(gas(), calledAddress, 0x00, 0x44, 0x60, 0x20)
            if iszero(success) {
                revert(0x00, 0x00)
            }
            let res1 := mload(0x60)
            // second call
            mstore(0x04, 0x03)
            mstore(0x24, 0x4)
            success := staticcall(gas(), calledAddress, 0x00, 0x44, 0x60, 0x20)
            if iszero(success) {
                revert(0x00, 0x00)
            }
            let res2 := mload(0x60)
            // add results
            let res := add(res1, res2)
            // return data
            mstore(0x60, res)
            return(0x60, 0x20)
        }
    }
 }
```



我们通过使用临时空间来存储函数选择器及其参数，并对第二次调用重用相同的内存空间，同时将返回的数据存储在零槽中，从而无需扩展内存，从而节省了gas。如果您要调用的外部函数的参数超过 64 字节，并且您正在进行一次外部调用，那么用汇编语言编写它不会节省任何显著的 gas。但是，如果进行多次调用。您仍然可以通过使用内联汇编对两次调用重用相同的内存槽来节省 gas。注意：如果空闲内存指针指向的偏移量已被使用，请务必记住更新它，以避免 solidity 覆盖存储在那里的数据或以意外的方式使用存储在那里的值。还要注意，如果该调用堆栈中有未定义的动态内存值，则避免覆盖零槽（0x60 内存偏移量）。另一种方法是显式定义动态内存值，或者如果使用，则在退出汇编块之前将槽设置回 0x00。  

### 测试

**文件位置：**

```Bash
src/assembly/MemoryExp.sol
test/assembly/MemoryExp.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_memexp_calls_ -vvv --optimize
```



![内存优化：多个外部调用图示](/images/gas-optimization-master/assembly/05-multiple-external-calls-01.png)



### 总结

## 对应源码

- [`src/assembly/MemoryExp.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/assembly/MemoryExp.sol)
- [`test/assembly/MemoryExp.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/assembly/MemoryExp.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
