# 继承

## 分析

在 Solidity 中，使用继承通常比组合更简单，也更节省 Gas。通过继承扩展合约时，子合约可以高效地将其变量与父合约的变量打包在一起。

**注意顺序**：变量的顺序由[C3 线性化](https://en.wikipedia.org/wiki/C3_linearization)确定。您只需知道子变量位于父变量之后即可。这可以提高存储打包效率，而这正是优化 Gas 使用的关键。

1. 继承 vs 组合的基本概念

继承（Inheritance）

```Solidity
contract Parent {
    uint128 parentVar1;
    uint128 parentVar2;
}

contract Child is Parent {
    uint128 childVar1;
    uint128 childVar2;
}
```

组合（Composition）

```Solidity
contract Parent {
    uint128 parentVar1;
    uint128 parentVar2;
}

contract Child {
    Parent public parent;
    uint128 childVar1;
    uint128 childVar2;
}
```

2. 存储布局的差异

继承的存储布局

```Solidity
存储槽 0: [parentVar1(128位)] [parentVar2(128位)]
存储槽 1: [childVar1(128位)]  [childVar2(128位)]
```

- 所有变量在同一个合约的存储空间中

- 可以实现跨父子类的变量打包

- 总共使用 2 个存储槽

组合的存储布局

Child 合约:

```Solidity
存储槽 0: [parent合约地址(160位)] [未使用(96位)]
存储槽 1: [childVar1(128位)] [childVar2(128位)]
```

Parent 合约（独立存储）:

```Solidity
存储槽 0: [parentVar1(128位)] [parentVar2(128位)]
```

- 需要额外存储父合约的地址

- 无法跨合约进行变量打包

- 访问父合约变量需要额外的外部调用

## 测试

**文件位置：**

```Bash
src/contract/Inheritance.sol
test/contract/Inheritance.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_inheritance_ -vvv --optimize
```

![继承图示](/images/gas-optimization-master/contract/16-inheritance-01.png)





**查看存储结构：**

```Bash
forge inspect InheritanceChild  storageLayout
forge inspect CompositionChild  storageLayout
```

![继承图示 2](/images/gas-optimization-master/contract/16-inheritance-02.png)

![继承图示 3](/images/gas-optimization-master/contract/16-inheritance-03.png)



||**继承**|**组合**|
|---|---|---|
|**存储成本**|变量共享存储空间，可以打包|需要额外存储父合约地址，无法打包|
|**访问成本**|直接内存/存储访问|需要外部合约调用|
|**部署成本**|单个合约，代码可能更大但只部署一次|需要部署多个合约|

## 总结

- 优先使用继承的场景

    - 需要频繁访问父合约的状态变量

    - 希望最大化存储打包效率

    - 父子关系紧密，逻辑高度相关

- 考虑使用组合的场景

    - 需要运行时更换依赖合约

    - 父合约可能被多个子合约共享

    - 需要更灵活的架构设计

## 对应源码

- [`src/contract/Inheritance.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/Inheritance.sol)
- [`test/contract/Inheritance.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/Inheritance.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
