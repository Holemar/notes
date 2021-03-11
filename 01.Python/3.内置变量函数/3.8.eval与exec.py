
定义
    eval(expression, globals=None, locals=None)
    exec(object[, globals[, locals]])

    参数说明：
    globals： 可选参数，表示全局命名空间（存放全局变量），如果被提供，则必须是一个字典对象。
        通常传入 globals()，其返回一个表示当前全局标识符表的字典。
        这永远是当前模块的字典（在一个函数或方法内部，这是指定义该函数或方法的模块，而不是调用该函数或方法的模块）
    locals：可选参数，表示当前局部命名空间（存放局部变量），如果被提供，可以是任何映射对象。如果该参数被忽略，那么它将会取与 globals 相同的值。
        通常传入 locals()，其更新并返回一个表示当前局部标识符表的字典。
        自由变量在函数内部被调用时，会被 locals()函数返回；自由变量在类不被调用时，不会被 locals()函数返回。


差异
    eval()函数只能计算单个表达式的值，而 exec()函数可以动态运行代码段。
    eval()函数可以有返回值，而 exec()函数返回值永远为 None。
    exec 用来执行储存在字符串或文件中的Python语句。
    eval 只能执行单独一条表达式；但是 exec 能够执行多条语句，导入(import)，函数声明
    实际上 exec 能执行整个Python程序的字符串。


Python 2 与 Python 3 的比较
            Python 2                                              Python 3
        ① exec codeString                                       exec(codeString)
        ② exec codeString in global_namespace                   exec(codeString, global_namespace)
        ③ exec codeString in global_namespace, local_namespace  exec(codeString, global_namespace, local_namespace)
    说明:
        ① 就像 print 语句在Python 3里变成了一个函数一样, exec 语句在Python 3里也变成一个函数。
        ② exec 可以指定名字空间，代码将在这个由全局对象组成的私有空间里执行。
        ③ exec 还可以指定一个本地名字空间(比如一个函数里声明的变量)。

    例：
    exec('print("Hello World")')  # 执行打印语句
    print(eval('2*3'))  # 打印：6


eval 范例
    x = 10
    y = 20
    print(globals())  # 打印: {..., 'x': 10, 'y': 20}
    a = eval('x + y')
    print('a: ', a)  # 打印: a:  30,  说明使用了 globals() 变量
    b = eval('x + y', {'x': 1, 'y': 2})
    print('b: ', b)  # 打印: b:  3,  说明使用了 传入的 globals 变量
    c = eval('x + y', {'x': 1, 'y': 2}, {'y': 3, 'z': 4})
    print('c: ', c)  # 打印: c:  4,  说明使用了 传入的 变量，且传入的 locals 变量比 globals 变量优先级更高
    d = eval('print(x, y)')  # 打印: 10 20, 运行一个表达式，说明前面的 eval 运行不会更改这里的 globals() 变量
    print('d: ', d)  # 打印: d:  None, 说明上述语句没有返回值
    print(globals())  # 打印: {..., 'x': 10, 'y': 20, 'a': 30, 'b': 3, 'c': 4, 'd': None}


exec 范例1
    x = 10
    expr = """
    z = 30
    sum = x + y + z
    print(sum)
    """

    def func():
        y = 20
        print(globals())  # 打印: {..., 'x': 10, 'expr': '\nz = 30\nsum = x + y + z\nprint(sum)\n'}
        print(locals())  # 打印: {'y': 20}
        exec(expr)  # 打印: 60， 说明使用了 globals() 变量
        exec(expr, {'x': 1, 'y': 2})  # 打印: 33,  说明使用了 传入的 globals 变量
        exec(expr, {'x': 1, 'y': 2}, {'y': 3, 'z': 4})  # 打印: 34,  说明使用了 传入的 变量，且传入的 locals 变量比 globals 变量优先级更高
        exec('print(x, y)')  # 打印: 10 20, 运行一个表达式，说明前面的 exec 运行不会更改这里的 globals() 变量
        print(globals())  # 打印: {..., 'x': 10, 'expr': '\nz = 30\nsum = x + y + z\nprint(sum)\n'}
        print(locals())  # 打印: {'y': 20, 'z': 30, 'sum': 60}， 注意这里的 sum=60，说明没传入参数时使用 globals() 且会改变里面的值。而传入参数时改变的也是传入的。

    func()
    print(globals())  # 打印: {..., 'x': 10, 'expr': '\nz = 30\nsum = x + y + z\nprint(sum)\n'}
    print(locals())  # 打印: {..., 'x': 10, 'expr': '\nz = 30\nsum = x + y + z\nprint(sum)\n'}， 说明这里的 locals() 使用了 globals()


exec 范例2
    x = 10
    y = 20
    expr = """
    z = 30
    sum = x + y + z
    print(sum)
    """

    a = {'x': 1, 'y': 2}
    b = {'y': 3, 'z': 4}
    exec(expr, a, b)  # 打印: 34,  说明使用了 传入的 变量，且传入的 locals 变量比 globals 变量优先级更高
    exec('print(x, y)')  # 打印: 10 20, 运行一个表达式，说明前面的 exec 运行不会更改这里的 globals() 变量
    print(a)  # 打印: {'x': 1, 'y': 2, '__builtins__':...}
    a.pop('__builtins__', None)  # 自动添加的 __builtins__ 内容太多，影响查看
    print(a)  # 打印: {'x': 1, 'y': 2}
    print(b)  # 打印: {'y': 3, 'z': 30, 'sum': 34}， 说明传入的 locals 变量被改变了。





