# -*- coding: utf-8 -*-
"""
数据库公用函数(django数据库的操作,原生SQL模式)
Created on 2015/12/9
Updated on 2019/1/18
@author: Holemar

依赖第三方库:
    Django==1.8.1

"""

import datetime
import logging
import itertools
from time import time

from django.conf import settings
from django.db import models, connection, transaction
from django.db.backends.utils import CursorWrapper # 修改这个类的函数，用来输出 ORM 操作日志，主要是为了监控 SQL 执行效率
from django.core.management.color import no_style # Style是用来输出语句时着色的，没什么用
from django.db.backends.base.creation import BaseDatabaseCreation # 这个类就是用来生成SQL语句的。


__all__=('execute_sql', 'executemany', 'select_sql', 'create_table', 'get_table_name')

# SQL 超时警告时间(单位：秒， 执行时间大于这个数值则发启警告， 配置成 0 或者 None 则关闭此警告)
SQL_WARN_TIME = getattr(settings, 'SQL_WARN_TIME', 1)
logger = logging.getLogger('libs_my.django.db')


def execute_sql(sql, param=None, rowid=False, connection=connection, transaction=transaction):
    """
    执行原生SQL语句(增删改操作)
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool} rowid: 为 True则在insert语句时返回新增主键(没有主键则返回影响的行数),为False则只返回影响行数(默认False)
    :param connection: 数据库连接(有传则使用传来的,没有则用默认的,便于使用事务)
    :param transaction: 数据库连接的事务(有传则使用传来的,没有则用默认的)
    :return {int}: 返回执行SQL影响的行数/新增主键id
    @example
        row = execute_sql("INSERT INTO product_log(uid,v) VALUES (%s,%s)", (20125412, '1.2.3', ))
        或者 row = execute_sql("INSERT INTO product_log (uid,v) VALUES (%(uid)s, %(v)s)", {'uid':20125412, 'v':'1.2.3'}) # MySQL支持 dict 参数，但 sqlite3 不支持
    """
    cursor = connection.cursor()
    # 数据修改操作——提交要求
    if param is None:
        row = cursor.execute(sql)
    else:
        row = cursor.execute(sql, param)
    # 提交事务
    transaction.commit()
    # sqlite3 数据库在前面执行时不直接返回影响行数，这里得再处理一下
    if not isinstance(row, int):
        row = cursor.rowcount
    # 插入,返回主键
    if rowid and sql.strip().lower().startswith('insert '):
        row = cursor.lastrowid or row # 如果表没有主键,则 lastrowid 会为0
    return row


def executemany(sql, param, connection=connection, transaction=transaction):
    """
    执行SQL语句(增删改操作), 同一个SQL语句,执行不同的多个参数
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param connection: 数据库连接(有传则使用传来的,没有则用默认的,便于使用事务)
    :param transaction: 数据库连接的事务(有传则使用传来的,没有则用默认的)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数)
    @example
        row = executemany("INSERT INTO product_log(uid,v) VALUES (%s,%s)", [(20125412, '1.2.3', ),(20125413, '2.0.3', ),(56721, '2.32.3', )])
        或者 row = executemany("INSERT INTO product_log (uid,v) VALUES (%(uid)s, %(v)s)", [{'uid':20125412, 'v':'1.2.3'},{'uid':56721, 'v':'2.32.3'}])
    """
    cursor = connection.cursor()
    if param is None:
        row = cursor.executemany(sql)
    else:
        row = cursor.executemany(sql, param)
    # 提交事务
    transaction.commit()
    # sqlite3 数据库在前面执行时不直接返回影响行数，这里得再处理一下
    if not isinstance(row, int):
        row = cursor.rowcount
    return row


