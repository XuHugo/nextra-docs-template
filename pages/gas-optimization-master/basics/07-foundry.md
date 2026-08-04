# Foundry 介绍

## Foundry 简介与安装

**什么是 Foundry？**

忘掉那些需要用 JavaScript 写测试、切换各种工具的旧模式吧。Foundry 是一套用 Rust 编写的、极速的、可移植的以太坊开发工具箱。它的核心优势在于：

- **用 Solidity 写测试**：是的，你没听错！你可以直接在 Solidity 中编写测试用例，就像写合约一样。这极大地降低了心智负担，让你能更专注于合约逻辑本身。

- **速度极快**：Foundry 的测试执行速度非常快，这对于需要频繁迭代和测试的 Gas 优化工作来说至关重要。

- **内置工具集**：提供了 \`forge\` \(测试和部署\)、\`cast\` \(与链交互\) 等强大的命令行工具。



**安装 Foundry**

安装 Foundry 非常简单。打开你的终端（在 macOS 或 Linux 上）并运行以下命令：

```Bash
curl -L https://foundry.sh | bash
```

然后，在你的终端中运行 `foundryup` 来安装最新版本。

安装完成后，通过运行以下命令来验证安装是否成功：

```Bash
forge --version
```

如果你能看到版本号，那么恭喜你，你已经准备好进入高效的 Gas 优化世界了！



## Foundry 项目结构与核心概念

让我们从创建一个新的 Foundry 项目开始。在终端中运行：

```Bash
forge init my-gas-optimization-project
cd my-gas-optimization-project
```

你会看到一个这样的目录结构：

```Plain Text
my-gas-optimization-project/
├── lib/              # 存放依赖库，例如 OpenZeppelin
├── script/           # 存放部署脚本
├── src/              # 存放你的合约代码
└── test/             # 存放你的测试合约
```



**核心概念：**

- **测试合约**：在 Foundry 中，测试用例是写在以 `.t.sol `结尾的 Solidity 文件中的。这些文件通常放在 \`test/\` 目录下。

- **测试函数**：测试函数以` test `开头（例如 `test_myFunction()`）。

- **断言 \(Assertion\)**：我们使用断言来验证代码的行为是否符合预期。Foundry 提供了丰富的断言函数，例如 `assertEq` \(断言相等\)、`assertTrue `\(断言为真\) 等。

- `forge test`: 这是运行所有测试的核心命令。



## 编写你的第一个 Gas 测试

现在，让我们进入实战。假设我们有一个简单的合约 `Counter.sol`，我们想测试它的 `increment` 函数的 Gas 消耗。

**1\. 编写合约 \(**`src/Counter.sol`**\)**

```Solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;
*contract* Counter {
    *uint256* *public* number;

    *function* increment() *public* {
        number += 1;
    }
}
```



**2\. 编写测试合约 \(**`test/Counter.t.sol`**\)**

这是我们的重点。在 `test` 目录下创建一个新文件 `Counter.t.sol`。

```Solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/Counter.sol";

*contract* CounterTest is Test {
    Counter *public* counter;

    // setUp 函数是一个特殊的函数，它会在每个测试函数运行之前执行
    // 非常适合用来初始化合约状态
    *function* setUp() *public* {
        counter = new Counter();
    }

    // --- 测试函数从这里开始 ---

    // 一个基础的测试，确保 increment 函数能正常工作
    *function* test_Increment() *public* {
        counter.increment();
        assertEq(counter.number(), 1, "number should be 1 after incrementing");
    }
}
```



**3\. 运行测试并查看 Gas 报告**

现在，回到你的终端，运行以下命令：

```Bash
forge build
forge test --gas-report  --mt test_Increment
```

你会看到一个类似这样的输出，清晰地列出了每个函数的 Gas 消耗：

```Plain Text
| Contract | Function | Min | Max | Avg |
|----------|----------|-----|-----|-----|
| Counter  | increment| 21564 | 21564 | 21564 |
```



**关键点：**

- `--gas-report` 标志是 Foundry 的一个杀手级功能。它会自动计算并显示每个函数的 Gas 成本。

- 通过比较优化前后 `forge test --gas-report` 的输出，你可以精确地知道你的优化节省了多少 Gas。



## 测试的核心：断言与高级技巧



**1\. 基础断言 \(Assertions\)**

测试的核心是断言——验证代码的行为是否符合预期。`forge-std/Test.sol` 提供了丰富的断言函数，它们是编写有效测试的基础。

|函数|描述|
|---|---|
|`assertEq(a, b)`|断言 `a` 等于 `b`。支持多种类型。|
|`assertTrue(condition)`|断言 `condition` 为真。|
|`assertGt(a, b)`|断言 `a` 大于 `b`。|
|`assertLt(a, b)`|断言 `a` 小于 `b`。|
|`assertNotEq(a, b)`|断言 `a` 不等于 `b`。|



**示例：**

```Solidity
*function* test_Assertions() *public* {
    assertTrue(1 == 1, "1 should be equal to 1");
    assertEq(*address*(this).balance, 0, "initial balance should be 0");
    assertGt(100, 99, "100 should be greater than 99");
}
```



**2\. 使用 **`console.log`**进行调试**

当你需要调试复杂的逻辑时，`console.log` 是你的好朋友。你需要在你的合约顶部导入它：

```Solidity
import "forge-std/console.sol";
```

然后你就可以在你的函数中像这样使用它：

```Solidity
*function* someFunction() *public* {
    *uint256* myVar = 42;
    console.log("The value of myVar is:", myVar);
}
```



```Plain Text

