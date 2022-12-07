#!python
# -*- coding:utf-8 -*-
"""
发送http请求(仅支持py3)
"""
import os
import json
import time
import logging
from urllib import request, parse
from urllib.parse import unquote

import requests
try:
    from flask import g
except:
    g = None
from .json_util import CustomJSONEncoder, decode2str

# http 请求的超时时间，单位：秒
HTTP_TIME_OUT = int(os.environ.get('HTTP_TIME_OUT') or 30)
# http 超时警告时间，单位：秒
HTTP_WARN_TIME = float(os.environ.get('HTTP_WARN_TIME') or 1)


def send(url, param=None, method='GET', timeout=HTTP_TIME_OUT, ensure_ascii=True, repeat=1,
         headers=None, send_json=True, return_json=True, return_requests=False, browser=False, **kwargs):
    """
    发出请求获取网页内容(会要求服务器使用gzip压缩返回结果,也会提交文件等内容,需要服务器支持这些功能)
    :param {string} url: 要获取内容的网页地址(GET请求时可直接将请求参数写在此url上)
    :param {dict|string} param: 要提交到网页的参数(get请求时会拼接到 url 上)
    :param {string} method: 提交方式,如 GET、 POST
    :param {int} timeout: 请求超时时间(单位:秒,设为 None 则是不设置超时时间)
    :param {bool} ensure_ascii: 请求数据是否该进行unicoede转换
    :param {int} repeat: 网络错误时的重试次数(不包括本次请求，所以填2是会最多发送3次)
    :param {dict} headers: 请求的头部信息
    :param {bool} send_json: 请求参数是否json形式传输
    :param {bool} return_json: 返回结果是否json形式
    :param {bool} return_requests: 返回 requests 的 response 结果。由外部决定如何取值。
    :param {bool} browser: 是否模拟浏览器(header加入浏览器参数，让对方识别不出是机器请求)
    :param kwargs: 其它参数，直接传给 requests 的参数
    :return {string}: 返回获取的页面内容字符串
    """
    start_time = time.time()
    method = method.strip().upper()
    param_dict = kwargs.copy()
    param_dict.setdefault('timeout', timeout)
    if url.lower().startswith('https://'):
        param_dict.setdefault('verify', False)

    headers = {} if headers is None else headers
    # 返回结果
    if return_json and not headers.get('Accept') and not return_requests:
        headers.update({'Accept': 'application/json'})
    # get 方式的参数处理, 参数拼接
    if method == 'GET' and param:
        url += "&" if "?" in url else "?"
        if isinstance(param, dict):
            param = {k: (v if isinstance(v, str) else json.dumps(v)) for k, v in param.items()}
            param = parse.urlencode(param)
        param = param.decode() if isinstance(param, (bytes, bytearray)) else str(param)
        url += param
        param = None
    # 请求参数
    elif send_json:
        if param and not isinstance(param, (bytes, str)):
            param = json.dumps(param, ensure_ascii=ensure_ascii, cls=CustomJSONEncoder)
            param = bytes(param, 'utf8')
        if not headers.get('Content-Type'):
            headers.update({'Content-Type': 'application/json'})
    elif param and isinstance(param, dict) and 'files' not in kwargs:
        param = parse.urlencode(param).encode('utf-8')
    # 模拟浏览器
    if browser:
        headers.update({
            'Accept': 'application/json, text/plain, */*',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        })
    param_dict['headers'] = headers

    try:
        if method == 'GET':
            response = requests.get(url, params=param, **param_dict)
        elif method == 'POST':
            response = requests.post(url, data=param, **param_dict)
        elif method == 'PUT':
            response = requests.put(url, data=param, **param_dict)
        elif method == 'DELETE':
            response = requests.delete(url, params=param, **param_dict)
        else:
            raise RuntimeError('不支持的请求方式!')

        res = response.text
        status_code = response.status_code
        response.close()
    except request.HTTPError as e:
        status_code = e.code
        res = e.read()
        # 认证信息不输出
        logging.error("%s 请求url:%s, headers:%s, param:%s, 状态码:%s, 返回:%s",
                      method, url, headers, param, status_code, res)
        # 有可能时网络错误导致，故重试
        if repeat > 0:
            repeat -= 1
            return send(url, param=param, method=method, timeout=timeout, ensure_ascii=ensure_ascii, repeat=repeat,
                        headers=headers, send_json=send_json, return_json=return_json, return_requests=return_requests,
                        browser=browser, **kwargs)
        return res
    except Exception as e:
        logging.exception("%s 请求url:%s, param:%s, 异常:%s", method, url, param, e)
    else:
        # 认证信息不输出
        duration = time.time() - start_time
        if duration >= HTTP_WARN_TIME:
            logging.warning("%s 请求耗时太长:%.4f秒, url:%s, headers:%s, param:%s, 状态码:%s, 返回:%s",
                            method, duration, url, headers, param, status_code, res)
        else:
            logging.debug("%s 请求url:%s, headers:%s, param:%s, 状态码:%s, 返回:%s",
                          method, url, headers, param, status_code, res)
        if return_requests:
            return response
        elif return_json:
            try:
                return response.json()
            except:
                # 有可能时网络错误导致，返回了nginx的html报错内容，故重试
                if repeat > 0:
                    repeat -= 1
                    return send(url, param=param, method=method, timeout=timeout, ensure_ascii=ensure_ascii,
                                repeat=repeat, headers=headers, send_json=send_json, return_json=return_json,
                                return_requests=return_requests, browser=browser, **kwargs)
        if g:
            if not hasattr(g, 'http_list'):
                g.http_list = []
            g.http_list.append({'method': method, 'url': url, 'headers': headers, 'param': param,
                                'status_code': status_code, 'duration': duration, 'response': res})
        return res


def get(url, param=None, headers=None, **kwargs):
    """发送get请求"""
    kwargs.pop('method', None)
    return send(url, param=param, method='GET', headers=headers, **kwargs)


def post(url, param=None, headers=None, **kwargs):
    """发送post请求"""
    kwargs.pop('method', None)
    return send(url, param=param, method='POST', headers=headers, **kwargs)


def put(url, param=None, headers=None, **kwargs):
    """发送put请求"""
    kwargs.pop('method', None)
    return send(url, param=param, method='PUT', headers=headers, **kwargs)


def delete(url, param=None, headers=None, **kwargs):
    """发送delete请求"""
    kwargs.pop('method', None)
    return send(url, param=param, method='DELETE', headers=headers, **kwargs)


def get_request_params(url):
    """
    获取url里面的参数,以字典的形式返回
    :param {string} url: 请求地址
    :return {dict}: 以字典的形式返回请求里面的参数
    """
    result = {}
    if isinstance(url, (bytes, bytearray)):
        url = decode2str(url)
    if not isinstance(url, str):
        if isinstance(url, dict):
            return url
        else:
            return result

    # li = re.findall(r'\w+=[^&]*', url) # 为了提高效率，避免使用正则
    i = url.find('?')
    if i != -1:
        url = url[i + 1:]
    li = url.split('&')

    if not li:
        return result

    for ns in li:
        if not ns: continue
        (key, value) = ns.split('=', 1) if ns.find('=') != -1 else (ns, '')
        value = value.replace('+', ' ')  # 空格会变成加号
        result[key] = unquote(value)  # 值需要转码

    return result
