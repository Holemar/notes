
编码规范：可读性很重要 Coding Style: Readability Counts

    Program must be writtern for people to read, and only incidentally for machines to exceute.
    程序主要是写给人看的，顺带着让机器去执行
    Try to make your program easy to read and obvious.
    请让你的代码简单明了可读。


PEP 8: Python编码规范指导 PEP 8: Style Guide for Python Code

    PEP = Python Enhancement Proposal
    PEP = Python提高建议

    A PEP is a design document providing information to the Python community,
    PEP是一份为Python社区提供的设计文档
    or describing a new feature for Python or its processes or environment.
    或者是python的新功能，新流程，新环境

    The Python community has its own standards for what source code should be like,
    Python社区对代码怎么写有明确的标准
    codified in PEP 8
    在PEP 8 中有规定
    These standards are different from those of other communities,
    这些标准与其它社区定义的有所不同，
    like C, C++, C#, Java, VB, etc.
    如C, C++, C#, Java, VB等等。

    Because identation and whitespace are so important in Python,
    由于缩进和空格在Python中如此重要
    the Style Guide for Python Code approaches a standard.
    Python风格规范中把它做为了一个明确规定
    It would be wise to adhere to the guide!
    聪明的话还是遵守规范吧
    Most open-source projects and (hopefully) in-house projects follow the style guide quite closely.
    大部分的开源代码和业内代码（希望如此）都严格遵守了这个编码规范。


空格 1 Whitespace 1

    4 spaces per indentation level
    4个空格组成一个缩进
    No hard tabs
    没有制表符
    Never mix tabs and spaces
    绝不允许制表符和空格符混用
    One blank line between functions
    函数之间以一个空行分割
    类之间以二个空行分割


空格 2 Whitespace 2

    Add a space after “,” in dicts, lists, tuples, argument lists, and after “:” in dicts, but not before
    在”,”, lists, tuples, 参数列表，dict中的”:”后面加一个空格
    Put spaces around assignments, comparisons (except in argument lists)
    在赋值和比较周围加入空格
    No spaces just inside parentheses or just before argument lists
    不要在小括号或者是参数列表之前加空格
    No spaces just inside docstrings
    不要在docstrings中加入空格

        def make_squares(key, value=0):
            """Return a dictionary and a list..."""
            d = {key: value}
            l = {key: value}
            return d, l


命名 Naming

    joined_lower for functions, methods, attributes
    对函数，方法，属性统一使用小写加下划线
    joined_lower or ALL_CAPS for contrants
    对常数使用小写加下划线或者全大写
    StudlyCaps for classes
    对于类使用StudlyCaps
    camelCase only to conform to pre-existing conventions
    对于已经存在的转换：camelCase
    Attributes: interface, _internal, __private


长整行及换行 Long Lines & Continuations

    Keep lines below 80 characters in length
    保持每一行小于80个字符
    Use implied line continuation inside parentheses/brackets/braces:
    在小括号，中括号，大括号中隐式换行

        def __init__(self, first, second, third,
                     fourth, fifth, sixth):
            output = (first + second + third
                      + fourth + fifth + sixth)

    Use backslashes as a last resort:
    实在不行，用反斜杠

        VeryLong.left_hand_side \
            = even_longer.right_hand_side()

    Backslashes are fragile; the must end the line they’re on.
    反斜杠很脆弱，它们必须作为每行的最后一个字符
    If you add a space after the backslash, it won’t work any more.
    如果你在反斜杠后面加入一个空格，它就不能正常工作了。
    Also, they’re ugly.
    另外，它们丑爆了


