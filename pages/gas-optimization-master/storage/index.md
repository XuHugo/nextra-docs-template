# 存储优化

围绕 Storage、Memory、Calldata 和瞬态存储降低读写成本。

## 文章目录

1. [减少非零字节](./01-reduce-nonzero-bytes)
2. [避免存储值从零变为非零](./02-avoid-zero-to-one-storage)
3. [缓存数据](./03-cache-storage-data)
4. [变量打包](./04-variable-packing)
5. [字符串尽量小于32个字节](./05-short-strings)
6. [使用 constant 和 immutable](./06-constants-and-immutables)
7. [使用 mapping 避免数组长度检查](./07-mapping-over-array)
8. [使用位图替换大量 bool](./08-bitmaps)
9. [使用 SSTORE2 或 SSTORE3 存储大量数据](./09-sstore2-and-sstore3)
10. [使用存储指针代替内存](./10-storage-pointer)
11. [使用 Calldata 替换 Memory](./11-calldata-over-memory)
12. [待验证：冗余操作](./12-remove-redundant-operations)
13. [数据类型的选择](./13-data-type-selection)
14. [使用瞬态存储](./14-transient-storage)
15. [退款](./15-gas-refunds)
16. [事件](./16-events)
