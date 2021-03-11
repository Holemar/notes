
intern 驻留机制
    要了解这个机制之前，必须先清楚 id, is, == 之间的不同，以及代码块的范围。


id, is, ==
    在Python中， id 是什么？ id 是内存地址。
    那就有人问了，什么是内存地址呢？ 你只要创建一个数据（对象）那么都会在内存中开辟一个空间，将这个数据临时加在到内存中，那么这个空间是有一个唯一标识的，就好比是身份证号，标识这个空间的叫做内存地址，也就是这个数据（对象）的 id，那么你可以利用 id() 去获取这个数据的内存地址：

    name = '太白'
    print(id(name))  # 1585831283968

    那么 is 是什么？ == 又是什么？
    == 是比较的两边的数值是否相等，而 is 是比较的两边的内存地址是否相等。
    如果内存地址相等，那么这两边其实是指向同一个内存地址。
    可以说如果内存地址相同，那么值肯定相同，但是如果值相同，内存地址不一定相同。


代码块(code blocks)
    根据提示我们从官方文档找到了这样的说法：
    A Python program is constructed from code blocks. A block is a piece of Python program text that is executed as a unit. The following are blocks: a module, a function body, and a class definition. Each command typed interactively is a block. A script file (a file given as standard input to the interpreter or specified as a command line argument to the interpreter) is a code block. A script command (a command specified on the interpreter command line with the ‘-c‘ option) is a code block. The string argument passed to the built-in functions eval() and exec() is a code block.
    A code block is executed in an execution frame. A frame contains some administrative information (used for debugging) and determines where and how execution continues after the code block’s execution has completed.

    上面的主要意思是：
    Python程序是由代码块构造的。块是一个python程序的文本，他是作为一个单元执行的。
    代码块：一个模块，一个函数，一个类，一个文件等都是一个代码块。
    而作为交互方式输入的每个命令都是一个代码块。
    什么叫交互方式？就是在终端中进入Python解释器里面，每一行代码都是一个代码块。
    而对于一个文件中的两个函数，也分别是两个不同的代码块。
    可以这样理解：在学校里，学生就好比是代码，班级就好比是代码块，我们想让代码运行起来，必须依靠班级去执行，也就是代码块。


代码块的缓存机制
    前提条件：在同一个代码块内。
    机制内容：Python在执行同一个代码块的初始化对象的命令时，会检查是否其值是否已经存在，如果存在，会将其重用。
            换句话说：执行同一个代码块时，遇到初始化对象的命令时，他会将初始化的这个变量与值存储在一个字典中，在遇到新的变量时，会先在字典中查询记录，如果有同样的记录那么它会重复使用这个字典中的之前的这个值。
    适用对象： int(float), str, bool。
    对象的具体细则:
        int(float):任何数字在同一代码块下都会复用。
        bool:True和False在字典中会以1，0方式存在，并且复用。
        str：几乎所有的字符串都会符合缓存机制。

    如果在同一代码块下，则采用同一代码块下的缓存机制。
    如果是不同代码块，则采用小数据池的驻留机制。


字符串的 intern(字符串驻留) 机制
    >>> a = "Hello_Python"
    >>> b = "Hello" + "_Python"
    >>> a is b
    True

    >>> a = "(Hello)_Python"
    >>> b = "(Hello)" + "_Python"
    >>> a is b
    False

    >>> a = "Hello_Python"
    >>> h = "Hello"
    >>> b = h + "_Python"
    >>> a is b
    False

    >>> a = "Hello_Python"
    >>> b = ''.join(["Hello", "_Python"])
    >>> a is b
    False

    >>> 'a' * 20 is 'aaaaaaaaaaaaaaaaaaaa'
    True
    >>> 'a' * 21 is 'aaaaaaaaaaaaaaaaaaaaa'  # 说明字符串池的长度有限，超过20不再使用池。
    False


    Python字符串的intern机制规定：
    1.直接的字符串都满足代码块的缓存机制
    2.由加法拼接、join得到的、乘数>=2得到的：仅含大小写字母，数字，下划线，总长度<=20，满足代码块的缓存机制
    3.当字符串不满足2条件时，相同值的字符串变量在创建时都会申请一个新的内存地址来保存值。
    注：终端的intern机制跟文件的不一样，且 py2 与 py3 也有所不同。

    Incomputer science, string interning is a method of storing only onecopy of each distinct string value, which must be immutable. Interning strings makes some stringprocessing tasks more time- or space-efficient at the cost of requiring moretime when the string is created or interned. The distinct values are stored ina string intern pool. –引自维基百科
    翻译: python会将一定规则的字符串在字符串驻留池中，创建一份，当你将这些字符串赋值给变量时，并不会重新创建对象， 而是使用在字符串驻留池中创建好的对象。


小整数对象池
    Python字符串有intern机制的限制，同样的，整形数也有大小整数对象池的限制。
    Python语言在设计之初为了减少频繁申请和销毁内存的资源开销，规定了[-5, 256]之间的整数全部常驻在内存中且不会被垃圾回收只能增减引用计数，这就是小整数对象池，池外的数在创建时每次都得申请新的内存空间而不是增加引用计数。

    对于整数，Python官方文档中这么说：
    The current implementation keeps an array of integer objects for all integers between -5 and 256, when you create an int in that range you actually just get back a reference to the existing object. So it should be possible to change the value of 1. I suspect the behaviour of Python in this case is undefined.

    例子如下：
    >>> a = 256
    >>> b = 256
    >>> a is b
    True
    >>> print(id(a), id(b))
    1953505712 1953505712

    >>> a = 257
    >>> b = 257
    >>> a is b
    False
    >>> print(id(a), id(b))  # 终端超过 256 的不再缓存到池中
    2037325924592 2037325924368


大整数对象池
    在交互式终端环境中，每次创建大型数时都是去申请新的内存空间。
    但是在编写Python文件时每次运行都把代码加载到内存中，整个项目代码都属于一个整体。
    这时就是大型整数对象池发挥作用的时候了，它把处于相同代码块的所有等值的大型整数变量都处理为一个对象。

    例子如下：
    class A(object):
        a = 100
        b = 100
        c = 1000
        d = 1000

    class B(object):
        a = 100
        b = 1000

    print(A.a is A.b)  # True
    print(A.a is B.a)  # True
    print(A.c is A.d)  # True  重点是这一个
    print(A.c is B.b)  # False 虽然在同一个文件中，但是类本身就是代码块，所以这是在两个不同的代码块下，不满足小数据池（驻存机制），则指向两个不同的地址。


指定驻留
    from sys import intern  # py3 才有
    a = intern('hello!@'*20)
    b = intern('hello!@'*20)
    print(a is b)  # True
    # 指定驻留是你可以指定任意的字符串加入到小数据池中，让其只在内存中创建一个对象，多个变量都是指向这一个字符串。


引用扩展
    扩展点Python内存管理方面的姿势吧。

    >>> id([1,2,3]) == id([4,5,6])
    True
    >>> a = [1,2,3]
    >>> b = [4,5,6]
    >>> print(id(a), id(b))
    2037326252488 2037326229256

    有人问为什么 id([1,2,3]) == id([4,5,6])，这是因为Python会实时销毁没有引用计数的对象。
    一旦在内存中创建了一个对象但是没有为其添加引用计数，该段代码执行完后就会回收地址，在这个例子中计算完[1,2,3]的id后list被销毁，计算右边的id时list实时创建，复用了左边list用过的内存。
    但是生成的时间有先后，他们并不代表同一个对象。

