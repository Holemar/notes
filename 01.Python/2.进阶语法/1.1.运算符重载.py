
Python中常见运算符重载方法
      方法                重构               调用
    __init__            构造函数            对象建立：X = Class(args)
    __del__             析构函数            X对象收回
    __add__             运算符+             如果没有_iadd_, X + Y, X += Y
    __or__              运算符|(位OR)       如果没有 _ior_, X | Y, X |= Y
    __repr__, __str__   打印，转换          print(X), repr(X), str(X)
    __call__            函数调用            X(*args, **kargs)
    __getattr__         点号运算            X.undefined
    __setattr__         属性赋值语句         X.any = value
    __delattr__         属性删除            del X.any
    __getattribute__    属性获取            X.any
    __getitem__         索引运算            X[key], X[i:j], 没__iter__时的for循环和其他迭代器
    __setitem__         索引赋值语句         X[key] = value, X[i:j] = sequence
    __delitem__         索引和分片删除       del X[key], del X[i:j]
    __len__             长度               len(X), 如果没有__bool__, 真值测试
    __bool__            布尔测试            bool(X), 真测试（在python2.6中叫做_
    __lt__, __gt__      特定比较            X < Y, X > Y, X <= Y, X >= Y
    __le__, __ge__      特定比较            X == Y, X != Y
    __radd__            右侧加法            other + X
    __iadd__            实地（增强的）加法    X += Y (or else add
    __iter__, __next__  迭代环境            I = iter(X), next(I); for loops,
    __contains__        成员关系测试         item in X(任何可迭代的对象)
    __index__           整数值              hex(X), bin(X), oct(X), O[X], O[X:]
    __enter__, __exit__ 环境管理器           with obj as var:
    __get__, __set__    描述符属性           X.attr, X.attr = value, del X.value
    __delete__          描述符属性           descr.__delete__(self, obj) –> None
    __new__             创建                在 __init__ 之前创建对象


构造函数和析构函数: __init__ 和 __del__
  它们的主要作用是进行对象的创建和回收，当实例创建时，就会调用__init__构造方法。当实例对象被收回时，析构函数__del__会自动执行。
  范例：
    class Human(object):
        def __init__(self, n):
            self.name = n
            print("__init__ ",self.name)
        def __del__(self):
            print("__del__")

    h = Human('Tim')  # __init__  Tim
    h = 'a'  # __del__


索引取值和赋值: __getitem__, __setitem__
  通过实现这两个方法，可以通过诸如 X[i] 的形式对对象进行取值和赋值，还可以对对象使用切片操作。
  范例：
    class Indexer(object):
        data = [1, 2, 3, 4, 5, 6]

        def __getitem__(self, index):
            print(self.data[index])
            return self.data[index]

        def __setitem__(self, k, v):
            self.data[k] = v
            print(self.data)

    i = Indexer()
    i[0] # 1
    i[1:4] # [2, 3, 4]
    i[0]=10 # [10, 2, 3, 4, 5, 6]


设置和访问属性: __getattr__ , __setattr__
  我们可以通过重载 __getattr__ 和 __setattr__ 来拦截对对象成员的访问。
  __getattr__ 在访问对象中不存在的成员时会自动调用。
  __setattr__ 方法用于在初始化对象成员的时候调用，即在设置 __dict__ 的item时就会调用 __setattr__ 方法。
  __delattr__ 方法将拦截所有的属性删除
  __getattribute__ 方法将拦截所有属性的获取(不管该属性是否已经定义，只要获取它的值，该方法都会调用)
        当一个类中同时重载了 __getattr__ 和 __getattribute__ 方法，那么 __getattr__ 也会被调用(当获取的属性未定义时)，但是 __getattribute__ 先调用。
        另外， __getattribute__ 方法仅仅存在于 Python2.6 的新式类和 Python3 的所有类中；

  范例：
	class A(object):
		def __init__(self, ax, bx):
			self.a = ax
			self.b = bx

		def f(self):
			print (self.__dict__)

		def __getattr__(self, name):
			print ("__getattr__")

		def __setattr__(self, name, value):
			print ("__setattr__")
			self.__dict__[name] = value

	a = A(1, 2)  # 初始化函数里面设置了 self.a 和 self.b,所以打印： __setattr__ \n __setattr__
	a.f()  # {'a': 1, 'b': 2}
	print(a.x)  # __getattr__ \n None
	a.x = 3  # __setattr__
	a.f()  # {'a': 1, 'b': 2, 'x': 3}
	print(a.x)  # 3


委托->包装对象
  委托，字面理解就是，假装这件事是我在做，但是事实上我委托了其他人来帮我处理这件事。
  python中的委托，和现实中的委托是何其相似！
  范例：
	class Wrapper(object):
		def __init__(self, obj):
			self.wrapper = obj

		def __getattr__(self, item):
			print("trace:", item)
			return getattr(self.wrapper, item)

	if __name__ == '__main__':
		x = Wrapper([1, 2, 3, 4])
		x.append(35)  # trace: append
		x.remove(2)  # trace: remove
		print(x.wrapper)  # [1, 3, 4, 35]
		x.append(11)  # trace: append
		print(x.wrapper)  # [1, 3, 4, 35, 11]


