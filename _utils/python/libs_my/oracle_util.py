#!python
# -*- coding:utf-8 -*-
"""
公用函数(oracle数据库的操作)
Created on 2019/7/31
Updated on 2019/8/30
@author: Holemar

依赖第三方库:
    cx_Oracle==7.2.1

使用前必须先设置oracle数据库的连接
"""
import os
import sys
import time
import logging
import threading
import functools

os.environ['NLS_LANG'] = os.environ.get('NLS_LANG') or 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 防止中文乱码问题
import cx_Oracle as oracle

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    basestring = unicode = str
    long = int

__all__ = ('set_conn', 'get_conn', 'ping', 'select', 'get', 'execute', 'execute_list', 'executemany', 'Atom',
           'query_data', 'add_data', 'add_datas', 'del_data', 'update_data', 'format_sql', 'get_table', 'add_sql')

# 数据库连接
db_conn = None

# 请求默认值
CONFIG = {
    'host': '127.0.0.1',
    'port': '1521',
    'user': 'system',
    'password': 'oracle',
    'sid': 'xe',
}


def set_conn(conn_config):
    """
    设置数据库连接,使用前必须先设置
    :param {dict} conn_config: redis数据库连接配置
    :return {bool}: 是否成功连接上数据库,失败时会报异常
    """
    global CONFIG
    global db_conn
    CONFIG.update(conn_config)
    try:
        # 打开数据库连接
        db_conn = oracle.connect('{user}/{password}@{host}:{port}/{sid}'.format(**CONFIG))
    except Exception as e:
        logging.error('oracle connection error:%s', e, exc_info=True)
        raise
    return True


def ping(**kwargs):
    """
    探测oracle数据库是否连上
    :return {bool}: 能连上则返回True, 否则报异常
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if not conn:
            conn, cursor = get_conn()
        conn.ping()
        return True
    finally:
        close_conn(conn, cursor)


def get_conn(repeat_time=3):
    """
    获取数据库连接
    :return {tuple}: conn, cursor
    """
    conn = None
    cursor = None
    global db_conn, CONFIG
    # 允许出错时重复提交多次,只要设置了 repeat_time 的次数
    while repeat_time > 0:
        try:
            if db_conn is None:
                db_conn = oracle.connect('{user}/{password}@{host}:{port}/{sid}'.format(**CONFIG))
            if db_conn:
                conn = db_conn
                # 尝试连接数据库
                conn.ping()
                cursor = oracle.Cursor(conn)
                return conn, cursor
        # 数据库连接,默认8小时没有使用会自动断开,这里捕获这异常
        except Exception as e:
            repeat_time -= 1
            logging.error('oracle connection error:%s', e, exc_info=True)
            try:
                if cursor:
                    cursor.close()
            except:
                pass
            try:
                if conn:
                    conn.close()
            except:
                pass
    return conn, cursor


def close_conn(conn=None, cursor=None):
    """
    关闭数据库连接
    """
    # 每次请求都关闭连接的话,在多线程高并发时会导致报错,性能也会下降。
    # 这里不关闭连接,每次使用时探测可用性,并捕获连接超时断开的异常
    try:
        # if cursor:cursor.close()
        pass
    except:
        pass
    try:
        # if conn:conn.close()
        pass
    except:
        pass


def _init_execute(func):
    """处理获取数据库连接、超时记日志问题"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # 数据库连接(没有则获取, 有则不用)
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if conn is None and cursor is None:
            conn, cursor = get_conn()
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
        # 参数处理
        if args and len(args) >= 2:
            if not isinstance(args[1], (tuple, list, dict)):
                args = list(args)
                args[1] = [args[1]]
        elif 'param' in kwargs:
            param = kwargs.get('param')
            if param and not isinstance(param, (tuple, list, dict)):
                kwargs['param'] = [param]
        # 执行SQL
        method = kwargs.pop('function', None) or func
        result = method(*args, **kwargs)
        # 关闭数据库连接
        close_conn(conn, cursor)
        # 判断运行时间是否太长
        use_time = float(time.time() - start_time)
        log_param = str((args, kwargs.get('param', '')))
        # 为了更方便阅读,执行SQL的结果如果很短,则将它提前写
        logging.info(u"SQL, 耗时 %.4f 秒, 执行:%s, 返回:%s", use_time, log_param, result)
        return result
    return wrapper


