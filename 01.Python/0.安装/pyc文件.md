﻿
# 文件类型

1. Python的文件类型分为3种，即源代码、字节代码和优化代码。  
    这些都可以直接运行，不需要进行编译或连接。
2. 源代码以 `.py` 为扩展名，由python来负责解释；
3. 源文件经过编译后生成扩展名为 `.pyc` 的文件，即编译过的字节文件。  
    这种文件不能使用文本编辑器修改。  
    `pyc` 文件是和平台无关的，可以在大部分操作系统上运行。  
    如下语句可以用来产生 `pyc` 文件：  
    ```python
    import py_compile
    py_compile.compile('hello.py')
    ```

4. 经过优化的源文件会以“.pyo”为后缀，即优化代码。  
    它也不能直接用文本编辑器修改，如下命令可用来生成pyo文件：  
    `python -O -m py_complie hello.py`


# 字节编译的 .pyc 文件

- 输入一个模块相对来说是一个比较费时的事情，所以Python做了一些技巧，以便使输入模块更加快一些。  
- 其中一种方法是创建 字节编译的文件，这些文件以 `.pyc` 作为扩展名。  

- 这些字节编译的文件也是与平台无关的。  
当你在下次从别的程序输入这个模块的时候，`.pyc` 文件是十分有用的——它会快得多，因为一部分输入模块所需的处理已经完成了。  

- 注意：虽说 python 是源码公开的，但服务器上可以只保留 `.pyc` 文件，而不保留源码，照样正常运行。这样可以保证源码不被看到。  

- `pyc` 的内容，是跟 python 的版本相关的，不同版本编译后的`pyc`文件是不同的，2.5编译的`pyc`文件，2.4版本的 python 是无法执行的。  

- 根据 python 源码中提供的 opcode，可以根据 `pyc` 文件反编译出 py 文件源码, 2.6之后源码不提供反编译,不过可以另外设法做到。  


# 将 py 文件生成 pyc 文件：
1. 直接通过命令来运行  
    可以看到下面的命令中并没有用到 `compile()` 函数  
    这是因为 `py_compile` 模块的 `main()` 函数中调用了 `compile()` .
    ```shell script
    python -m py_compile test.py
    python -O -m py_compile test.py

    -O 优化成字节码
    -m 表示把后面的模块当成脚本运行
    -OO 表示优化的同时删除文档字符串
    ```
    如果想看 `compile()`, `compile_dir()`, `compile_path()` 具体每个参数用途，  
    可以使用 `print(py_compile.compile().__doc__)` 来查看，  
    或者直接打开 `py_compile.py`，`compileall.py` 文件来看。  

2. 通过写 python 代码来编译 `.py` 文件,然后运行这个 python 脚本即可，运行过程中输入你要编译的 `.py` 文件。
    ```python
    import py_compile
    file = raw_input("Please enter filename: ")
    py_compile.compile(file)
    ```

3. 如果是在 Linux 环境下，可以通过写一个 bash 脚本编译 `.py`。
    ```shell script
    #! /bin/sh
    (echo 'import compileall'; echo 'compileall.compile_dir("./")') | python
    ```
    完成上述代码后用bash命令运行即可。

4. 禁止 python 在运行的时候自动生成 `.pyc` 文件

    1) python2.6 新增的一个特性  
     把环境变量 PYTHONDONTWRITEBYTECODE 设置为 x  
     mac上是在 `~/.bash_profile` 文件中添加：  
     `export PYTHONDONTWRITEBYTECODE=x`

    2) 使用 -B参数 即：
     `python -B test.py`

    3) 在导入的地方写:
        ```python
        import sys
        sys.dont_write_bytecode = True
        ```

5. 实际生成时，交付客户的代码不希望提供源码  

    1) 这时需要将整个项目批量生成 `pyc` 文件交付。

    2) python2 时在项目目录下执行:
    `python -m compileall .`

    3) python3 时，会生成在 `__pycache__` 目录下，需要再加参数 `-b` 解决。
    `python3 -m compileall -b .`

    4) 可以增加优化项: -O ，生成字节码优化运行代码。
    `python3 -O -m compileall -b .`

    5) 后续工作  
        删除`py`文件
        `find . -name "*.py"|xargs rm -rf`

        删除`__pycache__`目录
        `find . -name "__pycache__" |xargs rm -rf`

        打成tar包
        ```shell script
        cd ..
        tar -cjvf xxx.1.1.0.0.tar.bz2 xxx
        ```


