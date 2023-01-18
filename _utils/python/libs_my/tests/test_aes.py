#!python
# -*- coding:utf-8 -*-
"""
公用函数(密码处理) aes.py 的测试
Created on 2016/9/2
Updated on 2019/1/18
@author: Holemar
"""
import time
import logging
import unittest

from __init__ import *
from libs_my import aes
# from libs_my import aes_c as aes


key = 'fgjtjirj4o234234'  # 加密key，必须16、24、32 位，且值在 0 ~ 255 之间


class AES_Test(unittest.TestCase):

    def test_english(self):
        # 普通英文 + 英文符号测试
        txt = 'abc321cc55+-*/,.,.dfdehryz908&^%$#@!~*()_+-='
        secret_txt = aes.encryptData(txt, key)
        assert secret_txt
        assert aes.decryptData(secret_txt, key) == txt

    def test_chinese(self):
        # 中文测试
        txt = '15呵呵5@#E$$@#gh，。h()_=154中文4*4616'
        secret_txt = aes.encryptData(txt, key)
        assert secret_txt
        self.assertEqual(aes.decryptData(secret_txt, key), txt)

    def test_unicode(self):
        # unicode测试
        txt = u'15呵呵5@#E$$@#gh，。h()_=154中文4*4616'
        secret_txt = aes.encryptData(txt, key)
        assert secret_txt
        self.assertEqual(aes.decryptData(secret_txt, key), txt)

    def test_param(self):
        # 明文参数为空测试
        secret_txt = aes.encryptData('', key)
        assert not secret_txt
        secret_txt = aes.encryptData(None, key)
        assert not secret_txt

        # 密文参数为空测试
        real_text = aes.decryptData('', key)
        assert not real_text
        real_text = aes.decryptData(None, key)
        assert not real_text


        # 加密 key 为空测试
        txt = '13800138000'
        has_error = False
        try:
            secret_txt = aes.encryptData(txt, '')
        except:
            has_error = True
        assert has_error

        has_error = False
        try:
            secret_txt = aes.encryptData(txt, None)
        except:
            has_error = True
        assert has_error


        # 解密 key 为空测试
        has_error = False
        try:
            real_text = aes.decryptData(txt, '')
        except:
            has_error = True
        assert has_error

        has_error = False
        try:
            real_text = aes.decryptData(txt, None)
        except:
            has_error = True
        assert has_error

    def test_stress(self):
        # 性能 测试
        repeat_times = 10
        txt = '15呵呵5@#E$$@#gh，。h()_=154中文4*4616' * 10

        start_time = time.time()
        cipher = aes.encryptData(txt, key)
        end_time = time.time()
        logging.info(u'单次加密耗时：%.4f秒' % (end_time - start_time))
        logging.info('*'*100)

        start_time = time.time()
        for i in range(repeat_times):
            cipher = aes.encryptData(txt, key)
        end_time = time.time()
        logging.info(u'%d次加密耗时：%.4f秒' % (repeat_times, end_time - start_time))
        logging.info('*'*100)

        start_time = time.time()
        decr = aes.decryptData(cipher, key)
        end_time = time.time()
        logging.info(u'单次解密耗时：%.4f秒' % (end_time - start_time))
        logging.info('*'*100)

        start_time = time.time()
        for i in range(repeat_times):
            decr = aes.decryptData(cipher, key)
        end_time = time.time()
        logging.info(u'%d次解密耗时：%.4f秒' % (repeat_times, end_time - start_time))
        logging.info('*'*100)

    def test_AES_Cipher(self):
        if not hasattr(aes, 'AES_Cipher'):
            return
        encrypt = "P37w+VZImNgPEO1RBhJ6RtKl7n6zymIbEG1pReEzghk="
        test_key = "test key"
        cipher = aes.AES_Cipher(test_key)
        text = cipher.decrypt(encrypt)
        # print("明文:{}".format(text))
        assert text == 'hello world'

        aes2 = aes.AES_Cipher("我的key")
        p = "a secretsdfsdfsdfs"
        e = aes2.encrypt(p)
        # print("加密：", type(e), e)
        d = aes2.decrypt(e)
        # print("解密：", type(d), d)
        assert d == p

        p2 = "a secretsa哈sdfsdfs"
        e2 = aes2.encrypt(p2)
        # print("加密：", type(e2), e2)
        d2 = aes2.decrypt(e2)
        # print("解密：", type(d2), d2)
        assert d2 == p2


if __name__ == "__main__":
    unittest.main()

