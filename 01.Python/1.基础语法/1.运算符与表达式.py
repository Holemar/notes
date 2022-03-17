﻿
运算符与表达式:

运算符
   运算符   名称          说明
     +       加          两个对象相加,也可以字符串拼接
     -       减          得到负数或是一个数减去另一个数
     *       乘          两个数相乘 或是返回一个被重复若干次的字符串
     **      幂          返回x的y次幂(正数的平方根是 num ** 0.5)
     /       除          x除以y
     //      取整除      返回商的整数部分
     %       取模        返回除法的余数  # 8%3得到2。 -25.5%2.25得到1.5
     <<      左移        把一个数的二进制向左移一定数目 # 2 << 2得到8
     >>      右移        把一个数的二进制向右移一定数目 # 11 >> 1得到5
     &       按位与      数的按位与 # 5 & 3得到1。
     |       按位或      数的按位或 # 5 | 3得到7。
     ^       按位异或    数的按位异或 # 5 ^ 3得到6
     ~       按位翻转    x的按位翻转是-(x+1) # ~5得到6。
     <       小于        返回x是否小于y
     >       大于        返回x是否大于y
     <=      小于等于    返回x是否小于等于y
     >=      大于等于    返回x是否大于等于y
     ==      等于        比较对象是否相等
     !=      不等于      比较两个对象是否不相等(python3删除了“<>”符号)
     not     布尔“非”  如果x为True，返回False。如果x为False，它返回True。 # x = True; not x返回False。
     and     布尔“与”  如果x为False，x and y返回False，否则它返回y的计算值。 # x=False; y=True; x and y返回False。
     or      布尔“或”  如果x是True，它返回True，否则它返回y的计算值。# x = True; y = False; x or y返回True。
     in, not in          成员测试 (由类里面的 __contains__ 函数指定返回值)
     is, is not          同性测试 (两值的 is 运算是判断引用,与“==”的比较有所不同)


   说明:
     1.加号“+”:有数学相加，也有字符串拼接作用,注意:不能字符串和数字相加。如: 3 + 5得到8; 'a' + 'b'得到'ab'。
     2.乘号“*”:两个数相乘，也可以把字符串重复拼接若干次,如: 2 * 3得到6; 'la' * 3得到'lalala'。
     3.幂“**” :这种写法,其他语言好像没见到过,如: 3 ** 4得到81(即3 * 3 * 3 * 3)
     4.除号“/”:整数的除法得到整数结果,浮点数的得到浮点数,如:4/3得到1(返回相除后结果的向下取整(floor)); 4.0/3或4/3.0得到1.333...
       注意:Python 3.0开始,移除了含糊的除法符号('/')，而只返回浮点数。如:4/3得到1.333...
     5.取整除“//”:将两数相除,然后对结果取整,如: 7 // 3得到2; 4 // 3.0得到1.0
     6.比较运算符:所有比较运算符返回1表示真，返回0表示假。这分别与特殊的变量 True 和 False 等价。注意大小写。
       如果两个操作数都是数字，它们首先被转换为一个共同的类型(如double)。否则，它总是返回 False 。
       5 < 3返回0(即False); 而3 < 5返回1(即True)。比较可以被任意连接: 3 < 5 < 7返回True。
       大于、小于、小于等于、大于等于时:数字跟数字可以比较，字符串跟字符串可以比较，但数字不能跟字符串比较。
       等于、不等于时: 数字跟数字可以比较，字符串跟字符串可以比较，数字跟字符串比较返回 False (表示不相等)
       等于: Python 使用“==”来做比较，用“=”来赋值。但不允许内嵌的赋值，所以不会出现你本以为在做比较而意外的写成赋值的情况。
     7.布尔运算: and 和 or 都是短路运算,没有非短路运算的运算符。
       短路运算:当前面一个表达式可以决定结果时，后面的语句不用再判断。非短路运算时，还照样判断后面的。
       注意：在 and or 运算中，空字符串'',数字0,空列表[],空字典{},空元组(), None,在逻辑运算中都被当作假来处理。
     8.and 和 or 的特殊用法:
       由于语言的松散性,用 and 和 or 在赋值语句时有判断作用。
       1) or 用在赋值语句里，返回第一个逻辑为真的值, 没有逻辑为真的返回最后一个。(如下这写法比较常用)
          如:ss = False or None or 0 or '' or -1 or 'sss'; print(ss) # 打印:-1 (-1作if判断时返回 True)
          设定预设值的写法: edittype = edittype or "text"; # 如果 edittype 之前有值,则取之前的值; 之前为空,则取默认值
       2) and 用在赋值语句里，与 or 刚好相反，返回第一个逻辑为假的值, 没有逻辑为假的返回最后一个。
          如: a = 0 and 1; print(a) # 打印: 0
          a = 2 and 1; print(a) # 打印: 1
          应用： valid = True; valid = valid and checkLength(name, 16); valid = valid and checkLength(name, 16); # 如果前面的验证不通过，则后面的不再验证
       简便的记忆是: and 偏 False, or 偏 True
       要理解 and 和 or 的这种写法，得考虑到它的短路运算特性。它是在做逻辑判断，但返回的是前或后一个的值，而不是返回 True 或 False 。
     9.三目运算符：
       Python 没有三目运算符“cond ? a : b”,但可以使用 and 和 or 来代替(需理解前面的 and 和 or 的特殊用法)，如下：
       1) c = cond and a or b   # 这多数情况下是正确的，但当 a 是空字符串''、数字0等逻辑运算为假的情况下会出错。
       2) c = (cond and [a] or [b])[0] # 即使 a或者b为一个逻辑假的值，将他放入集合中后，就为真了，也就是[False] [None]都不为假。
       3) c = (b, a)[cond and 1 or 0] # 注意 a和b的位置是颠倒的,将表达式结果转成1和0来作为元组下标而选择结果。
       4) c = a if cond else b # 使用 if else 写条件(python特有的写法,建议使用,前3种写法难理解也容易出错)
     10.自增,自减:
       Python 没有“++”和“--”两个语法,自增自减时只能写: i = i + 1 或者 i += 1, 不能用 i++
       这在一定程度上避免出错，因为新手经常搞错“++”放前面还是放后面; 但这也导致 for 循环的写法与其它语言很不同
     11.switch/case 语句
        Python现在不支持这语句，但可以用 range(N) 生成一个 列表
     12.一次性的多比较
        “ if (0 < n < 4000) ”这种写法在python是允许的，它等价于“ if ((0 < n) and (n < 4000)) ”但前者更适合阅读。


