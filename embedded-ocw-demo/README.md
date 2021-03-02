Substrate 进阶课第 4 讲作业参考答案

## 作业题目

以 lecture-demo 作基础，把它拷到 assignment 目录里来修改，最后提交这个代码库。

利用 offchain worker 取出 DOT 当前对 USD 的价格，并把写到一个 Vec 的存储里，你们自己选一种方法提交回链上，并在代码注释为什么用这种方法提交回链上最好。只保留当前最近的 10 个价格，其他价格可丢弃 （就是 Vec 的长度长到 10 后，这时再插入一个值时，要先丢弃最早的那个值）。

这个 http 请求可得到当前 DOT 价格：https://api.coincap.io/v2/assets/polkadot。

这作业题目总分 10 分

## 注意

- 请用 rust stable, `rustc 1.49.0 (e1884a8e3 2020-12-29)` 来编译。
- 其中一个要难点是怎样从 JSON 里的 string 转换为十进制小数，这里我用了 [substrate-fixed 这个库](https://github.com/encointer/substrate-fixed)。
- 学员用 **不具签名交易** 或 **不具签名但有签名数据交易** 来提交交易都可以。因为不应该跟某个用户挂勾，而是系统用户。不过如果能提交数据到链上，而数据是数值，不是字符串，已可获 9 分。如果是用以上二者之一，再多给 1 分。
