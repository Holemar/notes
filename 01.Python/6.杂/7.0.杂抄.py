

变量的绑定时机
    ### 示例1,变量值中途被修改了 ####
    def create_multipliers():
        return [lambda x : i * x for i in range(5)]

    for multiplier in create_multipliers():
        print multiplier(2)

    # 期望打印值是: 0, 2, 4, 6, 8
    # 实际打印值是: 8, 8, 8, 8, 8

    '''
    解析,闭包的变量值,会被外部函数改变
    这示例实际使用时, i 的值随着外部改变,已经是最后一个值了,即 i= 4

    另外，由于 create_multipliers 函数比较难懂，这里写个易懂的等价函数来
    def create_multipliers():
        l = []
        for i in range(5):
            l.append(lambda x: i * x)
        return l
    '''

    ### 示例2,用传参把当时变量定型下来 ###
    def create_multipliers():
        return [lambda x, i=i : i * x for i in range(5)] # 定义 lambda 函数时,需要设定参数默认值，此时定下了参数值

    for multiplier in create_multipliers():
        print multiplier(2)


    ### 示例3,利用元组不能改变的特性把当时变量定型下来 ###
    def create_multipliers():
        return (lambda x: i * x for i in range(5))

    for multiplier in create_multipliers():
        print multiplier(2)


判断奇数
    # 经典的写法，对2求余
    if a % 2: print 'it is even'

    # 自然是使用位操作最快了
    if a & 1: print 'it is even'


计算任何数的阶乘
    # Python 2.x.
    result= (lambdak: reduce(int.__mul__,range(1,k+1),1))(3)
    print(result) #-> 6

    # Python 3.x.
    import functools
    result= (lambdak: functools.reduce(int.__mul__,range(1,k+1),1))(3)
    print(result) #-> 6


找到列表中出现最频繁的数
    # 利用 list 的 count 函数
    list1 = [1,2,3,4,2,2,3,1,4,4,4]
    print(max(set(list1),key=list1.count)) # -> 4


重置递归限制
    # Python 限制递归次数到 1000，我们可以重置这个值
    # 请只在必要的时候采用。
    import sys
    x = 1001
    print(sys.getrecursionlimit()) # -> 1000
    sys.setrecursionlimit(x)
    print(sys.getrecursionlimit()) # -> 1001



检查一个对象的内存使用
    # 在 Python 2.7 中，一个 32 比特的整数占用 24 字节，在 Python 3.5 中利用 28 字节。为确定内存使用，我们可以调用 getsizeof 方法：

    # 在 Python 2.7 中
    import sys
    x=1
    print(sys.getsizeof(x)) # -> 24

    # 在 Python 3.5 中
    import sys
    x=1
    print(sys.getsizeof(x)) # -> 28


一行代码搜索字符串的多个前后缀
    print('http://www.google.com'.startswith(('http://','https://'))) # -> True
    print('http://www.google.co.uk'.endswith(('.com','.co.uk'))) # -> True


Python 也可以有 end
    有不少编程语言，循环、判断代码块需要用 end 标明结束（比如 Shell），这样一定程序上会使代码逻辑更加清晰一点，
    其实这种语法在 Python 里并没有必要，但如果你想用，也不是没有办法，具体你看下面这个例子。

    __builtins__.end = None

    def m(x):
        if x >= 0:
            return x
        else:
            return -x
        end
    end

    print(m(5))  # 打印：5
    print(m(-5)) # 打印：5

    # 其实只是加了一个全局变量 end, 且这个变量的值指定为 None，但没法强制要求函数写end


省略号 ...
    ... 这是省略号，在Python中，一切皆对象。它也不例外。
    在 Python 中，它叫做 Ellipsis 。
    在 Python 3 中你可以直接写 ... 来得到这玩意。
    >>> ...
    Ellipsis
    >>> type(...)
    <class 'ellipsis'>


    而在 py2 中没有 ... 这个语法，只能直接写Ellipsis来获取。
    >>> Ellipsis
    Ellipsis
    >>> type(Ellipsis)
    <type 'ellipsis'>


    它转为布尔值时为真,且不可以赋值
    >>> bool(...)
    True

    最后，这东西是一个单例。
    >>> id(...)
    4362672336
    >>> id(...)
    4362672336

    这东西有啥用呢？据说它是 Numpy 的语法糖，不玩 Numpy 的人，可以说是没啥用的。
    在网上只看到这个 用 ... 代替 pass ，稍微有点用，但又不是必须使用的。

    try:
        1/0
    except ZeroDivisionError:
        ...


修改解释器提示符
    这个当做今天的一个小彩蛋吧。应该算是比较冷门的，估计知道的人很少了吧。
    正常情况下，我们在 终端下 执行Python 命令是这样的。

    >>> for i in range(2):
    ...     print (i)
    ...
    0
    1

    你是否想过 >>> 和 ... 这两个提示符也是可以修改的呢？

    >>> import sys
    >>> sys.ps1
    '>>> '
    >>> sys.ps2
    '... '
    >>>
    >>> sys.ps2 = '---------------- '
    >>> sys.ps1 = 'Python编程时光>>>'
    Python编程时光>>>for i in range(2):
    ----------------    print (i)
    ----------------
    0
    1

    注：只在终端的情况下可以，如果是文件里面，则会报错: AttributeError: 'module' object has no attribute 'ps1'


