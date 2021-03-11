
class 里面的 __slots__
	__slots__ 本质上是一个类变量，变量的值可以是元组、列表、任何可迭代对象，当然也可以是一个字符串，但那就意味着该类只有一个成员变量。
	由于每次实例化一个类都要分配一个新的 __dict__，存在空间的浪费，因此有了 __slots__ 。它包括了当前能访问到的属性。
	当定义了slots后，slots中定义的变量变成了类的描述符。类的实例只能拥有slots中定义的变量，不能再增加新的变量。
	注意：定义了 __slots__ 后，就不再有 __dict__。


1.限制 class 的属性

	class Student(object):
		__slots__ = ('name', 'age')  # 用 __slots__ 定义允许绑定的属性名称

	s = Student()  # 创建新的实例
	s.name = 'Michael'
	s.age = 25
	try:
		s.score = 99  # 报错: AttributeError: 'Student' object has no attribute 'score'
	except AttributeError as e:
		print(e)

	# 使用__slots__要注意，__slots__ 定义的属性限制仅对当前类起作用，对继承的子类是不起作用的：
	class GraduateStudent(Student):
		pass

	g = GraduateStudent()
	g.score = 9999  # 不报错

	'''
	常见误区：
	关于 __slots__ 的一个常见误区是它可以作为一个封装工具来防止用户给实例增加新的属性。
	尽管它可以达到这样的目的,但是这个并不是它的初衷。更多的是用来作为一个内存优化工具。
	'''


2.性能提升
	from timeit import repeat

	class A(object): pass

	class B(object): __slots__ = ('x')

	def get_set_del_fn(obj):
		def get_set_del():
			obj.x = 1
			obj.x
			del obj.x
		return get_set_del

	a = A()
	b = B()
	ta = sum(repeat(get_set_del_fn(a), repeat=10))  # repeat函数: 重复执行传入函数10次(repeat参数指定次数,默认3次)，返回执行时间列表
	tb = sum(repeat(get_set_del_fn(b), repeat=10))
	print("%.2f%%" % ((ta/tb - 1)*100))  # 在本人电脑上测试速度有10%-30%左右的提升


3.节省内存
	import sys

	class Student(object):
		__slots__ = ('name', 'age')

		def __init__(self, name, age):
			self.name = name
			self.age = age

	class Student2(object):

		def __init__(self, name, age):
			self.name = name
			self.age = age

	s1 = Student('Michael', 25)
	s2 = Student2('Michael', 25)

	s1_size = sum(sys.getsizeof(getattr(s1, k, None)) for k in dir(s1))
	s2_size = sum(sys.getsizeof(getattr(s2, k, None)) for k in dir(s2))
	print(s1_size)  # 使用了slots的内存使用量，打印: 2421
	print(s2_size)  # 直接建类的内存使用量，打印: 2653


4.查看 __dict__

	class Student(object):
		__slots__ = ('name', 'age')

	class GraduateStudent(Student):
		pass

	s = Student()  # 创建新的实例
	s.name = 'Michael'
	s.age = 25
	print(s.__slots__)  # 打印: ('name', 'age')
	try:
		print(s.__dict__)  # 报错: AttributeError: 'svc' object has no attribute '__dict__'
	except AttributeError as e:
		print(e)

	g = GraduateStudent()
	g.score = 9999  # 不报错
	g.name = 'Lily'
	g.age = 21
	print(g.__dict__)  # 已存在 __slots__ 的属性不再分配空间到 __dict__ 里面,打印: {'score': 9999}
	print(g.__slots__)  # 打印: ('name', 'age')


5.不同实例之间，互不干扰
	# 这并没有什么好奇怪的，普通的类本就是这样。但下面的类成员变量会干扰实例，这里仅为下面内容铺垫
	class Base(object):
		__slots__ = ('y',)

	b1 = Base()
	b2 = Base()
	b1.y = 66
	b2.y = 33
	print(b1.y)  # 打印: 66
	print(b2.y)  # 打印: 33


5.0 如果类变量与slots中的变量同名，则该变量被设置为readonly！
	# 以下写法在 py2.7 中允许这样定义类。但在 py3.6 中这样定义类会报错 ValueError: 'y' in __slots__ conflicts with class variable
	class Base(object):
		__slots__ = ('y',)
		y = 22  # y是类变量,y与__slots__中的变量同名


	b = Base()
	print(b.y)  # 打印: 22
	print(Base.y)  # 打印: 22
	try:
		b.y = 66  # AttributeError: 'base' object attribute 'y' is read-only
	except AttributeError as e:
		print(e)


5.1 如果设置了slots的类变量，则该变量被设置为 readonly！

	class Base(object):
		__slots__ = ('y',)


	b1 = Base()
	b2 = Base()
	b1.y = 66
	print(b1.y)  # 打印: 66
	print(Base.y)  # 打印: <member 'y' of 'Base' objects>
	try:
		print(b2.y)  # 报错 AttributeError: y
	except AttributeError as e:
		print(e)

	Base.y = 11  # 这样当作成员变量设置之后，所有实例都受影响，变成对实例 readonly 且值也被统一修改了。
	print(b1.y)  # 打印: 11
	print(b2.y)  # 打印: 11
	print(Base.y)  # 打印: 11

	try:
		b1.y = 66  # 报错 AttributeError: 'Base' object attribute 'y' is read-only
	except AttributeError as e:
		print(e)

	try:
		b2.y = 22  # 报错 AttributeError: 'Base' object attribute 'y' is read-only
	except AttributeError as e:
		print(e)

	# 继承的子类，不受 readonly 影响
	class Student(Base):
		pass

	s1 = Student()
	s1.y = 55
	print(s1.y)  # 打印: 55


5.2 如果类定义时设置了slots的类变量，则该变量被设置为 readonly！
	class Base(object):
		__slots__ = ('y',)
		x = 22  # 允许额外定义属性，但对实例来说，它是 readonly 的，仅允许当成员变量用


	b = Base()
	print(b.x)  # 打印: 22
	print(Base.x)  # 打印: 22

	try:
		b.x = 5  # 报错 AttributeError: 'Base' object attribute 'x' is read-only
	except AttributeError as e:
		print(e)

	Base.x = 5
	print(b.x)  # 打印: 5
	print(Base.x)  # 打印: 5

	# 继承的子类，不受 readonly 影响
	class Student(Base):
		pass

	s1 = Student()
	s1.x = 55
	print(s1.x)  # 打印: 55

