
# REPL(交互式解释器)
REPL(Read Eval Print Loop:交互式解释器) 表示一个电脑的环境，类似 Windows 系统的终端或 Unix/Linux shell，我们可以在终端中输入命令，并接收系统的响应。

Node 自带了交互式解释器，可以执行以下任务：
- 读取 - 读取用户输入，解析输入的 Javascript 数据结构并存储在内存中。
- 执行 - 执行输入的数据结构
- 打印 - 输出结果
- 循环 - 循环操作以上步骤直到用户两次按下 ctrl-c 按钮退出。

Node 的交互式解释器可以很好的调试 Javascript 代码。

# REPL 命令

命令 | 含义
--- | ---
ctrl + c | 退出当前终端。
ctrl + c 按下两次 | 退出 Node REPL。
ctrl + d | 退出 Node REPL.
向上/向下 键 | 查看输入的历史命令
tab 键 | 列出当前命令
.help | 列出使用命令
.break | 退出多行表达式
.clear | 退出多行表达式
.save filename | 保存当前的 Node REPL 会话到指定文件
.load filename | 载入当前 Node REPL 会话的文件内容。


## 启动 Node 的终端
`$ node`

```shell
$ node

# 简单的表达式运算
> 1 + ( 2 * 3 ) - 4
3

# 变量声明需要使用 var 关键字，如果没有使用 var 关键字变量会直接打印出来。
# 使用 var 关键字的变量可以使用 console.log() 来输出变量。
> x = 10
10
> var y = 10
undefined
> x + y
20
> console.log(y)
10
undefined
> console.log("Hello World")
Hello World
undefined

# 多行表达式
> do {
... x++;
... console.log("x: " + x);
... } while ( x < 12 );
x: 11
x: 12
undefined
>

# 可以使用下划线(_)获取上一个表达式的运算结果
> x + y
22
> var s = _
undefined
> s
22

```

