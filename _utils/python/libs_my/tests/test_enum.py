#!python
# -*- coding:utf-8 -*-

'''
公用函数 enum_util.py 的测试类
Created on 2015/12/11
Updated on 2019/7/11
@author: Holemar
'''
import logging
import unittest

from __init__ import *
from libs_my.enum_util import Const, get_enum_value

class Platform(Const):
    ios = (1, 'IOS')
    android = (2, 'ANDROID')
    wp = (3, 'WP')

class LocationType(Const):
    asia = ('Asia', u'亚洲')
    europe = ('Europe', u'欧洲')
    america = ('America', '美洲') # str 类型与 unicode 类型的字符串需区分
    australia = ('Australia', '澳洲')

class LocationType2(Const):
    asia = {'value':'Asia', 'label':u'亚洲'}
    europe = {'value':'Europe', 'label':u'欧洲'}
    america = {'value':'America', 'label':'美洲'} # str 类型与 unicode 类型的字符串需区分
    australia = {'value':'Australia', 'label':'澳洲'}

class LocationType3(Const):
    Asia = u'亚洲'
    Europe = u'欧洲'
    America = '美洲'
    Australia = '澳洲'

class TestConst(unittest.TestCase):

    def test_items(self):
        u'''返回数值列表 测试'''
        logging.info(u'测试 枚举 选项的取值')
        assert Platform() == [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        assert Platform._items == [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        # 会自动排序
        assert LocationType() == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]
        assert LocationType._items == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]
        # dict 值
        assert LocationType2() == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]
        assert LocationType2._items == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]
        # 字符串 值
        assert LocationType3() == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]
        assert LocationType3._items == [('America', '美洲'), ('Asia', u'亚洲'), ('Australia', '澳洲'), ('Europe', u'欧洲')]

    def test_key(self):
        u'''获取键 测试'''
        logging.info(u'测试 枚举.key 的取值')
        # 数字类型的值
        assert Platform.ios == 1
        assert Platform.android == 2
        assert Platform.wp == 3
        # 字符串类型的值
        assert LocationType.asia == 'Asia'
        assert LocationType.europe == 'Europe'
        assert LocationType.america == 'America'
        assert LocationType.australia == 'Australia'
        # dict 值
        assert LocationType2.asia == 'Asia'
        assert LocationType2.europe == 'Europe'
        assert LocationType2.america == 'America'
        assert LocationType2.australia == 'Australia'
        # 字符串 值
        assert LocationType3.Asia == 'Asia'
        assert LocationType3.Europe == 'Europe'
        assert LocationType3.America == 'America'
        assert LocationType3.Australia == 'Australia'

    def test_value(self):
        u'''获取展示值 测试'''
        logging.info(u'测试 枚举._attrs[键] 的取值')
        # 数字类型的值
        assert Platform._attrs[Platform.ios] == 'IOS'
        assert Platform._attrs == {1: 'IOS', 2: 'ANDROID', 3: 'WP'}
        assert Platform._labels_to_values == {'ANDROID': 2, 'IOS': 1, 'WP': 3}
        assert Platform._values == {'android': 2, 'ios': 1, 'wp': 3}
        assert Platform._labels == {'android': 'ANDROID', 'ios': 'IOS', 'wp': 'WP'}
        # 字符串类型的值
        assert LocationType._attrs[LocationType.asia] == u'亚洲'
        assert LocationType._attrs == {'Europe': u'欧洲', 'Australia': '澳洲', 'America': '美洲', 'Asia': u'亚洲'}
        assert LocationType._labels_to_values == {'澳洲': 'Australia', '美洲': 'America', u'欧洲': 'Europe', u'亚洲': 'Asia'}
        assert LocationType._values == {'europe': 'Europe', 'australia': 'Australia', 'america': 'America', 'asia': 'Asia'}
        assert LocationType._labels == {'europe': u'欧洲', 'australia': '澳洲', 'america': '美洲', 'asia': u'亚洲'}
        # dict 值
        assert LocationType2._attrs[LocationType2.asia] == u'亚洲'
        assert LocationType2._attrs == {'Europe': u'欧洲', 'Australia': '澳洲', 'America': '美洲', 'Asia': u'亚洲'}
        assert LocationType2._labels_to_values == {'澳洲': 'Australia', '美洲': 'America', u'欧洲': 'Europe', u'亚洲': 'Asia'}
        assert LocationType2._values == {'europe': 'Europe', 'australia': 'Australia', 'america': 'America', 'asia': 'Asia'}
        assert LocationType2._labels == {'europe': u'欧洲', 'australia': '澳洲', 'america': '美洲', 'asia': u'亚洲'}
        # 字符串 值
        assert LocationType3._attrs[LocationType3.Asia] == u'亚洲'
        assert LocationType3._attrs == {'Europe': u'欧洲', 'Australia': '澳洲', 'America': '美洲', 'Asia': u'亚洲'}
        assert LocationType3._labels_to_values == {'澳洲': 'Australia', '美洲': 'America', u'欧洲': 'Europe', u'亚洲': 'Asia'}
        assert LocationType3._values == {'Europe': 'Europe', 'Australia': 'Australia', 'America': 'America', 'Asia': 'Asia'}
        assert LocationType3._labels == {'Europe': u'欧洲', 'Australia': '澳洲', 'America': '美洲', 'Asia': u'亚洲'}

    def test_get_value(self):
        u'''获取枚举值 测试'''
        logging.info(u'测试 枚举.get_enum_value 的取值')
        # 数字类型的值
        assert get_enum_value(Platform, 'ios') == 1
        assert get_enum_value(Platform, 'IOS') == 1
        assert get_enum_value(Platform, 1) == 1
        assert get_enum_value(Platform, '1') == 1
        assert get_enum_value(Platform, 'android') == 2
        assert get_enum_value(Platform, 'wp') == 3
        # 取不到值
        assert get_enum_value(Platform, 0) == None
        assert get_enum_value(Platform, '0') == None
        assert get_enum_value(Platform, 'app') == None
        # 字符串类型的值
        assert get_enum_value(LocationType, 'asia') == 'Asia'
        assert get_enum_value(LocationType, u'亚洲') == 'Asia'
        assert get_enum_value(LocationType, '亚洲') == 'Asia'
        assert get_enum_value(LocationType, 'Asia') == 'Asia'
        assert get_enum_value(LocationType, 'europe') == 'Europe'
        assert get_enum_value(LocationType, 'america') == 'America'
        assert get_enum_value(LocationType, '美洲') == 'America'
        assert get_enum_value(LocationType, u'美洲') == 'America'
        assert get_enum_value(LocationType, 'australia') == 'Australia'
        # dict 值
        assert get_enum_value(LocationType2, 'asia') == 'Asia'
        assert get_enum_value(LocationType2, 'europe') == 'Europe'
        assert get_enum_value(LocationType2, 'america') == 'America'
        assert get_enum_value(LocationType2, 'australia') == 'Australia'
        # 字符串 值
        assert get_enum_value(LocationType3, 'Asia') == 'Asia'
        assert get_enum_value(LocationType3, 'Europe') == 'Europe'
        assert get_enum_value(LocationType3, 'America') == 'America'
        assert get_enum_value(LocationType3, 'Australia') == 'Australia'


if __name__ == "__main__":
    unittest.main()
