
操作CSV文件使用自带的csv包

1.读写函数
    reader=csv.reader(f, delimiter=',')：用来读取数据，reader为生成器，每次读取一行，每行数据为列表格式，可以通过delimiter参数指定分隔符
    writer=csv.writer(f)：用来写入数据，按行写入，writer支持writerow(列表)单行写入，和writerows(嵌套列表)批量写入多行，无须手动保存。

    当文件中有标题行时，可以使用header=next(reader)先获取到第一行的数据，再进行遍历所有的数据行。
    写入时，可以先使用writer.writerow(标题行列表)，写入标题行，再使用writer.writerows(多行数据嵌套列表)，写入多行数据（也可以逐行写入）。

    ### 读取示例 ###
    import csv
    import sys

    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    # py3 中，可以在打开文件时指定编码，但 py2 的 open 不能。兼容方式是 py2 使用 codecs.open
    if PY2:
        from codecs import open  # 打开文件时，可以指定编码

    with open('data.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        for row in reader:
            print(row)
    # 注意：reader必须在文件打开的上下文中使用，否则文件被关闭后reader无法使用
    # 所有的数字被作为字符串，如果要使用数字格式，应使用int()/float()做相应转换


    ### 写入示例 ###
    import csv

    header = ['name', 'password', 'status']

    data = [
        ['abc', '123456', 'PASS'],
        ['张五', '123#456', 'PASS'],
        ['张#abc123', '123456', 'PASS'],
        ['666', '123456', 'PASS'],
        ['a b', '123456', 'PASS']
    ]

    with open('result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    # 注意，打开文件时应指定格式为w, 文本写入，不支持wb,二进制写入，当然，也可以使用a/w+/r+
    # 打开文件时，指定不自动添加新行newline='',否则每写入一行就或多一个空行。
    # 如果想写入的文件Excel打开没有乱码，utf-8可以改为utf-8-sig。


2.使用字典格式的数据：DictReader, DictWriter
    注意数据必须有标题行时才能使用

    reader=csv.DictReader(f)：直接将标题和每一列数据组装成有序字典（OrderedDict）格式，无须再单独读取标题行
    writer=csv.DictWriter(f, 标题行列表)：写入时可使用writer.writeheader()写入标题，然后使用writer.writerow(字典格式数据行)或write.writerows(多行数据)

    ### 读取示例 ###
    import csv

    with open('data.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['name'], row['password'])

    ### 写入示例 ###
    import csv

    header = ['name', 'password', 'status']

    data = [
        {'name':'abc', 'password':'123456', 'status':'PASS'},
        {'name':'张五', 'password':'123#456', 'status':'PASS'},
        {'name':'张#abc123', 'password':'123456', 'status':'PASS'},
        {'name':'666', 'password':'123456', 'status':'PASS'},
        {'name':'a b', 'password':'123456', 'status':'PASS'}
    ]

    with open('result2.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()  # 先写入表头
        writer.writerows(data)

