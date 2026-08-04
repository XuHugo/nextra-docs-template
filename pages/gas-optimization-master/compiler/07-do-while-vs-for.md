# Do-While 替换 for

## 分析

Solidity do\-while 循环比 for 循环更节省气体，即使您为循环根本不执行的情况添加 if 条件检查。

**少一次条件跳转**：do\-while 是在循环体后判断是否继续，for\-loop 需要在每次执行前都做一次判断跳转。一个少即约 `~5 gas`。

```Solidity

    function loop(uint256 times) public pure {
        for (uint256 i; i < times;) {
            unchecked {
                ++i;
            }
        }
    }


    function loop(uint256 times) public pure {
        if (times == 0) {
            return;
        }
uint256 i;
do {
            unchecked {
                ++i;
            }
        } while (i < times);
    }
 
```



## 测试



**文件位置：**

```Bash
src/compiler/Loop.sol
test/compiler/Loop.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_loop_ -vvv --optimize
```

![Do-While 替换 for图示](/images/gas-optimization-master/compiler/07-do-while-vs-for-01.png)



## 总结

- 在极度追求 gas 优化的场景下，可以使用 `do-while` 替代 `for`；

- 仅当你确定循环至少一次或能提前 `return` 时才使用；

- 对于一次性执行或用户输入次数量不多的循环，普通代码可读性更重要时，可以继续使用 `for`；

## 对应源码

- [`src/compiler/Loop.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/compiler/Loop.sol)
- [`test/compiler/Loop.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/compiler/Loop.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
