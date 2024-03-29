元类(metaclass)

类也是对象
    在理解元类之前，你需要先掌握Python中的类。
    Python中类的概念借鉴于 Smalltalk ，这显得有些奇特。
    在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。
    在Python中这一点仍然成立：

        >>> class ObjectCreator(object):
        …       pass
        …
        >>> my_object = ObjectCreator()
        >>> print(my_object)
        <__main__.ObjectCreator object at 0x8974f2c>

    但是，Python中的类还远不止如此。类同样也是一种对象。是的，没错，就是对象。
    只要你使用关键字 class, Python解释器在执行的时候就会创建一个对象。
    下面的代码段：

        >>> class ObjectCreator(object):
        …       pass
        …

    将在内存中创建一个对象，名字就是ObjectCreator。
    这个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。
    但是，它的本质仍然是一个对象，于是乎你可以对它做如下的操作：
        1)   你可以将它赋值给一个变量
        2)   你可以拷贝它
        3)   你可以为它增加属性
        4)   你可以将它作为函数参数进行传递

    下面是示例：

        >>> print(ObjectCreator) # 你可以打印一个类，因为它其实也是一个对象
        <class '__main__.ObjectCreator'>
        >>> def echo(o):
        …       print(o)
        …
        >>> echo(ObjectCreator) # 你可以将类做为参数传给函数
        <class '__main__.ObjectCreator'>
        >>> print(hasattr(ObjectCreator, 'new_attribute'))
        False
        >>> ObjectCreator.new_attribute = 'foo' #  你可以为类增加属性
        >>> print(hasattr(ObjectCreator, 'new_attribute'))
        True
        >>> print(ObjectCreator.new_attribute)
        foo
        >>> ObjectCreatorMirror = ObjectCreator # 你可以将类赋值给一个变量
        >>> print(ObjectCreatorMirror())
        <__main__.ObjectCreator object at 0x8997b4c>


动态地创建类
    因为类也是对象，你可以在运行时动态的创建它们，就像其他任何对象一样。
    首先，你可以在函数中创建类，使用 class 关键字即可。

        >>> def choose_class(name):
        …       if name == 'foo':
        …           class Foo(object):
        …               pass
        …           return Foo # 返回的是类，不是类的实例
        …       else:
        …           class Bar(object):
        …               pass
        …           return Bar
        …
        >>> MyClass = choose_class('foo')
        >>> print(MyClass) # 函数返回的是类，不是类的实例
        <class '__main__'.Foo>
        >>> print(MyClass()) # 你可以通过这个类创建类实例，也就是对象
        <__main__.Foo object at 0x89c6d4c>

    但这还不够动态，因为你仍然需要自己编写整个类的代码。
    由于类也是对象，所以它们必须是通过什么东西来生成的才对。
    当你使用 class 关键字时，Python解释器自动创建这个对象。
    但就和Python中的大多数事情一样，Python仍然提供给你手动处理的方法。
    还记得内建函数 type 吗？这个古老但强大的函数能够让你知道一个对象的类型是什么，就像这样：

        >>> print(type(1))
        <type 'int'>
        >>> print(type("1"))
        <type 'str'>
        >>> print(type(ObjectCreator))
        <type 'type'>
        >>> print(type(ObjectCreator()))
        <class '__main__.ObjectCreator'>

    这里， type 有一种完全不同的能力，它也能动态的创建类。 type 可以接受一个类的描述作为参数，然后返回一个类。
    （我知道，根据传入参数的不同，同一个函数拥有两种完全不同的用法是一件很傻的事情，但这在Python中是为了保持向后兼容性）

    type 可以像这样工作：
    type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
    比如下面的代码：

        >>> class MyShinyClass(object):
        …       pass

    可以手动像这样创建：

        >>> MyShinyClass = type('MyShinyClass', (), {}) # 返回一个类对象
        >>> print(MyShinyClass)
        <class '__main__.MyShinyClass'>
        >>> print(MyShinyClass()) #  创建一个该类的实例
        <__main__.MyShinyClass object at 0x8997cec>

    你会发现我们使用“MyShinyClass”作为类名，并且也可以把它当做一个变量来作为类的引用。
    类和变量是不同的，这里没有任何理由把事情弄的复杂。
    type 接受一个字典来为类定义属性，因此

        >>> class Foo(object):
        …       bar = True

    可以翻译为：

        >>> Foo = type('Foo', (), {'bar':True})

    并且可以将Foo当成一个普通的类一样使用：

        >>> print(Foo)
        <class '__main__.Foo'>
        >>> print(Foo.bar)
        True
        >>> f = Foo()
        >>> print(f)
        <__main__.Foo object at 0x8a9b84c>
        >>> print(f.bar)
        True

    当然，你可以向这个类继承，所以，如下的代码：

        >>> class FooChild(Foo):
        …       pass

    就可以写成：

        >>> FooChild = type('FooChild', (Foo,),{})
        >>> print(FooChild)
        <class '__main__.FooChild'>
        >>> print(FooChild.bar) # bar属性是由Foo继承而来
        True

    最终你会希望为你的类增加方法。只需要定义一个有着恰当签名的函数并将其作为属性赋值就可以了。

        >>> def echo_bar(self):
        …       print(self.bar)
        …
        >>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
        >>> hasattr(Foo, 'echo_bar')
        False
        >>> hasattr(FooChild, 'echo_bar')
        True
        >>> my_foo = FooChild()
        >>> my_foo.echo_bar()
        True

    你可以看到，在Python中，类也是对象，你可以动态的创建类。
    这就是当你使用关键字 class 时Python在幕后做的事情，而这就是通过元类来实现的。


