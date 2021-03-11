
面向对象的编程
    面向过程的编程:根据操作数据的函数或语句块来设计程序的。
    面向对象的编程:把数据和功能结合起来, 用称为对象的东西包裹起来组织程序的方法。
    类和对象是面向对象编程的两个主要方面。“类”创建一个新类型, 而“对象”是这个类的实例。
    域:属于一个对象或类的变量。
    方法:属于类的函数, 被称为类的方法。
    域和方法可以合称为类的属性。
    域有两种类型——属于每个实例/类的对象或属于类本身。它们分别被称为实例变量和类变量。
    类使用class关键字创建。类的域和方法被列在一个缩进块中。

self 参数
    类的方法与普通的函数只有一个特别的区别——它们“必须”有一个额外的第一个参数名称, 但是在调用这个方法的时候你不为这个参数赋值, Python会提供这个值。这个特别的变量指对象本身, 按照惯例它的名称是self。
    虽然你可以给这个参数任何名称, 但是“强烈建议”使用self这个名称——其他名称都是不赞成使用的。
    使用一个标准的名称有很多优点——1.方便别人阅读；2.有些IDE(集成开发环境)也可以帮助你。
    Python中的self等价于C++中的self指针和Java、C#中的this参考。

    例:
    class Person:
        def sayHi(self):  # self参数必须写
            print('Hello, how are you?')

    p = Person()
    p.sayHi() # self参数不需赋值
    print(p)  # 打印: <__main__.Person instance at 0xf6fcb18c>   (已经在__main__模块中有了一个Person类的实例)


类的变量和对象的变量
    类的变量: 由一个类的所有对象(实例)共享使用。当某个对象对类的变量做了改动的时候, 这个改动会反映到所有其他的实例上。
    对象的变量: 由类的每个对象/实例拥有。它们不是共享的, 在同一个类的不同实例中, 虽然对象的变量有相同的名称, 但是是互不相关的。
    使用的数据成员名称以“双下划线前缀”且不是双下划线后缀,比如__privatevar, Python的名称管理体系会有效地把它作为私有变量。
    惯例: 如果某个变量只想在类或对象中使用, 就应该以单下划线前缀。而其他的名称都将作为公共的, 可以被其他类/对象使用。

    例:
    class Person:
        '''Represents a person.'''
        population = 0 # 类的变量

        def __init__(self, name):
            '''Initializes the person's data.'''
            # 每创建一个对象都增加1
            Person.population += 1 # 调用类的变量,必须用 类名.变量名,如果写 self.变量名 则是对象的变量了
            self.name = name # 对象的变量,每个对象独立的
            print('(Initializing %s) We have %d persons here.' % (self.name, Person.population))

        def __del__(self):
            '''I am dying.'''
            print('%s says bye.' % self.name)
            Person.population -= 1

        def sayHi(self):
            self.__sayHi2() # 调用私有方法,外部不能调用的

        # 以双下划线开头(但没有双下划线结尾),则变成私有,仅供内部调用
        def __sayHi2(self): # 使用 self.population 也可以读取类的变量,只是改变的时候却只改变对象的变量
            print('Hi, my name is %s. We have %d persons here.' % (self.name, self.population))

    swaroop = Person('Swaroop')
    swaroop.sayHi() # 打印: Swaroop, 1

    kalam = Person('Abdul Kalam')
    kalam.sayHi() # 打印: Abdul Kalam, 2

    swaroop.sayHi() # 打印: Swaroop, 2
    print(Person.population) # 打印: 2
    del swaroop # 调用对象的 __del__ 方法
    print(Person.population) # 打印: 1

    print(Person.__doc__) # 打印类的docstring
    print(Person.__init__.__doc__) # 打印类的方法的docstring


对象序列化
    class A(object):
        a = 5

        # 如果 __repr__, __str__, __unicode__ 只想写一个的话，建议写 __repr__, 因为 str/unicode/repr 函数都会调用到
        def __repr__(self):return 'repr:%s' % self.a

        def __str__(self):return 'str:%s' % self.a

        def __unicode__(self):return 'unicode:%s' % self.a

    a = A()
    print(a) # 先 __str__, 再找 __repr__, 没有就用 object 默认的
    >>> a  # 终端交互时，则只找 __repr__, 没有就用 object 默认的
    print(str(a)) # 先 __str__, 再找 __repr__, 没有就用 object 默认的
    print(unicode(a)) # 先 __unicode__, 再找 __str__, 再找 __repr__, 没有就用 object 默认的
    print(repr(a)) # 先 __repr__, 没有就用 object 默认的



