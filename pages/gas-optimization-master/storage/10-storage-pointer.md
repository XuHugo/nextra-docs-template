# 使用存储指针代替内存

## 分析

在 Solidity 中，存储指针是指向合约存储位置的变量。它们与 C/C\+\+ 等语言中的指针并不完全相同。了解如何有效地使用存储指针有助于避免不必要的存储读取，并执行节省 gas 的存储更新。以下示例展示了存储指针的用途。

```Solidity
contract UnPointer {
    struct User {
        uint256 id;
        string name;
        uint256 lastSeen;
    }

    constructor() {
        users[0] = User(0, "John Doe", block.timestamp);
    }

    mapping(uint256 => User) public users;

    function calls(uint256 *_id*) public view returns (uint256) {
        User memory _user = users[_id];
        uint256 lastSeen = block.timestamp - _user.lastSeen;
        return lastSeen;
    }
}
```

上面我们有一个函数，它返回用户在给定索引处的最后上线时间。它获取 lastSeen 值，并从当前 block\.timestamp 中减去该值。然后，我们将整个结构体复制到内存中，并获取 lastSeen 值，用于计算秒前的最后上线时间。这种方法效果很好，但效率不高，因为我们将整个结构体从存储复制到内存中，包括我们不需要的变量。如果能有一种方法可以只从 lastSeen 存储槽读取数据（无需汇编），那就更好了。这时，存储指针就派上用场了。

```Solidity
// This results in approximately 5,000 gas savings compared to the previous version.
contract Pointer {
    struct User {
        uint256 id;
        string name;
        uint256 lastSeen;
    }

    constructor() {
        users[0] = User(0, "John Doe", block.timestamp);
    }

    mapping(uint256 => User) public users;

    function calls(uint256 *_id*) public view returns (uint256) {
        User storage _user = users[_id]; 
        uint256 lastSeen = block.timestamp - _user.lastSeen;
        return lastSeen;
    }
}
```

这里唯一的变化是将内存改为存储，而我们被告知任何存储都是昂贵的，应该避免？在这里，我们将users\[\_id\]的存储指针存储在堆栈上的固定大小变量中（结构体的指针基本上是结构体开头的存储槽，在本例中，这将是的存储槽user\[\_id\]\.id）。由于存储指针是惰性的（意味着它们只在被调用或引用时才起作用（读或写）。接下来，我们只访问结构体的 lastSeen 键。这样，我们只需进行一次存储加载，然后将其存储在堆栈上，而不是进多次存储加载和内存存储，然后再从内存中取出一小块到堆栈上。

## 测试

**文件位置：**

```Bash
src/storage/Pointer.sol
test/storage/Pointer.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_pointer_ -vvv --optimize
```

![使用存储指针代替内存图示](/images/gas-optimization-master/storage/10-storage-pointer-01.png)



## 总结

- **识别**：检查您的合约函数，特别是那些对数组或映射中的特定元素有多个引用的函数。

- **修改**：在函数开始时，获取一次存储引用并将其存储在本地存储类型变量中。

- **重构**：用本地存储类型变量替换所有后续访问。

## 对应源码

- [`src/storage/Pointer.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Pointer.sol)
- [`test/storage/Pointer.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Pointer.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
