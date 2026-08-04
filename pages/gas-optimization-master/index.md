# Gas 优化大师课

这套专栏系统整理 Solidity 与 EVM Gas 优化方法，从费用模型和底层数据区出发，
逐步进入存储、合约架构、内联汇编、编译器技巧和真实业务场景。

配套代码仓库：[XuHugo/gas_optimization_master](https://github.com/XuHugo/gas_optimization_master)。
本文内容对应代码版本：[`8960383`](https://github.com/XuHugo/gas_optimization_master/tree/8960383)。

> Gas 优化不是越低越好。可读性、安全性、可维护性和协议版本差异，
> 都应当与节省的 Gas 一起评估。带有“待验证”标记的内容保留了原稿中的疑问性质。

## 学习路线

### 1. [基础知识](./basics/)

理解 Gas 费用、EVM 数据区、Yul 与 Foundry 测试方法。

共 7 篇。

### 2. [存储优化](./storage/)

围绕 Storage、Memory、Calldata 和瞬态存储降低读写成本。

共 16 篇。

### 3. [合约优化](./contract/)

从部署、调用、错误处理和架构选择优化合约成本。

共 18 篇。

### 4. [汇编优化](./assembly/)

使用内联汇编控制内存、调用、哈希和常见数学操作。

共 11 篇。

### 5. [编译器优化](./compiler/)

比较条件、循环、运算符、可见性和编译器配置的 Gas 差异。

共 20 篇。

### 6. [场景与设计模式](./patterns/)

把批量调用、签名、代理和代币标准用于真实业务场景。

共 7 篇。

### 7. [非常规技巧](./unconventional/)

实验性较强的优化方法，以及它们的适用边界和风险。

共 5 篇。

## 如何复现实验

```bash
git clone https://github.com/XuHugo/gas_optimization_master.git
cd gas_optimization_master
git checkout 8960383
git submodule update --init --recursive
forge build
forge test --gas-report
```
