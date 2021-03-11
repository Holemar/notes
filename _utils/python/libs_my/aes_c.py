#!python
# -*- coding:utf-8 -*-
"""
公用函数(aes加密)，依赖 C 库
Created on 2016/10/18
Updated on 2019/1/18
@author: Holemar

需要安装： pip install PyCrypto==2.6.1
"""
import sys
import base64
import hashlib

from Crypto.Cipher import AES
from Crypto import Random

bs = AES.block_size
MODE = AES.MODE_CBC  # mode
system_encoding = "utf-8"

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    unicode = str


def pad(s):
    s = to_bytes(s)
    c = to_bytes(chr(bs - len(s) % bs))
    return s + (bs - len(s) % bs) * c


def unpad(s):
    s = to_str(s)
    return to_str(s[:-ord(s[-1])])


def to_bytes(data):
    """如果传入 str 类型，转成 bytes 类型返回。如果传入 bytes 类型，直接返回"""
    u_type = type(b"".decode(system_encoding))
    if isinstance(data, u_type):
        return data.encode(system_encoding)
    return data


def to_str(text):
    """
    中文转换，将 unicode/bytes 编码转成 str 编码(utf-8)
    :param {string} text: 原字符串
    :return {string}: 返回转换后的字符串
    """
    if PY3:
        u_type = type(b"".decode(system_encoding))
        if not isinstance(text, u_type):
            return text.decode(system_encoding)
        return text
    else:
        # py2 的处理
        if isinstance(text, unicode):
            return text.encode(system_encoding)
        return str(text)


class AES_Cipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(to_bytes(key)).digest()

    def encrypt(self, plaintext):
        """加密，传入 str类型 的明文，返回加密后的 base64 编码的密文"""
        iv = Random.new().read(AES.block_size)  # 生成随机初始向量IV
        cryptor = AES.new(self.key, MODE, iv)
        ciphertext = cryptor.encrypt(pad(plaintext))
        encryption_text = iv + ciphertext
        return to_str(base64.b64encode(encryption_text))

    def decrypt(self, encryption_text):
        """解密，传入 base64 编码的密文，返回解密的原始明文(str类型)"""
        encryption_text = base64.b64decode(encryption_text)
        iv = encryption_text[:AES.block_size]
        cipher_text = encryption_text[AES.block_size:]
        cipher = AES.new(self.key, MODE, iv)
        plaintext = cipher.decrypt(cipher_text)
        return unpad(plaintext)


def encryptData(data, key):
    """
    将明文字符串，用AES加密成密文
    :param {string} data: 明文的字符串
    :param {string} key: 加密/解密的key值
    :return {string}: 返回加密后的密文
    """
    if not data:
        return data
    if not key:
        raise RuntimeError(u'缺少加密的key!')
    data = to_str(data)
    # 随机向量
    iv = Random.new().read(bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    data = base64.b64encode(data)
    return to_str(data)


def decryptData(data, key):
    """
    将AES加密后的密文，解密出来
    :param {string} data: 加密后的密文
    :param {string} key: 加密/解密的key值
    :return {string}: 返回解密后的明文
    """
    if not data:
        return data
    if not key:
        raise RuntimeError(u'缺少解密的key!')
    try:
        data = base64.b64decode(data)
    except:  # base64 解码异常，很可能传来的是明文，直接返回
        return data
    if len(data) <= bs:
        return data
    iv = data[:bs]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data[bs:]))
    return to_str(data)


if __name__ == '__main__':
    cleartext = u"This is a test with several blocks!中文坎坎坷坷吞吞吐吐yy语音男男女女"  # 加密、解密的字符串
    key = 'fgjtjirj4o234234'  # 必须16、24、32 位

    encrypt_data = encryptData(cleartext, key)
    print('encrypt_data:')
    print(encrypt_data)

    decrypt_data = decryptData(encrypt_data, key)
    print('decrypt_data:')
    print(decrypt_data)

    encrypt = "P37w+VZImNgPEO1RBhJ6RtKl7n6zymIbEG1pReEzghk="
    test_key = "test key"
    cipher = AES_Cipher(test_key)
    text = cipher.decrypt(encrypt)
    print("明文:{}".format(text))
    assert text == 'hello world'

    aes2 = AES_Cipher("我的key")
    p = "a secretsdfsdfsdfs"
    e = aes2.encrypt(p)
    print("加密：", type(e), e)
    d = aes2.decrypt(e)
    print("解密：", type(d), d)
    assert d == p

    p2 = "a secretsa哈sdfsdfs"
    e2 = aes2.encrypt(p2)
    print("加密：", type(e2), e2)
    d2 = aes2.decrypt(e2)
    print("解密：", type(d2), d2)
    assert d2 == p2
    print('*'*20)