def select_sql(sql, param=None, fetchone=False, connection=connection, transaction=transaction):
    """
    原生SQL语句查询
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool|int} fetchone: 为 True则只返回第一条结果, 为False则返回所有的查询结果, 为 int 类型则返回指定的条数
    :param connection: 数据库连接(有传则使用传来的,没有则用默认的,便于使用事务)
    :param transaction: 数据库连接的事务(有传则使用传来的,没有则用默认的)
    :return {list<dict> | dict}:
        当 参数 fetchone 为 True 时, 返回SQL查询的结果(dict类型),查不到返回 None,执行有异常时抛出 RuntimeError 异常
        当 参数 fetchone 为 False 时, 返回SQL查询结果集,查不到时返回空的 tuple,执行有异常时抛出 RuntimeError 异常
    @example
        results = select("SELECT * FROM product_log WHERE flag=%s AND v=%s", param=('n','1.2.0',))
        或者 results = select("SELECT * FROM product_log WHERE flag=%(flag)s AND v=%(v)s", param={'flag':'n', 'v':'1.2.0'})
    """
    cursor = connection.cursor()
    # 数据修改操作——提交要求
    if param is None:
        row = cursor.execute(sql)
    else:
        row = cursor.execute(sql, param)

    # 查不到时
    if row <= 0:
        result = None if fetchone == True else tuple()
    # 只返回1行
    elif fetchone == True:
        #result = [cursor.fetchone()]
        result = cursor.fetchmany(1)
    # 返回所有
    elif fetchone == False:
        result = cursor.fetchall()
    # 返回指定行数
    elif isinstance(fetchone, (int, long)):
        result = cursor.fetchmany(fetchone)
    else:
        result = cursor.fetchall()

    # 结果集转成 dict 类型
    if result:
        column_names = [d[0] for d in cursor.description]
        result = [Row(itertools.izip(column_names, row)) for row in result]
        if fetchone == True:
            result = result[0]
    return result


def create_table(model, connection=connection, transaction=transaction):
    """
    创建 model 所对应的表
    :param {django.db.models.Model} model: 生成表的 model 类
    :param connection: 数据库连接(有传则使用传来的,没有则用默认的,便于使用事务)
    :param transaction: 数据库连接的事务(有传则使用传来的,没有则用默认的)
    @raise : 执行有异常时抛出 RuntimeError 异常
    :return {string}: 建表语句
    """
    c = BaseDatabaseCreation(connection)
    create_sql = c.sql_create_model(model(), no_style())[0][0] # 生成建表的SQL语句
    try:
        execute_sql(create_sql, connection=connection, transaction=transaction) # 执行SQL
    except: pass # 可能表已存在
    return create_sql


def bulk_create(object_list):
    """
    批量新增
    :param object_list: 要批量新增的model实例列表(要求各实例是同一个类型)
    """
    if not object_list:
        return
    assert isinstance(object_list, (tuple, list))
    cls = type(object_list[0])
    try:
        cls.objects.bulk_create(object_list, batch_size=200)
    except:
        for obj in object_list:
            try:
                obj.save(force_insert=True)
            except Exception, e:
                logger.error(u"批量新增异常:%s", e, exc_info=True)


def bulk_save(object_list, update_fields=None, batch_size=100):
    """
    批量更新
    :param object_list: 要批量更新的model实例列表(要求各实例是同一个类型)
    :param update_fields: 要更新的参数列表
    :param batch_size: 每批更新多少行
    """
    if not object_list:
        return
    assert isinstance(object_list, (tuple, list))

    # 批量更新(分页算法)
    i = 0
    loop_times = len(object_list) / batch_size  # 需要用几个事务来提交更新
    while i <= loop_times:
        begin = i * batch_size
        end = (i + 1) * batch_size
        bulk_slice = object_list[begin:end]
        i += 1
        if not bulk_slice: continue
        with transaction.atomic():
            for o in bulk_slice:
                if isinstance(o, models.Model):
                    obj = o
                    _update_fields = update_fields
                elif isinstance(o, (tuple, list)):
                    obj = o[0]
                    _update_fields = o[1]
                else:
                    raise RuntimeError(u'参数错误!')
                if _update_fields:
                    obj.save(update_fields=_update_fields)
                else:
                    obj.save()


