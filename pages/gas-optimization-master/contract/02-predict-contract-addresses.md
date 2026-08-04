# 预测合约地址的妙用

## 分析

想象一下，我们有两个合约 A 和 B，它们之间存在这样的关系：

- 合约 A 在创建时，需要知道合约 B 的地址。

- 合约 B 在创建时，也需要知道合约 A 的地址。

    这就形成了一个“先有鸡还是先有蛋”的困境。文件中的 StorageContract 和 Writer 就模拟了这种关系：

- StorageContract 需要知道 Writer 的地址，以便只允许 Writer 调用 setX。

- Writer 需要知道 StorageContract 的地址，以便能调用它。

    

以下实现是解决这个问题的一种简单方法。它通过在部署后设置存储变量的 setter 函数来处理这个问题。但是存储变量address的StorageContract开销很大，我们宁愿避免使用它们。

```Solidity
contract StorageContract {
    address immutable public writer;
    uint256 public x;
    
    constructor(address _writer) {
        writer = _writer;
    }
function setX(uint256 x_) external {
        require(msg.sender == address(writer), "only writer can set");
        x = x_;
    }
 }
contract Writer {
    StorageContract public storageContract;
// cost: 49291
    function set(uint256 x_) external {
        storageContract.setX(x_);
    }
    function setStorageContract(address _storageContract) external {
            storageContract = StorageContract(_storageContract);
    }
 }
```

这在部署和运行时都会花费更多gas。

使用传统合约部署时，智能合约的地址可以根据部署者的地址及其随机数 \(nonce\) 确定性地计算出来。Solady[的 LibRLP 库](https://github.com/Vectorized/solady/blob/6c54795ef69838e233020e9ab29f3f6288efdf06/src/utils/LibRLP.sol#L27)可以帮助我们做到这一点。更有效的方法是预先计算StorageContract和Writer将要部署到的地址，并在它们的构造函数中设置它们。以下是此示例：

```Solidity
import {LibRLP} from "[https://github.com/vectorized/solady/blob/main/src/utils/LibRLP.sol](https://github.com/vectorized/solady/blob/main/src/utils/LibRLP.sol)";
contract StorageContract {
    address immutable public writer;
    uint256 public x;
    constructor(address _writer) {
        writer = _writer;
    }
// cost: 47158
    function setX(uint256 x_) external {
        require(msg.sender == address(writer), "only writer can set");
        x = x_;
    }
 }
contract Writer {
    StorageContract immutable public storageContract;
    constructor(StorageContract _storageContract) {
        storageContract = _storageContract;
    }
    function set(uint256 x_) external {
        storageContract.setX(x_);
    }
 }
// one time deployer.
 contract BurnerDeployer {
    using LibRLP for address;
function deploy() public returns(StorageContract storageContract, address writer) {
        StorageContract storageContractComputed = StorageContract(address(this).computeAddress(2)); // contracts nonce start at 1 and only increment when it creates a contract
        writer = address(new Writer(storageContractComputed)); // first creation happens here using nonce = 1
        storageContract = new StorageContract(writer); // second create happens here using nonce = 2
        require(storageContract == storageContractComputed, "false compute of create1 address"); // sanity check
         selfdestruct(*payable*(msg.sender));
    }
 }
```

这里，调用Writer\.setX\(\)消耗 47,000 Gas。我们通过在部署之前预先计算部署地址，StorageContract以便在部署时使用Writer，从而节省了超过 2,000 Gas，因此无需使用 setter 函数。使用此技术无需使用单独的合约，您可以在部署脚本中执行此操作。

## 测试



**文件位置：**

```Bash
src/contract/PredictAddr.sol
test/contract/PredictAddr.t.sol
```



**测试结果：**

```Bash
forge test --gas-report --mt test_predict_ -vvvvv --optimize
```



![预测合约地址的妙用图示](/images/gas-optimization-master/contract/02-predict-contract-addresses-01.png)



![预测合约地址的妙用图示 2](/images/gas-optimization-master/contract/02-predict-contract-addresses-02.png)



## 总结

- 账户 nonce \+ LibRLP 预计算地址 可实现交互合约间互知部署地址，无须额外存储或 setter 函数。

- 节省了部署和运行时的 gas，合约结构更简洁高效。

- 不仅适用于两个合约，也可扩展到多个相互依赖合约的批量部署。

## 对应源码

- [`src/contract/PredictAddr.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/src/contract/PredictAddr.sol)
- [`test/contract/PredictAddr.t.sol`](https://github.com/XuHugo/gas_optimization_master/blob/8960383/test/contract/PredictAddr.t.sol)

> 本文配套代码固定到提交 `8960383`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。
