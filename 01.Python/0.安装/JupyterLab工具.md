
### 安装和使用JupyterLab

#### 安装和启动

如果已经安装了 Anaconda，可以在“Anaconda-Navigator”中直接启动 Notebook 或 JupyterLab。

按照官方的说法，JupyterLab 是下一代的 Notebook，提供了更友好的界面和更强大的功能，我们也推荐大家使用 JupyterLab。

Windows 用户也可以在开始菜单中打开“Anaconda Prompt”或“Anaconda PowerShell”，由于已经激活了 Anaconda 默认的虚拟环境，只需要输入`jupyter lab`命令来启动JupyterLab。

macOS 系统在安装 Anaconda以后，每次打开终端时会自动激活 Anaconda 默认的虚拟环境，也是通过输入`jupyter lab`命令就可以启动JupyterLab。

对于安装了 Python 环境但是没有安装 Anaconda 的用户，可以用 Python 的包管理工具`pip`来安装 JupyterLab，安装成功后在终端或命令行提示符中执行`jupyter lab`命令来启动 JupyterLab，如下所示。

安装 JupyterLab：

```Bash
pip install jupyterlab
```

安装 Python 数据分析三大神器：

```Bash
pip install numpy pandas matplotlib
```

启动 JupyterLab：

```Bash
jupyter lab
```

JupyterLab 是基于网页的用于交互计算的应用程序，可以用于代码开发、文档撰写、代码运行和结果展示。

简单的说，你可以在网页中直接**编写代码**和**运行代码**，代码的运行结果也会直接在代码块下方进行展示。

如在编写代码的过程中需要编写说明文档，可在同一个页面中使用 Markdown 格式进行编写，而且可以直接看到渲染后的效果。

此外，Notebook 的设计初衷是提供一个能够支持多种编程语言的工作环境，目前它能够支持超过40种编程语言，包括 Python、R、Julia、Scala 等。

首先，我们可以创建一个用于书写 Python 代码的 Notebook，如下图所示。

<img src="https://github.com/jackfrued/Python-for-Data-Analysis/blob/master/res/day02/jupyterLab_1.png" style="zoom:50%;">

接下来，我们就可以编写代码、撰写文档和运行程序啦，如下图所示。

<img src="https://github.com/jackfrued/Python-for-Data-Analysis/blob/master/res/day02/jupyterLab_2.png" style="zoom:50%;">

#### 使用技巧

如果使用 Python 做工程化的项目开发，PyCharm 肯定是最好的选择，它提供了一个集成开发环境应该具有的所有功能，尤其是智能提示、代码补全、自动纠错这类功能会让开发人员感到非常舒服。

如果使用 Python 做数据科学相关的工作，JupyterLab 并不比 PyCharm 逊色，在数据和图表展示方面 JupyterLab 更加优秀。

为此，JetBrains 公司还专门开发了一个对标 JupyterLab 的新工具 DataSpell，有兴趣的读者可以自行了解。

下面我们为大家介绍一些 JupyterLab 的使用技巧，希望能够帮助大家提升工作效率。

1. 自动补全。在使用 JupyterLab 编写代码时，按`Tab`键会获得代码提示和补全功能。

2. 获得帮助。如果希望了解一个对象（如变量、类、函数等）的相关信息或使用方式，可以在对象后面使用`?`并运行代码， 窗口下方会显示出对应的信息，帮助我们了解该对象，如下所示。

    <img src="https://github.com/jackfrued/Python-for-Data-Analysis/blob/master/res/day02/jupyterLab_3.png" style="zoom:100%;">

3. 搜索命名。如果只记得一个类或一个函数名字的一部分，可以使用通配符`*`并配合`?`进行搜索，如下所示。

    <img src="https://github.com/jackfrued/Python-for-Data-Analysis/blob/master/res/day02/jupyterLab_4.png" style="zoom:100%;">

4. 调用命令。可以在 JupyterLab 中使用`!`后面跟系统命令的方式来执行系统命令。

