
# dataclasses 模块

`dataclasses` 模块是 Python 3.7 中引入的标准库，它提供了一种简单的方法来定义数据类。
数据类是指包含少量数据和方法的类，这些数据和方法可以自动生成，并提供默认的 `__init__`、`__repr__`、`__eq__` 等方法。

## 基本用法

### 0. 使用 `dataclasses` 模块定义数据类并创建实例

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int = 0  # 提供默认值

# 创建 Person 实例
p = Person(name="Alice", age=30)

# 自动生成的 __repr__ 方法会返回一个易读的字符串表示
print(p)  # 输出: Person(name='Alice', age=30)
```

**说明：**

- **@dataclass 装饰器**：该装饰器会自动为类生成 `__init__`、`__repr__`、`__eq__` 等方法，减少手动编写样板代码。
- **字段类型声明**：在类中，每个字段都可以通过类型注解来指定其类型。上例中 `name` 是字符串，`age` 是整数，且为 `age` 提供了默认值 0。
- **自动生成方法**：例如，创建实例时，不需要显式编写构造函数，dataclasses 自动根据字段生成 `__init__` 方法；同样，打印对象时会调用自动生成的 `__repr__` 方法，输出一个包含所有字段的字符串。

这个例子展示了 dataclasses 在简化数据存储类定义方面的优势。通过这种方式，可以让代码更简洁、易读，并减少人为错误。


下面再举几个 dataclasses 模块的高级用法示例，展示除了自动生成构造函数和打印方法之外的其它用途。

---

### 1. 使用 `default_factory` 为可变类型字段提供默认值

直接将可变类型（如列表、字典）作为默认值可能会导致所有实例共享同一对象。利用 `field(default_factory=…)` 可以避免这个问题：

```python
from dataclasses import dataclass, field

@dataclass
class Inventory:
    items: list = field(default_factory=list)

inv1 = Inventory()
inv2 = Inventory()

inv1.items.append("apple")
print(inv1)  # 输出: Inventory(items=['apple'])
print(inv2)  # 输出: Inventory(items=[])
```

这里每个 `Inventory` 实例都会得到一个独立的空列表。

---

### 2. 创建不可变（Frozen）数据类

通过设置 `frozen=True` 参数，可以使数据类实例不可变，即一旦创建后属性值不能更改。这在需要保证数据不被意外修改时很有用：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
# p.x = 3  # 这行代码会抛出异常，因为 p 是不可变的
print(p)  # 输出: Point(x=1, y=2)
```

---

### 3. 利用 `order=True` 实现对象的比较排序

通过设置 `order=True`，数据类会自动生成比较方法（如 `__lt__`, `__le__` 等），使对象可以直接进行排序比较：

```python
from dataclasses import dataclass

@dataclass(order=True)
class Student:
    grade: float
    name: str

s1 = Student(90.5, "Alice")
s2 = Student(88.0, "Bob")
print(s1 > s2)  # 输出: True，因为 90.5 > 88.0
```

---

### 4. 使用辅助函数 `asdict` 和 `astuple`

dataclasses 模块提供了 `asdict` 和 `astuple` 方法，方便将数据类实例转换为字典或元组，便于序列化或其他数据处理场景：

```python
from dataclasses import dataclass, asdict, astuple

@dataclass
class Car:
    brand: str
    model: str

car = Car("Toyota", "Corolla")
print(asdict(car))  # 输出: {'brand': 'Toyota', 'model': 'Corolla'}
print(astuple(car))  # 输出: ('Toyota', 'Corolla')
```

---

### 5. 继承与后处理（`__post_init__` 方法）

dataclasses 支持继承，且可以在实例初始化后通过 `__post_init__` 方法进行额外的处理，例如数据校验或计算衍生属性：

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str

@dataclass
class Dog(Animal):
    breed: str
    sound: str = ""

    def __post_init__(self):
        # 根据品种设置默认的叫声
        if not self.sound:
            self.sound = "Woof" if self.breed.lower() == "labrador" else "Bark"

dog = Dog(name="Buddy", breed="Labrador")
print(dog)  # 输出: Dog(name='Buddy', breed='Labrador', sound='Woof')
```

在这个例子中，`__post_init__` 用于在所有字段初始化后，依据 `breed` 设置 `sound` 的默认值。

---

这些示例展示了 dataclasses 模块在管理数据对象时的灵活性与简洁性，能够大大减少样板代码，同时增强代码的可读性与安全性。
