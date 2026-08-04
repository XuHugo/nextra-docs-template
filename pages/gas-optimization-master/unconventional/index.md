# 非常规技巧

实验性较强的优化方法，以及它们的适用边界和风险。

如果您正在参加气体优化竞赛，那么这些不寻常的设计模式可能会有所帮助，但强烈不建议在生产中使用它们，或者至少应该极其谨慎地进行。  


```Solidity
for (uint256 i; i < limit; ) {
    // inside the loop
    unchecked {
        ++i;
    }
 }
```

## 文章目录

1. [使用 gasprice() 或 msg.value 传递信息](./01-gasprice-msgvalue-data)
2. [使用 gasleft() 在关键点进行分支决策](./02-gasleft-branching)
3. [将函数设为 Payable](./03-payable-functions)
4. [外部库跳转](./04-external-library-jumps)
5. [将字节码附加到合约末尾](./05-append-bytecode)
