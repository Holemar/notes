
Decorator(装饰器)
@符号修饰函数(有的语言称为:注释)
    python 2.4以后，增加了 @符号修饰函数 对函数进行修饰, python3.0/2.6又增加了对类的修饰。
    修饰符必须出现在函数定义前一行，不允许和函数定义在同一行。也就是说 @A def f(): 是非法的。

    简单的来说就是用一个新的对象来替换掉原有的对象，新的对象包含原有的对象，并且会处理它的执行结果和输入参数。
    python另外一个很有意思的属性：可以在函数中定义函数。
    其实总体说起来，装饰器其实也就是一个函数，一个用来包装函数的函数，返回一个修改之后的函数对象，将其重新赋值原来的标识符，并永久丧失对原始函数对象的访问。

    实际上，装饰器并不是必须的。意思就是说，你完全可以不使用装饰器，使用它是为了使我们的代码
        更加优雅，代码结构更加清晰
        将实现特定的功能代码封装成装饰器，提高代码复用率，增强代码可读性

    官方的说明:
    http://www.python.org/dev/peps/pep-0318/


代码上解释 Decorator(装饰器) 就是这样：
    @decomaker
    def func(arg1, arg2, ...):
        pass

    # 上面相当于这样写：
    result = decomaker(func)(arg1, arg2, ...)


