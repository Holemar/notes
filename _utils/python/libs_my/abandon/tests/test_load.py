#!python
# -*- coding:utf-8 -*-
"""
公用函数 load.py 的测试类
Created on 2014/7/16
Updated on 2019/1/18
@author: Holemar
"""
import os
import unittest

from __init__ import *
from libs_my.abandon import load

class LoadTest(unittest.TestCase):
    def test_get_path(self):
        # 获取路径
        base_path = os.getcwd()
        assert load.get_path('.') == base_path + os.sep
        assert load.get_path('..') == os.path.abspath('..') + os.sep
        assert load.get_path('../../libs/') == os.path.abspath('../../libs/') + os.sep
        # 带上参考位置
        assert load.get_path('.', current_path="C:\\Windows\\System32\\com\\en-US\\comrepl.exe.mui") == "C:\\Windows\\System32\\com\\en-US\\"
        assert load.get_path('../zh-CN', current_path="C:\\Windows\\System32\\com\\en-US\\comrepl.exe.mui") == "C:\\Windows\\System32\\com\\zh-CN\\"

    def test_load_modules(self):
        module_list = load.load_modules(file_name='test_analysis_list.py', path='.')
        self.assertEqual(len(module_list), 1)
        VirtualObject = module_list[0].VirtualObject
        assert VirtualObject # 能获取到这个类
        VirtualObject(year=2016, month=12, data_type='cost', value=5) # 使用这个类不报错，说明获取成功

if __name__ == "__main__":
    unittest.main()

