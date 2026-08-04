# 使用 constant 和 immutable

## 分析

在 Solidity 中，不打算更新的变量应该是常量或不可变的。这是因为常量和不可变值直接嵌入到定义它们的合约的字节码中，因此不占用存储空间。在 Solidity 中，存在 constant 和 immutable 两种常量声明方案。两者的区别如下:

- constant 在 solidity 编译过程中就被写入字节码 

- immutable 在 solidity 合约部署过程中被写入字节码，所以我们可以在构造器 constructor 内对其进行赋值  

上述两个关键词都是直接将变量打包进入字节码，我们可以使用 CODECOPY 操作码直接访问使用 constant 或 immutable 定义的常量。而 CODECOPY 操作码只需要固定的 3 gas，相比于访问存储槽，直接访问常量显然更加便宜的。  

但需要注意，天下没有免费的午餐。运行时更低成本的 gas 对应着部署时的合约体积增加，我们需要消耗更多的 gas 以部署合约。但一般来说，合约部署时多消耗的 gas 远小于用户多次交互时消耗的 gas，所以我建议任何开发者都在使用常量时进行此优化。

constant 和 immutable 的访问成本几乎完全相同。区别在于，`constant` 的值被复制到了每一个使用它的地方。如果一个 constant 的值很大（比如一个很长的string），并且在多个函数中被使用，那么这个大的数据就会在字节码中被复制多份。

而 immutable 的值，无论多大，都只在合约的字节码中存储一次。当访问它时，EVM 只是从代码的那个固定位置加载它。

## 测试

**文件位置：**

```Bash
src/storage/Constants.sol
test/storage/Constants.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_pack_ -vvv --optimize
```

![使用 constant 和 immutable图示](/images/gas-optimization-master/storage/06-constants-and-immutables-01.png)

## 总结

- 因为 immutable 的值在字节码中只存在一份，访问它只是一个简单的加载。而 constant的值会被复制到所有使用它的地方，如果值很大且被多次使用，可能会导致字节码膨胀，从而产生轻微的额外开销。

- 由于`constant`变量不是编译字节码中的真正常量，因此它们不能在某些常量环境（如汇编或其他库）中被引用。

## 对应源码

- [`src/storage/Constants.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/storage/Constants.sol)
- [`test/storage/Constants.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/storage/Constants.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