def make_dict_factory(cursor):
    """
    将查询返回的 tuple 结果转换成 dict 结果
    :param cursor: 数据库连接的 Cursor Object
    :return:
    """
    column_names = [d[0] for d in cursor.description]
    return lambda *args: dict(zip(column_names, args))


@_init_execute
def select(sql, param=None, fetchone=False, **kwargs):
    """
    查询SQL结果
    :param {string} sql: 要查询的 SQL 语句，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool|int} fetchone: 为 True则只返回第一条结果, 为False则返回所有的查询结果, 为 int 类型则返回指定的条数
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {tuple<dict> | dict}:
        当 参数 fetchone 为 True 时, 返回SQL查询的结果(dict类型),查不到返回 None
        当 参数 fetchone 为 False 时, 返回SQL查询结果集,查不到时返回空的 tuple
    @example
        results = select("SELECT * FROM product_log WHERE flag=:1 AND v=:2", param=('n','1.2.0',))
        或者 results = select("SELECT * FROM product_log WHERE flag=:flag AND v=:v", param={'flag':'n', 'v':'1.2.0'})
    """
    try:
        result = None
        cursor = kwargs.get('cursor', None)
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        cursor.rowfactory = make_dict_factory(cursor)
        # count = cursor.rowcount  # 只有执行了 fetchall 之后才知道有多少行，没法预先判断
        # 查不到时
        # if count <= 0:
        #     return None if fetchone is True or fetchone == 1 else tuple()
        # 只返回1行(True 与 1 一样)
        if fetchone is True or fetchone == 1:
            return cursor.fetchone() or None
        # 返回所有
        elif fetchone is False or fetchone == 0:
            return cursor.fetchall()
        # 返回指定行数
        elif isinstance(fetchone, (int, long)):
            return cursor.fetchmany(fetchone)
        else:
            return cursor.fetchall()
    except Exception as e:
        logging.error("查询失败:%s, SQL:%s, %s, 返回:%s", e, sql, param, result, exc_info=True)
        return False


def get(sql, param=None, **kwargs):
    """
    查询SQL结果
    :param {string} sql: 要查询的 SQL 语句，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {dict}: 返回SQL查询的结果(dict类型),查不到返回 None,执行有异常时返回 False
    @example
        results = get("SELECT * FROM product_log WHERE flag=:1 AND v=:2", param=('n','1.2.0',))
        或者 results = get("SELECT * FROM product_log WHERE flag=:flag AND v=:v", param={'flag':'n', 'v':'1.2.0'})
    """
    kwargs.pop('fetchone', None)
    return select(sql, param=param, fetchone=True, **kwargs)


@_init_execute
def execute(sql, param=None, clash=1, transaction=True, **kwargs):
    """
    执行SQL语句(增删改操作)
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param {int} clash: 发生主键冲突,或者唯一键冲突时的返回值,默认1
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        row = execute("INSERT INTO product_log(uid,v) VALUES (:1, :2)", (20125412, '1.2.3', ))
        或者 row = execute("INSERT INTO product_log (uid,v) VALUES (:uid, :v)", {'uid':20125412, 'v':'1.2.3'})
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        # 开启事务
        # if transaction: conn.autocommit(0)
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        row = cursor.rowcount
        if transaction:
            conn.commit()
        return row
    # 主键冲突,或者唯一键冲突,重复insert,忽略错误
    except oracle.IntegrityError:
        logging.warning(u"主键冲突:%s, %s", sql, param)
        return clash
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s, 参数:%s", e, sql, param, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1


@_init_execute
def executemany(sql, param, clash=1, transaction=True, **kwargs):
    """
    执行SQL语句(增删改操作), 同一个SQL语句,执行不同的多个参数
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {int} clash: 发生主键冲突,或者唯一键冲突时的返回值,默认1
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        row = executemany("INSERT INTO product_log(uid,v) VALUES (:1, :2)", [(20125412, '1.2.3', ),(20125413, '2.0.3', ),(56721, '2.32.3', )])
        或者 row = executemany("INSERT INTO product_log (uid,v) VALUES (:uid, :v)", [{'uid':20125412, 'v':'1.2.3'},{'uid':56721, 'v':'2.32.3'}])
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        # 开启事务
        # if transaction: conn.autocommit(0)
        if param is None:
            cursor.executemany(sql)
        else:
            cursor.executemany(sql, param)
        if transaction:
            conn.commit()
        row = cursor.rowcount
        return row
    # 主键冲突,或者唯一键冲突,重复insert,忽略错误
    except oracle.IntegrityError:
        logging.warning("主键冲突:%s, %s", sql, param)
        return clash
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s, 参数:%s", e, sql, param, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1