长字符串 Long Strings

    Adjacent literal strings are concatenated by the parser:
    邻接的字母会被编译器连接在一起组成字符串

        >>> print 'o' 'n' 'e'
        one

    The spaces between literals are not required, but help with readability. Any type of quoting can be used:
    字母之间的空格并不是必须的，但是可以提高可读性，单引号和双引号可以混用

        >>> print 't' r'\/\/' """o"""
        t\/\/o

    The string prefixed with an “r” is a “raw” string. Backslashes are not evaluated as escape in raw strings.
    以”r”打头的字符串都是”raw”字符串。反斜线在raw字符串中不会被作为转义字符。
    They’re usefual for regular expressions and Windows file system path.
    这一点在正则表达式和Windows文件系统目录中很有用。

    Note named string objects are not concatenated.
    注意命名的字符串不能直接组成字符串。

        >>> a = 'three'
        >>> b = 'two'
        >>> a b
        File "<stdin>", line 1
        a b
          ^
        SyntaxError: invalid syntax

    That is because the automatic concatenation is a feature of the Python parser/compiler,
    那是因为自动连接是Python编译器的功能，
    not the interpreter. You must use the “+” to concatenate strings at run time.
    而不是解释器的功能。在运行时，你必须使用”+”来连接字符串。

    The parentheses allow implicit line continuation.
    圆括号中允许隐式行连接。

        text = ('Long strings can be made up '
        'of several shorter strings.')

    Multiline strings use triple quotes:
    多行字符串可以使用三个引号

        """Triple
        double
        quotes"""

        '''\
        Triple
        single
        quotes\
        '''

    In the last example above (triple single quotes), note how the backslashes are used to
    在上面的最后一个例子中(三个单引号), 注意反斜线是如何使用来转义行尾的。
    escape newlines. This eliminates extra newlines, while keeping the text and quotes nicely
    这样继减少了新的空行，又使得文字保持了漂亮的左对齐。
    left-justified. The backslashes must be at the end of their lines.
    反斜线必须用在每一行的最后。

    Compound statements
    复合表达式
    Good:

        if foo == 'blah':
            do_something()
        do_one()
        do_two()
        do_three()

    Bad:

        if foo == 'blah': do_something()
        do_one(); do_two(); do_three()

    Whitespace & indentations are useful visual indicators of the program flow. The indentation
    空格和缩进对代码的流程有直观的指示作用。
    of the second “Good” line above shows the reader that something’s going on, whereas the lack
    在”Good”中第二行的缩进向读者显示了有的事情还在继续，
    of indentation in “Bad” line hides the “if” statement.
    而在”Bad”中没有缩进则隐藏了”if”表达式。

    Docstrings & Comments
    文档说明和注释
    Docstrings = How to use code
    文档说明 = 如何使用代码
    Comments = Why (rationale) & how code works
    注释 = 代码为什么要这样写，如何工作

    Docstrings explain how to use code, and are for the users of your code.
    文档说明用来解释代码是如何工作的，是写给读代码的人看的。
    Uses of docstrings:
    文档说明的作用：
    - Explain the purpose of the fuction even if it seems obvious to you, because it might not be
    - 解释函数的功能，即使它看起来对你显而易见，但它对后来看你的代码的人来说未必显而易见。
    - obvious to someone else later on.
    - Describe the parameters expected, the return values, and any exceptions raised.
    - 描述期望的参数，返回值和任何可能出现的异常
    - If the method is tightly coupled with a single caller, make some mention of the caller.
    - 如果这个方法与调用者紧密相关，有必要提一下调用者
    - (Though be careful that the caller might be changed later)
    - 但要注意调用者后面可能会改变
    - Comments explain why, and are for the maintainers of your code. Examples include notes to yourself, like:
    - 注释是为了维护代码而写的，它解释了为什么要这样做。例如写一些note来提醒一下自己。

    # !!! BUG: ...
    # !!! FIX: This is a hack
    # ??? Why is this here?

    Both of these groups include you, so write good docstrings and comments!
    所有的这些都与你相关，所以写好文档说明和注释
    Docstrings are useful in interactive use (help()) and for auto-documentation systems.
    文档说明在使用交互式help命令时有用，也可以用来自动生成文档。

    False comments & docstrings are worse than none at all.
    不正确的注释和文档说明比没有还要糟糕。
    So keep them up to date!
    所以要让它们保持最新
    When you make changes, make sure the comments & docstrings are consisitent with the code,
    当你改代码的时候，把注释和文档说明也要一起更新
    and don’t contradict it.
    不能让它们自相矛盾。



实用性高于纯粹性 Practicality Beats Purity

    There are always exceptions. From PEP 8:
    事情总有例外，从PEP 8:

    But most importantly: know when to be inconsistent - sometimes the style guide just doesn’t apply.
    最重要的是：知道什么时候不再保持一致性 – 有时候规范指导并不有效。
    When in doubt, use your best judgement. Look at other examples and decide what looks best.
    当你有所怀疑的时候，尝试做尽可能好的决定。参考其它的例子来决定怎么做最好。
    And don’t hesitate to ask!
    有问题不要犹豫
    Two good reasons to break a particular rule:
    两个打破特殊规则的理由：
    1. When applying the rule would make the code less readable,
    当使用该规则会让代码变得难以理解，
    even for someone who is used to reading code that follows the rules.
    即使是对于那些熟知规则的人来说也是这样。
    2. To be consisitent with surrouding code that also breaks it (maybe for historic reasons)
    （也许是历史原因）与周围的代码一致也不符合规则
    – although this is also an opportunity to clean up someone else’s mess.
    尽管这是一个清理他人烂摊子的好机会。
    … But practicality shouldn’t beat purity to a pulp!
    但也不能因为实用就把代码变成一坨屎.

