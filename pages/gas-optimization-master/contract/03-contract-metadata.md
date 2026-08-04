# 优化合约元数据

## 分析

[我们已经在智能合约元数据](https://www.rareskills.io/post/solidity-metadata)  Solidity 编译器会将 51 个字节的元数据附加到实际的智能合约代码中。由于每个部署字节需要消耗 200 Gas，因此删除这些字节可能会减少部署成本 10,000 以上。但这并不总是理想的，因为它会影响智能合约验证。相反，开发人员可以挖掘代码注释，使附加的 IPFS 哈希中包含更多零。  

## 测试

**文件位置：**

```Bash
src/contract/Metadatas.sol
test/contract/Metadatas.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_metadata_ -vvv --optimize --no-metadata
```



![优化合约元数据图示](/images/gas-optimization-master/contract/03-contract-metadata-01.png)



![优化合约元数据图示 2](/images/gas-optimization-master/contract/03-contract-metadata-02.png)



## 总结

- **Gas 节省**：每个字节需要 200 Gas，如果 IPFS 哈希包含更多零或禁用元数据，合约的字节数减少，部署 Gas 成本会显著降低（例如 10,000\+ Gas）。

- **影响验证**：虽然删除或优化元数据可以减少部署成本，但它可能会影响合约的 **验证**。如果你需要在区块链浏览器（如 Etherscan）上验证合约代码，删除元数据或调整哈希可能会导致合约无法通过自动验证。

- **更好的平衡**：因此，虽然优化字节数是个有效的节省 Gas 方法，但开发者需要在 **节省 Gas **和 **合约验证 **之间做出平衡。

## 对应源码

- [`src/contract/Metadatas.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Metadatas.sol)
- [`test/contract/Metadatas.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Metadatas.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
