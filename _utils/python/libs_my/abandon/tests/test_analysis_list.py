#!python
# -*- coding:utf-8 -*-

"""
公用函数 analysis_list.py 的测试类
Created on 2017/4/27
Updated on 2019/1/18
@author: Holemar
"""
import logging
import unittest

from __init__ import *
from libs_my.abandon.analysis_list import VirtualObject, MultiLineAnalysis, MultiColumnsAnalysis


def create_MultiLine_data():
    """生成测试数据"""
    return [
        VirtualObject(year=2016, month=12, data_type='cost', value=5),
        VirtualObject(year=2017, month=1, data_type='cost', value=11),
        VirtualObject(year=2017, month=2, data_type='cost', value=12),
        VirtualObject(year=2017, month=3, data_type='cost', value=13),
        VirtualObject(year=2017, month=5, data_type='cost', value=55),
        VirtualObject(year=2017, month=1, data_type='salary', deparment='行政部', value=21),
        VirtualObject(year=2017, month=5, data_type='salary', deparment='市场部', value=25),
        VirtualObject(year=2017, month=2, data_type='salary', deparment='技术部', value=22),
        VirtualObject(year=2017, month=3, data_type='salary', deparment='技术部', value=23),
        VirtualObject(year=2017, month=4, data_type='salary', deparment='运营部', value=24),
    ]

class TestMultiLineAnalysis(unittest.TestCase):

    def test_filter(self):
        logging.info(u'测试 filter 函数')
        objects_list = create_MultiLine_data()
        result = MultiLineAnalysis(objects_list, col_name='data_type', value_col_name='value')
        assert len(result.object_list) == len(objects_list)
        assert result.object_list[0].year == 2016

        # filter 会改变类内部的 objects_list
        result2 = result.filter(year=2017)
        assert len(result.object_list) == len(objects_list) - 1
        assert result.object_list[0].year == 2017
        assert result == result2

        # _filter 不改变类内部的 objects_list
        result3 = result._filter(data_type='cost')
        assert result3 != result.object_list
        assert len(result.object_list) == len(objects_list) - 1
        assert result.object_list[0].year == 2017
        assert len(result3) == 4
        assert result3[0].data_type == 'cost'


    def test_get_months_list(self):
        logging.info(u'测试 get_months_list 函数')
        objects_list = create_MultiLine_data()
        result = MultiLineAnalysis(objects_list, col_name='data_type', value_col_name='value').filter(year=2017)

        l1 = result.get_months_list(data_type='salary')
        assert l1 == [21,22,23,24,25,0,0,0,0,0,0,0]

        l3 = result.get_months_list(data_type='cost')
        assert l3 == [11,12,13,0,55,0,0,0,0,0,0,0]

        l2 = result.get_months_list()
        assert l2 == [21,22,23,24,55,0,0,0,0,0,0,0] # 当筛选出两个不同 month 的值时，自动选最大的一个


    def test_get_dict_list(self):
        logging.info(u'测试 get_dict_list 函数')
        objects_list = create_MultiLine_data()
        result = MultiLineAnalysis(objects_list, col_name='data_type').filter(year=2017)

        l1 = result.get_dict_list('data_type', month=1)
        assert l1 == [{'name': 'cost', 'value':11}, {'name': 'salary', 'value':21}]

        l2 = result.get_dict_list('deparment', data_type='salary')
        assert l2 == [{'name': '行政部', 'value':21}, {'name': '市场部', 'value':25}, {'name': '技术部', 'value':22}, {'name': '技术部', 'value':23}, {'name': '运营部', 'value':24}]


    def test_to_MultiColumns(self):
        logging.info(u'测试 to_MultiColumns 函数')
        objects_list = create_MultiLine_data()
        result = MultiLineAnalysis(objects_list, col_name='data_type').filter(year=2017)

        mc = result.to_MultiColumns(('year', 'month'), col_name='data_type', value_col_name='value')
        assert isinstance(mc, MultiColumnsAnalysis)
        assert len(mc.object_list) == 5
        for o in mc.object_list:
            assert 0 <= o.cost <= 55 # 4月份的没有值，补上的 0 值
            assert 21 <= o.salary <= 25


def create_MultiColumns_data():
    '''生成测试数据'''
    return [
        VirtualObject(year=2016, month=12, cost=5, salary=21),
        VirtualObject(year=2017, month=1, cost=11, salary=21),
        VirtualObject(year=2017, month=2, cost=12, salary=22),
        VirtualObject(year=2017, month=3, cost=13, salary=23),
        VirtualObject(year=2017, month=4, cost=14, salary=24),
        VirtualObject(year=2017, month=5, cost=15, salary=25),
    ]

class TestMultiColumnsAnalysis(unittest.TestCase):

    def test_filter(self):
        logging.info(u'测试 filter 函数')
        objects_list = create_MultiColumns_data()
        result = MultiColumnsAnalysis(objects_list)
        assert len(result.object_list) == len(objects_list)
        assert result.object_list[0].year == 2016

        # filter 会改变类内部的 objects_list
        result2 = result.filter(year=2017)
        assert len(result.object_list) == len(objects_list) - 1
        assert result.object_list[0].year == 2017
        assert result == result2

        # _filter 不改变类内部的 objects_list
        result3 = result._filter(month=1)
        assert result3 != result.object_list
        assert len(result.object_list) == len(objects_list) - 1
        assert result.object_list[0].year == 2017
        assert len(result3) == 1
        assert result3[0].cost == 11


    def test_get_months_list(self):
        logging.info(u'测试 get_months_list 函数')
        objects_list = create_MultiColumns_data()
        result = MultiColumnsAnalysis(objects_list, month_col_name='month').filter(year=2017)

        l1 = result.get_months_list('salary')
        assert l1 == [21,22,23,24,25,0,0,0,0,0,0,0]

        l3 = result.get_months_list('cost')
        assert l3 == [11,12,13,14,15,0,0,0,0,0,0,0]


    def test_get_dict_list(self):
        logging.info(u'测试 get_dict_list 函数')
        objects_list = create_MultiColumns_data()
        result = MultiColumnsAnalysis(objects_list).filter(year=2017)

        l1 = result.get_dict_list(name_col_name='cost', value_col_name='salary')
        assert l1 == [{'name': 11, 'value': 21}, {'name': 12, 'value': 22}, {'name': 13, 'value': 23}, {'name': 14, 'value': 24}, {'name': 15, 'value': 25}]



if __name__ == "__main__":
    unittest.main()
