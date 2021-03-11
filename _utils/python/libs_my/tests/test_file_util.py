#!python
# -*- coding:utf-8 -*-

"""
公用函数 file_util.py 的测试类
Created on 2017/4/5
Updated on 2019/1/18
@author: Holemar
"""
import os
import logging
import unittest

from __init__ import *
from libs_my.file_util import *

tem_file = './_test.txt'
tem_lines = ['first line', '2222222222', '3333333333', '', 'last  line']


class TestFileUtil(unittest.TestCase):

    def setUp(self):
        """初始化"""
        super(TestFileUtil, self).setUp()

        # 首行是空行，且清空文件旧内容
        f = open(tem_file, mode="w")
        f.write('\n')
        for line in tem_lines:
            # 处理空行
            if not line:
                f.write('\n')
            else:
                f.write(line)
                f.write('\n')
        else:
            f.close()

    def tearDown(self):
        """销毁"""
        # 删除测试文件
        remove(tem_file)
        super(TestFileUtil, self).tearDown()


    def test_get_first_lines(self):
        logging.info(u'测试 获取文件的开头几行')

        # 默认只读取第一行(不包括空行)
        lines = get_first_lines(tem_file)
        assert lines == tem_lines[0]

        # 读取两行(不包括空行)
        lines = get_first_lines(tem_file, 2)
        assert lines == tem_lines[0:2]

        # 读取四行(不包括空行)
        lines = get_first_lines(tem_file, len(tem_lines))
        assert lines == [n for n in tem_lines if n]

        # 读取全部(包括空行)
        lines = get_first_lines(tem_file, len(tem_lines) + 1, include_blank=True)
        assert lines == [''] + tem_lines # 由于首行加上了空行


    def test_get_last_lines(self):
        logging.info(u'测试 获取文件的最后几行')

        # 默认只读取最后一行(不包括空行)
        lines = get_last_lines(tem_file)
        assert lines == tem_lines[-1]

        no_blank_lines = [n for n in tem_lines if n]

        # 读取两行(不包括空行)
        lines = get_last_lines(tem_file, 2)
        assert lines == no_blank_lines[-2:]

        # 读取四行(不包括空行)
        lines = get_last_lines(tem_file, len(tem_lines))
        assert lines == no_blank_lines

        # 读取全部(包括空行)
        lines = get_last_lines(tem_file, len(tem_lines), include_blank=True)
        assert lines == tem_lines


    def test_remove(self):
        logging.info(u'测试 删除文件')

        assert os.path.exists(tem_file) == True
        remove(tem_file)
        assert os.path.exists(tem_file) == False


    def test_clear(self):
        logging.info(u'测试 清空文件')

        assert os.path.exists(tem_file) == True
        assert os.path.getsize(tem_file) > 0
        clear(tem_file)
        assert os.path.exists(tem_file) == True
        assert os.path.getsize(tem_file) == 0


    def test_download_file(self):
        logging.info(u'测试 网络文件下载')

        file_path = './jquery.js'
        url = 'http://code.jquery.com/jquery.min.js'

        assert os.path.exists(file_path) == False
        download_file(url, file_path)
        assert os.path.exists(file_path) == True
        assert os.path.getsize(file_path) > 0

        # 删除下载的文件
        os.popen('del /q /f "%s"' % file_path)

    def test_file_quantity(self):
        logging.info(u'测试 计算目录的总文件数')

        num = file_quantity(os.getcwd())
        num2 = get_file_quantity(os.getcwd())
        self.assertTrue(num > 2)
        self.assertEqual(num, num2)


if __name__ == "__main__":
    unittest.main()
