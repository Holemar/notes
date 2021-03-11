#!python
# -*- coding:utf-8 -*-
"""
兼容py2及py3的log设置
1. 日志内容的长度截取
2. 支持自定义日志存储，如数据库存储
"""

import os
import sys
import time
import datetime
import decimal
import uuid
import logging
from logging.handlers import TimedRotatingFileHandler as FileHandler

from flask import request

# 读取外部配置
DEBUG = os.environ.get('DEBUG') in ('True', 'true', '1')  # 是否 debug 模式
LOG_PARAM_LEN = int(os.environ.get('LOG_PARAM_LEN') or 1000)  # 日志里各参数的最大长度限制
BASE_PATH = os.getcwd()  # 本项目的运行路径

LOG_MIN = 50  # 嵌套日志的最短长度，过短会导致无限递归截取。
_FORMAT = '[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)s] %(levelname)s: %(message)s'
_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=_LEVEL, format=_FORMAT)
# 数据库日志的日志级别: DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
DB_LOG_LEVEL = int(os.environ.get('DB_LOG_LEVEL') or 30)


def short_log(value, length=None):
    """日志截取，避免日志过长"""
    length = length or LOG_PARAM_LEN
    if not length:
        return value
    if value is None:
        return None
    length = max(length, LOG_MIN)  # 长度不能无限小
    if not isinstance(value, str):
        _value = str(value)
        # 只有长度超过的，才转换类型，否则不轻易转换。避免格式化错误。
        if len(_value) > length:
            value = _value
    if isinstance(value, str) and len(value) > length:
        value = value[0:length // 2] + '...' + value[-length // 2:]
    return value


def deep_short_log(value, length=None):
    """
    将 list,tuple,set,dict 等类型里面的字符截短
    :param value: 将要被转码的值,类型可以是:dict,list,tuple,set 等类型
    :param length: 截取长度
    :return: 尽量返回原本的参数类型(list,tuple,set,dict等类型会保持不变)，但参数过长则会变成字符串类型截取
    """
    length = length or LOG_PARAM_LEN
    if not length:
        return value
    if not value:
        return value
    length = max(length, LOG_MIN)  # 长度不能无限小
    # str/bytes 类型的
    if isinstance(value, (str, bytes, bytearray)):
        return short_log(value, length=length)
    # 不会超出长度的类型，直接返回(这里认为设置的长度不小于100)
    elif isinstance(value, (bool, float, complex, uuid.UUID, time.struct_time, datetime.datetime, datetime.date)):
        return value
    # 这些数值也有可能几百位，超出长度限制
    elif isinstance(value, (int, decimal.Decimal)):
        return short_log(value, length=length)
    # list,tuple,set 类型,递归转换
    elif isinstance(value, (list, tuple, set)):
        arr = [deep_short_log(item, length=length // 2) for item in value]
        # 尽量不改变原类型
        if isinstance(value, list): return arr
        if isinstance(value, tuple): return tuple(arr)
        if isinstance(value, set): return set(arr)
    # dict 类型,递归转换(字典里面的 key 也会转成 unicode 编码)
    elif isinstance(value, dict):
        this_value = {}  # 不能改变原参数
        for key1, value1 in value.items():
            # 字典里面的 key 也转成 unicode 编码
            key1 = deep_short_log(key1, length=length // 2)
            this_value[key1] = deep_short_log(value1, length=length // 2)
        return this_value
    # 其它类型
    else:
        return short_log(value, length=length)


class StringFilter(logging.Filter):
    """用于修改日志的字符串"""

    def filter(self, record):
        msg = record.msg
        # 已处理过，不再处理
        if hasattr(record, '_filter_msg'):
            return record._filter_msg
        if isinstance(msg, (bytes, bytearray)):
            msg = msg.decode()
        elif not isinstance(msg, str):
            try:
                msg = str(msg)
            except Exception as e:
                logging.exception('日志值类型格式化错误:%s, %s', e, msg)
                record._filter_msg = False
                return False  # 报异常就别再打印此日志了
        if isinstance(msg, str) and '%' in msg and record.args:
            try:
                args = record.args
                # list,tuple,set,dict 类型,递归转换
                if isinstance(args, (list, tuple, set, dict)):
                    args = deep_short_log(args, length=LOG_PARAM_LEN)
                # 字符串合并
                msg %= args
                record.args = ()
            # 捕获未知错误，有可能日志里包含二进制、错误编码等
            except Exception as e:
                logging.exception('日志参数传递错误:%s, %s', e, msg)
                record._filter_msg = False
                return False  # 报异常就别再打印此日志了
        # 字符串处理完毕
        record.msg = short_log(msg, length=LOG_PARAM_LEN * 3)
        record._filter_msg = True
        return True


class DbHandler(logging.Handler):
    """写入数据库的日志记录"""

    def emit(self, record):
        """日志输出"""
        # 存储不被截取的log消息
        obj = {
            'name': record.name,  # logger 名称
            'level': record.levelno,  # 日志级别，跟 logging 的级别一样的数值
            'message': record.getMessage(),  # 日志内容
            'created_at': datetime.datetime.fromtimestamp(record.created),

            'file_path': record.pathname,  # 写日志的代码所在文件的路径
            'module': record.module,  # 写日志的代码所在的 module
            'func_name': record.funcName,  # 写日志的代码所在的 函数名
            'line_no': record.lineno,  # 写日志的代码所在文件的 行数
            'thread_name': record.threadName,  # 写日志的代码所在的 线程名
            'process_name': record.processName,  # 写日志的代码所在的 进程名

            'exc_info': str(record.exc_info) if record.exc_info else None,  # 抛出的Exception
            'exc_text': str(record.exc_text) if record.exc_text else None,  # 错误信息的堆栈
            'stack_info': str(record.stack_info) if record.stack_info else None,
        }
        if record.levelno >= 40:
            obj['f_locals'] = get_locals(record.pathname)  # 出错时的各变量key/value
        if record.exc_info or obj.get('f_locals'):
            obj['exc_text'] = obj['exc_text'] or traceback.format_exc()
        db = get_db()  # 获取数据库连接，依赖外部
        db.log.insert(obj)

# 数据库记录日志的 Log 类范例  ##### start #####
import types
import traceback
from mongoengine import Document
from mongoengine.fields import IntField, StringField, DictField, DateTimeField

# 记录各变量时，排除的类型
NotRecordTypes = (types.FunctionType, types.LambdaType, types.ModuleType, type(Document), type)


def get_locals(pathname):
    """获取报错时的所有变量值
    :param pathname:报错logger所在文件名
    """
    # 获取报错时的变量
    t, v, tb = sys.exc_info()
    if tb is None:
        return {}
    frame = tb.tb_frame
    while frame and hasattr(frame, 'f_back') and pathname != frame.f_code.co_filename:
        frame = frame.f_back
    if not frame:
        return {}

    # 获取打印 logger 行的所有变量
    f_locals = getattr(frame, 'f_globals', {})
    f_locals.update(getattr(frame, 'f_locals', {}))
    result = {}
    for k, v in f_locals.items():
        if k.startswith('__') or type(v) in NotRecordTypes:
            continue
        if repr(v).startswith(('<class ', '<built-in ')):
            continue
        # request 请求，记录详情
        if v is request:
            try:
                result[k] = dict(method=request.method, url=request.full_path, headers=dict(request.headers),
                                 ip=request.headers.getlist("X-Forwarded-For") or request.remote_addr,
                                 body=request.data.decode() if request.data else None, endpoint=request.endpoint
                                 )
            except:
                result[k] = repr(v)
        else:
            result[k] = repr_value(v)
    return result


def repr_value(value):
    """
    格式化变量，以便数据库存储
    其中 list,tuple,set,dict 等类型需要递归转变
    :param {任意} value 将要被格式化的值
    :return {type(value)}: 返回原本的参数类型(list,tuple,set,dict等类型会保持不变)
    """
    if value is None:
        return None
    # str 类型的
    elif isinstance(value, str):
        return value
    elif isinstance(value, (bytes, bytearray)):
        return repr(value)
    # 考虑是否需要转成字符串的类型
    elif isinstance(value, (bool, int, float, complex)):
        return value
    # time, datetime 类型转成字符串,需要写格式(不能使用 json.dumps,会报错)
    elif isinstance(value, time.struct_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', value)
    elif isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, decimal.Decimal):
        return str(value)
    elif isinstance(value, uuid.UUID):
        return value.hex
    # list,tuple,set 类型,递归转换
    elif isinstance(value, (list, tuple, set)):
        arr = [repr_value(item) for item in value]
        # 尽量不改变原类型
        if isinstance(value, list):  return arr
        if isinstance(value, tuple): return tuple(arr)
        if isinstance(value, set):   return set(arr)
    # dict 类型,递归转换(字典里面的 key 也会转成 unicode 编码)
    elif isinstance(value, dict):
        this_value = {}  # 不能改变原参数
        for key1, value1 in value.items():
            # 字典里面的 key 也转成 unicode 编码
            key1 = repr_value(key1)
            this_value[key1] = repr_value(value1)
        return this_value
    # 其它类型
    else:
        return repr(value)


''' 使用 model 的方式
class DbHandler(logging.Handler):
    """写入数据库的日志记录"""

    def emit(self, record):
        """日志输出"""
        # 存储不被截取的log消息
        msg = getattr(record, 'old_msg', record.getMessage())
        Log.add(record, msg)


class Log(Document):
    """Log Model."""
    meta = {
        'db_alias': 'lark_bot',  # db_alias用于指定model绑定的mongo连接，和connect函数中的alias对应
        'collection': 'log',
    }

    name = StringField()  # logger 名称
    level = IntField()  # 日志级别，跟 logging 的级别一样的数值
    message = StringField()  # 日志内容
    created_at = DateTimeField(db_field='_created', default=datetime.datetime.now)

    file_path = StringField()  # 写日志的代码所在文件的路径
    module = StringField()  # 写日志的代码所在的 module
    func_name = StringField()  # 写日志的代码所在的 函数名
    line_no = IntField()  # 写日志的代码所在文件的 行数
    thread_name = StringField()  # 写日志的代码所在的 线程名
    process_name = StringField()  # 写日志的代码所在的 进程名

    exc_info = StringField()  # 抛出的Exception
    exc_text = StringField()  # 错误信息的堆栈
    stack_info = StringField()
    f_locals = DictField()  # 出错时的各变量key/value

    @classmethod
    def add(cls, record):
        """写日志
        :param record: logging record
        """
        try:
            # 过滤 bad request 请求日志
            if record.name == "werkzeug" and record.module == "_internal" and record.funcName == "_log":
                return
            obj = cls()
            obj.name = record.name
            obj.level = record.levelno
            obj.file_path = record.pathname
            obj.module = record.module
            obj.func_name = record.funcName
            obj.line_no = record.lineno
            obj.thread_name = record.threadName
            obj.process_name = record.processName
            obj.message = record.getMessage()
            obj.created_at = datetime.datetime.fromtimestamp(record.created)
            obj.exc_info = str(record.exc_info) if record.exc_info else None
            obj.exc_text = str(record.exc_text) if record.exc_text else None
            if record.levelno >= 40:
                obj.f_locals = get_locals(record.pathname)
            if record.exc_info or obj.f_locals:
                obj.exc_text = obj.exc_text or traceback.format_exc()
            obj.stack_info = str(record.stack_info) if record.stack_info else None
            obj.save(force_insert=True)
        # 避免写日志的错误影响其它代码
        except Exception as e:
            print('数据库日志记录异常:', e)
            print(traceback.format_exc())
'''
# 数据库记录日志的 Log 类范例  ##### end #####


# 没有日志文件的目录，则先创建目录，避免因此报错
file_path = os.path.join(BASE_PATH, 'logs')
if not os.path.isdir(file_path):
    os.makedirs(file_path)

logger = logging.root
formatter = logging.Formatter(_FORMAT)
string_filter = StringFilter()
# 数据库日志(日志内容的长度不截取)
db_handler = DbHandler()
db_handler.setFormatter(formatter)
db_handler.setLevel(DB_LOG_LEVEL)
logger.addHandler(db_handler)
# 日志文件
filename = os.path.join(file_path, 'run.log')
file_handler = FileHandler(filename, when='midnight', backupCount=30)
stdout_handler = logging.StreamHandler(sys.stdout)  # 屏幕日志
for handler in (file_handler, stdout_handler):
    handler.setFormatter(formatter)
    handler.setLevel(_LEVEL)
    handler.addFilter(string_filter)
    # 排除同类 Handler，如屏幕输出(StandardErrorHandler)、文件输出
    logger.handlers[:] = [h for h in logger.handlers if not type(h) == type(handler)]
    logger.addHandler(handler)

