# 条件优化：>= 还是 >

## 分析

EVM 没有用于检查小于等于或大于等于的操作码，所以编译器需要更多指令才能实现这个功能，似乎使用严格不等式 \(\<, \>\)，而不是非严格不等式 \(\<=, \>=\)。例如这种情况下，严格不等式消耗的gas就更少。

```Solidity
function inequality2(uint256 *x*, uint256 *y*) public pure returns (bool) {
        return x >= y;
    }
    function inequality2(uint256 *x*, uint256 *y*) public pure returns (bool) {
        return x > y;
    }
```

查看汇编，发现非严格不等式，会多执行一次iszero操作，所以会多消耗3gas。

![条件优化：>= 还是 >图示](/images/gas-optimization-master/compiler/01-gte-vs-gt-01.png)

有时候情况可能正好相反，**非严格不等式消耗更少 gas**。原因同上，严格不等式操作会多执行一次 `ISZERO`（用来判断反向结果），从而增加额外开销。例如：

```Solidity
function inequality(uint256 *x*, uint256 *y*) public pure returns (uint256) {
        if (y <= x) return 1;
        else return 2;
    }    
    function inequality(uint256 *x*, uint256 *y*) public pure returns (uint256) {
        if (x > y) return 1;
        else return 2;
    }
```

查看汇编

![条件优化：>= 还是 >图示 2](/images/gas-optimization-master/compiler/01-gte-vs-gt-02.png)

实际情况是，你应该尝试两种比较方法，因为使用非严格不等式并不总是能节省 Gas。这很大程度上取决于周围操作码的上下文。

## 测试

**文件位置：**

```Bash
src/compiler/Inequality.sol
test/compiler/Inequality.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_inequality_ -vvv --optimize
```



![条件优化：>= 还是 >图示 3](/images/gas-optimization-master/compiler/01-gte-vs-gt-03.png)



## 总结

执行智能合约时，几个 Gas的差异就可能产生相当大的影响，尤其是在大量交易的情况下。采用哪种不等式，最好根据实际测试来决定。作为开发者，关注这些细微的细节可以确保开发出经济高效的智能合约，使最终用户和网络都受益。

## 对应源码

- [`src/compiler/Inequality.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Inequality.sol)
- [`test/compiler/Inequality.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Inequality.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
