
# inspect模块
- `inspect`模块也被称为 检查现场对象。这里的重点在于“现场”二字，也就是当前运行的状态。
- `inspect`模块提供了一些函数来了解现场对象，包括 模块、类、实例、函数和方法。
- `inspect`函数主要用于以下四个方面
  1. 对是否是模块、框架、函数进行类型检查
  2. 获取源码包
  3. 获取类或者函数的参数信息
  4. 解析堆栈

# 获取成员与判断
1. `inspect.getmembers(object[, predicate])`  
第二个参数通常可以根据需要调用如下16个方法；  
返回值为object的所有成员，以`(name,value)`对组成的列表

| 函数                                    | 说明                                                                |
|---------------------------------------|-------------------------------------------------------------------|
| `inspect.ismodule(object)`            | 是否为模块                                                             |
| `inspect.isclass(object)`             | 是否为类                                                              |
| `inspect.ismethod(object)`            | 是否为方法（bound method written in python）                             |
| `inspect.isfunction(object)`          | 是否为函数(python function, including lambda expression)               |
| `inspect.isgeneratorfunction(object)` | 是否为python生成器函数                                                    |
| `inspect.isgenerator(object)`         | 是否为生成器                                                            |
| `inspect.istraceback(object)`         | 是否为`traceback`                                                    |
| `inspect.isframe(object)`             | 是否为`frame`                                                        |
| `inspect.iscode(object)`              | 是否为`code`                                                         |
| `inspect.isbuiltin(object)`           | 是否为`built-in`函数或`built-in`方法                                      |
| `inspect.isroutine(object)`           | 是否为用户自定义或者`built-in`函数或方法                                         |
| `inspect.isabstract(object)`          | 是否为抽象基类                                                           |
| `inspect.ismethoddescriptor(object)`  | 是否为方法标识符                                                          |
| `inspect.isdatadescriptor(object)`    | 是否为数字标识符，数字标识符有`__get__` 和`__set__`属性； 通常也有`__name__`和`__doc__`属性 |
| `inspect.isgetsetdescriptor(object)`  | 是否为`get-set descriptor`                                           |
| `inspect.ismemberdescriptor(object)`  | 是否为`member descriptor`                                            |


2. `inspect.getmoduleinfo(path)`  
返回一个命名元组`(name, suffix, mode, module_type)`  
  `name`：模块名（不包括其所在的package）   
  `suffix`：  
  `mode`：open()方法的模式，如：'r', 'a'等  
  `module_type`: 整数，代表了模块的类型  

3. `inspect.getmodulename(path)`  
根据path返回模块名（不包括其所在的package）


# 获取源代码
| 函数                               | 说明                                                          |
|----------------------------------|-------------------------------------------------------------|
| `inspect.getdoc(object)`         | 获取object的documentation信息                                    |
| `inspect.getcomments(object)`    | 获取object的注释信息                                               |
| `inspect.getfile(object)`        | 返回对象的文件名                                                    |
| `inspect.getmodule(object)`      | 返回object所属的模块名                                              |
| `inspect.getsourcefile(object)`  | 返回object的python源文件名；object不能使built-in的module, class, mothod |
| `inspect.getsourcelines(object)` | 返回object的python源文件代码的内容，行号+代码行                              |
| `inspect.getsource(object)`      | 以string形式返回object的源代码                                       |


# 类与函数
`inspect.getclasstree(classes[, unique])`  
`inspect.getargspec(func)`  
`inspect.getargvalues(frame)`  
`inspect.formatargspec(args[, varargs, varkw, defaults, formatarg, formatvarargs, formatvarkw, formatvalue, join])`  
`inspect.formatargvalues(args[, varargs, varkw, locals, formatarg, formatvarargs, formatvarkw, formatvalue, join])`  
`inspect.getmro(cls)`： 元组形式返回cls类的基类（包括cls类），以method resolution顺序;通常cls类为元素的第一个元素  
`inspect.getcallargs(func[, *args][, **kwds])`：将args和kwds参数到绑定到为func的参数名；对bound方法，也绑定第一个参数（通常为self）到相应的实例；返回字典，对应参数名及其值；  


# 调用栈
`inspect.getframeinfo(frame[, context])`  
`inspect.getouterframes(frame[, context])`  
`inspect.getinnerframes(traceback[, context])`  
`inspect.currentframe()`  
`inspect.stack([context])`  
`inspect.trace([context])`