for 死循环
    用 while 写死循环很容易，但用 for 可就不容易了。那 for 该怎么写死循环呢？
    while 的写法：  while True: pass

    某网友的 for 写法：
    for i in iter(int, 1):pass 

    是不是懵逼了。 iter 还有这种用法？这为啥是个死循环？
    这真的是个冷知识，关于这个知识点，你如果看中文网站，可能找不到相关资料。
    还好你可以通过 IDE 看py源码里的注释内容，介绍了很详细的使用方法。

    def iter(source, sentinel=None): # known special case of iter
        """
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator

        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
        """
        pass

    原来 iter 有两种使用方法，通常我们的认知是第一种，将一个列表转化为一个迭代器。
    而第二种方法，他接收一个 callable 对象，和一个 sentinel 参数。第一个对象会一直运行，直到它返回 sentinel 值才结束。

    那 int 呢，这又是一个知识点， int 是一个内建方法。通过看注释，可以看出它是有默认值 0 的。你可以在终端上输入 int() 看看是不是返回 0 。

    class int(object):

        def __init__(self, x, base=10): # known special case of int.__init__
            """
            int(x=0) -> integer
            int(x, base=10) -> integer

            Convert a number or string to an integer, or return 0 if no arguments
            are given.  If x is a number, return x.__int__().  For floating point
            numbers, this truncates towards zero.

            If x is not a number or if base is given, then x must be a string,
            bytes, or bytearray instance representing an integer literal in the
            given base.  The literal can be preceded by '+' or '-' and be surrounded
            by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
            Base 0 means to interpret the base from the string as an integer literal.
            >>> int('0b100', base=0)
            4
            """
            pass


两次 return
    我们都知道， try... finally... 语句的用法，不管 try 里面是正常执行还是报异常，最终都能保证 finally 能够执行。
    同时，我们又知道，一个函数里只要遇到 return 函数就会立马结束。
    基于以上这两点，我们来看看这个例子，到底运行过程是怎么样的？

    def func():
        a = {'a':1, 'b':2}
        try:
            return a.pop('a')
        finally:
            return a

    print(func())  # {'b': 2}


    惊奇的发现，在 try 里的 return 居然不起作用。但 return 后面的语句又确实执行了。
    原因是，在 try... finally... 语句中， try 中的 return 会被直接忽视，因为要保证 finally 能够执行。


交互式“_”操作符
    对于 _ ，我想很多人都非常熟悉。
    给变量取名好艰难，用 _；
    懒得长长的变量名，用 _；
    无用的垃圾变量，用 _；

    以上，我们都很熟悉了，今天要介绍的是他在交互式中使用，可以返回上次取值结果。

    >>> 3 + 4
    7
    >>> _
    7
    >>> name='ming'
    >>> name
    'ming'
    >>> _
    'ming'  # 它可以返回上一次的运行结果。
    >>> print("hello")
    hello
    >>> _
    'ming'  # 如果是print函数打印出来的就不行了。
    >>> a=None
    >>> a
    >>> _
    'ming'  # 它会忽略None值。


改变递归次限制
    大家都知道使用递归是有风险的，递归深度过深容易导致堆栈的溢出。
    那到底，默认递归次数限制是多少呢？
    可以使用sys这个库来查看

    >>> import sys
    >>> sys.getrecursionlimit()
    1000

    可以查，当然也可以自定义修改次数，退出即失效。
    不过友情提醒，这玩意还是不要轻易去碰，万一导致系统崩溃了我可不背锅。
    >>> sys.setrecursionlimit(2000)
    >>> sys.getrecursionlimit()
    2000


负负得正
    从初中开始，我们就开始接触了负数 这个概念。知道了负负得正，这和武侠世界里的以毒功毒，有点神似。
    Python 作为一门高级语言，它的编写符合人类的思维逻辑，这其中也包括负负得正这个思想。

    >>> 5-3
    2
    >>> 5--3
    8
    >>> 5+-3
    2
    >>> 5++3
    8
    >>> 5---3
    2


数值与字符串比较
    在 Python2 中，数字可以与字符串直接比较。结果是数值永远比字符串小。
    >>> 100000000 < ""
    True
    >>> 100000000 < "ming"
    True

    但在 Python3 中，却不行。
    >>> 100000000 < ""
    TypeError: '<' not supported between instances of 'int' and 'str'


x == +x 吗?
    由于 Counter 的机制，"+" 用于两个 Counter 实例相加，而相加的结果如果元素的个数 <= 0，就会被丢弃。

    from collections import Counter
    ct = Counter('abcdbcaa')
    print(ct)  # Counter({'a': 3, 'b': 2, 'c': 2, 'd': 1})

    ct['c'] = 0
    ct['d'] = -2
    print(ct)  # Counter({'a': 3, 'b': 2, 'c': 0, 'd': -2})
    print(ct+ct)  # Counter({'a': 6, 'b': 4})


有趣的 import

    >>> import __hello__
    Hello world...    # py2 时的结果
    Hello World!      # py3 时的结果

    >>> import this
    # 显示 python 之禅

    >>> import antigravity
    # 自动打开一个网页，反地心引力漫画，网址: https://xkcd.com/353/


