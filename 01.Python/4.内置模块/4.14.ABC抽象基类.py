
1.abc 模块作用
    Python 本身不提供抽象类和接口机制，要想实现抽象类，可以借助 abc 模块。
    ABC 是 Abstract Base Class 的缩写。

    ABC(抽象基类)，主要定义了基本类和最基本的抽象方法，可以为子类定义共有的API，不需要具体实现。
    相当于是Java中的接口或者是抽象类。
    抽象基类可以不实现具体的方法而是将其留给派生类实现。
    （当然也可以实现，只不过子类如果想调用抽象基类中定义的方法需要使用super()）

    抽象基类提供了逻辑和实现解耦的能力，即在不同的模块中通过抽象基类来调用，可以用最精简的方式展示出代码之间的逻辑关系，让模块之间的依赖清晰简单。
    同时，一个抽象类可以有多个实现，让系统的运转更加灵活。极简版的抽象类实现，也让代码可读性更高。
    而针对抽象类的编程，让每个人可以关注当前抽象类，只关注其方法和描述，而不需要考虑过多的其他逻辑，这对协同开发有很大意义。

    抽象基类的使用：
    1：直接继承
        直接继承抽象基类的子类就没有这么灵活，抽象基类中可以声明”抽象方法“和“抽象属性”，只有完全覆写（实现）了抽象基类中的“抽象”内容后，才能被实例化，而虚拟子类则不受此影响。
    2：虚拟子类
        将其他的类”注册“到抽象基类下当虚拟子类（调用register方法），虚拟子类的好处是你实现的第三方子类不需要直接继承自基类，可以实现抽象基类中的部分API接口，也可以根本不实现，但是issubclass(), issubinstance()进行判断时仍然返回真值。


2.模块中的类和函数

    abc.ABCMeta
    # 这是用来生成抽象基础类的元类。由它生成的类可以被直接继承。


    from abc import ABCMeta

    class MyABC:
        __metaclass__ = ABCMeta

    MyABC.register(tuple)

    assert issubclass(tuple, MyABC)
    assert isinstance((), MyABC)


实例：
    import abc
    import six

    # 为了解决 Python2&3 的兼容问题，需要引入six模块，该模块中有一个针对类的装饰器 @six.add_metaclass(MetaClass) 可以为两个版本的Python类方便地添加 metaclass
    @six.add_metaclass(abc.ABCMeta)
    class BaseClass(object):

        @abc.abstractproperty # 声明“抽象属性”(只读属性)
        def my_abstract_property(self):
            """
            an abstract property need to be implemented
            """

        # 声明“抽象属性”(读写属性)
        def get_x(self): pass
        def set_x(self, value): pass
        x = abc.abstractproperty(get_x, set_x)

        # 声明“抽象属性”(读写属性)
        def get_y(self): pass
        def set_y(self, value): pass
        y = abc.abstractproperty(get_y, set_y)


        @abc.abstractmethod # 声明“抽象方法”
        def func_a(self, data):
            """
            an abstract method need to be implemented
            """

        @abc.abstractmethod
        def func_b(self, data):
            """
            another abstract method need to be implemented
            """

    # 派生类，直接继承，要求完全实现抽象基类中的“抽象”内容
    class SubclassImpl(BaseClass):

        # 实现抽象属性(只读属性)
        @property
        def my_abstract_property(self):
            return 555


        # 实现抽象属性x (只读属性)
        @property # 申明这是一个属性,同时也定义了取值函数、doc
        def x(self):
            '''属性x的doc'''
            if not hasattr(self, '__x'):
                self.__x=None
            return self.__x

        @x.setter # 赋值函数
        def x(self,value):
            self.__x=value


        # 实现抽象属性y(只读属性)
        y = 1111


        # 实现抽象方法
        def func_a(self, data):
            print("Overriding func_a, " + str(data))

        @staticmethod
        def func_d(c1, data):
            print(type(c1) + str(data))


    # 虚拟子类， 可以实现抽象基类中的部分API接口，也可以根本不实现
    class RegisteredImpl(object):
        @staticmethod
        def func_c(data):
            print("Method in third-party class, " + str(data))
    BaseClass.register(RegisteredImpl)


    if __name__ == '__main__':
        for subclass in BaseClass.__subclasses__():
            print("subclass of BaseClass: " + subclass.__name__)
        print("subclass do not contains RegisteredImpl")
        print("-----------------------------------------------")

        print("RegisteredImpl is subclass: " + str(issubclass(RegisteredImpl, BaseClass)))
        print("RegisteredImpl object  is instance: " + str(isinstance(RegisteredImpl(), BaseClass)))
        print("SubclassImpl is subclass: " + str(issubclass(SubclassImpl, BaseClass)))

        print("-----------------------------------------------")
        obj1 = RegisteredImpl()
        obj1.func_c("RegisteredImpl new object OK!")
        print("-----------------------------------------------")
        obj2 = SubclassImpl()  #由于没有实例化所有的方法，所以这里会报错 Can't instantiate abstract class SubclassImpl with abstract methods func_b
        obj2.func_a("It's right!")