运行 `forge test -vvv` 可以看到这些日志输出。
```

**3\. 测试失败场景 **`vm.expectRevert`

测试一个函数是否会像预期那样失败（revert）同样重要。

```Solidity
*function* test_RevertWhen_NotOwner() *public* {
    // 告诉 Foundry，我们期望下一个外部调用会因为指定的错误而失败
    vm.expectRevert(*bytes*("Not owner"));
    // 这个调用应该会失败
    otherContract.doSomething();
}
```



## 高级调试与分析技巧

当 `console.log` 不足以解决问题，或者你想知道一个函数调用背后究竟发生了什么时，就需要用到下面的高级工具了。



**1\. 交互式调试器 \(**`forge test --debug`**\)**

这是 Foundry 最强大的功能之一。当一个测试失败时，你可以像使用传统编程语言的 `gdb` 或 `pdb` 一样，逐行调试你的代码。

**如何使用：**

假设你的 `test_SomethingFails()` 测试失败了，运行以下命令启动调试器：

```Bash
forge test --match-test test_SomethingFails --debug
```

- `--match-test <测试函数名>`: 指定只运行并调试这一个测试。

- `--debug`: 在测试失败的地方启动交互式调试器。

**调试器界面：**

启动后，你会进入一个文本用户界面 \(TUI\)，它会显示：

- 当前执行到的 Solidity 源代码。

- EVM 的操作码 \(Opcode\) 视图。

- 当前的堆栈 \(Stack\) 和内存 \(Memory\) 状态。

**常用调试命令：**

|按键|命令|描述|
|---|---|---|
|`s`|step|执行下一个操作码（步入函数调用）。|
|`n`|next|执行到下一行 Solidity 代码（跳过函数调用内部）。|
|`c`|continue|继续执行直到下一个断点或测试结束。|
|`p`|print|打印堆栈上的一个值。|
|`q`|quit|退出调试器。|



**使用场景：**

当你的测试因为一个复杂的逻辑错误而 `revert`，而你无法通过 `console.log` 快速定位问题时，调试器是你的救星。你可以清晰地看到每一步执行后所有变量和内存的变化。



**2\. 查看执行追踪 \(Execution Tracing with **`-v`** flags\)**

Foundry 的 `-v` 标志可以让你深入了解函数的执行过程。它的核心功能是**逐级扩大追踪（Trace）的范围**，并显示更详细的日志。

- `-vv`: 显示 `console.log `的输出。

- `-vvv`: 启用追踪器，显示**测试函数**的调用栈追踪 \(call stack traces\)。

- `-vvvv`: 扩大追踪范围，额外显示`setUp`函数的调用栈追踪。

- `-vvvvv`: 进一步扩大范围，额外显示**合约部署**的追踪信息。

当你启用追踪器（`-vvv`及更高）时，Foundry 的默认追踪器会为你展示一个**高级别的调用摘要**，包括函数签名、Gas 消耗和返回值，但**不包含**底层的 EVM 操作码。

**如何使用：**

```Bash
# 查看 test_Increment 函数的调用栈摘要
forge test --match-test test_Increment -vvv
```



你会看到类似这样的输出，它告诉你调用了哪个函数，消耗了多少 Gas：

```Bash
Traces:
  [<gas>] CounterTest::test_Increment()
    └─ [<gas>] Counter::increment()
      └─ ← () 
```

**使用场景：**

- 快速了解一个复杂的函数调用了哪些内部或外部函数。

- 检查每个调用的 Gas 消耗和出入参。



**3\. 查看优化的中间表示 \(**`forge inspect xxx irOptimized`**\)**

在深入研究底层操作码之前，通常更有用的是查看编译器在进行优化后生成的“中间表示”（Intermediate Representation, IR）。这是一种比 EVM 汇编更易读的格式，它能清晰地展示出编译器的优化决策。

**如何使用：**

```Bash
forge inspect Counter irOptimized
```

这将输出 \`Counter\` 合约经过优化后的 IR。你会看到类似 Yul 的语法，它展示了函数的基本块、跳转和变量。

**输出示例 \(简化版\):**

```Bash
// --- increment() ---
function increment() {
  let var_number_sload := sload(0)
  let var_add := add(var_number_sload, 1)
  sstore(0, var_add)
}
```



**使用场景：**

- **理解编译器行为**：当你使用 \`unchecked\` 块或特定的 Solidity 语法时，查看 IR 可以让你准确地知道编译器是如何理解和优化你的代码的。

- **Yul 优化前的参考**：在用手写 Yul 替换一段 Solidity 代码之前，先查看它的 IR，这能给你一个很好的起点和优化思路。

- **学习高级优化**：通过比较不同 Solidity 写法生成的 IR，你可以学习到哪些模式能被编译器更有效地优化。



现在，你不仅能编写和测试你的合约，还能深入到 EVM 内部，像一个真正的工程师一样，精确地诊断和优化你的代码。

记住，**优化不是靠猜，而是靠测量和分析**。Foundry 为我们提供了完成这项工作所需的一切。下课！

## 对应源码

- [`src/Counter.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/Counter.sol)
- [`test/Counter.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/Counter.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