到底什么是元类（终于到主题了）
    元类就是用来创建类的“东西”。
    你创建类就是为了创建类的实例对象，不是吗？
    但是我们已经学习到了Python中的类也是对象。
    好吧，元类就是用来创建这些类（对象）的，元类就是类的类，你可以这样理解 为：

        MyClass = MetaClass()
        MyObject = MyClass()

    你已经看到了 type 可以让你像这样做：

        MyClass = type('MyClass', (), {})

    这是因为函数 type 实际上是一个元类。
    type 就是Python在背后用来创建所有类的元类。
    现在你想知道那为什么 type 会全部采用小写形式而不是 Type 呢？
    好吧，我猜这是为了和 str 保持一致性， str 是用来创建字符串对象的类，而 int 是用来创建整数对象的类。
    type 就是创建类对象的类。你可以通过检查 __class__ 属性来看到这一点。
    Python中所有的东西，注意，我是指所有的东西——都是对象。
    这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。

        >>> age = 35
        >>> age.__class__
        <type 'int'>
        >>> name = 'bob'
        >>> name.__class__
        <type 'str'>
        >>> def foo(): pass
        >>>foo.__class__
        <type 'function'>
        >>> class Bar(object): pass
        >>> b = Bar()
        >>> b.__class__
        <class '__main__.Bar'>

    现在，对于任何一个 __class__ 的 __class__ 属性又是什么呢？

        >>> a.__class__.__class__
        <type 'type'>
        >>> age.__class__.__class__
        <type 'type'>
        >>> foo.__class__.__class__
        <type 'type'>
        >>> b.__class__.__class__
        <type 'type'>

    因此，元类就是创建类这种对象的东西。
    如果你喜欢的话，可以把元类称为“类工厂”（不要和工厂类搞混了:D）
    type 就是Python的内建元类，当然了，你也可以创建自己的元类。

        >>> class Something(object):
        ...     pass
        ...
        >>> Something
        <class '__main__.Something'>
        >>> type(Something)
        <type 'type'>
        >>> type(int) # 说明 int 类是用 type 创建的
        <type 'type'>
        >>> type(type) # 说明 type 类也是用 type 创建的
        <type 'type'>


