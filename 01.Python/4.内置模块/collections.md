
# collections 容器的集合
`collections`模块实现了特定目标的容器，以提供Python标准内建容器`dict` ,`list` , `set`, 和`tuple`的替代选择。

函数名 | 基类                                            | 含义
--- |-----------------------------------------------| ---
`namedtuple`	| 无 | 创建命名元组子类的工厂函数，生成可以使用名字来访问元素内容的`tuple`子类
`deque`	| object | 类似列表(`list`)的容器，实现了在两端快速添加(`append`)和弹出(`pop`) 
`ChainMap`	| collections.abc.MutableMapping | 类似字典(`dict`)的容器类，将多个映射集合到一个视图里面 
`Counter`	| dict | 字典的子类，提供了可哈希对象的计数功能 
`OrderedDict`	| dict | 字典的子类，保存了他们被添加的顺序，有序字典 
`defaultdict`	| dict | 字典的子类，提供了一个工厂函数，为字典查询提供一个默认值 
`UserDict`	| collections.abc.MutableMapping | 封装了字典对象，简化了字典子类化 
`UserList`	| collections.abc.MutableSequence | 封装了列表对象，简化了列表子类化
`UserString`	| collections.abc.Sequence | 封装了字符串对象，简化了字符串子类化（中文版翻译有误）


## `defaultdict`
`defaultdict`可以说是这个库当中使用最简单的一个，并且它的定义也很简单，我们从名称基本上就能看得出来。  
它解决的是我们使用dict当中最常见的问题，就是key为空的情况。

在正常情况下，我们在dict中获取元素的时候，都需要考虑key为空的情况。如果不考虑这点，那么当我们获取了一个不存在的key，会导致系统抛出异常。  
我们当然可以在每次get之前写一个if判断，但是稍微麻烦点，或者使用dict当中为我们提供带默认值的get方法。

举个例子，比如当key存在重复，我们希望将key相同的value存进一个list当中：
```python
data = [(1, 3), (2, 1), (1, 4), (2, 5), (3, 7)]
d = {}

for k, v in data:
    if k in d:
        d[k].append(v)
    else:
        d[k] = [v]

print(d)  # 打印: {1: [3, 4], 2: [1, 5], 3: [7]}
```

这个例子也可以改成使用dict当中为我们提供带默认值的get方法：
```python
data = [(1, 3), (2, 1), (1, 4), (2, 5), (3, 7)]
d = {}

for k, v in data:
    cur = d.get(k, [])
    cur.append(v)
    d[k] = cur

print(d)  # 打印: {1: [3, 4], 2: [1, 5], 3: [7]}
```

上面两种写法都比较复杂，我们试试使用`collections`当中的`defaultdict`：
```python
from collections import defaultdict
data = [(1, 3), (2, 1), (1, 4), (2, 5), (3, 7)]
d = defaultdict(list)

for k, v in data:
    d[k].append(v)

print(d)  # 打印: defaultdict(<class 'list'>, {1: [3, 4], 2: [1, 5], 3: [7]})
```

使用`defaultdict`之后，如果key不存在，容器会自动返回我们预先设置的默认值。  
需要注意的是`defaultdict`传入的默认值可以是一个类型也可以是一个方法。  
如果我们传入`int`，那么默认值会被设置成`int()`的结果，也就是`0`，如果我们想要自定义或者修改，我们可以传入一个方法，比如：

```python
from collections import defaultdict
data = [(1, 3), (2, 1), (1, 4), (2, 5), (3, 7)]
d = defaultdict(lambda: 3)  # 直接写 defaultdict(3) 会报错： TypeError: first argument must be callable or None

for k, v in data:
    d[k] += v

print(d)  # 打印: defaultdict(<function <lambda> at 0x1041cf040>, {1: 10, 2: 9, 3: 10})
```

## `Counter`
在我们实际的编程当中，我们经常遇到一个问题，就是数数和排序。  
`Counter`是一个`dict`的子类，用于计数可哈希对象。  
比如说我们在分析文本的时候，会得到一堆单词。于是我们希望计算一下这些单词出现过的数量，只保留出现次数最高的若干个。

