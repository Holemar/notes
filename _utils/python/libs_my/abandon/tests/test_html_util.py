#!python
# -*- coding:utf-8 -*-
"""
公用函数(字符串处理) html_util.py 的测试
Created on 2015/1/19
Updated on 2019/1/18
@author: Holemar
"""
import logging
import unittest

from __init__ import *
from libs_my.abandon import html_util


class TestXhtml(unittest.TestCase):
    # html 测试
    def test_html(self):
        logging.info(u'测试 html_util')
        self.assertEqual(html_util.to_html("  "), '&nbsp;&nbsp;')
        self.assertEqual(html_util.to_text('&nbsp;xx&nbsp;'), " xx ")
        self.assertEqual(html_util.remove_html("x<div>haha</div>x"), "xhahax")
        self.assertEqual(html_util.remove_html("""x<div>haha</div>x<!--点点滴滴-->啊啊
        <style>body {margin: 0;}</style>
        <script type="text/javascript" src="/manifest.2be1e4cb32664bc84cf0.js"></script>
        <script type="text/javascript"> function ...</script>"""),
                         "xhahax啊啊")

    def test_change_utf8_meta(self):
        logging.info(u'测试 编码转换')
        html = "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=gb2312\">\r\n<meta content=\"text/html; charset=gbk\">\r\n<meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">\r\n</head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"
        html2 = "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\r\n<meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">\r\n</head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"
        self.assertEqual(html_util.change_utf8_meta(html), html2)

        html = """<html>\r\n<head>
            <meta http-equiv='Content-Type' content='text/html; charset=gb2312'/>
            <meta content='text/html; charset=gbk'/>
        <meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">
        </head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"""
        html2 = """<html>\r\n<head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">
        </head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"""
        self.assertEqual(html_util.change_utf8_meta(html), html2)

        html = "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n<meta content=\"text/html; charset=gb2312\">\r\n</head>\r\n<body>\r\n</body>\r\n</html>\r\n"
        html2 = "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\r\n</head>\r\n<body>\r\n</body>\r\n</html>\r\n"
        self.assertEqual(html_util.change_utf8_meta(html), html2)

        html = "<!DOCTYPE html>\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=gb2312\">\r\n<meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">\r\n<title>尊敬的猎聘用户冯光，您收到了新的应聘简历。</title>\r\n</head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"
        html2 = "<!DOCTYPE html>\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\r\n<meta name=\"viewport\" content=\"width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no\">\r\n<title>尊敬的猎聘用户冯光，您收到了新的应聘简历。</title>\r\n</head>\r\n<body>\r\n\r\n</body>\r\n</html>\r\n"
        self.assertEqual(html_util.change_utf8_meta(html), html2)


if __name__ == "__main__":
    unittest.main()

