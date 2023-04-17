#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拼音学习，纠正自己不认识或者认不准的字词读音
"""
import os
import sys
import json
import logging

sys.path.insert(1, '../notes_web/')  # 导入运行环境
from bottle import route, run, static_file, request

current_dir, _ = os.path.split(os.path.abspath(__file__))
current_dir = current_dir or os.getcwd()  # 当前目录
current_dir = os.path.abspath(current_dir)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    from codecs import open  # 打开文件时，可以指定编码


def read_json():
    """读取文件，并返回其内容
    """
    source_path = os.path.abspath(os.path.join(current_dir, 'source.txt'))
    target_path = os.path.abspath(os.path.join(current_dir, 'source.json'))
    # 文件找不到
    if not os.path.exists(source_path):
        return '没有您需要的页面!'
    # 读取文件内容
    with open(source_path, 'r') as txt_f:
        context = txt_f.readlines()

    # 将文件内容，编译成 json
    json_characters = {}
    json_words = {}
    # word_dict = {'character': None, 'pronounce': None, 'words': None, 'mean': None, 'right': 0, 'wrong': 0}
    for line in context:
        line = line.strip()
        if not line or line.startswith(('字【拼音】', '词【拼音】', '-----')):
            continue
        # 连续多个空格，转成一个
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.replace('【', ' 【', 1)
        results = line.split(' ')
        # print(len(results), results)
        # 字
        if '】' in results[1]:
            character = results[0]
            pronounce = results[1].strip('【').strip('】')
            words = results[2]
            mean = ' '.join(results[3:])  # 允许含义中有空格
            word_dict = {'words': words, 'mean': mean, 'right': 0, 'wrong': 0}
            json_characters.setdefault(character, {})[pronounce] = word_dict
        # 词
        else:
            word = results[0]
            pronounce = results[1: len(word) + 1]
            pronounce[0] = pronounce[0].strip('【')
            pronounce[-1] = pronounce[-1].strip('】')
            pronounce = ' '.join(pronounce)
            mean = ' '.join(results[len(word) + 1:])  # 允许含义中有空格
            word_dict = {'pronounce': pronounce, 'mean': mean, 'right': 0, 'wrong': 0}
            json_words[word] = word_dict

    # 读取已存数据
    with open(target_path, 'r') as json_f:
        json_context = json_f.read()
        json_values = json.loads(json_context)
    # 排序(字按拼音排序)
    for character in sorted(json_characters, key=lambda x: list(json_characters[x].keys())[0]):
        json_values[character] = json_characters[character]
    json_values.update(json_words)
    # 输出 json 文件
    with open(target_path, 'w', encoding='utf-8') as dump_file:
        value_json = json.dumps(json_values, ensure_ascii=False)
        value_json = value_json.replace('}, "', '}, \r\n"')  # 各字词换行
        value_json = '{\r\n' + value_json[1: -1] + '\r\n}'  # 首尾换行
        dump_file.write(value_json)


@route('/mp3/<audio:re:.*>')
def static_mp3_file(audio):
    """加载拼音mp3"""
    return static_file('/mp3/' + audio + '.mp3', root=current_dir)


if __name__ == '__main__':
    read_json()
    # run(host='localhost', port=18081)
