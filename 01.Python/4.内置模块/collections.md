
# collections 容器的集合
`collections`模块实现了特定目标的容器，以提供Python标准内建容器`dict` ,`list` , `set`, 和`tuple`的替代选择。

函数名 | 基类                                           | 含义
--- |----------------------------------------------| ---
`namedtuple`	| tuple | 创建命名元组子类的工厂函数，生成可以使用名字来访问元素内容的`tuple`子类
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

# elements 返回一个迭代器，其中每个元素将重复出现计数值所指定次。 元素会按首次出现的顺序返回。 如果一个元素的计数值小于1，elements() 将会忽略它。
print(list(counter.elements()))  # 打印：['apple', 'apple', 'pear', 'pear', 'watermelon', 'peach']

# 由于 Counter 是 dict 的子类，也能按 dict 来使用
print(counter.items())  # 打印: dict_items([('apple', 2), ('pear', 2), ('watermelon', 1), ('peach', 1)])

# 但有两个原生 dict 函数不一样，一个是 `fromkeys(iterable)` 函数没有实现，使用了会报错
# 另一个是 `update([iterable-or-mapping])` 从迭代对象计数元素或者从另一个映射对象 (或计数器) 添加。 像 dict.update() 但是是加上，而不是替换。另外，迭代对象应该是序列元素，而不是一个 (key, value) 对。
counter.update(('a', 'b'))
print(counter)  # 打印: Counter({'apple': 2, 'pear': 2, 'watermelon': 1, 'peach': 1, 'a': 1, 'b': 1})

counter.update({'a':2, 'b':1})
print(counter)  # 打印: Counter({'a': 3, 'apple': 2, 'pear': 2, 'b': 2, 'watermelon': 1, 'peach': 1})

# subtract() 从迭代对象或映射对象减去元素。像dict.update() 但是是减去，而不是替换。
counter.subtract(Counter(apple=2, watermelon=1, c=3))
print(counter)  # 打印: Counter({'a': 3, 'pear': 2, 'b': 2, 'peach': 1, 'apple': 0, 'watermelon': 0, 'c': -3})

# 字符串计数
print(Counter('gallahad'))  # 打印: Counter({'a': 3, 'l': 2, 'g': 1, 'h': 1, 'd': 1})
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
```python
from collections import Counter
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)

# add two counters together:  c[x] + d[x]
print(c + d)  # 打印: Counter({'a': 4, 'b': 3})
# subtract (keeping only positive counts)
print(c - d)  # 打印: Counter({'a': 2})
# intersection:  min(c[x], d[x]) 
print(c & d)  # 打印: Counter({'a': 1, 'b': 1})
# union:  max(c[x], d[x])
print(c | d)  # 打印: Counter({'a': 3, 'b': 2})

# 单目加和减（一元操作符）意思是从空计数器加或者减去。
c1 = Counter(a=2, b=-4)
print(+c1)  # 打印: Counter({'a': 2})
print(-c1)  # 打印: Counter({'b': 4})
```

## `deque`
我们都知道`queue`是队列，`deque`也是队列，不过稍稍特殊一些，是双端队列。  
对于`queue`来说，只允许在队尾插入元素，在队首弹出元素。而`deque`既然称为双端队列，那么说明它的队首和队尾都支持元素的插入和弹出。  

除了常用的`clear`、`copy`、`count`、`extend`等api之外，`deque`当中最常用也是最核心的api还有`append`、`pop`、`appendleft`和`popleft`。  
从名字上我们就看得出来，`append`和`pop`和`list`的`append`和`pop`一样，而`appendleft`和`popleft`则是在队列左侧，也就是头部进行`pop`和`append`的操作。

函数名 | 含义
--- | ---
`append(item)` | 添加 item 到右端
`appendleft(item)` | 添加 item 到左端
`index(item)` | 返回 item 在 deque 中的位置（在索引 start 之后，索引 stop 之前）。 返回第一个匹配项，如果未找到则引发 ValueError
`insert(index, item)` | 在位置 index 插入 item 。<br>如果插入会导致一个限长 deque 超出长度 maxlen 的话，就引发一个 IndexError
`pop()` | 移去并且返回一个元素，deque 最右侧的那一个。 如果没有元素的话，就引发一个 IndexError
`popleft()` | 移去并且返回一个元素，deque 最左侧的那一个。 如果没有元素的话，就引发 IndexError
`clear()` | 移除所有元素，使其长度为0
`copy()` | 创建一份浅拷贝
`reverse()` | 将deque逆序排列。返回 None
`count(item)` | 计算 deque 中元素等于 item 的个数
`remove(value)` | 移除找到的第一个 value。 如果没有的话就引发 ValueError
`extend(deque)` | 扩展 deque 的右侧，通过添加 iterable 参数中的元素
`extendleft(deque)` | 扩展 deque 的左侧，通过添加 iterable 参数中的元素。<br>注意，左添加时，在结果中 iterable 参数中的顺序将被反过来添加
`rotate(number)` | 向右循环移动 number 步。 如果 number 是负数，就向左循环。<br>如果deque不是空的，向右循环移动一步就等价于 `d.appendleft(d.pop())` ， 向左循环一步就等价于 `d.append(d.popleft())` 。

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

