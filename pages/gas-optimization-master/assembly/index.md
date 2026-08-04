# 汇编优化

使用内联汇编控制内存、调用、哈希和常见数学操作。

内联汇编允许开发者编写低级、高效的代码，这些代码可由 EVM 直接执行，而无需昂贵的 Solidity 操作码。内联汇编还能更精确地控制内存和存储的使用，从而进一步降低 Gas 成本。此外，内联汇编可用于执行仅使用 Solidity 难以实现的复杂操作，从而为优化 Gas 使用提供更大的灵活性。

你不应该想当然地认为编写汇编代码就能自动提高代码效率。我们列出了一些通常情况下用汇编代码更高效的领域，但你始终应该测试非汇编版本。 

## 文章目录

1. [内存扩展优化](./01-memory-expansion)
2. [内存优化：错误消息](./02-error-messages)
3. [内存优化：调用合约](./03-contract-calls)
4. [内存优化：创建多个合约](./04-multiple-contract-creation)
5. [内存优化：多个外部调用](./05-multiple-external-calls)
6. [内存优化：事件](./06-events)
7. [内存优化：Hash](./07-hashing)
8. [使用汇编检查Address(0)](./08-address-zero-check)
9. [数学运算:min 和 max](./09-min-max)
10. [数学运算:偶奇校验](./10-even-odd)
11. [待验证：selfbalance 与 address(this).balance](./11-selfbalance)
