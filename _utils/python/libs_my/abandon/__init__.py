#!python
# -*- coding:utf-8 -*-
"""
本目录是已废弃的公用类库,不涉及具体业务逻辑,各系统可公用
目前只考虑 py2.6 ~ py2.7 版本的使用，不保证兼容其它版本

Created on 2019/8/3
Updated on 2019/8/3
@author: Holemar
"""
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    # 避免编码问题导致报错
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except:pass
else:
    basestring = unicode = str
    long = int