__metaclass__ 属性
    你可以在写一个类的时候为其添加 __metaclass__ 属性。

        # py2.x 的元类继承写法
        class Foo(object):
            __metaclass__ = something…
        […]

        # py3.x 的元类继承写法
        class Foo(object, metaclass = something…):
            pass


    如果你这么做了，Python就会用元类来创建类Foo。小心点，这里面有些技巧。
    你首先写下 class Foo(object)，但是类对象Foo还没有在内存中创建。
    Python会在类的定义中寻找 __metaclass__ 属性，如果找到了，Python就会用它来创建类Foo，如果没有找到，就会用内建的 type 来创建这个类。
    把下面这段话反复读几次。当你写如下代码时:

        class Foo(Bar):
            pass

    Python做了如下的操作：
    Foo中有 __metaclass__ 这个属性吗？如果是，Python会在内存中通过 __metaclass__ 创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）。
    如果Python没有找到 __metaclass__ ，它会继续在Bar（父类）中寻找 __metaclass__ 属性，并尝试做和前面同样的操作。
    如果Python在任何父类中都找不到 __metaclass__ ，它就会在模块层次中去寻找 __metaclass__ ，并尝试做同样的操作。
    如果还是找不到 __metaclass__ ，Python就会用内置的 type 来创建这个类对象。

    现在的问题就是，你可以在 __metaclass__ 中放置些什么代码呢？答案就是：可以创建一个类的东西。
    那么什么可以用来创建一个类呢？ type ，或者任何使用到 type 或者子类化 type 的东东都可以。


自定义元类
    元类的主要目的就是为了当创建类时能够自定义地改变类。
    通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。
    假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。
    有好几种方法可以办到，但其中一种就是通过在模块级别设定 __metaclass__ 。
    采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

    幸运的是， __metaclass__ 实际上可以被任意调用，它并不需要是一个正式的类（我知道，某些名字里带有‘class’的东西并不需要是一个 class ，画画图理解下，这很有帮助）。
    所以，我们这里就先以一个简单的函数作为例子开始。

        # 元类会自动将你通常传给‘type’的参数作为自己的参数传入
        def upper_attr(future_class_name, future_class_parents, future_class_attr):
            '''返回一个类对象，将属性都转为大写形式'''

            # 选择所有不以'__'开头的属性
            attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))

            # 将它们转为大写形式
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)

            # 通过'type'来做类对象的创建
            return type(future_class_name, future_class_parents, uppercase_attr)

        # 这会作用到这个模块中的所有类
        __metaclass__ = upper_attr

        # 注意：这里绝不能继承 object 类。
        # 否则按 __metaclass__ 的查找顺序会去查找 父类object 的 __metaclass__ ， 再去查找 父类object 的模块的 __metaclass__ 。那就导致这模块的 __metaclass__ 失效。
        # 另外，发现在 py2.6、py2.7 中这样可运行成功。但 py3.x 失败，估计是不再允许作用于整个模块的元类。
        class Foo():

            # 我们也可以只在这里定义 __metaclass__ ，这样就只会作用于这个类中
            bar = 'bip'

        print( hasattr(Foo, 'bar') ) # 输出: False
        print( hasattr(Foo, 'BAR') ) # 输出:True

        f = Foo()
        print( f.BAR ) # 输出:'bip'


    现在让我们再做一次，这一次用一个真正的 class 来当做元类。

        # 请记住，'type'实际上是一个类，就像'str'和'int'一样。 所以，你可以从type继承
        class UpperAttrMetaClass(type):

            # __new__ 是在 __init__ 之前被调用的特殊方法
            # __new__ 是用来创建对象并返回之的方法
            # 而 __init__ 只是用来将传入的参数初始化给对象
            # 你很少用到 __new__ ，除非你希望能够控制对象的创建
            # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写 __new__
            # 如果你希望的话，你也可以在 __init__ 中做些事情
            # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用

            def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
                attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
                uppercase_attr = dict((name.upper(), value) for name, value in attrs)
                return type(future_class_name, future_class_parents, uppercase_attr)
                # 这写法只能供本类的 __metaclass__ 来用， 如果是子类则不生效。


    但是，这种方式其实不是OOP。我们直接调用了 type ，而且我们没有改写父类的 __new__ 方法。现在让我们这样去处理:

        class UpperAttrMetaclass(type):
            def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
                attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
                uppercase_attr = dict((name.upper(), value) for name, value in attrs)
                # 复用type.__new__方法
                # 这就是基本的OOP编程，没什么魔法
                return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)
                # 这写法即使是子类也会生效。

    你可能已经注意到了有个额外的参数 upperattr_metaclass ，这并没有什么特别的。
    类方法的第一个参数总是表示当前的实例，就像在普通的类方法中的 self 参数一样。
    当然了，为了清晰起见，这里的名字我起的比较长。但是就像 self 一样，所有的参数都有它们的传统名称。
    因此，在真实的产品代码中一个元类应该是像这样的：

        class UpperAttrMetaclass(type):
            def __new__(cls, name, bases, dct):
                attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
                uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
                return type.__new__(cls, name, bases, uppercase_attr)

    如果使用 super 方法的话，我们还可以使它变得更清晰一些，这会缓解继承
    （是的，你可以拥有元类，从元类继承，从 type 继承）

        class UpperAttrMetaclass(type):

            # cls: 将要创建的类，类似与self，但是self指向的是instance，而这里cls指向的是class
            # name: 类的名字，也就是我们通常用类名.__name__获取的。
            # bases: 基类的元组
            # attrs: 属性的dict。dict的内容可以是变量(类属性），也可以是函数（类方法）。
            def __new__(cls, name, bases, dct):
                attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
                uppercase_attr = dict((name.upper(), value) for name, value in attrs)
                return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

    就是这样，除此之外，关于元类真的没有别的可说的了。
    使用到元类的代码比较复杂，这背后的原因倒并不是因为元类本身，而是因为你通常会使用元类去做一些晦涩的事情，依赖于自省，控制继承等等。
    确实，用元类来搞些“黑暗魔法”是特别有用的，因而会搞出些复杂的东西来。
    但就元类本身而言，它们其实是很简单的：
        1)   拦截类的创建
        2)   修改类
        3)   返回修改之后的类