def raw_sql(queryset):
    """
    获取queryset的原生sql
    :param queryset:
    :return:
    """
    sql_compiler = queryset.query.get_compiler(using=queryset.db)
    try:
        raw_sql, params = sql_compiler.as_sql()
    except Exception as e:
        logger.error(e.message, exc_info=True)
        raw_sql, params = None, None
    return raw_sql, params, queryset.model


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def get_table_name(sql):
    """
    获取SQL的首个执行表名
    :param {string} sql: 要执行的 SQL 语句
    :return {string}: 首个表的名称
    """
    if not sql: return ''
    try:
        sql = sql.lower().replace('\n', ' ').replace(',', ' ').replace('(', ' ').replace(';', ' ')
        ss = sql.strip().split(' ')
        ss[:] = [s for s in ss if s] # 去掉列表里的空字符串(sql里有连续多个空格导致)
        if not ss: return ''
        if ss[0] == 'select':
            while 'from' in ss:
                ss[:] = ss[ss.index('from')+1:]
                if 'where' in ss:
                    ss[:] = ss[:ss.index('where')]
        elif ss[0] == 'delete':
            if 'from' in ss:
                ss[:] = ss[ss.index('from')+1:]
            if 'where' in ss:
                ss[:] = ss[:ss.index('where')]
        elif ss[0] == 'insert':
            ss[:] = [ss[2]]
        elif ss[0] == 'update':
            ss[:] = [ss[1]]
        elif ss[0] == 'update':
            ss[:] = [ss[1]]
        elif 'table' in ss:
            ss[:] = ss[ss.index('table')+1:]
        elif 'on' in ss:
            ss[:] = ss[ss.index('on')+1:]
        table_name = ss[0] if ss else ''
        table_name = table_name.strip().replace('`', '')
        return table_name
    except:
        return ''


def run_log(run_time, sql, parm=None, result=None):
    """
    监控SQL的执行效率，执行超时的发起警告
    :param {int | long | float} run_time: SQL 执行时间，单位：秒
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    """
    if SQL_WARN_TIME and run_time >= SQL_WARN_TIME:
        try:
            content = u'SQL执行超时，耗时:%.4f秒，SQL:%s; 参数:%s， 返回:%s' % (run_time, sql, parm, result)
            logger.warn(content, extra={'duration': run_time, 'sql': sql, 'params': parm})
        except Exception, e:
            logger.error(u"记录SQL超时日志错误:%s", e, exc_info=True)
    else:
        logger.info(u'执行SQL，耗时:%.4f秒，SQL:%s， 参数:%s, 返回:%s', run_time, sql, parm, result, extra={'duration': run_time, 'sql': sql, 'params': parm, 'result':result})


def _execute(self, sql, params=None):
    start = time()
    result = None
    try:
        result = self._orig_execute(sql, params)
        return result
    except Exception, e:
        run_sql = self.db.ops.last_executed_query(self.cursor, sql, params)
        logger.error(u"SQL执行失败:%s, SQL:%s; 参数:%s, 返回:%s", e, run_sql, params, result, exc_info=True)
        raise
    finally:
        run_sql = self.db.ops.last_executed_query(self.cursor, sql, params)
        duration = time() - start
        run_log(duration, run_sql, params, result)

def _executemany(self, sql, param_list):
    start = time()
    result = None
    try:
        result = self._orig_executemany(sql, param_list)
        return result
    except Exception, e:
        logger.error(u"SQL执行失败:%s, SQL:%s, 参数:%s, 返回:%s", e, sql, param_list, result, exc_info=True)
        raise
    finally:
        duration = time() - start
        run_log(duration, sql, param_list, result)

# 修改 django 的 ORM SQL 日志输出, 以便监控性能
_orig_execute = getattr(CursorWrapper, 'execute')
_orig_executemany = getattr(CursorWrapper, 'executemany')
setattr(CursorWrapper, '_orig_execute', _orig_execute)
setattr(CursorWrapper, '_orig_executemany', _orig_executemany)
setattr(CursorWrapper, 'execute', _execute)
setattr(CursorWrapper, 'executemany', _executemany)
