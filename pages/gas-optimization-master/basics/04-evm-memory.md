# Memory

内存是 EVM 中一个至关重要但又经常被误解的概念。与永久的“存储 \(Storage\)”不同，内存是**易失的 \(volatile\)**，其生命周期仅限于单次交易执行期间。它主要用于暂存数据、拼接字节码、以及作为合约间调用时传递参数的临时区域。

理解内存的工作方式，特别是其**动态扩展机制**和与之关联的 **Gas 成本**，对于编写高效、低成本的智能合约至关重要。本文档将重点分析这些指令背后的 Gas 消耗模型。

## EVM 内存核心概念

- **易失性**: 每次交易开始时，内存都是一块干净的、全为零的区域。交易结束后，内存中的所有内容都会被丢弃。

- **线性结构**: 内存可以被看作一个非常大的、可按字节寻址的字节数组。

- **32 字节为单位**: 虽然可以按字节寻址，但 EVM 的操作（读/写）通常以 32 字节的“字 \(word\)”为单位进行。

- **动态扩展**: 内存可以根据需要动态扩展。当你尝试读取或写入一个超出当前内存大小的地址时，EVM 会自动将内存扩展到足够容纳该操作的大小。这是 Gas 成本的主要来源。



## calculate_gas_extend_memory: 内存的二次方成本陷阱

EVM 中 Gas 成本最需要注意的部分之一就是内存扩展的成本。这个成本**不是线性的**，而是**二次方增长**的。

Gas 成本的计算公式基于内存大小（以 **word** 为单位，1 word = 32 bytes）。

`calculate_gas_extend_memory`这个函数用于计算扩展 EVM 内存以容纳新数据所需的 gas 成本。代码中 `before_size` 值为我们写入前内存已被使用的长度，`after_size` 为我们写入后内存被使用的长度。我们可以看到内存占用成本实际上只对两次的差值收取 gas。

```Python
*def* calculate_gas_extend_memory(
    *memory*: *bytearray*, *extensions*: List[Tuple[U256, U256]]
) -> ExtendMemory:

        ...     
        before_size = ceil32(current_size)
        after_size = ceil32(Uint(start_position) + Uint(size))
        if after_size <= before_size:
            continue

        size_to_extend += after_size - before_size
        already_paid = calculate_memory_gas_cost(before_size)
        total_cost = calculate_memory_gas_cost(after_size)
        to_be_paid += total_cost - already_paid
        ...
```



`calculate_gas_extend_memory` 函数负责计算这一成本。它会检查一个操作需要访问的所有内存范围，确定最终需要的内存大小，然后计算出需要支付的额外 Gas。

```Python
*def* calculate_memory_gas_cost(*size_in_bytes*: Uint) -> Uint:
    size_in_words = ceil32(size_in_bytes) // Uint(32)
    #  **线性成本**: 每扩展一个 word (32字节)，支付 3 Gas。
    linear_cost = size_in_words * GAS_MEMORY
    #  **二次方成本**: 成本随着内存大小的平方增长。
    quadratic_cost = size_in_words ** Uint(2) // Uint(512)
    total_gas_cost = linear_cost + quadratic_cost
    return total_gas_cost
```

这个二次方成本模型是为了防止合约滥用内存资源，从而导致节点处理负担过重。



**示例**: 假设我们要写入一个地址，这会触发内存扩展。

- **写入地址 **\`0x10\`** \(16\)**: 内存扩展到 32 字节 \(1 word\)。

    - `linear_cost` = 1 \* 3 = 3

    - `quadratic_cost` = 1\*1 / 512 = 0

    - 总成本 = 3 Gas。

- **写入地址 **\`0x400\`** \(1024\)**: 内存扩展到 1024\+32=1056 字节 \(33 words\)。

    - `linear_cost` = 33 \* 3 = 99

    - `quadratic_cost` = 33\*33 / 512 = 1089 / 512 = 2

    - 总成本 = 101 Gas。

- **写入地址 **\`0x20000\`** \(128KB\)**: 内存扩展到 131072 字节 \(4096 words\)。

    - `linear_cost` = 4096 \* 3 = 12,288

    - `quadratic_cost` = 4096\*4096 / 512 = 32,768

    - 总成本 = 45,056 Gas。

**结论**: 避免在合约中不必要地使用或分配大的内存块，特别是避免跳跃式地访问遥远的内存地址。



## MLOAD: 从内存中读取

`MLOAD` 从内存的指定位置加载一个 32 字节的 word 到堆栈上。

```Python
# STACK
    start_position = pop(evm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        evm.memory, [(start_position, U256(32))]
    )
    charge_gas(evm, GAS_VERY_LOW + extend_memory.cost)