为什么要用 metaclass 类而不是函数?
    由于 __metaclass__ 可以接受任何可调用的对象，那为何还要使用类呢，因为很显然使用类会更加复杂啊？这里有好几个原因：
        1） 意图会更加清晰。当你读到 UpperAttrMetaclass(type) 时，你知道接下来要发生什么。
        2） 你可以使用OOP编程。元类可以从元类中继承而来，改写父类的方法。元类甚至还可以使用元类。
        3） 你可以把代码组织的更好。当你使用元类的时候肯定不会是像我上面举的这种简单场景，通常都是针对比较复杂的问题。将多个方法归总到一个类中会很有帮助，也会使得代码更容易阅读。
        4） 你可以使用 __new__, __init__ 以及 __call__ 这样的特殊方法。它们能帮你处理不同的任务。就算通常你可以把所有的东西都在 __new__ 里处理掉，有些人还是觉得用 __init__ 更舒服些。
        5） 哇哦，这东西的名字是 metaclass ，肯定非善类，我要小心！

    究竟为什么要使用元类？
    现在回到我们的大主题上来，究竟是为什么你会去使用这样一种容易出错且晦涩的特性？好吧，一般来说，你根本就用不上它：

    “元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。”  —— Python界的领袖 Tim Peters

    元类的主要用途是创建API。一个典型的例子是 Django ORM 。它允许你像这样定义：

        class Person(models.Model):
            name = models.CharField(max_length=30)
            age = models.IntegerField()

    但是如果你像这样做的话：

        guy  = Person(name='bob', age='35')
        print(guy.age)

    这并不会返回一个 IntegerField 对象，而是会返回一个 int ，甚至可以直接从数据库中取出数据。
    这是有可能的，因为 models.Model 定义了 __metaclass__ ， 并且使用了一些魔法能够将你刚刚定义的简单的Person类转变成对数据库的一个复杂hook。
    Django框架将这些看起来很复杂的东西通过暴露出一个简单的使用元类的API将其化简，通过这个API重新创建代码，在背后完成真正的工作。


