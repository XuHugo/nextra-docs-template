# 编译器优化

比较条件、循环、运算符、可见性和编译器配置的 Gas 差异。

已知以下技巧可以提高 Solidity 编译器的 Gas 效率。然而，预计 Solidity 编译器会随着时间的推移而改进，这些技巧的效果会逐渐减弱，甚至适得其反。您不应盲目使用此处列出的技巧，而应同时对两种方案进行基准测试。其中一些技巧在使用\-\-via\-ir编译器标志时已被编译器集成，甚至可能在使用该标志时降低代码效率。基准测试。务必进行基准测试。  

## 文章目录

1. [条件优化：>= 还是 >](./01-gte-vs-gt)
2. [条件优化：使用 ! 代替 == 判断](./02-not-vs-eq)
3. [待验证：无符号整数使用 != 0 代替 > 0](./03-nonzero-comparison)
4. [条件优化：短路布尔值](./04-short-circuit-booleans)
5. [条件优化：拆分与返回关联的布尔表达式](./05-split-boolean-expressions)
6. [适当使用unchecked](./06-unchecked)
7. [Do-While 替换 for](./07-do-while-vs-for)
8. [展开循环](./08-loop-unrolling)
9. [频繁使用的函数名](./09-function-name-selector)
10. [通过哈希比较数组和字符串](./10-hash-array-string-comparison)
11. [使用 ++i 替换 i++](./11-prefix-increment)
12. [使用位移替换乘除运算](./12-bit-shifts)
13. [n * n * n替换n 3](./13-cube-vs-exponentiation)
14. [合理使用 private 和 internal](./14-private-internal-visibility)
15. [x = x + y 与 x += y](./15-compound-assignment)
16. [使用枚举而不是字符串](./16-enums-over-strings)
17. [编译器优化器设置](./17-compiler-optimizer)
18. [查找表](./18-lookup-tables)
19. [预编译合约](./19-precompiles)
20. [始终使用命名返回](./20-named-returns)