```

**EVM 操作**

1. 从堆栈弹出一个 `start_position`（起始地址）。

2\.  **计算 Gas**:

- 支付 `GAS_VERY_LOW` \(3 Gas\) 的基础费用。

- 计算内存扩展成本。如果 `start_position + 32` 大于当前的内存大小，EVM 会扩展内存，并收取相应的 `extend_memory.cost`。

2. 执行操作：

    - 如果需要，用 `0x00` 字节填充以扩展内存。

    - 从 `start_position` 读取 32 字节数据。

    - 将读取到的值推入堆栈。

**Gas 成本分析**

- **基础成本**: 3 Gas \(\`GAS\_VERY\_LOW\`\)。

- **动态成本 \(内存扩展\)**: 如果读取操作越过了当前内存的边界，则需要支付二次方增长的扩展费用。

## MSTORE: 写入内存

`MSTORE` 将一个 32 字节的 word 写入内存，而 `MSTORE8` 只写入一个字节。

```Python
# STACK
    start_position = pop(evm.stack)
    value = pop(evm.stack).to_be_bytes32()

    # GAS
    extend_memory = calculate_gas_extend_memory(
        evm.memory, [(start_position, U256(len(value)))]
    )

    charge_gas(evm, GAS_VERY_LOW + extend_memory.cost)
```

**EVM 操作**

1. 从堆栈弹出 `start_position` 和 `value`。

2\.  **计算 Gas**:

- 支付 `GAS_VERY_LOW` \(3 Gas\) 的基础费用。

- 计算内存扩展成本。如果 `start_position + 32` \(对于 `MSTORE`\) 或 `start_position + 1` \(对于 `MSTORE8`\) 超出内存边界，则支付扩展费用。

2. 执行操作：

    - 扩展内存。

    - 将 `value` 写入内存的 `start_position`。对于 `MSTORE8`，只会写入 `value` 的最低有效字节。

**Gas 成本分析**

- **基础成本**: 3 Gas \(\`GAS\_VERY\_LOW\`\)。

- **动态成本 \(内存扩展\)**: 与 \`MLOAD\` 相同，这是主要成本来源。



## MCOPY: 在内存中复制数据

`MCOPY` \(EIP\-3\) 是一个较新的指令，用于在内存中高效地复制数据，取代了过去需要循环 `MLOAD`/`MSTORE` 的昂贵操作。

```Python
# STACK
    start_position = pop(evm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        evm.memory, [(start_position, U256(32))]
    )
    charge_gas(evm, GAS_VERY_LOW + extend_memory.cost)
```

**EVM 操作**

1. 从堆栈弹出 `destination`, `source`, 和 `length`。

2\.  **计算 Gas**:

- 支付 `GAS_VERY_LOW` \(3 Gas\) 的基础费用。

- **复制成本**: \`GAS\_COPY \* words\`，其中 \`words\` 是需要复制的 word 数量 \(\`ceil32\(length\) / 32\`\)。\`GAS\_COPY\` 是 3 Gas。所以每复制 32 字节，成本为 3 Gas。

- **内存扩展成本**: 这是最复杂的部分。EVM 需要确保**源区域** \(\`source\` 到 \`source \+ length\`\) 和**目标区域** \(\`destination\` 到 \`destination \+ length\`\) 都在内存范围内。它会计算这两个区域所需的最大内存，并一次性扩展到位，收取相应的 \`extend\_memory\.cost\`。

2. 执行操作：

    - 扩展内存。

    - 从 `source` 读取 `length` 字节的数据，然后将其写入 `destination`。

**Gas 成本分析**

- **基础成本**: 3 Gas \(\`GAS\_VERY\_LOW\`\)。

- **动态成本 \(复制\)**: \`3 \* \(ceil32\(length\) / 32\)\` Gas。与复制的数据量成线性关系。

- **动态成本 \(内存扩展\)**: 二次方增长的成本，取决于 \`source \+ length\` 和 \`destination \+ length\` 中的最大值。





|指令|基础 Gas|动态 Gas \(主要来源\)|
|---|---|---|

\| **MLOAD** \| 3 \| 内存扩展 \(二次方\) \|

\| **MSTORE** \| 3 \| 内存扩展 \(二次方\) \|

\| **MSTORE8** \| 3 \| 内存扩展 \(二次方\) \|

\| **MSIZE** \| 2 \| 无 \|

\| **MCOPY** \| 3 \| 内存扩展 \(二次方\) \+ 复制成本 \(线性\) \|



**最佳实践**:



1\.  **警惕内存的二次方成本**: 避免在单个交易中分配和使用大量内存（例如，处理巨大的数组或字符串）。

2\.  **紧凑使用内存**: 尽可能地连续使用内存地址，避免跳跃式地写入很远的地址，因为这会立即触发高昂的扩展成本。

3\.  **\*\*优先使用 **\`MCOPY\`**\*\***: 当需要在内存中移动数据时，\`MCOPY\` 远比手动的 \`MLOAD\`/\`MSTORE\` 循环便宜。

4\.  **理解 Solidity 的内存管理**: Solidity 会自动管理内存，通常将新变量放在“空闲内存指针” \(free memory pointer\) 之后。了解这一点有助于在 \`assembly\` 块中安全地操作内存。

## 对应源码

- [Gas Optimization Master 配套代码](https://github.com/XuHugo/gas_optimization_master/tree/8960383)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