结语
    首先，你知道了类其实是能够创建出类实例的对象。
    好吧，事实上，类本身也是实例，当然，它们是元类的实例。

        >>>class Foo(object): pass
        >>>id(Foo)

    Python中的一切都是对象，它们要么是类的实例，要么是元类的实例，除了 type 。
    type 实际上是它自己的元类，在纯Python环境中这可不是你能够做到的，这是通过在实现层面耍一些小手段做到的。
    其次，元类是很复杂的。对于非常简单的类，你可能不希望通过使用元类来对类做修改。
    你可以通过其他两种技术来修改类：
        1） Monkey patching
        2)  class decorators

    当你需要动态修改类时，99%的时间里你最好使用上面这两种技术。
    当然了，其实在99%的时间里你根本就不需要动态修改类 :D


范例(使用元类实现单例)：
    class Singleton(type):
        # 每次 new MyClass类 时都会执行， 且首参数 cls 是 MyClass类 而不是 MyClass类实例(因为这是元类)。
        def __call__(cls, *args, **kw):
            if not hasattr(cls, '_instance'):
                cls._instance = super(Singleton, cls).__call__(*args, **kw)
            return cls._instance

    # py2.x 的元类继承写法
    class MyClass(object):
        __metaclass__ = Singleton

    # py3.x 的元类继承写法
    class MyClass(object, metaclass = Singleton):
        pass


