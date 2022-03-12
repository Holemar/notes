#!python
# -*- coding:utf-8 -*-
"""
公用函数(html字符串处理)
Created on 2015/1/19
Updated on 2021/3/11
@author: Holemar
"""
import re
import html

__all__ = ('to_html', 'to_text', 'remove_html', 'is_html_file', 'change_utf8_meta')


def to_html(sour):
    """
    转换字符串成 Html 页面上显示的编码
    :param {string} sour: 需要转换的字符串
    :return {string}: 转换后的字符串
    @example to_html(" ") 返回: &nbsp;
    """
    sour = html.escape(sour)  # & 符号
    sour = sour.replace("\n", "\n<br/>")
    # 强转下面不会 escape 的符号
    sour = sour.replace(" ", "&nbsp;")
    sour = sour.replace("%", "&#37;")
    sour = sour.replace("+", "&#43;")
    return sour


def to_text(sour):
    """
    转换字符串由 Html 页面上显示的编码变回正常编码(以上面的方法对应)
    :param sour: 需要转换的字符串
    :return {string}:转换后的字符串
    @example to_text("&nbsp;") 返回: " "
    """
    sour = html.unescape(sour)  # & 符号
    sour = re.sub(r'\n?<[Bb][Rr]\s*/?>\n?', '\r\n', sour)  # 转换换行符号
    return sour


def remove_html(text):
    """
    清除HTML标签
    :return {string}:清除标签后的内容
    @example remove_htmlTag("<div>haha</div>") 返回: "haha"
    """
    # 清除注释
    text = text.strip().replace("<!--.*?-->", "")
    # 样式 内容删除
    text = re.sub(re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I), '', text)
    # java script 内容删除
    text = re.sub(re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I), '', text)
    # 标题换行: </title> ==> 换行符
    text = re.sub(r'</[Tt][Ii][Tt][Ll][Ee]>', '\n', text)
    # tr换行: </tr> ==> 换行符
    text = re.sub(r'</[Tt][Rr]>', '\n', text)
    # html標籤清除
    text = re.sub(r'<[^>]+>', '', text)
    # 转换字符串由 Html 页面上显示的编码变回正常编码
    text = to_text(text)
    return text.strip()


def is_html_file(file_io):
    """判断文件是否html内容"""
    content = str(file_io).lower()
    value = '<html ' in content or '</html>' in content \
            or '<div ' in content or '</div>' in content \
            or '<meta ' in content or '<a ' in content
    return value


def change_utf8_meta(content):
    """将HTML页面里的 <meta>标签指定编码改成 utf-8 编码"""
    if not content:
        return content
    if not is_html_file(content):
        return content
    after_meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
    for code in ('gb2312', 'gbk', 'big5', 'gb18030'):
        s = '<meta +(http-equiv=[\'"]?Content-Type[\'"]?)? *content=[\'"]text/html; *charset=' + code + '[\'"] */?>'
        if re.search(s, content):
            content = re.sub(s, after_meta, content, flags=re.M + re.I)
            break
    # else:
    #     content = content + after_meta
    return content