5. 魔法指令。JupyterLab 中有很多非常有趣且有用的魔法指令，例如可以使用`%timeit`测试语句的执行时间，可以使用`%pwd`查看当前工作目录等。如果想查看所有的魔法指令，可以使用`%lsmagic`，如果了解魔法指令的用法，可以使用`%magic`来查看，如下图所示。

    <img src="https://github.com/jackfrued/Python-for-Data-Analysis/blob/master/res/day02/jupyterLab_5.png" style="zoom:100%;">

   常用的魔法指令有：

   | 魔法指令                                    | 功能说明                                   |
       | ------------------------------------------- | ------------------------------------------ |
   | `%pwd`                                      | 查看当前工作目录                           |
   | `%ls`                                       | 列出当前或指定文件夹下的内容               |
   | `%cat`                                      | 查看指定文件的内容                         |
   | `%hist`                                     | 查看输入历史                               |
   | `%matplotlib inline`                        | 设置在页面中嵌入matplotlib输出的统计图表   |
   | `%config Inlinebackend.figure_format='svg'` | 设置统计图表使用SVG格式（矢量图）          |
   | `%run`                                      | 运行指定的程序                             |
   | `%load`                                     | 加载指定的文件到单元格中                   |
   | `%quickref`                                 | 显示IPython的快速参考                      |
   | `%timeit`                                   | 多次运行代码并统计代码执行时间             |
   | `%prun`                                     | 用`cProfile.run`运行代码并显示分析器的输出 |
   | `%who` / `%whos`                            | 显示命名空间中的变量                       |
   | `%xdel`                                     | 删除一个对象并清理所有对它的引用           |

6. 快捷键。JupyterLab 中的很多操作可以通过快捷键来实现，使用快捷键可以提升工作效率。JupyterLab 的快捷键可以分为命令模式下的快捷键和编辑模式下的快捷键，所谓编辑模式就是处于输入代码或撰写文档状态的模式，在编辑模式下按`Esc`可以回到命令模式，在命令模式下按`Enter`可以进入编辑模式。

   命令模式下的快捷键：

   | 快捷键                                   | 功能说明                                     |
       | ---------------------------------------- | -------------------------------------------- |
   | `Alt` + `Enter`                          | 运行当前单元格并在下面插入新的单元格         |
   | `Shift` + `Enter`                        | 运行当前单元格并选中下方的单元格             |
   | `Ctrl` + `Enter`                         | 运行当前单元格                               |
   | `j` / `k`、`Shift` + `j` / `Shift` + `k` | 选中下方/上方单元格、连续选中下方/上方单元格 |
   | `a` / `b`                                | 在下方/上方插入新的单元格                    |
   | `c` / `x`                                | 复制单元格 / 剪切单元格                      |
   | `v` / `Shift` + `v`                      | 在下方/上方粘贴单元格                        |
   | `dd` / `z`                               | 删除单元格 / 恢复删除的单元格                |
   | `Shift` + `l`                            | 显示或隐藏当前/所有单元格行号                |
   | `Space` / `Shift` + `Space`              | 向下/向上滚动页面                            |

   编辑模式下的快捷键：

   | 快捷键                     | 功能说明                               |
       | -------------------------- | -------------------------------------- |
   | `Shift` + `Tab`            | 获得提示信息                           |
   | `Ctrl` + `]`/ `Ctrl` + `[` | 增加/减少缩进                          |
   | `Alt` + `Enter`            | 运行当前单元格并在下面插入新的单元格   |
   | `Shift` + `Enter`          | 运行当前单元格并选中下方的单元格       |
   | `Ctrl` + `Enter`           | 运行当前单元格                         |
   | `Ctrl` + `Left` / `Right`  | 光标移到行首/行尾                      |
   | `Ctrl` + `Up` / `Down`     | 光标移动代码开头/结尾处                |
   | `Up` / `Down`              | 光标上移/下移一行或移到上/下一个单元格 |

   > **说明**：对于 macOS 系统可以将`Alt`键替换成`Option`键，将`Ctrl`键替换成`Command`键。

