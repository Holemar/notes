

#随机数
import random

# 生成0至1之间的随机浮点数，结果大于等于0.0，小于1.0
print( random.random() )
# 生成1至10之间的随机浮点数
print( random.uniform(1, 10) )

# 产生随机整数
print( random.randint(1, 5) ) # 生成1至5之间的随机整数，结果大于等于1，小于等于5，前一个参数必须小于等于第二个参数
for i in xrange(5):
    print(i, random.randint(10, 90) ) # 产生 10~90 的随机整数(结果包含 10 和 90)

# 随机选取0到100间的偶数(第二个参数是选取间隔,如果从1开始,就是选取基数)
print( random.randrange(0, 101, 2) )

# 在指定范围内随机选一个值
print( random.choice(range(50)) ) # 这的选值范围是0~49
print( random.choice(['a', 2, 'c']) ) # 从列表中随机挑选一个数，也可以是元组、字符串
print( random.choice('abcdefg') ) # 可从字符串中随机选一个字符
# 在指定范围内随机选多个值(返回一个 list, 第二个参数是要选取的数量)
print( random.sample('abcdefghij',3) )
print( random.sample(['a', 2, 'c', 5, 0, 'ii'],2) )

# 洗牌,让列表里面的值乱序
items = [1, 2, 3, 4, 5, 6]
random.shuffle(items) # 这句改变列表里面的值,返回:None
print( items ) # 输出乱序后的列表


import os
a = os.urandom(16) # 生成16个随机unicode值
print([ord(i) for i in a]) # 打印出来，直接 print a 是无法阅读的


############### 实例：概率算法 ###############
    '''
    题目: 40%出现1,40%出现2，20%出现3，如何取这个随机数？
    其中数字和百分比会动态变化，有可能变成了，40%出现1,40%出现2,10%出现3,10%出现4
    '''

    from random import randint
    d = [
        (40, 1), # 第一个值表示出现的百分比，这里是 40% 概率出现
        (40, 2), # 这里出现概率 40%
        (20, 3), # 剩下 20% 的概率
    ]

    d2 = []
    max_rate = 0
    for rate, value in d:
        d2.append((rate + max_rate, value))
        max_rate += rate

    def get_number():
        i = randint(0, max_rate)
        for x, y in d2:
            if i <= x:
                return y

    # 判断上述概率是否正确
    n1, n2, n3 = 0, 0, 0
    for i in range(10000):
        num = get_number()
        if num == 1: n1 += 1
        if num == 2: n2 += 1
        if num == 3: n3 += 1

    print(n1, n2, n3)


############### 实例2 ###############
    '''
    题目：随机奖励金额，0.01~10 元，平均概率是 2 元
    '''

    import random

    d = [
        (20, 1), # 第一个值表示出现的百分比，这里是 20% 概率出现。第二个值是随机出现的范围，这里是随机出现 0~1 元(含小数)
        (40, 2), # 这里出现概率 40%, 随机出现 0~2 元(含小数)
        (20, 4.95), # 第二个值为了修复从 0.01 开始产生的误差
        (20, 10),
    ]

    d2 = []
    max_rate = 0
    for rate, value in d:
        d2.append((rate + max_rate, value))
        max_rate += rate

    def get_number():
        i = random.randint(0, max_rate)
        for x, y in d2:
            if i <= x:
                # 最低奖励 0.01 元
                n = random.uniform(0.01, y)
                # 由于是金额，需要四舍五入到小数点两位
                return round(n, 2)


    # 白盒测试，判断上述概率是否正确
    total = 0
    for rate, value in d:
        total += rate / 100.0 * (value + 0.01) / 2.0
    assert total == 2

    # 黑盒测试，判断上述概率是否正确
    n1, n2, n3 = 0, 0, 0
    for i in range(10000):
        n = get_number()
        n1 += n
        if n == 10: n2 += 1
        elif n == 0.01: n3 += 1

    print(n1, n2, n3)

