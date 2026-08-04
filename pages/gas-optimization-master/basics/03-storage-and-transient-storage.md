# Storage 与 Transient Storage

## 简介：两种存储

在 EVM 中，智能合约有两种主要的数据存储区域：

**持久化存储 \(Storage\)**

这是我们通常所说的“状态”。它是一个键值对映射（key\-value store），将 32 字节的键映射到 32 字节的值。

- **持久性**: 数据永久保存在以太坊区块链上，除非被合约逻辑修改。

- **高成本**: 读写操作非常昂贵，因为它们会改变区块链的状态，需要所有节点达成共识。

- **指令**: \`SLOAD\` 和 \`SSTORE\`

**瞬时存储 \(Transient Storage\)**

这是由 [EIP\-1153](https://eips.ethereum.org/EIPS/eip-1153) 引入的新概念。它也是一个键值对映射，但其生命周期仅限于单次交易。

- **瞬时性**: 数据在交易开始时为空，在交易结束时被丢弃。它不会永久改变区块链状态。

- **低成本**: 读写操作比持久化存储便宜得多，因为它不涉及永久的状态变更。

- **用途**: 主要用于在同一次交易内的不同合约调用之间传递状态，而无需昂贵地使用持久化存储。例如，在复杂的 DeFi 协议中用于“重入锁”或传递手续费信息。

- **指令**: \`TLOAD\` 和 \`TSTORE\`



## SLOAD: 从持久化存储中读取

`SLOAD` 指令用于从合约的持久化存储中加载一个值到堆栈上。

```Python
# STACK 从堆栈 (Stack) 弹出一个 32 字节的 key。
    key = pop(evm.stack).to_be_bytes32()

    # GAS 计算 Gas 费用
    if (evm.message.current_target, key) in evm.accessed_storage_keys:
        charge_gas(evm, GAS_WARM_ACCESS)
    else:
        evm.accessed_storage_keys.add((evm.message.current_target, key))
        charge_gas(evm, GAS_COLD_SLOAD)

    # OPERATION 从当前合约的存储中，读取 key 对应的 value
    value = get_storage(
        evm.message.block_env.state, evm.message.current_target, key
    )
```

**Gas 成本：冷热访问 \(Cold vs\. Warm Access\)**

为了防止拒绝服务攻击 \(DoS\)，EVM 对首次访问某个存储槽（slot）的操作收取更高的费用。

**冷访问 \(Cold Access\)**: 在一笔交易中，**第一次**访问某个账户的某个存储 \`key\`。

- Gas 成本: `GAS_COLD_SLOAD` \(2100 Gas\)

- 代码中，通过检查 `evm.accessed_storage_keys` 集合来判断。如果 `(address, key)` 不在该集合中，就是冷访问。访问后，该键会被添加到集合中。

**热访问 \(Warm Access\)**: 在同一笔交易中，对一个已经访问过的存储 \`key\` 进行**再次**访问。

- Gas 成本: `GAS_WARM_ACCESS` \(100 Gas\)

- 因为节点已经加载过这个数据，所以后续访问的成本要低得多。



## SSTORE: 写入持久化存储

`SSTORE` 是最复杂的操作之一，因为它直接修改区块链状态，并且有复杂的 Gas 计费和退款机制。

```Python
if (evm.message.current_target, key) not in evm.accessed_storage_keys:
    evm.accessed_storage_keys.add((evm.message.current_target, key))
    gas_cost += GAS_COLD_SLOAD

if original_value == current_value and current_value != new_value:
    if original_value == 0:
        gas_cost += GAS_STORAGE_SET
    else:
        gas_cost += GAS_STORAGE_UPDATE - GAS_COLD_SLOAD
else:
    gas_cost += GAS_WARM_ACCESS

# Refund Counter Calculation
if current_value != new_value:
    if original_value != 0 and current_value != 0 and new_value == 0:
        # Storage is cleared for the first time in the transaction
        evm.refund_counter += *int*(GAS_STORAGE_CLEAR_REFUND)

    if original_value != 0 and current_value == 0:
        # Gas refund issued earlier to be reversed
        evm.refund_counter -= *int*(GAS_STORAGE_CLEAR_REFUND)

    if original_value == new_value:
        # Storage slot being restored to its original value
        if original_value == 0:
            # Slot was originally empty and was SET earlier
            evm.refund_counter += *int*(GAS_STORAGE_SET - GAS_WARM_ACCESS)
        else:
            # Slot was originally non-empty and was UPDATED earlier
            evm.refund_counter += *int*(
                GAS_STORAGE_UPDATE - GAS_COLD_SLOAD - GAS_WARM_ACCESS
            )