def execute_list(sql_list, must_rows=False, transaction=True, **kwargs):
    """
    执行多条SQL语句，并且是一个原子事件(任何一条SQL执行失败，或者返回结果为0，都会全体回滚)
    :param {list<tuple<string,dict>>} sql_list: 形式为 [(sql1, param1),(sql2, param2),(sql3, param3),...]
    :param {bool} must_rows: 为 True则要求每个SQL语句影响的行数都必须大于1,影响行数为0会认为执行出错。为False则允许执行影响数为0
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数,执行有异常时返回 -1
    """
    conn = None
    cursor = None
    try:
        # 数据库连接(没有则获取, 有则不用)
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if conn is None and cursor is None:
            conn, cursor = get_conn()
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
        # 开启事务
        # if transaction: conn.autocommit(0)
        row = 0
        for args in sql_list:
            # 取出 sql 及 参数
            if isinstance(args, (list, tuple)):
                length = len(args)
                if length == 0:
                    continue
                elif length == 1:
                    sql, param = args[0], None
                else:
                    sql, param = args[0], args[1]
            elif isinstance(args, str):
                sql, param = args, None
            else:
                raise RuntimeError('其中一条参数无法解析:%s' % args)
            this_row = execute(sql, param=param, raise_error=True, transaction=False, **kwargs)
            if must_rows and this_row <= 0:
                raise RuntimeError('其中一条执行失败,影响行数为%s, SQL:%s, %s' % (this_row, sql, param))
            row += this_row
        if transaction:
            conn.commit()
        return row
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s", e, sql_list, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1
    finally:
        close_conn(conn, cursor)


def query_data(table, condition=None, orderby=None, **kwargs):
    """
    查询一个表
    :param {string} table: 要查询的表的名称(注意:表名的前缀"t_"也要求写,如果有的话)
    :param {dict} condition: 要查询的条件
    :param {string} orderby: 要排序的条件
    :param {bool|int} fetchone: 为 True则只返回第一条结果, 为False则返回所有的查询结果, 为 int 类型则返回指定的条数
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {tuple<dict> | dict}:
        当 参数 fetchone 为 True 时, 返回SQL查询的结果(dict类型),查不到返回 None
        当 参数 fetchone 为 False 时, 返回SQL查询结果集,查不到时返回空的 tuple
    @example
        results = query_data('service_conf', {"bid":333, "category":"cc"})
        实际执行: SELECT * FROM service_conf WHERE bid=333 AND category ='cc'
    """
    sql = u'SELECT * FROM "%s" ' % get_table(table)
    if condition:
        condition_sql = format_sql(' AND ', condition)
        sql += u" WHERE %s" % (condition_sql)
    if orderby:
        sql += u" ORDER BY %s" % (orderby)
    rows = select(sql, param=condition, **kwargs)
    return rows


def add_data(table, param, **kwargs):
    """
    插入数据到一个表
    :param {string} table: 要插入的表的名称(注意:表名的前缀"t_"也要求写,如果有的话)
    :param {dict} param: 要插入的内容
    :param {int} clash: 发生主键冲突,或者唯一键冲突时的返回值,默认1
    :param {bool} rowid: 为 True则在insert语句时返回新增主键(没有主键则返回影响的行数),为False则只返回影响行数(默认False)
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        # 添加一行
        rows = add_data('goods_log', {'bid':'kc','name':"e'ee"})
            实际执行: INSERT INTO goods_log (bid, name) VALUES ('kc', 'e''ee')

        # 添加多行
        rows = add_data('goods_log', [{'bid':'kc','name':"哈哈"}, {'bid':'kc','name':"呵呵"}])
           实际执行: INSERT INTO goods_log (bid, name) VALUES ('kc', '哈哈'), ('kc', '呵呵')
    """
    # 只添加一行数据
    if isinstance(param, dict):
        sql = add_sql(table, param)
        row = execute(sql, param=param, **kwargs)
        return row
    # 添加多行数据
    elif isinstance(param, (list, tuple, set)) and len(param) >= 1:
        if isinstance(param, set):
            param = list(param)
        sql = add_sql(table, param[0])
        row = executemany(sql, param=param, **kwargs)
        return row


