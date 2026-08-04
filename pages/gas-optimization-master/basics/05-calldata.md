# Calldata

`calldata` 区域用于存储来自用户或者其他合约的请求参数，该区域的内容是不可变的，我们可以通过 `CALLDATALOAD` 操作码在此区域内读取数据至栈内，也可以通过使用 `CALLDATACOPY` 操作码将一定长度的数据读取到内存内部。其中，`CALLDATALOAD` 操作码消耗固定的 3 gas，而 `CALLDATACOPY` 操作码则根据复制的 `calldata` 长度与写入到内存的位置\(`offset`\)决定 gas 消耗。



## CALLDATALOAD

从 calldata 中读取一个 32 字节（一个字）的数据。

```Python
*def* calldataload(*evm*: Evm) -> None:
        # GAS
        charge_gas(evm, GAS_VERY_LOW)
```

- 行为: 它会从 calldata\[position : position\+32\] 读取数据。如果读取范围超出了 calldata 的边界，超出的部分会用零来填充，最终总是返回一个 32 字节的值。

- Gas 成本: 非常低，是一个固定的少量 Gas（3 Gas）。



## CALLDATACOPY

将 calldata 中的一部分数据复制到 EVM 的内存 \(memory\) 中。

```Python
# GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = GAS_COPY * words
    extend_memory = calculate_gas_extend_memory(
        evm.memory, [(memory_start_index, size)]
    )
    charge_gas(evm, GAS_VERY_LOW + copy_gas_cost + extend_memory.cost)
```

Gas 成本: 这个操作的成本由两部分组成：

1. 复制成本: 与复制的数据量（按字计算）成正比。

2. 内存扩展成本: 如果向内存写入数据导致内存需要扩展，就会产生额外的成本。这个成本与内存大小的平方成正比，可能会变得非常昂贵。



## 总结

将 `calldata` 视为廉价的只读存储，在进行 Gas 优化时，可以将 calldata 看作是一个可以通过偏移量直接访问的、廉价的只读数据源。当处理复杂数据结构时，最佳实践是：

- 按需读取：计算出所需数据在 calldata 中的偏移量，然后使用 calldataload 直接读取，而不是先把整个结构体复制到内存。

- 仅在必要时复制：只在需要修改数据，或者需要对数据进行大量、无序的随机访问时，才考虑使用 calldatacopy 将其复制到内存。

## 对应源码

- [Gas Optimization Master 配套代码](https://github.com/XuHugo/gas_optimization_master/tree/8960383)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
