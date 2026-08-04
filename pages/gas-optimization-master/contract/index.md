# 合约优化

从部署、调用、错误处理和架构选择优化合约成本。

在设计智能合约时，需要牢记以下几点以优化 gas：

- a\) 避免不必要的状态变量修改：不必要的状态变量修改可能会导致额外的 Gas 成本。除非绝对必要，否则尽量减少状态更改，并在适当的情况下考虑使用局部变量。

- b\) 删除未使用或冗余的代码：未使用或冗余的代码会增加合约的大小，并可能导致更高的 Gas 消耗。定期检查你的合约，删除任何不必要或重复的代码段。

- c\) 使用修饰符代替重复的代码模式：如果您发现在多个函数中重复了代码模式，请考虑使用修饰符。修饰符允许您一次定义一段代码，并将其应用于多个函数，从而减少重复和 Gas 成本。

- d\) 最小化合约所需的存储空间：存储操作比内存操作更昂贵。设计合约时，尽可能利用局部变量和临时存储来最小化所需的存储空间。

## 文章目录

1. [payable](./01-payable)
2. [预测合约地址的妙用](./02-predict-contract-addresses)
3. [优化合约元数据](./03-contract-metadata)
4. [临时合约中使用 selfdestruct](./04-selfdestruct-temporary-contracts)
5. [内部函数和修饰符](./05-internal-functions-and-modifiers)
6. [待验证：修改器中使用内部视图函数](./06-modifier-view-functions)
7. [使用克隆合约](./07-clones)
8. [使用单体架构](./08-monolithic-architecture)
9. [选择 Gas 优化库](./09-gas-optimized-libraries)
10. [转账时使用 fallback 或 receive](./10-fallback-and-receive)
11. [使用 EIP2930 预热存储槽](./11-eip2930-access-lists)
12. [使用自定义错误](./12-custom-errors)
13. [使用现有的 create2 工厂](./13-existing-create2-factory)
14. [Solidity 0.8+ 不再需要 SafeMath](./14-safemath)
15. [external 与 public](./15-external-vs-public)
16. [继承](./16-inheritance)
17. [使用钩子转移代币](./17-token-transfer-hooks)
18. [仅使用一次的内部函数可以内联](./18-inline-single-use-functions)
