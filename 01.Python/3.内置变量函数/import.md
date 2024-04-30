
# `from ... import` 语句
- 如果你想要直接输入 `argv` 变量到你的程序中(避免在每次使用它时打`sys.`)，那么你可以使用 `from sys import argv` 语句。
- 如果你想要输入所有 `sys` 模块使用的名字，那么你可以使用 `from sys import *`语句。
- 这对于所有模块都适用。
- 注意:
    1. 使用 `from package import item` 方式导入包时，这个子项(item)既可以是包中的一个子模块(或一个子包)，也可以是包中定义的其它命名，像函数、类或变量。  
       `import` 语句首先核对是否包中有这个子项，如果没有，它假定这是一个模块，并尝试加载它。如果没有找到它，会引发一个 `ImportError` 异常。
    2. 使用像 `import item.subitem.subsubitem` 这样的语句时，这些子项必须是包，最后的子项可以是包或模块，但不能是前面子项中定义的类、函数或变量。
    3. 应该避免使用 `from...import` 而使用 `import` 语句，因为这样可以使你的程序更加易读，也可以避免名称的冲突。


# `import ... as`
- 为 import 的模块起一个简称。如: `import cPickle as p`
- 起简称后,下面的语句即可使用简称,如原本的 `cPickle.dump()` 可写成 `p.dump()`


# __import__ 用法:
`__import__(name[, globals[, locals[, fromlist[, level]]]])`
- 被 `import` 语句调用的函数。它的存在主要是为了你可以用另外一个有兼容接口的函数 来改变 `import` 语句的语义.

- 如果你写过较庞大的 Python 程序, 那么你就应该知道 `import` 语句是用来导入外部模块的 (当然也可以使用 `from-import` 版本).
- 不过你可能不知道 `import` 其实是靠调用内建 函数 `__import__` 来工作的.
- 通过这个戏法你可以动态地调用函数. 当你只知道模块名称(字符串)的时候, 这将很方便.


## 使用 `__import__` 函数加载模块
- 同目录下建一个 `example-plugin.py` 文件,里面内容为:
```python
def hello():
    print("example-plugin says hello")
```
- 注意这个示例里面 `plug-in` 模块文件名中有个 "-" (hyphens). 这意味着你不能使用普通的 `import` 命令, 因为 Python 的辨识符不允许有 "-" .

- 测试代码 1
```python
import os
import glob

modules = []

for module_file in glob.glob("*-plugin.py"):
    try:
        # module_file 是一个包含文件后缀名的文件名，这里分隔出文件名和后缀
        module_name, ext = os.path.splitext(os.path.basename(module_file))
        module = __import__(module_name)
        modules.append(module)
    except ImportError:
        pass # ignore broken modules

# 调用所有 modules 里面的 hello 函数
for module in modules:
    module.hello()
```

- 测试代码 2
```python
import sys
custom_plugins = ['example-plugin', ]  # 要 import 的配置列表
for plugin in custom_plugins:
    __import__(plugin)
    sys.modules[plugin].hello()
```


## 使用 `__import__` 函数获得特定函数
```python
def get_function_by_name(module_name, function_name):
    module = __import__(module_name)
    return getattr(module, function_name)

op = get_function_by_name("dumbdbm", "open") # 获取到此函数
print(repr(op)) # 打印: <function open at 0x01B9B7F0>
```

- 相当于这样写:
```python
import dumbdbm
op = dumbdbm.open
print(repr(op))
```


## 使用 `__import__` 函数实现 延迟导入
```python
class LazyImport:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None
    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)

s = LazyImport("string")
print(s.lowercase) # 打印: abcdefghijklmnopqrstuvwxyz
print(s.uppercase) # 打印: ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

# 理解模块的缓存
- 在一个模块内部重复引用另一个相同模块，实际并不会导入两次
- 原因是在使用关键字 `import` 导入模块时，它会先检索 `sys.modules` 里是否已经载入这个模块
- 如果已经载入，则不会再次导入，如果不存在，才会去检索导入这个模块
- `sys.modules` 是一个字典（key：模块名，value：模块对象），它存放着在当前 namespace 所有已经导入的模块对象。

- 来实验一下:
```shell
$ cat my_mod01.py  # 模块内有一个打印语句，import就会触发
print('in mod01')

$ cat my_mod02.py
import my_mod01  # import 两次 my_mod01 这个模块，看打印多少次
import my_mod01

$ python my_mod02.py  # 验证结果是，只打印了一次。
in mod01
```

- 由于有模块缓存的存在，使得我们无法重新载入一个模块。
- 但若你想反其道行之，可以借助 importlib 这个神奇的库来实现。
- 事实也确实有此场景，比如在代码调试中，在发现代码有异常并修改后，我们通常要重启服务再次载入程序。
- 这时候，若有了模块重载，就无比方便了，修改完代码后也无需服务的重启，就能继续调试。

- 还是以上面的例子来理解，my_mod02.py 改写成如下
```python
# my_mod02.py

import importlib
import my_mod01  # import 时print一次
importlib.reload(my_mod01)  # 再次import，所以再print一次
```


## 一个模块要执行其它模块主要有三种方法
1. import 模块或使用 `__import__()` 动态导入
2. 利用 `os.system()` 执行此模块文件
3. 利用 `execfile` 函数

- 同目录下建一个 `example-plugin.py` 文件,里面内容为:
```python
def hello():
    print("example-plugin says hello")
# 被导入的模块就不要将执行的代码写在if __name__ == "__main__"下，不然执行不了。
print('加载 example-plugin.py 成功。。。')
```

- 示例1:(使用 动态导入 `__import__()`)
```python
module = __import__('example-plugin') # 打印: 加载 example-plugin.py 成功。。。
module.hello() # 打印: example-plugin says hello
# 导入的模块，可以随意定义一个模块名称，然后按正常模块调用
```

- 示例2:(使用 `os.system()`)
```python
import os
module = os.system('python example-plugin.py' % (item.strip())) # 打印: 加载 example-plugin.py 成功。。。
# 没法调用模块里面的函数,因为 os.system 是执行系统命令,直接运行了此模块文件而不是导入它
```

- 示例3:(使用 `execfile` 函数, 仅 python2 有此函数)
```python
execfile('example-plugin.py') # 打印: 加载 example-plugin.py 成功。。。
# exec(open('example-plugin.py').read())  # python3 时的替代方案
hello() # 打印: example-plugin says hello
#调用模块里的函数可以直接按本模块的来用，没有新模块名称
```


