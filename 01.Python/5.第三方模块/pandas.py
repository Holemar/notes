
pandas
    Python Data Analysis Library 或 pandas 是基于 NumPy 的一种工具，该工具是为了解决数据分析任务而创建的。
    Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。
    pandas提供了大量能使我们快速便捷地处理数据的函数和方法。你很快就会发现，它是使Python成为强大而高效的数据分析环境的重要因素之一。


Pandas 中的数据结构
    Series : 一维数组，与Numpy中的一维array类似。
        二者与Python基本的数据结构List也很相近，其区别是 :
        List中的元素可以是不同的数据类型，而Array和Series中则只允许存储相同的数据类型，这样可以更有效的使用内存，提高运算效率。
    Time- Series : 以时间为索引的Series。
    DataFrame : 二维的表格型数据结构。很多功能与R中的data.frame类似。可以将DataFrame理解为Series的容器。以下的内容主要以DataFrame为主。
    Panel : 三维的数组，可以理解为DataFrame的容器。


# 范例
    import pandas as pd
    from django.db import connections

    # 定义个空的 DataFrame 对象
    df = pd.DataFrame()


  ### 数据读取 ###

    # 查询 数据库
    df = pd.read_sql(sql, connections['conn1']) # 直接用 SQL 查询
    df = pd.read_sql(sql, connections['conn2'], params=[参数1, 参数2, ...]) # 使用带参数的 SQL 查询

    # 判断是否有 取到数据
    if df.empty: print('没有数据')

    # 数据复制
    df_2 = df.copy()


  ### 数据 列名 ###

    # 各列的名称
    columns = df.columns # 字段名列表
    print(columns) # 打印如： Index([u'列名1', u'列名2', u'列名3'], dtype='object')
    if 'emp_id' not in df.columns:pass

    # 修改列表
    df = df.rename(columns={'旧列名':'新列名', '迟到小时数': 'late_hour', '旷工小时数': 'absent'})


  ### 数据合并 ###

    # 数据合并(扩展字段的形式合并)
    df = pd.merge(df, df2, how='left', on='emp_id') # left join 形式合并， on 字段 emp_id
    df = pd.concat([df1, df2], axis=0) #todo: 用法未知，跟上面一句几乎一样


  ### 数据导出 ###

    # 把数据集合转成 list<dict> 的形式返回
    data_list = df.to_dict('index').values()
    emp_ids = df.to_dict("list")['emp_id'] # 将 emp_id 列的值全部取出来

    # 只转变其中一列的数据, 以 list<字段类型> 的形式返回
    col_list = df.字段名1.values.tolist()
    col_list2 = df['字段名2'].tolist()
    col_list2 = df['字段名3'].values.tolist()


  ### 数据删除 ###

    # 删除里面的“字段名1”的列
    df_2 = df.drop('字段名1', axis=1) # 不修改原数据，返回一个新数据集合
    df.drop('字段名1', axis=1, inplace=True) # inplace=True 参数表示修改原数据， 没有返回值

    # 一起删除多列
    df_2 = df.drop(['字段名1','字段名2','字段名3',...], axis=1)
    df.drop(['字段名1','字段名2','字段名3',...], axis=1, inplace=True)

    # 只保留固定的列
    save_columns = {'emp_id', 'json', 'source', 'leave_date', 'is_new', 'has_salary', 'first_dep_name', 'remark'} # 会保留的字段名 set
    drop_list = list(set(df.columns).difference(save_columns))
    df.drop(drop_list, axis=1, inplace=True)

    # 只保留固定的列(且调整各列表的顺序)
    df = df[['字段名1','字段名2','字段名3',...]]

    # 注： inplace 参数表示是否在原数据基础上修改。 默认为 False 即不修改原数据, 而是返回新数据集合。
    # 设置 inplace=True 时修改原数据，且没有返回值


  ### 数据筛选 ###

    df_1 = df[~df.字段名1.isnull()] # 筛选出只有“字段名1”值非空的
    df_2 = df[df.字段名1.isnull()] # 筛选出只有“字段名1”值为空的
    df_3 = df[df.字段名2 == True] # 筛选出只有“字段名2”值为 True 的
    df_4 = df[~df.emp_id.isin(emp_id_list)] # 用 isin 函数指向列表， emp_id_list 是一个列表
    df_5 = df[(df.字段名3 == 3) | (df.字段名4 == 4)]
    df_6 = df[(df.字段名5.isnull()) & (df.字段名6.isnull())]

    # Pandas 空值默认使用是 numpy NAN, python 无法识别， 用None 代替 NaN
    df = df.where(pd.notnull(df), None)


  ### apply 操作 ###

    # 对某个列的各值操作
    df['字段名1'] = df.字段名1.apply(lambda x: x if x else 0) # 参数 x 是指各行的对应“字段名1”的值
    df['字段名1'] = df['字段名1'].apply(lambda x: x if x else 0)

    # 参数 axis=1 将按每行处理数据，默认参数 axis=0 时按每列处理数据
    df['字段名2'] = df.apply(lambda x: handle(x), axis=1, reduce=True) # 参数 x 是指各行的整行的值(dict形式读取出来)
    df['字段名2'] = df.apply(lambda x: handle(x), axis=1) #todo: reduce=True 参数的含义未知

    # 给各行加上“序号”
    df['index'] = range(1, df.shape[0] + 1) # 从 1 开始


  ### 赋值 ###

    # 整个列赋值(值都是同一个)
    df['字段名4'] = 11

    # 整个列赋值(逐个设置值。 得注意列表长度必须跟原 DataFrame 一样长,过长或者过短都会报错)
    df['列名2'] = ['21','22','23']


  ### 取值 ###

    # 求和 sum
    expected_amount = df['字段名5'].sum() # 求这一列的和值

    # 求总数量 count
    emp_count = df.shape[0]
    print(df.shape) # 打印如: (3, 4)     第一个值表示共有多少行，第二个值表示共有多少列

    # 取其中某行的一个值
    cost_total = df['字段名6'][0] # 取第一行的“字段名6”的值



  ### 读取 excel ###

    # 读取excel文件 (支持在线 url 文件，以及本地硬盘文件)
    df = pd.read_excel(url)
    df = pd.read_excel(path, skiprows=[0]) # skiprows 是指跳过的行,这里是跳过第一行(因为excel文件是二级标题的，所以第二行才是真正标题，第一行是大标题没用)


  ### 写 excel ###
    import xlsxwriter
    import pandas as pd
    from openpyxl import load_workbook

    book = load_workbook(file_path) # 读取一个excel文件进来
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, u'工资', header=None, index=False, startrow=2) # 写入数据
    writer.save() # 保存文件

