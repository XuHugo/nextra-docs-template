# 条件优化：拆分与返回关联的布尔表达式

## 分析



**对那些会导致函数提前退出（****`require`**** 或 ****`if … revert`****）的复合布尔表达式，拆分成多条判断确实能在失败路径节省 gas**。但要注意以下几点：

- **只有在失败时才会省 gas**

    - 如果第一个条件就不满足，函数会立即 revert，后面的判断根本不会执行，所以省下了额外的布尔运算和分支开销。

    - **如果两个条件都成立（成功路径）**，拆分后反而会多一条跳转和一次条件检查，可能会略微多消耗几 gas。

- **只能节约包含短路逻辑的复合表达式**

    - `x > 0 && y > 0`、`x < 10 || x > 20` 这种带短路的复合判断适用。

    - 纯算术或无短路意义的布尔组合（比如总要两个条件都算一次）拆分不会带来收益。

- **把最可能失败的条件放前面**

    - 为了最大化“早退”命中率，应当将失败概率高或检查简单的条件放在第一条；这样更多调用会在第一条就退出，节省更多。

- **实际效果依赖编译器和 EVM 版本**

    - 大多数主流编译器（0\.8\.x）和 EVM 客户端测试中，每拆分一次可在失败路径节省约 3 gas；但具体数值可能因版本略有差异，最好在你的代码里用 Foundry 做一次对比测试。

## 拆分require

### 分析

require\(\)通常用于验证智能合约函数中的条件，如果条件不满足，则会抛出异常并撤销更改。但需要注意的是，如果条件计算结果为 false，则不会退还`require()`所使用的 Gas 。

通过拆分`require()`使用运算符的复杂语句`&&`，我们可以降低长期 Gas 成本。虽然`require()`由于字节码大小增加，多个语句会导致部署 Gas 成本略有增加，但对于运行时调用频繁的合约来说，这还是有利的。

当我们拆分 require 语句时，本质上是说每个语句都必须为真，函数才能继续执行。如果第一个语句的计算结果为假，函数将立即回滚，并且不会检查后续的 require 语句。这样可以节省 gas 成本，而不是计算下一个 require 语句。

```Solidity
function calls(uint256 *x*, uint256 *y*) external pure returns (uint256) {
        require(x > 0 && y > 0); 
        return x * y;
    }
    function calls(uint256 *x*, uint256 *y*) external pure returns (uint256) {
        require(x > 0); 
        require(y > 0);

        return x * y;
    }
```

**为什么 gas 更省？**

- **早退机制**：只要第一条 `require` 不满足，后续所有判断都会跳过，节省 gas；

- **字节码更简单**：不用生成 `AND` 或 `OR` 相关的 opcode；

- **优化累积明显**：每次调用都节省约 3 gas，适用于高频逻辑中的多次短路判断。

### 测试

**文件位置：**

```Bash
src/compiler/Split.sol
test/compiler/Split.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_spilt_ -vvv --optimize
```



![条件优化：拆分与返回关联的布尔表达式图示](/images/gas-optimization-master/compiler/05-split-boolean-expressions-01.png)



### 总结

拆分使用该运算符的复杂`require()`语句`&&`可以为智能合约带来显著的长期 Gas 节省。尽管部署 Gas 成本略有增加，但随着时间的推移，这种优化技术将变得非常有利可图，尤其有利于频繁进行运行时调用和验证的合约。通过采用这种优化策略，开发者可以减少合约的 Gas 消耗，从而提高整体效率和成本效益。



## 拆分revert和return

### 分析

与拆分 require 语句类似，如果 if 语句中没有布尔运算符，通常可以节省一些 gas。

```Solidity
function splitIf(uint256 *x*) external pure {
        if (x < 10 || x > 20) {
            revert BadValue();
        }
    }

    function splitRet(uint256 *x*) external pure {
        if (x < 10 || x > 20) {
            return;
        }
    }  
    
    function splitIf(uint256 *x*) external pure {
        if (x < 10) {
            revert TooLow();
        }
        if (x > 20) {
            revert TooHigh();
        }
    }

    function splitRet(uint256 *x*) external pure {
        if (x < 10) {
            return;
        }
        if (x > 20) {
            return;
        }
    }  
```



### 测试

**文件位置：**

```Bash
src/compiler/Split.sol
test/compiler/Split.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_spilt_ -vvv --optimize
```



![条件优化：拆分与返回关联的布尔表达式图示 2](/images/gas-optimization-master/compiler/05-split-boolean-expressions-02.png)

如果revert换成return，也是一样的效果。

![条件优化：拆分与返回关联的布尔表达式图示 3](/images/gas-optimization-master/compiler/05-split-boolean-expressions-03.png)



### 总结

- **失败路径**：拆分复合布尔表达式，越早失败越省 gas。

- **成功路径**：拆分会略贵；如果在成功路径 gas 敏感场合（如高频调用的核心函数），要评估整体开销。

- **实践建议**：对关键的、可能失败的判断拆分试验；对成功路径高频函数，再用测试脚本验证是否值得。

## 对应源码

- [`src/compiler/Split.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Split.sol)
- [`test/compiler/Split.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Split.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