语法: `namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)`
1. `typename`：该参数指定所创建的`tuple`子类的类名，相当于用户定义了一个新类。
2. `field_names`：该参数是一个字符串序列，如 ['x'，'y']。
    - 此外，`field_names` 也可直接使用单个字符串代表所有字段名，多个字段名用空格、逗号隔开，如 'x y' 或 'x,y'。
    - 任何有效的 Python 标识符都可作为字段名（不能以下划线开头）。
    - 有效的标识符可由字母、数字、下画线组成，但不能以数字、下划线开头，也不能是关键字（如 return、global、pass、raise 等）。
3. `rename`：如果将该参数设为 `True`，那么无效的字段名将会被自动替换为位置名。
    - 例如指定 ['abc','def','ghi','abc']，它将会被替换为 ['abc', '_1','ghi','_3']，这是因为 def 字段名是关键字，而 abc 字段名重复了。
4. `defaults`：该参数设置对应 `field_names` 的默认值。
5. `module`：如果设置了该参数，那么该类将位于该模块下，因此该自定义类的 `__module__` 属性将被设为该参数值。

`namedtuple`除了继承`tuple`的方法，`namedtuple`还支持三个额外的函数和两个属性。为了防止字段名冲突，函数和属性以下划线开始。
1. `_make(iterable)` 函数从存在的序列或迭代实例创建一个新实例。
2. `_asdict()` 函数返回一个新的 `dict`，它将字段名称映射到它们对应的值。
3. `_replace(**kwargs)` 函数返回一个新的命名元组实例，并将指定 field 替换为新的值。
4. `_fields` 属性以字符串元组列出了字段名
5. `_field_defaults` 属性用字典返回字段名与默认值的映射

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

# 这个是实例。初始化实例，既可以用位置参数，也可用命名参数
student1 = Student('xiaoming', score=99, age=10)
print(student1.name, student1.score, student1.age)  # 打印: xiaoming 99 10
# 既可以根据字段名访问各元素，也可以像普通元组一样用根据索引访问元素
print(student1[0], student1[1], student1[2])  # 打印: xiaoming 99 10

# 这个是查看默认值的实例
student2 = Student(name='lilei')
print(student2)  # 打印: Student(name='lilei', score=60, age=18)

# 执行元组解包，按元素的位置解包
a, b, c = student2
print(a, b, c)  # 打印: lilei', 60, 18

# _make 创建一个新实例
student3 = student2._make(['xiaomei', 80, 20])
print(student3)  # 打印: Student(name='xiaomei', score=80, age=20)
# _asdict 生成当前值的字典
print(student3._asdict())  # 打印: {'name': 'xiaomei', 'score': 80, 'age': 20}
# _replace 生成一个新的实例，并改变指定值
student4 = student3._replace(name='andy', score=33)
print(student4)  # 打印: Student(name='andy', score=33, age=20)
print(student3)  # 原实例不变，打印: Student(name='xiaomei', score=80, age=20)
# _fields,_field_defaults 两个属性
print(student3._fields)  # 打印: ('name', 'score', 'age')
print(student3._field_defaults)  # 打印: {'score': 60, 'age': 18}
```

## `OrderedDict` 有序字典
有序词典就像常规词典一样，但有一些与排序操作相关的额外功能。  
由于内置的 `dict` 类获得了记住插入顺序的能力（在 Python 3.7 中保证了这种新行为），它们变得不那么重要了。

一些与 `dict` 的不同仍然存在：
- 常规的 `dict` 被设计为非常擅长映射操作。 跟踪插入顺序是次要的。
- `OrderedDict` 旨在擅长重新排序操作。 空间效率、迭代速度和更新操作的性能是次要的。
- 算法上， `OrderedDict` 可以比 `dict` 更好地处理频繁的重新排序操作。 这使其适用于跟踪最近的访问（例如在 LRU cache 中）。
- 对于 `OrderedDict` ，相等操作检查匹配顺序。
- `OrderedDict` 类的 `popitem()` 函数有不同的签名。它接受一个可选参数来指定弹出哪个元素。
- `OrderedDict` 类有一个 `move_to_end()` 函数，可以有效地将元素移动到任一端。
- Python 3.8之前， `dict` 缺少 `__reversed__()` 函数。

### `popitem()`
语法：`popitem(last=True)`
功能：有序字典的 `popitem()` 函数移除并返回一个 (key, value) 键值对。   
默认 last 值为真，则按 LIFO 后进先出的顺序返回键值对。如果设为 False 则按 FIFO 先进先出的顺序返回键值对。

### `move_to_end()`
语法: `move_to_end(item, last=True)`
将元素移动到最后端，或者最前端。

### `reversed()`
相对于通常的映射函数，有序字典还另外提供了逆序迭代的支持，通过`reversed()`。

```python
from collections import OrderedDict
d = OrderedDict.fromkeys('abcde')