def add_datas(table_list, **kwargs):
    """
    一起插入多个语句,原子操作，其中任意一个操作语句失败都会全体回滚
    :param {list<tuple<string,dict>>} table_list: 形式为 [(table_name1, param1),(table_name2, param2),(table_name3, param3),...]
    :param {bool} must_rows: 为 True则要求每个SQL语句影响的行数都必须大于1,影响行数为0会认为执行出错。为False则允许执行影响数为0
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数,执行有异常时返回 -1
    @example
        rows = add_datas([('goods_log',{'bid':'333','orderid':"e''ee"}),('product_log',{'bid':'444','orderid':u"哎f'f"})])
    """
    sql_list = []
    for table, params in table_list:
        sql = add_sql(table, params)
        sql_list.append((sql, params,))
    row = execute_list(sql_list, **kwargs)
    return row


def del_data(table, condition, **kwargs):
    """
    删除一个表的数据
    :param {string} table: 要删除数据的表的名称(注意:表名的前缀"t_"也要求写,如果有的话)
    :param {dict} condition: 要删除的条件,必须传此参数
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        rows = del_data('goods_log', {'bid':333,'orderid':"eee"})
        实际执行: DELETE FROM goods_log WHERE  bid=333 AND orderid ='eee'
    """
    if not condition:
        return 0
    condition_sql = format_sql(' AND ', condition)
    sql = u'DELETE FROM "%s" WHERE %s' % (get_table(table), condition_sql)
    row = execute(sql, param=condition, **kwargs)
    return row


def update_data(table, param, condition, **kwargs):
    """
    修改一个表的数据
    :param {string} table: 要修改数据的表的名称(注意:表名的前缀"t_"也要求写,如果有的话)
    :param {dict} param: 要修改的数据,必须传此参数
    :param {dict} condition: 要修改的条件,必须传此参数
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        rows = update_data('goods_log', {'bid':333,'orderid':"eee"}, {'id':223})
        实际执行: UPDATE goods_log SET bid=333, orderid ='eee' WHERE id=223
    """
    if not param:
        return 0
    up_sql = format_sql(' , ', param, keys_prefix='up_')
    condition_sql = format_sql(' AND ', condition, keys_prefix='cond_')
    sql = u'UPDATE "%s" SET %s WHERE %s' % (get_table(table), up_sql, condition_sql)
    # 参数合并(由于修改的数据字段名与条件的字段名有可能完全一样,所以得用前缀区分)
    sql_param = {}
    for k, v in param.items():
        sql_param[u'up_%s' % k] = v
    if condition:
        for k, v in condition.items():
            sql_param[u'cond_%s' % k] = v
    row = execute(sql, param=sql_param, **kwargs)
    return row


def format_sql(sep, param, keys_prefix='', **kwargs):
    """
    格式化SQL语句
    :param {string} seq: 分隔符
    :param {dict} param: 条件或值dict
    :param {list} keys_prefix: 替位符前缀(条件里面由于有相同的字段名,所以替位符得加上特殊前缀来标识)
    :return {string}: 语句拼接后的结果,如:
            format_sql(' AND ', {'flag':'xxx', 'v':2.56}) 返回: "flag=:flag AND v=:v"
            format_sql(', ', {'flag':'xxx', 'v':2.56}) 返回: "flag=:flag, v=:v"
    """
    if not param or not isinstance(param, dict):
        return '1=1'
    return (u"%s" % sep).join(u'"%s"=:%s%s' % (unicode(x).upper(), keys_prefix, unicode(x)) for x in param.keys())


def get_table(table, **kwargs):
    """
    转化表格名
    :param {string} table: 表格名
    :return {string}: 转化后的表格名
    """
    table = table.replace('"', '').replace("'", '')
    return str(table).upper()


def add_sql(table, param, **kwargs):
    """
    转成SQL插入语句
    :param {string} table: 表格名
    :param {dict} param: 条件或值dict
    :return {string}: 语句拼接后的结果,如:   INSERT INTO tableName (...) VALUES (...)
    """
    column = u", ".join(u'"%s"' % unicode(x).upper() for x in param.keys())
    value = u", ".join(u":%s" % unicode(x) for x in param.keys())
    sql = u'INSERT INTO "%s" (%s) VALUES (%s)' % (get_table(table), column, value)
    return sql