```

**Gas 成本：复杂的计费与退款机制**

`SSTORE` 的 Gas 成本取决于多种因素：

**访问成本**:

- 冷访问: 2100 Gas \(`GAS_COLD_SLOAD`\)

- 热访问: 100 Gas \(`GAS_WARM_ACCESS`\)

**写入成本**:

- **创建 \(Set\)**: 当一个值为 `0` 的存储槽被设置为**非 **`0`** **值时。

    - 成本: 20,000 Gas \(`GAS_STORAGE_SET`\)

- **更新 \(Update\)**: 当一个**非 **`0`值的存储槽被设置为另一个**非 **`0` 值时。

    - 成本: 2,900 Gas \(`GAS_STORAGE_UPDATE` \- `GAS_COLD_SLOAD`\)

    *也就是说，SSTORE 的写入成本已经包含了一次热访问的成本，如果你已经为冷访问付了 2100 gas，就不应该再全额收取 5000 gas，否则会重复计费。*

**Gas 退款 \(Refund\)**:

- 为了鼓励良好的状态管理（清理不再使用的存储），EVM 会提供 Gas 退款。

- **清理 \(Clear\)**: 当一个**非 **`0` 值的存储槽被设置为 `0` 时，会获得 4,800 Gas 的退款 \(\`GAS\_STORAGE\_CLEAR\_REFUND\`\)。

- 撤销退款（非0 → 0 → 非0），如果 slot 原来是非0，现在是0（说明之前已经清理过），但你又把它写回非0，然后又写回0。效果：撤销之前的退款，防止你通过反复写0骗取多次退款。

- 退款在交易结束时统一结算，并且最多只能退还当次交易所用 Gas 的一部分。如果你把 slot 的值改回了交易开始时的原值（即“恢复原状”）。效果：EVM 会返还你之前写入时多收的 gas，因为最终状态没变，相当于没做无用功。

    你在同一笔交易内，对同一个 slot 进行了多次 SSTORE 操作。最终，这个 slot 的值又被“还原”为交易开始时的 original\_value。EVM 规范规定：如果 slot 的最终值和 original\_value 一样，应该退还之前多收的写入 gas（因为最终状态没变，相当于没做无用功）。

    退款时只退“写入部分”，不退“访问部分”

    - 如果原来是0，现在又变回0，返还 GAS\_STORAGE\_SET \- GAS\_WARM\_ACCESS。

    - 如果原来是非0，现在又变回原来的非0，返还 GAS\_STORAGE\_UPDATE \- GAS\_COLD\_SLOAD \- GAS\_WARM\_ACCESS。



## TLOAD: 从瞬时存储中读取

`TLOAD` 用于从瞬时存储中加载一个值到堆栈。

```Python
# STACK 从堆栈弹出一个 32 字节的 key。
    key = pop(evm.stack).to_be_bytes32()

    # GAS 收取固定的 Gas 费用。
    charge_gas(evm, GAS_WARM_ACCESS)

    # OPERATION  从当前交易的瞬时存储中读取 key 对应的 value
    value = get_transient_storage(
        evm.message.tx_env.transient_storage, evm.message.current_target, key
    )
    push(evm.stack, value)
```

**Gas 成本**

`TLOAD` 的成本非常简单，它**不区分冷热访问**。

- Gas 成本: `GAS_WARM_ACCESS` \(100 Gas\)

- 

## TSTORE: 写入瞬时存储

`TSTORE` 用于向瞬时存储写入一个值。

```Python
# STACK  从堆栈弹出 key 和 new_value。
    key = pop(evm.stack).to_be_bytes32()
    new_value = pop(evm.stack)

    # GAS 收取固定的 Gas 费用。
    charge_gas(evm, GAS_WARM_ACCESS)
    if evm.message.is_static:
        raise WriteInStaticContext
    set_transient_storage(
        evm.message.tx_env.transient_storage,
        evm.message.current_target,
        key,
        new_value,
    )
```

**Gas 成本**

与 \`TLOAD\` 类似，\`TSTORE\` 的成本也很简单，**没有退款机制**。

- Gas 成本: `GAS_WARM_ACCESS` \(100 Gas\)

## 总结

|指令|存储类型|主要功能|Gas 成本|关键特性|
|---|---|---|---|---|

\| **SLOAD** \| 持久化 \| 读取数据 \| 2100 \(冷\) / 100 \(热\) \| 区分冷热访问 \|

\| **SSTORE** \| 持久化 \| 写入数据 \| 复杂，依赖值的变化 \| 有复杂的 Gas 计费和退款机制 \|

\| **TLOAD** \| 瞬时 \| 读取数据 \| 100 \(固定\) \| 成本低，数据仅在交易内有效 \|

\| **TSTORE** \| 瞬时 \| 写入数据 \| 100 \(固定\) \| 成本低，无退款，数据仅在交易内有效 \|

## 对应源码

- [Gas Optimization Master 配套代码](https://github.com/XuHugo/gas_optimization_master/tree/8960383)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