# popitem() 函数默认last=True
print(d.popitem())  # 打印: ('e', None)
print(d)  # 打印: OrderedDict([('a', None), ('b', None), ('c', None), ('d', None)])
#last=False时，弹出第一个
print(d.popitem(last=False))  # 打印: ('a', None)
print(d)  # 打印: OrderedDict([('b', None), ('c', None), ('d', None)])

# move_to_end() 函数默认last=True，将元素移动到最后端
d.move_to_end('b')
print(d)  # 打印: OrderedDict([('c', None), ('d', None), ('b', None)])
# 可以指定移动元素到最前端
d.move_to_end('b', last=False)
print(d)  # 打印: OrderedDict([('b', None), ('c', None), ('d', None)])

# `__reversed__()` 函数提供了逆序，但仅返回新值，不改变原集合
print(list(reversed(d)))  # 打印: ['d', 'c', 'b']
print(d)  # 打印: OrderedDict([('b', None), ('c', None), ('d', None)])
```

## 映射链-`ChainMap`
- `ChainMap`最基本的使用，可以用来合并两个或者更多个字典，当查询的时候，从前往后依次查询。
- `ChainMap`允许你将多个字典视为一个。换句话说:`ChainMap`是一个基于多`dict`的可更新的视图，它的行为就像一个普通的`dict`。
- `ChainMap`类用于快速链接多个映射，以便将它们视为一个单元。它通常比创建新字典和多次调用`update()`快得多。
- 使用案例如：配置读取

#### 特性
1. 找到一个就不找了：这个列表是按照第一次搜索到最后一次搜索的顺序组织的，搜索查询底层映射，直到一个键被找到。
2. 更新原始映射：不同的是，写，更新和删除只操作第一个映射。
3. 支持所有常用字典方法。

##### `new_child()`函数
用法：`new_child(m=None)`  
返回一个新的`ChainMap`类，包含了一个新映射(map)，后面跟随当前实例的全部映射map。  
如果m被指定，它就成为不同新的实例，就是在所有映射前加上 m，如果没有指定，就加上一个空字典，这样的话一个 `d.new_child()` 调用等价于`ChainMap({}, *d.maps)` 。  
这个函数用于创建子上下文，不改变任何父映射的值。

##### `parents`属性
属性返回一个新的`ChainMap`包含所有的当前实例的映射，除了第一个。这样可以在搜索的时候跳过第一个映射。  
一个`d.parents`的引用等价于`ChainMap(*d.maps[1:])`。

##### `maps`属性
一个可以更新的映射列表。这个列表是按照第一次搜索到最后一次搜索的顺序组织的。它是仅有的存储状态，可以被修改。列表最少包含一个映射。

```python
from collections import ChainMap
baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
# 存在重复元素时，也不会去重
c = ChainMap(adjustments, baseline)
print(c)  # 打印: ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})
print(list(c))  # 打印: ['music', 'art', 'opera']

d = c.new_child(m={'key_new':888})
print(c)  # 不改变原值，打印: ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})
print(d)  # 打印: ChainMap({'key_new': 888}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

print(c.parents)  # 打印: ChainMap({'music': 'bach', 'art': 'rembrandt'})
print(d.parents)  # 打印: ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

print(c.maps)  # 打印: [{'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'}]
print(d.maps)  # 打印: [{'key_new': 888}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'}]
```


