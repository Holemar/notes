#python
# -*- coding:utf-8 -*-
"""
本模块是 统计分析 工具类
Created on 2017/4/27
Updated on 2019/1/18
@author: Holemar
"""
from __init__ import *


class VirtualObject(object):
    """
    虚拟类，用来将dict转成类
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MultiLineAnalysis(object):
    """
    多行存储的统计结果类
    """

    def __init__(self, object_list, col_name, value_col_name='value', value_type=None, month_col_name='month'):
        """
        :param object_list:数据列表
        :param col_name:存储各种类型值的字段名
        :param value_col_name:存值字段的字段名
        :param value_type:数据类型
        :param month_col_name:月份字段的字段名
        """
        self.object_list = list(object_list)
        self.col_name = col_name
        self.value_col_name = value_col_name
        self.value_type = value_type
        self.month_col_name = month_col_name

    def filter(self, **kwargs):
        """
        获取指定的筛选条件过滤数据列表(类里的 object_list 会去掉被过滤的值)
        :param kwargs:筛选条件
        """
        # 筛选
        for k,v in kwargs.items():
            self.object_list[:] = [o for o in self.object_list if getattr(o, k) == v]
        return self

    def _filter(self, **kwargs):
        """
        获取指定的筛选条件过滤数据列表(类里的 object_list 会去掉被过滤的值)
        :param kwargs:筛选条件
        """
        # 筛选
        data = list(self.object_list)
        for k,v in kwargs.items():
            data[:] = [o for o in data if getattr(o, k) == v]
        return data

    def get_months_list(self, value_type=None, **kwargs):
        """
        获取指定的各月数据列表，且按月份排序
        :param value_type:数据类型
        :param kwargs:筛选条件(类里的 object_list 不变)
        :return: {list<value_type>} 按月排序的数值列表
        """
        value_type = value_type or self.value_type
        data = self._filter(**kwargs)
        ret = []
        # 按月份排序数据，没有数据的补0
        for m in range(1, 13):
            value = max([getattr(o, self.value_col_name) for o in data if int(getattr(o, self.month_col_name)) == m] or [0]) or 0
            value = value_type(value) if value_type else value
            ret.append(value)
        return ret

    def get_dict_list(self, col_name=None, value_type=None, **kwargs):
        """
        获取指定字段的数据列表
        :param col_name:需要返回的字段名
        :param value_type:数据类型
        :param kwargs:筛选条件(类里的 object_list 不变)
        :return: {list<dict>} 按月排序的数值列表
        """
        col_name = col_name or self.col_name
        value_type = value_type or self.value_type
        data = self._filter(**kwargs)
        ret = []
        # 取值
        for obj in data:
            name = getattr(obj, col_name)
            value = getattr(obj, self.value_col_name) or 0
            value = value_type(value) if value_type else value
            ret.append({'name': name, 'value':value})
        return ret

    def to_MultiColumns(self, group_columns, col_name=None, value_col_name=None, value_type=None, **kwargs):
        """
        转换成多列存储的统计结果
        :param group_columns:分组聚合在一起的字段名列表
        :param col_name:需要转成列名的字段名
        :param value_col_name:存值字段的字段名
        :param value_type:数据类型
        :param kwargs:筛选条件(类里的 object_list 不变)
        :return: {MultiColumnsAnalysis} 多列存储的统计结果集
        """
        assert group_columns and isinstance(group_columns, (tuple, list, set))
        col_name = col_name or self.col_name
        value_col_name = value_col_name or self.value_col_name
        value_type = value_type or self.value_type
        data = self._filter(**kwargs)
        data_dict = {}
        cols = set() # 由于某些数据类型的可能没有记录，所以得记录并且在后面补上
        for obj in data:
            keys = tuple([str(getattr(obj, col)) for col in group_columns])
            kw = dict([(_col_name,getattr(obj, _col_name)) for _col_name in group_columns])
            virtual_obj = data_dict.setdefault(keys, VirtualObject(**kw))
            col = getattr(obj, col_name)
            cols.add(col)
            value = getattr(obj, value_col_name) or 0
            value = value_type(value) if value_type else value
            setattr(virtual_obj, col, value)
        object_list = data_dict.values()
        for virtual_obj in object_list:
            for col in cols:
                if not hasattr(virtual_obj, col):
                    setattr(virtual_obj, col, 0)
        return MultiColumnsAnalysis(object_list, month_col_name=self.month_col_name, value_type=value_type)


class MultiColumnsAnalysis(object):
    """
    多列存储的统计结果类
    """

    def __init__(self, object_list, month_col_name='month', value_type=None):
        """
        :param object_list:数据列表
        :param month_col_name:月份字段的字段名
        """
        self.object_list = list(object_list)
        self.month_col_name = month_col_name
        self.value_type = value_type

    def filter(self, **kwargs):
        """
        获取指定的筛选条件过滤数据列表
        :param kwargs:筛选条件
        """
        # 筛选
        for k,v in kwargs.items():
            self.object_list[:] = [o for o in self.object_list if getattr(o, k) == v]
        return self

    def _filter(self, **kwargs):
        """
        获取指定的筛选条件过滤数据列表(类里的 object_list 会去掉被过滤的值)
        :param kwargs:筛选条件
        """
        # 筛选
        data = list(self.object_list)
        for k,v in kwargs.items():
            data[:] = [o for o in data if getattr(o, k) == v]
        return data

    def get_months_list(self, col_name, value_type=None, **kwargs):
        """
        获取指定的各月数据列表，且按月份排序
        :param col_name:需要返回的字段名
        :param value_type:数据类型
        :param kwargs:筛选条件(类里的 object_list 不变)
        :return: {list<value_type>} 按月排序的数值列表
        """
        assert col_name and isinstance(col_name, basestring)
        value_type = value_type or self.value_type
        data = self._filter(**kwargs)
        ret = []
        # 按月份排序数据，没有数据的补0
        for m in range(1, 13):
            value = max([getattr(o, col_name, 0) for o in data if int(getattr(o, self.month_col_name)) == m] or [0]) or 0
            value = value_type(value) if value_type else value
            ret.append(value)
        return ret

    def get_dict_list(self, name_col_name, value_col_name, value_type=None, **kwargs):
        """
        获取指定字段的数据列表
        :param name_col_name:需要返回名称的字段名
        :param value_col_name:需要返回数值的字段名
        :param value_type:数据类型
        :param kwargs:筛选条件(类里的 object_list 不变)
        :return: {list<dict>} 按月排序的数值列表
        """
        assert name_col_name and isinstance(name_col_name, basestring)
        value_type = value_type or self.value_type
        data = self._filter(**kwargs)
        ret = []
        # 取值
        for obj in data:
            name = getattr(obj, name_col_name)
            value = getattr(obj, value_col_name) or 0
            value = value_type(value) if value_type else value
            ret.append({'name': name, 'value':value})
        return ret