运算符优先级
    下面这个表给出Python的运算符优先级，从最低的优先级(最松散地结合)到最高的优先级(最紧密地结合)。
    在一个表达式中，Python会首先计算下表中较下面的运算符，然后在计算列在下表上部的运算符。
    在下表中列在同一行的运算符具有 相同优先级 。例如，+和-有相同的优先级。
    建议使用圆括号来分组运算符和操作数，以便能够明确地指出运算的先后顺序，使程序尽可能地易读。例如，2 + (3 * 4)显然比2 + 3 * 4清晰。

    运算符                   描述
    lambda                  Lambda表达式
    or                      布尔“或”
    and                     布尔“与”
    not x                   布尔“非”
    in，not in              成员测试
    is，is not              同一性测试
    <，<=，>，>=，!=，==    比较
    |                       按位或
    ^                       按位异或
    &                       按位与
    <<，>>                  移位
    +，-                    加法与减法
    *，/，%                 乘法、除法与取余
    +x，-x                  正负号
    ~x                      按位翻转
    **                      指数
    x.attribute             属性参考
    x[index]                下标
    x[index:index]          寻址段
    f(arguments...)         函数调用
    (experession,...)       绑定或元组显示
    [expression,...]        列表显示
    {key:datum,...}         字典显示
    'expression,...'        字符串转换


计算顺序
    默认地，运算符优先级表决定了哪个运算符在别的运算符之前计算。然而，如果要改变它们的计算顺序，得使用圆括号。
    例如，你想要在一个表达式中让加法在乘法之前计算，那么你就得写成类似(2 + 3) * 4的样子。


结合规律
    运算符通常由左向右结合，即具有相同优先级的运算符按照从左向右的顺序计算。例如，2 + 3 + 4被计算成(2 + 3) + 4。
    一些如赋值运算符那样的运算符是由右向左结合的，即a = b + c被处理为a = (b + c)。


is 用于判断两个引用所指的对象是否相同
    与“==”的比较有所不同
    与内置函数 id() 的判断一样

    #在Python中，整数和短小的字符，Python都会缓存这些对象，以便重复使用。当我们创建多个等于1的引用时，实际上是让所有这些引用指向同一个对象。
        a = 1
        b = 1
        print(a is b) # True
        print(id(a), id(b)) # (8423888, 8423888)

        a = "good"
        b = "good"
        print(a is b) # True

        a = "very good morning" *10
        b = "very good morning" *10
        print(a is b) # False (短字符串会缓存，长的就不会了，具体长度20)

        a = []
        b = []
        print(a is b) # False
        print(id(a), id(b)) # (30353488, 30351768)


    可以使用 sys 包中的 getrefcount()，来查看某个对象的引用计数
    需要注意的是，当使用某个引用作为参数，传递给 getrefcount() 时，参数实际上创建了一个临时的引用。因此, getrefcount() 所得到的结果，会比期望的多1。
        from sys import getrefcount
        a = [1, 2, 3]
        print(getrefcount(a)) # 2
        b = a
        print(getrefcount(a)) # 3
        print(getrefcount(b)) # 3


计算 平方，乘方，平方根，n次方根

1. 平方
    print(num ** 2)     # 方式一
    print(pow(num, 2))  # 方式二
    import numpy
    numpy.square(num)  # 方式三(需安装第三方库 numpy)

2. 乘方
    print(num ** 3)     # 方式一
    print(pow(num, 3))  # 方式二

3. 平方根
    print(num ** 0.5)     # 方式一
    print(pow(num, 0.5))  # 方式二
    import math
    math.sqrt(num)  # 方式三(使用系统库 math)

4. 开n次方根
    # 开3次方根
    print(num ** (1/3))     # 方式一
    print(pow(num, (1/3)))  # 方式二
    # 开r次方根
    print(num ** (1/r))     # 方式一
    print(pow(num, (1/r)))  # 方式二