class Atom(object):
    """
    使用事务,原子地操作多个语句时,可使用本类
    注:同一个实例无法完美支持多线程操作,故去掉多线程
    """
    # 连接池对象
    __pool = {}
    __lock = threading.Lock()

    def __init__(self, **kwargs):
        """
        本类的构造,会打开连接、设置事务等。 需要手动提交
        :param 其他参数,连接 Oracle 数据库的连接参数,跟 oracle.connect 的一致。 有传则用传来的连接, 没有则用本文件预设或默认的。
            如: host, port, user, passwd, db, charset, cursorclas ...
        """
        conn, cursor, db_key = Atom.__get_conn(**kwargs)
        if not conn:
            logging.error('[red]oracle connection error[/red], new Atom() fail', extra={'color': True})
            raise RuntimeError(u"oracle 数据库连接不上")
        # 开启事务
        conn.begin()
        self.conn = conn
        self.cursor = cursor
        self.db_key = db_key
        self.other_params = {'conn': conn, 'cursor': cursor, 'transaction': False, 'threads': False}  # 额外参数

    @staticmethod
    def __get_conn(repeat_time=3, **kwargs):
        """
        静态方法，从连接池中取出连接
        :return oracle.connection
        """
        conn = None
        cursor = None
        db_key = repr(kwargs)
        pool = Atom.__pool.get(db_key)
        if pool is None:
            # 锁定, 避免并发访问时改变连接池的引用,保证同一个 db_key 只有一个连接池
            Atom.__lock.acquire()
            pool = Atom.__pool.get(db_key)
            if pool is None:
                pool = set()
                Atom.__pool[db_key] = pool
            # 释放锁
            Atom.__lock.release()
        # 允许出错时重复提交多次,只要设置了 repeat_time 的次数
        while repeat_time > 0 or len(pool) > 0:
            try:
                conn = pool.pop()
                # 尝试连接数据库
                conn.ping()
                cursor = conn.cursor()
                return conn, cursor, db_key
            # set 内容为空时, pop 会抛异常
            except KeyError:
                # 数据库连接配置
                global CONFIG
                db_config = CONFIG.copy()
                db_config.update(kwargs)
                try:
                    conn = oracle.connect('{user}/{password}@{host}:{port}/{sid}'.format(**db_config))
                    cursor = conn.cursor()
                    return conn, cursor, db_key
                except Exception as e:
                    logging.error(u'[red]oracle connection error[/red]:%s', e, exc_info=True, extra={'color': True})
                    raise
            # 连接超时或已断开
            except Exception as e:
                repeat_time -= 1
                logging.error(u'[red]oracle connection error[/red]:%s', e, exc_info=True, extra={'color': True})
                try:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                except:
                    pass
        return conn, cursor, db_key

    @staticmethod
    def __release(db_key, conn=None, cursor=None):
        """
        使用完数据库连接,放回线程池
        """
        if conn:
            Atom.__pool[db_key].add(conn)
        try:
            if cursor:
                cursor.close()
        except:
            pass

    def commit(self, dispose=True):
        """
        提交
        :param {bool} dispose: 是否需要消耗此对象(默认销毁)
        """
        self.conn.commit()
        if dispose:
            self.dispose()
        logging.info(u'事务提交完成,销毁对象:%s', dispose)

    def rollback(self, dispose=True):
        """
        回滚
        :param {bool} dispose: 是否需要消耗此对象(默认销毁)
        """
        self.conn.rollback()
        if dispose:
            self.dispose()
        logging.info(u'事务回滚完成,销毁对象:%s', dispose)

    def dispose(self):
        """
        释放连接资源
        """
        Atom.__release(self.db_key, conn=self.conn, cursor=self.cursor)
        self.conn = None
        self.cursor = None

    def __del__(self):
        """Delete the db connection."""
        try:
            self.dispose()
        except:
            pass

    # 下面动态加入本文件的所有函数作为类里面的函数
    # 即:  'ping', 'select', 'get', 'execute', 'execute_list', 'executemany', 'query_data', 'add_data', 'add_datas', 'del_data', 'update_data', 'format_sql', 'add_sql'
    for __function in __all__:
        # 下面函数无法实现,就不再加了
        if __function in ('init', 'set_conn', 'get_conn', 'Atom'):
            continue
        # 获取 docstring
        __doc = eval(u"%s.__doc__" % __function) or ''
        # 动态加入函数
        exec(u"""def %(function)s (self, *args, **kwargs):
        u'''%(doc)s'''; # 生成 docstring
        kwargs.update(self.other_params); # 设置额外参数
        res = %(function)s(*args, **kwargs); # 调用本文件的对应操作函数
        return res;""" % {'function': __function, 'doc': __doc})
    # 删除上面产生的临时变量,避免遗留在这类里面
    del __doc
    del __function