特殊的方法
__init__ 方法
    创建完对象后调用, 对当前对象的实例的一些初始化, 无返回值
    注意, 这个名称的开始和结尾都是双下划线。( __init__ 方法类似于C++、C#和Java中的 constructor )

__new__ 方法
    创建对象前，先创建的类实例调用, 返回当前对象的一个类实例。
    __new__ 方法的调用是发生在 __init__ 之前的。先是 __new__ 创建了 类实例，然后才可以用 __init__ 初始化实例。
    __new__() 方法始终都是类的静态方法，即使没有被加上静态方法装饰器。

__new__ 的作用
    依照Python官方文档的说法， __new__ 方法主要是当你继承一些不可变的 class 时(比如 int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。
    另一个作用就是实现类的自定义的 metaclass 。
    首先我们来看一下第一个功能，具体我们可以用int来作为一个例子：
    假如我们需要一个永远都是正数的整数类型，通过集成int，我们可能会写出这样的代码。

        class PositiveInteger(int):
            def __init__(self, value):
                super(PositiveInteger, self).__init__(self, abs(value))

        i = PositiveInteger(-3)
        print(i)

    但运行后会发现，结果根本不是我们想的那样，我们任然得到了-3。
    这是因为对于 int 这种 不可变的对象，我们只有重载它的 __new__ 方法才能起到自定义的作用。
    这是修改后的代码：

        class PositiveInteger(int):
            def __new__(cls, value):
                return super(PositiveInteger, cls).__new__(cls, abs(value))

        i = PositiveInteger(-3)
        print(i)

    通过重载 __new__ 方法，我们实现了需要的功能。

__call__ 方法
    让类的实例（对象）可以被当做函数对待

    例:
    class Person(object):  # 注：py2的旧类不执行 __new__, 得用新类
        def __new__(cls, name):
            print('NEW ', name)
            return super(Person, cls).__new__(cls)
        def __init__(self, name):
            print('INIT ', name)
            self.test_name = name
        def __call__(self, a, b):
            self.a = a
            self.b = b
            print('CALL ({}, {})'.format(self.a, self.b))
        def sayHi(self):
            self.test = 'sss'  # 属性可以随处定义,不需事先定义
            print('Hello, my name is ' + self.test_name + ', ' + self.test)

    p = Person('Swaroop')  # 先打印 NEW, 然后再打印 INIT
    p.sayHi()  # 打印: Hello, my name is Swaroop, sss
    print('the Person test is ' + p.test)  # 打印: the Person test is sss
    p.test2 = 'haha...'
    print('the Person test2 is ' + p.test2)  # 打印: the Person test2 is haha...
    p(1, 2)  # 打印: CALL (1, 2)
    print(callable(p))  # True


各操作符(魔法函数)
    名称   说明
    __init__(self,...) 这个方法在新建对象恰好要被返回使用之前被调用。
    __del__(self) 在对象要被删除之前调用。如使用 del 删除时。

    # 比较运算符
    __lt__(self,other) 当使用 小于 运算符 (<) 的时候调用。
    __gt__(self,other) 当使用 大于 运算符 (>) 的时候调用。
    __eq__(self,other) 当使用 等于 运算符 (==) 的时候调用。
    __ne__(self,other) 当使用 不等于 运算符 (!=) 的时候调用。
    __le__(self,other) 当使用 小于等于 运算符 (<=) 的时候调用。
    __ge__(self,other) 当使用 大于等于 运算符 (>=) 的时候调用。

    # 一元操作符
    __pos__(self) 实现取正操作，例如 +some_object。
    __neg__(self) 实现取负操作，例如 -some_object。
    __abs__(self) 实现内建绝对值函数 abs() 操作。
    __invert__(self) 实现取反操作符 ~。
    __round__(self， n) 实现内建函数 round() ，n 是近似小数点的位数。
    __floor__(self) 实现 math.floor() 函数，即向下取整。
    __ceil__(self) 实现 math.ceil() 函数，即向上取整。
    __trunc__(self) 实现 math.trunc() 函数，即距离零最近的整数。

    # 常见算数操作符
    __add__(self, other) 当使用 加 (+) 的时候调用。
    __sub__(self, other) 当使用 减 (-) 的时候调用。
    __mul__(self, other) 实现乘法操作。
    __floordiv__(self, other) 实现使用 // 操作符的整数除法。
    __div__(self, other) 实现使用 / 操作符的除法。
    __truediv__(self, other) 实现 true 除法，这个函数只有使用 from __future__ import division 时才有作用。
    __mod__(self, other) 实现 % 取余操作。
    __divmod__(self, other) 实现 divmod 内建函数。
    __pow__(self, other) 实现 ** 操作符。
    __lshift__(self, other) 实现左移位运算符 << 。
    __rshift__(self, other) 实现右移位运算符 >> 。
    __and__(self, other) 实现按位与运算符 & 。
    __or__(self, other) 实现按位或运算符 | 。
    __xor__(self, other) 实现按位异或运算符 ^ 。
    # 反射算数运算符
    __radd__(self, other) 实现反射加法操作。
    __rsub__(self, other) 实现反射减法操作。
    __rmul__(self, other) 实现反射乘法操作。
    __rfloordiv__(self, other) 实现使用 // 操作符的整数反射除法。
    __rdiv__(self, other) 实现使用 / 操作符的反射除法。
    __rtruediv__(self, other) 实现 true 反射除法，这个函数只有使用 from __future__ import division 时才有作用。
    __rmod__(self, other) 实现 % 反射取余操作符。
    __rdivmod__(self, other) 实现调用 divmod(other, self) 时 divmod 内建函数的操作。
    __rpow__(self, other) 实现 ** 反射操作符。
    __rlshift__(self, other) 实现反射左移位运算符 << 的作用。
    __rshift__(self, other) 实现反射右移位运算符 >> 的作用。
    __rand__(self, other) 实现反射按位与运算符 & 。
    __ror__(self, other) 实现反射按位或运算符 | 。
    __rxor__(self, other) 实现反射按位异或运算符 ^ 

    # 增强赋值运算符
    __iadd__(self, other) 实现加法赋值操作。
    __isub__(self, other) 实现减法赋值操作。
    __imul__(self, other) 实现乘法赋值操作。
    __ifloordiv__(self, other) 实现使用 //= 操作符的整数除法赋值操作。
    __idiv__(self, other) 实现使用 /= 操作符的除法赋值操作。
    __itruediv__(self, other) 实现 true 除法赋值操作，这个函数只有使用 from __future__ import division 时才有作用。
    __imod__(self, other) 实现 %= 取余赋值操作。
    __ipow__(self, other) 实现 **= 操作。
    __ilshift__(self, other) 实现左移位赋值运算符 <<= 。
    __irshift__(self, other) 实现右移位赋值运算符 >>= 。
    __iand__(self, other) 实现按位与运算符 &= 。
    __ior__(self, other) 实现按位或赋值运算符 | 。
    __ixor__(self, other) 实现按位异或赋值运算符 ^= 。

    # 类型转换操作符
    __int__(self) 实现到int的类型转换。
    __long__(self) 实现到long的类型转换。
    __float__(self) 实现到float的类型转换。
    __complex__(self) 实现到complex的类型转换。
    __oct__(self) 实现到八进制数的类型转换。
    __hex__(self) 实现到十六进制数的类型转换。
    __index__(self) 实现当对象用于切片表达式时到一个整数的类型转换。如果你定义了一个可能会用于切片操作的数值类型，你应该定义 index。
    __trunc__(self) 当调用 math.trunc(self) 时调用该方法， trunc 应该返回 self 截取到一个整数类型（通常是long类型）的值。
    __coerce__(self) 该方法用于实现混合模式算数运算，如果不能进行类型转换， coerce 应该返回 None 。反之，它应该返回一个二元组 self 和 other ，这两者均已被转换成相同的类型。

    # 类的表示
    __str__(self) 在我们对对象使用 print 语句或是使用 str() 的时候调用。
    __repr__(self) 定义对类的实例调用 repr() 时的行为。 str() 和 repr() 最主要的差别在于“目标用户”。
                   repr() 的作用是产生机器可读的输出（大部分情况下，其输出可以作为有效的Python代码），而 str() 则产生人类可读的输出。
    __unicode__(self) 定义对类的实例调用 unicode() 时的行为。unicode() 和 str() 很像，只是它返回unicode字符串。
                      注意，如果调用者试图调用 str() 而你的类只实现了 __unicode__() ，那么类将不能正常工作。所有你应该总是定义 __str__() ，以防有些人没有闲情雅致来使用unicode。
    __format__(self) 定义当类的实例用于新式字符串格式化时的行为，例如， "Hello, 0:abc!".format(a) 会导致调用 a.format("abc") 。
                    当定义你自己的数值类型或字符串类型时，你可能想提供某些特殊的格式化选项，这种情况下这个魔法方法会非常有用。
    __hash__(self) 定义对类的实例调用 hash() 时的行为。它必须返回一个整数，其结果会被用于字典中键的快速比较。同时注意一点，实现这个魔法方法通常也需要实现 __eq__ ，并且遵守如下的规则：a == b 意味着 hash(a) == hash(b)。
    __nonzero__(self) 定义对类的实例调用 bool() 时的行为，根据你自己对类的设计，针对不同的实例，这个魔法方法应该相应地返回True或False。
    __dir__(self) 定义对类的实例调用 dir() 时的行为，这个方法应该向调用者返回一个属性列表。一般来说，没必要自己实现 __dir__ 。
                但是如果你重定义了 __getattr__ 或者 __getattribute__，乃至使用动态生成的属性，以实现类的交互式使用，那么这个魔法方法是必不可少的。

    # 自定义序列
    __len__(self) 返回容器的长度，可变和不可变类型都需要实现。
    __getitem__(self, key) 定义对容器中某一项使用 self[key] 的方式进行读取操作时的行为。
                          这也是可变和不可变容器类型都需要实现的一个方法。它应该在键的类型错误式产生 TypeError 异常，同时在没有与键值相匹配的内容时产生 KeyError 异常。
    __setitem__(self, key) 定义对容器中某一项使用 self[key] 的方式进行赋值操作时的行为。
                          它是可变容器类型必须实现的一个方法，同样应该在合适的时候产生 KeyError 和 TypeError 异常。
    __iter__(self, key) 它应该返回当前容器的一个迭代器。
                          迭代器以一连串内容的形式返回，最常见的是使用 iter() 函数调用，以及在类似 for x in container: 的循环中被调用。
                          迭代器是他们自己的对象，需要定义 __iter__ 方法并在其中返回自己。
    __reversed__(self) 定义了对容器使用 reversed() 内建函数时的行为。它应该返回一个反转之后的序列。当你的序列类是有序时，类似列表和元组，再实现这个方法，
    __contains__(self, item) 定义了使用 in 和 not in 进行成员测试时类的行为。
                          你可能好奇为什么这个方法不是序列协议的一部分，原因是，如果 contains 没有定义，Python就会迭代整个序列，如果找到了需要的一项就返回 True 。
    __missing__(self ,key) 在字典的子类中使用，它定义了当试图访问一个字典中不存在的键时的行为
                          （目前为止是指字典的实例，例如我有一个字典 d ， "george" 不是字典中的一个键，当试图访问 d["george'] 时就会调用 d.__missing__("george") ）。

    # 访问控制
    # 很多从其他语言转向Python的人都抱怨Python的类缺少真正意义上的封装（即没办法定义私有属性然后使用公有的getter和setter）。然而事实并非如此。实际上Python不是通过显式定义的字段和方法修改器，而是通过魔法方法实现了一系列的封装。
    __getattr__(self, name) 当用户试图访问一个根本不存在（或者暂时不存在）的属性时，你可以通过这个魔法方法来定义类的行为。
                            这个可以用于捕捉错误的拼写并且给出指引，使用废弃属性时给出警告（如果你愿意，仍然可以计算并且返回该属性），以及灵活地处理AttributeError。
                            只有当试图访问不存在的属性时它才会被调用，所以这不能算是一个真正的封装的办法。
    __setattr__(self, name, value) 它允许你自定义某个属性的赋值行为，不管这个属性存在与否，也就是说你可以对任意属性的任何变化都定义自己的规则。
    __delattr__(self, name) 它是用于处理删除属性时的行为。和 _setattr__ 一样，使用它时也需要多加小心，防止产生无限递归（在 __delattr__ 的实现中调用 del self.name 会导致无限递归）。
    __getattribute__(self, name) 它允许你自定义属性被访问时的行为，且只能用于新式类。
                            它也同样可能遇到无限递归问题（通过调用基类的 __getattribute__ 来避免）。__getattribute__ 基本上可以替代 __getattr__ 。只有当它被实现，并且显式地被调用，或者产生 AttributeError 时它才被使用。
                            这个魔法方法可以被使用，但不推荐你使用它，因为它的使用范围相对有限（通常我们想要在赋值时进行特殊操作，而不是取值时），而且实现这个方法很容易出现Bug。
        # 自定义这些控制属性访问的魔法方法很容易导致问题，考虑下面这个例子:
        def __setattr__(self, name. value):
            self.name = value
            # 因为每次属性幅值都要调用 __setattr__()，所以这里的实现会导致递归
            # 这里的调用实际上是 self.__setattr('name', value)。因为这个方法一直
            # 在调用自己，因此递归将持续进行，直到程序崩溃

        def __setattr__(self, name, value):
            self.__dict__[name] = value # 使用 __dict__ 进行赋值
            # 定义自定义行为

        # 到这里，我们对Python中自定义属性存取控制有了什么样的印象？它并不适合轻度的使用。
        # 实际上，它有些过分强大，而且违反直觉。然而它之所以存在，是因为一个更大的原则：Python不指望让杜绝坏事发生，而是想办法让做坏事变得困难。自由是至高无上的权利，你真的可以随心所欲。

    # 反射
    __instancecheck__(self, instance) 检查一个实例是否是你定义的类的一个实例（例如 isinstance(instance, class) ）。
    __subclasscheck__(self, subclass) 检查一个类是否是你定义的类的子类（例如 issubclass(subclass, class) ）。

    # 上下文管理器
    # 当对象使用 with 声明创建时，上下文管理器允许类做一些设置和清理工作。如：“with open('foo.txt') as bar:”
    __enter__(self) 定义使用 with 声明创建的语句块最开始上下文管理器应该做些什么。注意 __enter__ 的返回值会赋给 with 声明的目标，也就是 as 之后的东西。
    __exit__(self, exception_type, exception_value, traceback) 定义当 with 声明语句块执行完毕（或终止）时上下文管理器的行为。
                它可以用来处理异常，进行清理，或者做其他应该在语句块结束之后立刻执行的工作。如果语句块顺利执行， exception_type , exception_value 和 traceback 会是 None 。
                你可以选择处理这个异常或者让用户来处理。如果你想处理异常，确保 __exit__ 在完成工作之后返回 True 。如果你不想处理异常，那就让它发生吧。

    # 拷贝
    __copy__(self) 定义对类的实例使用 copy.copy() 时的行为。copy.copy() 返回一个对象的浅拷贝，这意味着拷贝出的实例是全新的，然而里面的数据全都是引用的。也就是说，对象本身是拷贝的，但是它的数据还是引用的（所以浅拷贝中的数据更改会影响原对象）。
    __deepcopy__(self, memodict=) 定义对类的实例使用 copy.deepcopy() 时的行为。copy.deepcopy() 返回一个对象的深拷贝，这个对象和它的数据全都被拷贝了一份。memodict 是一个先前拷贝对象的缓存，它优化了拷贝过程，而且可以防止拷贝递归数据结构时产生无限递归。当你想深拷贝一个单独的属性时，在那个属性上调用 copy.deepcopy() ，使用 memodict 作为第一个参数。



类变量,容易出错的:
    ##### 范例1, 错误示范 #####
        class A(object):
            x = 1

        class B(A):
            pass

        class C(A):
            pass

        # 初始化正常
        print(A.x, B.x, C.x) # 打印: 1 1 1

        # 改变类变量的值,也正常
        B.x = 2
        print(A.x, B.x, C.x) # 打印: 1 2 1

        # 下面就晕菜了,怎么改变 A 会影响 C,而又不影响 B ?
        A.x = 3
        print(A.x, B.x, C.x) # 打印: 3 2 3


    ##### 解说 范例1 #####
        python 的类变量是存放在一个内部处理的字典中,这字典通常被称为方法解析顺序(Method Resolution Order, 缩写为 MRO)
        所以, 在上面的代码中, 由于属性 x 未能在 C 类中找到, 它会被抬起到其父类中查找(即 A 类)。换句话说, C 不具有自己独立于 A 的 x 属性。
        所以, C.x 其实是一个 A.x 的引用。而 B.x 被赋值过,所以它有自己的 x 属性了。

        #### 把上面的 x 属性是否在类的 __dict__ 判断打印出来,会更容易理解 ####
        class A(object):
            x = 1

        class B(A):
            pass

        class C(A):
            pass

        # A 类里面有 x 属性, 而 B、C 类里面没有, B、C 类得去到父类里面才能找到这个属性
        print(A.x, B.x, C.x) # 打印: 1 1 1
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, False, False

        # B 类赋值了一个 x 属性, 所以有了自己独立于 A 类的 x 属性
        B.x = 2
        print(A.x, B.x, C.x) # 打印: 1 2 1
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, True, False

        # 改变了 A 类的 x 属性的值, C 类里面由于没有这个属性, 所以得用 A 类的。 B 类有自己独立的 x 属性,就用自己的了。
        A.x = 3
        print(A.x, B.x, C.x) # 打印: 3 2 3
        print('x' in A.__dict__, 'x' in B.__dict__, 'x' in C.__dict__) # 打印: True, True, False
