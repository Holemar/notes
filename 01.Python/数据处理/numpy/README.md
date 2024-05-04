## NumPy

Numpy 是一个开源的 Python 科学计算库，**用于快速处理任意维度的数组**。

Numpy **支持常见的数组和矩阵操作**，对于同样的数值计算任务，使用 NumPy 不仅代码要简洁的多，而且 NumPy 在性能上也远远优于原生 Python，至少是一到两个数量级的差距，而且数据量越大，NumPy 的优势就越明显。

NumPy 最为核心的数据类型是`ndarray`，使用`ndarray`可以处理一维、二维和多维数组，该对象相当于是一个快速而灵活的大数据容器。

NumPy 底层代码使用 C 语言编写，解决了 GIL 的限制，`ndarray`在存取数据的时候，数据与数据的地址都是连续的，这确保了可以进行高效率的批量操作，性能上远远优于 Python 中的`list`；  
另一方面`ndarray`对象提供了更多的方法来处理数据，尤其获取数据统计特征的方法，这些方法也是 Python 原生的`list`没有的。

NumPy 是一个运行速度非常快的数学库，主要用于数组计算，包含：

- 一个强大的N维数组对象 `ndarray`
- 广播功能函数
- 整合 C/C++/Fortran 代码的工具
- 线性代数、傅里叶变换、随机数生成等功能


1. [创建`ndarray`对象](./1.创建ndarray对象.md)  
2. [`ndarray`对象的属性](./2.ndarray对象的属性.md)  
3. [索引](./3.索引.md)  
4. [统计](./4.统计信息.md)  


numpy各函数的使用，参考 https://www.cjavapy.com/article/86/  
numpy教程： https://www.runoob.com/numpy/numpy-tutorial.html
