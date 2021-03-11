
标准库 itertools 模块是不应该忽视的宝藏。


chain 连接多个迭代器。
    import itertools
    it = itertools.chain(range(3), "abc")
    print(it) # <itertools.chain object at 0x01BBF1D0>
    print(list(it)) # [0, 1, 2, 'a', 'b', 'c']


combinations 返回指定⻓度的元素顺序组合序列。
    import itertools
    it = itertools.combinations("abcd", 2)
    print(list(it)) # 打印: [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
    it = itertools.combinations(range(4), 2)
    print(list(it)) # 打印: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

combinations_with_replacement 会额外返回同一元素的组合。(python 3.x 才有)
    import itertools
    it = itertools.combinations_with_replacement("abcd", 2)
    print(list(it)) # 打印: [('a', 'a'), ('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'c'), ('c', 'd'), ('d', 'd')]


compress 按条件表过滤迭代器元素。(python 3.x 才有)
    import itertools
    # 条件列表可以是任何布尔列表。
    it = itertools.compress("abcde", [1, 0, 1, 1, 0])
    print(list(it)) # 打印:['a', 'c', 'd']


count 从起点开始, "无限" 循环下去。
    import itertools
    #for x in itertools.count(10, step=2): # (python 3.x 才有 step 参数, 表示间隔, 将打印: 10, 12, 14, 16, 18)
    for x in itertools.count(10): # 打印: 10 ~ 18
        print(x)
        if x > 17: break


cycle 迭代结束，再从头来过。
    import itertools
    for i, x in enumerate(itertools.cycle("abc")):
        print(x)
        if i > 7: break
    # 打印: a b c a b c a b c


dropwhile 跳过头部符合条件的元素。
    import itertools
    it = itertools.dropwhile(lambda i: i < 4, [2, 1, 4, 1, 3])
    print(list(it)) # 打印: [4, 1, 3]

    # 范例2：有时你要处理一些以不需要的行（如注释）开头的文件。「itertools」再次提供了一种简单的解决方案：
    string_from_file = """  
// Author: ...  
// License: ...  
//  
// Date: ...  
Actual content... 
""" 
    import itertools  
    for line in itertools.dropwhile(lambda line: line.startswith("//"), string_from_file.splitlines()):
        print(line)


takewhile 则仅保留头部符合条件的元素。
    import itertools
    it = itertools.takewhile(lambda i: i < 4, [2, 1, 4, 1, 3])
    print(list(it)) # 打印: [2, 1]


groupby 将连续出现的相同元素进⾏分组。
    import itertools
    print([list(k) for k, g in itertools.groupby('AAAABBBCCDAABBCCDD')]) # 打印: [['A'], ['B'], ['C'], ['D'], ['A'], ['B'], ['C'], ['D']]
    print([list(g) for k, g in itertools.groupby('AAAABBBCCDAABBCCDD')]) # 打印: [['A', 'A', 'A', 'A'], ['B', 'B', 'B'], ['C', 'C'], ['D'], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']]

islice 迭代器切片
    # 如果对迭代器进行切片操作，会返回一个「TypeError」，提示生成器对象没有下标，但是我们可以用一个简单的方案来解决这个问题：
    import itertools
    s = itertools.islice(range(50), 10, 20)
    for val in s:
        print(val)

    # 但需要注意的是，该操作要使用切片之前的所有生成器项，以及「islice」对象中的所有项。查看下面的打印结果可以了解其运行过程。
    import itertools
    def get():
        for i in range(50):
            print(i, '---')
            yield i
    s = itertools.islice(get(), 10, 20)
    for val in s:
        print(val, '+++')