这个需求让我们自己实现当然也不困难，我们完全可以创建一个`dict`，然后对这些单词一个一个遍历。  
原本我们还需要考虑单词之前没有出现过的情况，如果我们上面说的`defaultdict`，又要简单许多。  
但是我们还是少不了计数然后排序的步骤，如果使用`Counter`这个步骤会缩减成一行代码。

```python
words = ['apple', 'apple', 'pear', 'watermelon', 'pear', 'peach']

from collections import Counter
counter = Counter(words)

print(counter)  # 打印: Counter({'apple': 2, 'pear': 2, 'watermelon': 1, 'peach': 1})

# 如果我们要筛选topK，也非常简单，它为我们提供了most_common方法，我们只需要传入需要求的K即可：
print(counter.most_common(2))  # 打印： [('apple', 2), ('pear', 2)]

# 由于 Counter 是 dict 的子类，也能按 dict 来使用
print(counter.items())  # 打印: dict_items([('apple', 2), ('pear', 2), ('watermelon', 1), ('peach', 1)])
```

除此之外，它的构造函数还接收`dict`类型。我们可以直接通过一个value是`int`类型的`dict`来初始化一个`Counter`，比如：

```python
from collections import Counter
c = Counter({'apple': 5, 'pear': 4})
c = Counter(apple=4, pear=3)
```
它还支持加减法的操作，比如我们可以将两个`Counter`相加，它会自动将两个`Counter`合并，相同的key对应的value累加。  
相减也是同理，会将能对应的value做减法，被减的key对应不上的会保留，而减数中对应不上的key则会被丢弃。  
并且需要注意，`Counter`支持value为负数。

## `deque`
我们都知道`queue`是队列，`deque`也是队列，不过稍稍特殊一些，是双端队列。  
对于`queue`来说，只允许在队尾插入元素，在队首弹出元素。而`deque`既然称为双端队列，那么说明它的队首和队尾都支持元素的插入和弹出。  

除了常用的`clear`、`copy`、`count`、`extend`等api之外，`deque`当中最常用也是最核心的api还有`append`、`pop`、`appendleft`和`popleft`。  
从名字上我们就看得出来，`append`和`pop`和`list`的`append`和`pop`一样，而`appendleft`和`popleft`则是在队列左侧，也就是头部进行`pop`和`append`的操作。

大多数情况下我们使用`deque`主要有两个原因，第一个原因是`deque`受到GIL的管理，它是线程安全的。  
而`list`则没有GIL锁，因此不是线程安全的。也就是说在并发场景下，`list`可能会导致一致性问题，而`deque`不会。  
另一个原因是`deque`支持固定长度，当长度满了之后，当我们继续`append`时，它会自动弹出最早插入的数据。  
比如说当我们拥有海量的数据，我们不知道它的数量，但是想要保留最后出现的指定数量的数据的时候，就可以使用`deque`。

```python
from collections import deque
dq = deque(maxlen=10)

for i in range(20):
    dq.append(i)

print(dq)  # 打印: deque([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], maxlen=10)
```

## `namedtuple`
`namedtuple`很特殊，它涉及到元编程。  
在常见的面向对象当中，我们都是定义类，然后通过类的构造函数来创建实例。  
而元编程指的是我们定义元类，根据元类创建出来的并不是一个实例，而是一个类。

`namedtuple`是一个非常简单的元类，通过它我们可以非常方便地定义我们想要的类。

我们直接来看例子，比如如果我们想要定义一个学生类，这个类当中有name、score、age这三个字段，那么这个类会写成：
```python
class Student:
    def __init__(self, name=None, score=None, age=None):
        self.name = name
        self.score = score
        self.age = age
```

如果我们使用`namedtuple`可以简化这个定义类的工作，我们来看代码：
```python
from collections import namedtuple
# 这个是类，columns也可以写成'name score age'，即用空格分开
# defaults设置了两个默认值，可以不设置默认值。这里会自动将两个默认值匹配上score和age字段。因为在Python的规范当中，必选参数一定在可选参数前面。所以`nuamdtuple`会自动右对齐。
Student = namedtuple('Student', ['name', 'score', 'age'], defaults=(60, 18))

# 这个是实例
student1 = Student(name='xiaoming', score=99, age=10)
print(student1.name, student1.score, student1.age)  # 打印: xiaoming 99 10

# 这个是查看默认值的实例
student2 = Student('lilei')
print(student2.name, student2.score, student2.age)  # 打印: lilei 60 18
```

