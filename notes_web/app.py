#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
以 markdown 形式来显示本笔记的内容。尽量兼顾 py2 及 py3 的形式。
"""
import os
import re
import sys
import logging

from bottle import route, run, static_file, request

current_dir, _ = os.path.split(os.path.abspath(__file__))
current_dir = current_dir or os.getcwd()  # 当前目录
BASE_PATH = os.path.dirname(current_dir)  # 上一层目录，认为是项目源目录

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    from codecs import open  # 打开文件时，可以指定编码

# 文件的编码尝试列表
CODING_LIST = ["utf-8", 'gb18030', "gbk", 'big5']
# 压缩包的文件后缀列表
ZIP_EXT = ('zip', 'rar', 'arj', 'z', 'tar', 'tgz', 'gz', 'bz2')
# 自动改编码,且后缀名对应的编程语言
LANGUAGE = {
    'txt': 'plaintext', 'css': 'css', 'conf': 'yaml', 'sh': 'bash', 'cpp': 'cpp', 'c': 'c', 'h': 'cpp', 'cs': 'csharp',
    'go': 'golang', 'http': 'http', 'https': 'https', 'java': 'java', 'jsp': 'java', 'js': 'javascript', 'json': 'json',
    'lua': 'lua', 'makefile': 'makefile', 'mk': 'makefile', 'xml': 'xml', 'plist': 'xml', 'html': 'html',
    'xhtml': 'html', 'perl': 'perl', 'php': 'php', 'py': 'python', 'scheme': 'scheme', 'sql': 'sql', 'yaml': 'yaml',
}


def get_ext(file_name):
    """获取文件后缀名"""
    file_name = file_name.strip()
    p = file_name.lower()
    _, ext = os.path.splitext(p)
    if ext.startswith('.'):
        return ext[1:]
    return ext


def read_file(file_path):
    """读取文件，并返回其内容
    :param file_path: 相对路径(以本笔记首目录为基准)
    :return: 文件内容
    """
    file_path = os.path.join(BASE_PATH, file_path)
    file_path = os.path.abspath(file_path)
    # 如果是目录，则找里面的"README.md"，没有则遍历目录文件
    if os.path.isdir(file_path):
        tem = os.path.join(file_path, 'README.md')
        if os.path.exists(tem):
            file_path = tem
        else:
            folders, files = [], []
            source_files = list(os.listdir(file_path))
            for file_name in source_files:
                # 系统自动生成的无用文件
                if file_name in ('.DS_Store', 'Thumbs.db', 'folder.ini',):
                    continue
                show_file_name1 = file_name.replace('[', '【').replace(']', '】')
                show_file_name2 = file_name.replace('(', '%28').replace(')', '%29')
                if os.path.isdir(os.path.join(file_path, file_name)):
                    folders.append("**[%s](./%s/)**" % (show_file_name1, show_file_name2))
                else:
                    files.append("[%s](./%s)" % (show_file_name1, show_file_name2))
            # 排序
            folders.sort()
            files.sort()
            return '  \r\n'.join(folders) + '  \r\n' + '  \r\n'.join(files)
    # 文件找不到
    if not os.path.exists(file_path):
        return '没有您需要的页面!'
    ext = get_ext(file_path)
    # 按不同编码尝试读取文件
    for encode in CODING_LIST:
        try:
            # 没报异常，正常返回了，则说明是这种编码
            with open(file_path, 'r', encoding=encode) as f:
                result = f.read()
            # 自动改编码
            if result and encode != CODING_LIST[0] and (ext == 'md' or ext in LANGUAGE):
                logging.warning('修改文件编码： %s', file_path)
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(result)
            return result
        except UnicodeDecodeError as e:
            pass


@route('/notes_web/<filename:re:.+>.js')
def markdeep(filename):
    """markdeep.js加载"""
    return static_file('/notes_web/' + filename, root=BASE_PATH)


@route('/:file_path#.*#')
def page(file_path):
    """打开页面"""
    ext = get_ext(file_path)
    # 压缩包，不能读
    if ext in ZIP_EXT:
        return '压缩文件，无法打开'
    text = read_file(file_path)
    # 对 markdown/编程 文件，自动加载样式。其它文件显示原文。
    if not file_path or file_path.endswith(('/', 'md')) or ext in LANGUAGE:
        # 高亮显示代码
        if ext in LANGUAGE:
            text = "~~~%s\r\n%s\r\n~~~\r\n" % (LANGUAGE.get(ext), text)
        if '```' in text:
            text = re.sub(r'``[`]+', '~~~', text)  # 兼容 markdeep 的编码块写法
        # 不使用 markdown 渲染
        if 'noformat' == request.query_string:
            text = text.replace('\n', '\n<br/>')
        else:
            # 加上双空格结尾表示换行的语法规则
            text = text.replace('\r\n', '\n')
            text = text.replace('  \n', '  <br/>\n')
            # 加载 markdown 样式
            text += '\r\n <META http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
            t = os.path.getmtime(os.path.join(BASE_PATH, "notes_web/markdeep.js"))
            text += '\r\n <!-- Markdeep: --><script src="/notes_web/markdeep.js?t=%s" charset="utf-8"></script>' % t
    else:
        text = text.replace('\n', '\n<br/>')
    return text


if __name__ == '__main__':  # pragma: no coverage
    run(host='localhost', port=8080)