范例(各函数的执行顺序)
    class ConstType(type):
        """生成 Class类 的构造器"""

        def __new__(mcs, name, bases, attrs):
            """本元类的 __new__ 会先于 __init__ 执行
            返回本类的实例，也是 Class类 的构造类型。且返回的结果将传给 本元类的 __init__ 及 __call__
            """
            print('... 2.1. metaclass __new__ ...', mcs, id(mcs), name, bases, attrs)
            meta_cls = type.__new__(mcs, name, bases, attrs)  # 返回一个类，而不是类实例
            print('... 2.2. metaclass __new__ ...', meta_cls, type(meta_cls), id(meta_cls))
            return meta_cls

        def __init__(cls, *args, **kwargs):
            """这函数等 __new__ 执行完再执行，且接收的参数 cls 是 metaclass __new__ 的返回值"""
            print('... 3.1. metaclass __init__ ...', cls, type(cls), id(cls), args, kwargs)
            super(ConstType, cls).__init__(*args, **kwargs)

        def __call__(cls, *args, **kwargs):
            """每次 new Class类 时都会执行， 且首参数 cls 是 Class类(本元类的 __new__ 的返回值) 而不是 Class类实例(因为这是元类)
            这函数的返回值，是个 Class类实例，将作为 new 一个 Class类的返回实例。
            """
            print('... 4.1. metaclass __call__ ...', cls, type(cls), id(cls), args, kwargs)
            obj = super(ConstType, cls).__call__(*args, **kwargs)  # 这将执行 Class类 的 __new__ 及 __init__
            # 返回的 obj 实际上由 Class类的 __new__ 生成
            print('... 4.2. metaclass __call__ ...', obj, type(obj), id(obj))
            return obj

    """
    # 由于py2及py3的使用元类写法不一致，这里为了兼容且不引起编译报错，改用统一写法
    if PY2:
        class Const(object):
            __metaclass__ = ConstType
    elif PY3:
        class Const(object, metaclass=ConstType):  # 这样写，py2编译时会报错。
            pass
    """
    Const = ConstType('Const', (object,), {})  # 这里会触发一次构造 Const 类的 metaclass __new__
    print('------- 1 -----')

    class Person(Const):
        name = 'person'
        print('... 1. load class attribute ...')

        def __new__(cls, *args, **kwargs):
            """本类的 __new__ 会先于 __init__ 执行
            返回本类的实例。且返回的结果将传给 本类的 __init__ 及 __call__
            """
            print('... 5.1. class __new__ ...', cls, type(cls), id(cls), args, kwargs)
            obj = super(Person, cls).__new__(cls)  # 返回一个本类的实例
            print('... 5.2. class __new__ ...', obj, type(obj), id(obj))
            return obj

        def __init__(self, *args, **kwargs):
            """这函数等 __new__ 执行完再执行，且接收的参数 self 是 本类的 __new__ 的返回值"""
            print('... 6. class __init__ ...', self, type(self), id(self), args, kwargs)
            self.name = args[0]
            super(Person, self).__init__()

        def __call__(self, *args, **kwargs):
            """本类的实例被调用时触发"""
            print('... 7. class __call__ ...', self, type(self), id(self), args, kwargs)
            return self.name

    # 此前，类的加载依次是 load class attribute、metaclass __new__、metaclass __init__
    print('------- 2 -----')
    print(Person.name)
    print('------- 3 -----')

    person = Person('teacher 1')  # 这里依次调用 metaclass __call__、class __new__、class __init__。 返回值 p 是由 metaclass __call__ 返回
    # 由于这里的 Person() 返回值是由 metaclass __call__ 返回，所以单例模式由 metaclass __call__ 实现。
    print('------- 4 -----')
    person('student 1')
    print('------- 5 -----')
    person2 = Person('teacher 2')
    person2('student 2')

    """ 打印结果如下，可以看出各个函数的执行顺序及参数传递
    ... 2.1. metaclass __new__ ... <class '__main__.ConstType'> 140668374627912 Const (<class 'object'>,) {}
    ... 2.2. metaclass __new__ ... <class '__main__.Const'> <class '__main__.ConstType'> 140668374629992
    ... 3.1. metaclass __init__ ... <class '__main__.Const'> <class '__main__.ConstType'> 140668374629992 ('Const', (<class 'object'>,), {}) {}
    ------- 1 -----
    ... 1. load class attribute ...
    ... 2.1. metaclass __new__ ... <class '__main__.ConstType'> 140668374627912 Person (<class '__main__.Const'>,) {'__module__': '__main__', '__qualname__': 'Person', 'name': 'person', '__new__': <function Person.__new__ at 0x1060d2ea0>, '__init__': <function Person.__init__ at 0x1060d2f28>, '__call__': <function Person.__call__ at 0x106144048>, '__classcell__': <cell at 0x10609c798: empty>}
    ... 2.2. metaclass __new__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920
    ... 3.1. metaclass __init__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920 ('Person', (<class '__main__.Const'>,), {'__module__': '__main__', '__qualname__': 'Person', 'name': 'person', '__new__': <function Person.__new__ at 0x1060d2ea0>, '__init__': <function Person.__init__ at 0x1060d2f28>, '__call__': <function Person.__call__ at 0x106144048>, '__classcell__': <cell at 0x10609c798: ConstType object at 0x7fefe8804208>}) {}
    ------- 2 -----
    person
    ------- 3 -----
    ... 4.1. metaclass __call__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920 ('teacher 1',) {}
    ... 5.1. class __new__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920 ('teacher 1',) {}
    ... 5.2. class __new__ ... <__main__.Person object at 0x10616b710> <class '__main__.Person'> 4397119248
    ... 6. class __init__ ... <__main__.Person object at 0x10616b710> <class '__main__.Person'> 4397119248 ('teacher 1',) {}
    ... 4.2. metaclass __call__ ... <__main__.Person object at 0x10616b710> <class '__main__.Person'> 4397119248
    ------- 4 -----
    ... 7. class __call__ ... <__main__.Person object at 0x10616b710> <class '__main__.Person'> 4397119248 ('student 1',) {}
    ------- 5 -----
    ... 4.1. metaclass __call__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920 ('teacher 2',) {}
    ... 5.1. class __new__ ... <class '__main__.Person'> <class '__main__.ConstType'> 140668374630920 ('teacher 2',) {}
    ... 5.2. class __new__ ... <__main__.Person object at 0x10616b748> <class '__main__.Person'> 4397119304
    ... 6. class __init__ ... <__main__.Person object at 0x10616b748> <class '__main__.Person'> 4397119304 ('teacher 2',) {}
    ... 4.2. metaclass __call__ ... <__main__.Person object at 0x10616b748> <class '__main__.Person'> 4397119304
    ... 7. class __call__ ... <__main__.Person object at 0x10616b748> <class '__main__.Person'> 4397119304 ('student 2',) {}
    """


