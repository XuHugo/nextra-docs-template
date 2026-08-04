# 字符串尽量小于32个字节

## 分析

在 Solidity 中，字符串是可变长度的动态数据类型，这意味着它们的长度可以根据需要变化和增长。如果字符串长度为 32 字节或更长，则定义它们的槽位会存储的长度len\(string\) \* 2 \+ 1，而其实际数据存储在其他位置（即该槽位的 keccak 哈希值）。但是，如果字符串小于 32 字节，则len\(string\) \* 2存储在其存储槽位的最低有效字节中，而字符串的实际数据则从定义它的槽位的最高有效字节开始存储。

也就是说，有区分短字符串（short string）和 长字符串（long string），而最低位的最后一位bit（0/1）用来区分是短/长字符串。这样解码时可以快速判断是短字符串还是长字符串，也可以还原出实际长度。



`bytes32`Solidity 中的和之间的选择`string`会影响 gas 消耗，因为它们处理数据存储的方式不同：

- **bytes32**：一种固定大小的数据类型，无论内容长度多少，都恰好占用 32 个字节。由于`bytes32`长度固定，因此无需额外空间来存储数据长度，从而简化了合约的存储需求。在以太坊智能合约中，存储操作成本高昂，但`bytes32`通过将其紧凑地装入 EVM 的单个存储槽（恰好为 32 字节）来优化存储成本。这种配置允许高效的读写操作，从而最大限度地降低 Gas 成本。

- **字符串**：一种动态大小的数据类型，每次存储时都需要额外的存储空间来存储长度信息。这种动态特性带来了复杂性，因为它`string`通常占用多个存储空间，尤其是在超过 32 个字节时。管理这些动态数组会增加定位数据起点和终点的计算需求，从而导致更高的 Gas 消耗。



如果需要极致的优化，还可以使用使用汇编语言调用，也是非常有效的。

```Solidity
// SPDX-License-Identifier: MIT
 pragma solidity 0.8.22;
 contract EfficientString {
    bytes32 shortString;
function getShortString() external view returns(string memory) {
        string memory value;
assembly {
            // get slot 0
            let slot0Value := sload(shortString.slot)
            
            // to get the byte that holds the length info, we mask it to rmove the string and divide it by 2 to get the length
            let len := div(and(slot0Value, 0xff), 2)
// to get string, we mask the slot value to remove the length// we are sure that it can't take more than a byte because of the length check in the `storeShortString` function
            let str := and(slot0Value, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00)
            
            // store length in memory
            mstore(0x80, len)
            
            // store string in memory
            mstore(0xa0, str)
// make `value` reference 0x80 so that solidity does the returning for us
            value := 0x80// update the free memory pointer
            mstore(0x40, 0xc0)
        }
return value;
    }
function storeShortString(string calldata value) external {
        assembly {
            // require that the length is less than 32
            if gt(value.length, 31) {
                revert(0, 0)
            }
// multiply the length, so we can store length*2 following solidity's convention
            let length := mul(value.length, 2)
// get the string itself
            let str := calldataload(value.offset)
// or the length and str to get what we need to store in storage
            let toBeStored := or(str, length)
// store it in storage
            sstore(shortString.slot, toBeStored)
        }
    }
 }
 
```

这个合约 EfficientString 的核心目的是高效地存储和读取长度小于32字节的字符串，并且通过手动实现的编码方式将字符串及其长度都压缩进一个 32 字节（bytes32）的存储槽里。

**setString\(string calldata value\)  **

- 只允许长度小于 32 字节（严格来说是小于 32，即最多 31 字节，见 if gt\(value\.length, 31\)）。  

- 通过 calldataload 直接把 calldata 的字符串内容读出来。  

- 自己手动编码：高字节区域存放字符串内容（最多 31 字节）。\*\*低字节（最低的1个字节）\*\*存放字符串长度的“2倍”。

- 然后用 or 把两部分拼在一起，整体存进 shortString 的 storage 槽。

**getString\(\)**

- 读取 storage 槽内容，拆分出字符串和长度。

- 低字节部分（最低1字节）存的是 len\*2，需要还原回长度。

- 字符串内容存储在高位部分（slot value去掉低一字节，即 and\(slot0Value, 0xffff\.\.\.ff00\)）。

- 手动在内存分配字符串格式，返回字符串。

使用汇编的优势

- 更高效：可以直接操作存储槽、内存、calldata，省去 Solidity 运行时的各种边界检查和中间变量消耗，节省 gas。

- 自定义编码：允许你用自己的方式打包数据（如本例中自己决定如何编码字符串和长度）。

- 极限优化：可以省略一些安全检查和冗余操作，做到极致紧凑。

## 测试

**文件位置：**

```Bash
src/storage/StringShort.sol
test/storage/StringShort.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_str_31(32\asm) -vvv --optimize
```



![字符串尽量小于32个字节图示](/images/gas-optimization-master/storage/05-short-strings-01.png)



![字符串尽量小于32个字节图示 2](/images/gas-optimization-master/storage/05-short-strings-02.png)





![字符串尽量小于32个字节图示 3](/images/gas-optimization-master/storage/05-short-strings-03.png)



## 总结

- 长度乘以2是为了兼容 Solidity 的 packed storage encoding 规范（低位1bit为类型标记）。

- 存储一个31字节的字符串时，Solidity自带方法和汇编优化版本都只需要1个slot；但汇编版本让你完全掌控打包方式，适合特殊优化需求。

- 汇编带来极致效率和灵活性，但开发复杂、风险高；常规写法安全易用但 gas 成本更高。

- 在 Solidity 中，字符串（`string` 或 `bytes` 类型）如果长度小于等于 32 字节，会被更高效地存储在内存和存储中\.

## 对应源码

- [`src/storage/StringShort.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/StringShort.sol)
- [`test/storage/StringShort.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/StringShort.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
