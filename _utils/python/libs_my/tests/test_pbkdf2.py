#!python
# -*- coding:utf-8 -*-
"""
公用函数(密码处理) pbkdf2.py 的测试
Created on 2016/4/22
Updated on 2019/1/18
@author: Holemar
"""
import time
import logging
import unittest

from __init__ import *
from libs_my import pbkdf2


class Pbkdf2Test(unittest.TestCase):

    def run_fun(self, password):
        # 遍历所有算法
        algos = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
        for algo in algos:
            method = 'pbkdf2:' + algo
            start_time = time.time()
            pwhash = pbkdf2.generate_password_hash(password, method=method)
            end_time1 = time.time()
            check = pbkdf2.check_password_hash(pwhash, password, method=method) # True
            end_time2 = time.time()
            logging.info('生成密码耗时：%.4f秒，类型：%s。验证耗时：%.4f秒，结果：%s，密码：%s', (end_time1 - start_time), algo, (end_time2 - end_time1), check, pwhash)
            assert check
            assert len(pwhash) > 32
            assert '$' in pwhash

    def test_english(self):
        # 普通英文 + 英文符号测试
        password = '1515@#E$$@#ghfgh()_=154484*4616'
        self.run_fun(password)

    def test_chinese(self):
        # 中文测试
        password = '15呵呵5@#E$$@#gh，。h()_=154中文4*4616'
        self.run_fun(password)

    def test_unicode(self):
        # unicode测试
        password = u'15呵呵5@#E$$@#gh，。h()_=154中文4*4616'
        self.run_fun(password)

    def _test_stress(self):
        # 性能 测试
        repeat_times = 1000
        password = '15呵呵5@#E$$@#gh，。h()_=154中文4*4616' * 10

        # 遍历所有算法
        algos = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
        for algo in algos:
            method = 'pbkdf2:' + algo
            start_time = time.time()
            for i in range(repeat_times):
                pwhash = pbkdf2.generate_password_hash(password, method=method)
            end_time1 = time.time()
            for i in range(repeat_times):
                check = pbkdf2.check_password_hash(pwhash, password, method=method) # True
            end_time2 = time.time()
            logging.info('%d次生成密码耗时：%.4f秒，类型：%s。验证耗时：%.4f秒，结果：%s，密码：%s',
                repeat_times, (end_time1 - start_time), algo, (end_time2 - end_time1), check, pwhash)
            assert check
            assert len(pwhash) > 32
            assert '$' in pwhash


if __name__ == "__main__":
    unittest.main()