范例(普通函数的用法,查看函数运行时间)：
    import time
    def timeit(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print( 'used:' + str(end - start) )
            return result
        return wrapper

    @timeit
    def foo():
        print( 'in foo()' )

    def foo2():
        print( 'in foo2()' )

    # 装饰器,其实也是函数。这样写同样起到装饰作用,也就是函数重载
    foo2 = timeit(foo2)

    # 调用被修饰过的函数,跟普通函数没啥区别
    foo()
    foo2()


范例(多个修饰函数,原函数带参数)：
    def bold(fn):
        def wrapped(arg):
            return "<b>" + fn(arg) + "</b>"
        return wrapped

    def italic(fn):
        def wrapped(arg):
            return "<i>" + fn(arg) + "</i>"
        return wrapped

    @bold   # 相当于: bold(italic(hello))(arg)
    @italic # 相当于: italic(hello)(arg)
    def hello(s):
        return "hello " + s

    # 调用被修饰过的函数,跟普通函数没啥区别
    print( hello('holemar') ) # 打印: <b><i>hello holemar</i></b>


    # 下面用一个不写“@”装饰的函数测试调用方法
    def hello2(s):
        return "hello " + s

    # 不被装饰的函数,真实的修饰这样写:
    print( italic(hello2)('world') ) # 打印: <i>hello world</i>
    print( bold(hello2)('world') ) # 打印: <b>hello world</b>
    print( bold(italic(hello2))('world') ) # 打印: <b><i>hello world</i></b>


范例(装饰器带参数的用法)：
    def say_hello(contry):
        def wrapper(func):
            def deco(*args, **kwargs):
                if contry == "china":
                    print("你好!")
                elif contry == "america":
                    print('hello.')
                else:
                    return

                # 真正执行函数的地方
                func(*args, **kwargs)
            return deco
        return wrapper


    @say_hello("china")
    def xiaoming():
        print('小明，中国人')

    @say_hello("america")
    def jack():
        print('jack，美国人')

    # 看看执行效果
    xiaoming()  # 打印: 你好! \n 小明，中国人
    print("------------")
    jack()  # 打印: hello.\n jack，美国人


范例(装饰器带参数的用法,通用的处理输入和输出结果)：
    # 如果装饰器需要带参数,则里面需要嵌套两层函数(不带参数的只需嵌套一层),看下面的“相当于”就会明白
    def accepts(*types):
        """判断接收参数的类型，目前仅支持 *args 格式的参数，未能支持 **kwargs 格式"""
        def check_accepts(f):
            def new_f(*args):
                assert len(types) == len(args)
                for (a, t) in zip(args, types):
                    assert isinstance(a, t), "arg %r does not match %s" % (a, t)
                return f(*args)
            new_f.__name__ = f.__name__
            return new_f
        return check_accepts

    def returns(rtype):
        def check_returns(f):
            def new_f(*args, **kwds):
                result = f(*args, **kwds)
                assert isinstance(result, rtype), "return value %r does not match %s" % (result, rtype)
                return result
            new_f.__name__ = f.__name__
            return new_f
        return check_returns

    # 注意这两个装饰器的顺序，如果倒过来会出错，因为 @accepts 先过滤了 func 函数，而 @returns 又过滤 @accepts 函数的结果
    @returns((int, float))  # 表示返回的是一个参数，且参数类型属于 (int,float) 中的一种
    @accepts(int, (int, float))  # 表示输入两个参数，且第一个参数必须是 int 类型，第二个参数类型属于 (int,float) 中的一种
    def func(arg1, arg2):
        return arg1 * arg2

    # 测试一下运行结果
    print(func(2, 3.2))  # 打印： 6.4
    print(func.__name__)

    # 下面用一个不写“@”装饰的函数测试调用方法
    def func2(arg1, arg2):
        return arg1 * arg2

    # 下面的调用,要注意理解各个圆括号, 尤其最后一行嵌套的写法
    print(returns((int, float))(func2)(2, 5))  # 打印： 10
    print(accepts(int, (int, float))(func2)(2, 5.1))  # 打印： 10.2
    print(returns((int, float))(accepts(int, (int, float))(func2))(2, 5.1))  # 打印： 10.2
    print(func2.__name__)


范例(高阶:不带参数的类装饰器)
    """
    以上都是基于函数实现的装饰器，在阅读别人代码时，还可以时常发现还有基于类实现的装饰器。
    基于类装饰器的实现，必须实现 __call__ 和 __init__两个内置函数。
        __init__ ：接收被装饰函数
        __call__ ：实现装饰逻辑。
    """
    class logger(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            print("[INFO]: the function {func}() is running...".format(func=self.func.__name__))
            return self.func(*args, **kwargs)

    @logger
    def say(something):
        print("say {}!".format(something))

    say("hello")
    # 打印: [INFO]: the function say() is running...
    # 打印: say hello!


范例(高阶:带参数的类装饰)
    """
    上面不带参数的例子，你发现没有，只能打印INFO级别的日志，正常情况下，我们还需要打印DEBUG WARNING等级别的日志。这就需要给类装饰器传入参数，给这个函数指定级别了。
    带参数和不带参数的类装饰器有很大的不同。
        __init__ ：不再接收被装饰函数，而是接收传入参数。
        __call__ ：接收被装饰函数，实现装饰逻辑
    """
    class logger(object):
        def __init__(self, level='INFO'):
            self.level = level

        def __call__(self, func):  # 接受函数
            def wrapper(*args, **kwargs):
                print("[{level}]: the function {func}() is running...".format(level=self.level, func=func.__name__))
                func(*args, **kwargs)
            return wrapper  # 返回函数

    @logger(level='WARNING')
    def say(something):
        print("say {}!".format(something))

    say("hello")
    # 打印: [WARNING]: the function say() is running...
    # 打印: say hello!


范例(使用偏函数与类实现装饰器)
    """
    绝大多数装饰器都是基于函数和闭包实现的，但这并非制造装饰器的唯一方式。
    事实上，Python 对某个对象是否能通过装饰器（ @decorator）形式使用只有一个要求：decorator 必须是一个“可被调用（callable）的对象。
    对于这个 callable 对象，我们最熟悉的就是函数了。
    除函数之外，类也可以是 callable 对象，只要实现了__call__ 函数（上面几个例子已经接触过了）。
    还有容易被人忽略的偏函数其实也是 callable 对象。
    接下来就来说说，如何使用 类和偏函数结合实现一个与众不同的装饰器。

    如下所示，DelayFunc 是一个实现了 __call__ 的类，delay 返回一个偏函数，在这里 delay 就可以做为一个装饰器。
    """
    import time
    import functools

    class DelayFunc(object):
        def __init__(self,  duration, func):
            self.duration = duration
            self.func = func

        def __call__(self, *args, **kwargs):
            print('Wait for {} seconds...'.format(self.duration))
            time.sleep(self.duration)
            return self.func(*args, **kwargs)

        def eager_call(self, *args, **kwargs):
            print('Call without delay')
            return self.func(*args, **kwargs)

    def delay(duration):
        """
        装饰器：推迟某个函数的执行。
        同时提供 .eager_call 方法立即执行
        """
        # 此处为了避免定义额外函数，
        # 直接使用 functools.partial 帮助构造 DelayFunc 实例
        return functools.partial(DelayFunc, duration)

    def delay2(duration):
        """
        实现跟上面 delay 完全一样的功能，仅为了说明运行原理
        同样的也提供 .eager_call 方法立即执行
        """
        def wrapper(func):
            return DelayFunc(duration, func)
        return wrapper

    # 我们的业务函数很简单，就是相加
    @delay(duration=2)  # 也可以改用 delay2 装饰器试试看，效果是否一样
    def add(a, b):
        return a+b

    # 来看一下执行过程
    if __name__ == '__main__':
        print(add)  # 打印: <__main__.DelayFunc object at 0x107bd0be0>
        # 可见 add 变成了 Delay 的实例

        print(add(3, 5))  # 直接调用实例，进入 __call__
        # 打印： Wait for 2 seconds...
        # 打印： 8

        print(add.eager_call(2, 4))  # 立即执行
        # 打印: 6

        print(add.func)  # 实现实例方法
        # 打印: <function add at 0x107bef1e0>


范例(装饰类的装饰器)
    """
    用 Python 写单例模式的时候，常用的有三种写法。其中一种，是用装饰器来实现的。
    以下便是我自己写的装饰器版的单例写法。
    """

    instances = {}

    def singleton(cls):
        def get_instance(*args, **kw):
            cls_name = cls.__name__
            print('步骤 1')
            if cls_name not in instances:
                print('步骤 2')
                instance = cls(*args, **kw)
                instances[cls_name] = instance
            return instances[cls_name]
        return get_instance

    @singleton
    class User(object):
        _instance = None

        def __init__(self, name):
            print('步骤 3')
            self.name = name

    # 来看一下执行过程
    if __name__ == '__main__':
        u1 = User('student1')  # 打印： 步骤 1, 步骤 2, 步骤 3
        print('----------')
        u1.age = 20
        u2 = User('student2')  # 仅打印: 步骤 1
        print(u2.age)  # 打印: 20

    # 只要熟悉装饰器的实现过程，就不难实现对类的装饰。在上面这个例子中，装饰器就只是实现对类实例的生成的控制而已。


内置的装饰器
    有三个，分别是 staticmethod, classmethod 和 property
    作用分别是把类中定义的实例方法变成静态方法、类方法和类属性。
    由于模块里可以定义函数，所以静态方法和类方法的用处并不是太多，除非你想要完全的面向对象编程。
    而属性也不是不可或缺的，Java没有属性也一样活得很滋润。使用频率较少,了解即可。

staticmethod 和 classmethod 的用法与区别:
    对于 classmethod 的参数, 需要隐式地传递类名, 而 staticmethod 参数中则不需要传递类名, 其实这就是二者最大的区别。
    对于 staticmethod 就是为了要在类中定义而设置的，一般来说很少这样使用，可以使用模块级(module-level)的函数来替代它。既然要把它定义在类中，想必有作者的考虑。
    对于 classmethod, 可以通过子类来进行重定义。


范例(staticmethod 和 classmethod 的用法与区别)：
    class Person:
        def sayHi(self):  # self参数必须写，正常函数的写法
            print('Hello, how are you?')

        @staticmethod # 申明此方法是一个静态方法，外部可以直接调用
        def tt(a): # 静态方法，第一个参数不需要用 self
            print(a) # 第一个参数就是传过来的参数

        def ff(self):
            self.sayHi() # 正常方法的调用
            self.tt('dd') # 静态方法的调用

        @classmethod  # 申明此方法是一个类方法，第一个参数是类对象
        def class_method(class_name, arg1):
            c = class_name()
            c.sayHi() # 正常类方法的调用,用之前需要new这个类
            class_name.tt('cc') # 静态方法的调用
            print(arg1) # 第一个参数是类名,第二个参数开始才是传过来的参数

    p = Person()
    p.ff() # 正常方法的调用: self参数不需赋值, 必须先 new 出一个类才可以用

    Person.tt('tt') # 可以直接调用
    p.tt('tt') # 使用实例调用也行
    Person.class_method('cm') # 也可以直接调用


范例(利用 classmethod 实现单例模式)：
    class IOLoop(object):
        def __init__(self):
            print( 'IOLoop.__init__' )

        @classmethod
        def instance(cls):
            if not hasattr(cls, "_instance"):
                cls._instance = cls()
            return cls._instance

        @classmethod
        def initialized(cls):
            """Returns true if the singleton instance has been created."""
            return hasattr(cls, "_instance")

        def service(self):
          print 'Hello,World'

    # 下面调用一下,看看效果
    print( IOLoop.initialized() ) # 打印: False  表示还没有初始化这个类
    ioloop = IOLoop.instance()  # 打印: IOLoop.__init__  表示执行了这个类的 __init__ 构造函数
    ioloop.service() # 打印: Hello,World

    print( IOLoop.initialized() ) # 打印: True   表示已经初始化这个类了
    ioloop = IOLoop.instance() # 没有打印,因为 __init__ 不需要再次执行
    ioloop.service() # 打印: Hello,World


property 属性用法(原理可参考文档“1.6.3.属性”)
  1.现在介绍第一种使用属性的方法(不使用 @property 的写法)：
    在该类中定义三个函数，分别用作赋值、取值和删除变量(此处表达也许不很清晰，请看示例)

    # 假设定义了一个类:C, 该类必须继承自object类, 有一私有变量__x
    class C(object):
        def __init__(self):
            self.__x=None

        # 取值函数
        def getx(self):
            return self.__x

        # 赋值函数
        def setx(self,value):
            self.__x=value

        # 删除函数
        def delx(self):
            #del self.__x
            self.__x=None

        # 定变量名
        # property 函数原型为 property(fget=None, fset=None, fdel=None, doc=None), 所以根据自己需要定义相应的函数即可。
        x = property(getx, setx, delx, '属性x的doc')


    # 现在这个类中的x属性便已经定义好了，我们可以对它进行赋值、取值, 以及删除操作
    c=C() # new 一个实例
    c.x=100 # 赋值
    y=c.x # 取值
    print(y) # 打印: 100
    print(c.x) # 打印: 100

    del c.x # 删除变量
    print(c.x) # 打印: None
    print(C.x.__doc__) # 打印这属性的doc


  2.下面看第二种方法(在py2.6中新增, 使用 @property 修饰符的写法)
    注意同一属性的三个函数名要相同

    # 同样定义一个类:C, 该类也有一私有变量__x
    class C(object):
        def __init__(self):
            self.__x=None

        @property # 申明这是一个属性,同时也定义了取值函数、doc
        def x(self):
            '''属性x的doc
            '''
            return self.__x

        @x.setter # 赋值函数
        def x(self,value):
            self.__x=value

        @x.deleter # 删除函数
        def x(self):
            #del self.__x
            self.__x=None

    # 对属性进行赋值、取值, 以及删除的操作同上例, 不再写



functools 模块提供了两个装饰器。
    这个模块是Python 2.5后新增的，一般来说大家用的应该都高于这个版本。

    wraps(wrapped[, assigned][, updated]):
        函数是有几个特殊属性比如函数名，在被装饰后，上例中的函数名foo会变成包装函数的名字wrapper，这个装饰器可以解决这个问题，它能将装饰过的函数的特殊属性保留。

    total_ordering(cls):
        这个装饰器在特定的场合有一定用处，但是它是在Python 2.7后新增的。
        它的作用是为实现了至少 __lt__, __le__, __gt__, __ge__ 其中一个的类加上其他的比较方法，这是一个类装饰器。
        如果觉得不好理解，不妨仔细看看这个装饰器的源代码。

范例(functools.wraps 装饰器的用法与用途):
    import time
    import functools
    def timeit(func):
        @functools.wraps(func)
        def wrapper():
            start = time.time()
            func()
            end = time.time()
            print('used:', end - start)
        return wrapper

    @timeit
    def foo():
        print('in foo()')

    foo()
    print(foo.__name__) # 打印: foo,  没有 @functools.wraps 装饰过的话,打印 wrapper

    """
    使用 functools.wraps 装饰器，它的作用就是将 被修饰的函数(foo) 的一些属性值赋值给 修饰器函数(wrapper) ，最终让属性的显示更符合我们的直觉。
    其实查看 functools.wraps 装饰器的源码可以看到就是调用了一个函数update_wrapper，
    知道原理后，我们改写上面的代码，在不使用 wraps的情况下，也可以让 foo.__name__ 打印出 foo
    """
    import time
    WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')

    def timeit(func):
        def wrapper():
            start = time.time()
            func()
            end = time.time()
            print('used:', end - start)

        # 属性赋值
        for attr in WRAPPER_ASSIGNMENTS:
            try:
                value = getattr(func, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)
        return wrapper

    @timeit
    def foo():
        print('in foo()')

    foo()
    print(foo.__name__)  # 打印: foo

