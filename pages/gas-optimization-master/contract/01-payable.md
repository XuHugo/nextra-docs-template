# payable

## 分析

1. 构造函数

将构造函数设置为可支付函数，在部署时节省了 200 Gas。这是因为不可支付函数require\(msg\.value == 0\)中隐式插入了指令。此外，部署时字节码越少，调用数据就越少，Gas 成本也就越低。将常规函数设置为不可支付函数固然有其道理，但通常情况下，合约是由特权地址部署的，你可以合理地假设该地址不会发送 Ether。但如果是经验不足的用户部署合约，这可能就不适用了。 

2. 高级权限函数

我们可以将管理员特定的函数设置为可支付函数，以节省 Gas，因为编译器不会检查函数的调用值。由于创建和运行时代码中的操作码更少，这也能使合约更小、部署更便宜。  

## 测试



**文件位置：**

```Bash
src/contract/Payable.sol
test/contract/Payable.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_payable_ -vvv --optimize
```

![payable图示](/images/gas-optimization-master/contract/01-payable-01.png)



## 总结

虽然 Solidity 的`payable`修饰符主要用于支持将 Ether 转账到函数，但它也可以用于优化函数（这些函数可恢复为标准用户）的 Gas 成本。通过了解底层操作码及其 Gas 成本，开发者可以利用这一点，在不牺牲安全性的情况下创建更高效的智能合约。

## 对应源码

- [`src/contract/Payable.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Payable.sol)
- [`test/contract/Payable.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Payable.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
