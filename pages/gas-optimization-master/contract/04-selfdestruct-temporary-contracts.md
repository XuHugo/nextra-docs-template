# 临时合约中使用 selfdestruct

## 分析

有时，合约会在一笔交易中部署多个合约，这需要在构造函数中执行。如果合约的唯一用途是构造函数中的代码，那么在操作结束时自毁可以节省 Gas。虽然自毁功能已设置为在即将到来的硬分叉中移除，但根据[EIP 6780](https://eips.ethereum.org/EIPS/eip-6780)的规定，构造函数中仍将支持此功能。  



```Solidity
*contract* Contracts {
    *uint256* *public* value;

    *constructor*(*uint256* *_value*) {
        value = _value;
    }
}

*contract* SelfDestruct {
    *constructor*(*uint256* *_value*) {
        Contracts newContract = new Contracts(_value);

        selfdestruct(*payable*(msg.sender));
    }
}

*contract* SelfDestructNo {
    *constructor*(*uint256* *_value*) {
        Contracts newContract = new Contracts(_value);
    }
}
```



**`selfdestruct`****在构造函数中使用**

1. **部署另一个合约**：在示例中，合约在构造函数中`SelfDestructExample`部署了一个实例。`DeployedContract`

2. **执行所需的操作**：可以执行部署期间需要做的任何操作。

3. **调用****`selfdestruct`**：最后，`selfdestruct`调用该函数从区块链中删除合约，并将任何剩余的 Cfx 返回到部署者的地址。

## 测试

**文件位置：**

```Bash
src/contract/Selfdestruct.sol
test/contract/Selfdestruct.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_selfdestruct_ -vvv --optimize
```



![临时合约中使用 selfdestruct图示](/images/gas-optimization-master/contract/04-selfdestruct-temporary-contracts-01.png)



## 总结

EIP 6780 之后，在合约构造交易中调用：仍保留“立即销毁”的效果（删除代码、清除存储、归零）。在后续交易中调用：仅执行 Ether 转账功能，但 不再删除任何链上状态（不会移除代码或存储）。注意：构造函数之外的销毁行为将不再发生。未来 EVM 会进一步弃用 selfdestruct 相关操作（尤其是在一般交易中），甚至有观点认为它在长期内将会被彻底移除。

## 对应源码

- [`src/contract/Selfdestruct.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Selfdestruct.sol)
- [`test/contract/Selfdestruct.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Selfdestruct.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
