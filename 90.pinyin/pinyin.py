#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拼音学习，纠正自己不认识或者认不准的字词读音
主要参考来源： https://www.zdic.net/
"""
import os
import sys
import ssl
import json
import random
import logging

try:
    from ..notes_web.bottle import route, run, static_file, request as bottle_request
except:
    sys.path.insert(1, '../notes_web/')  # 导入运行环境
    from bottle import route, run, static_file, request as bottle_request

current_dir, _ = os.path.split(os.path.abspath(__file__))
current_dir = current_dir or os.getcwd()  # 当前目录
current_dir = os.path.abspath(current_dir)
TIMEOUT = 30  # 下载的超时时间(秒)
# 下载MP3拼音的地址
MP3_DOWNLOAD = 'https://img.zdic.net/audio/zd/py/%s.mp3'
context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    from urllib import quote
    import urllib2 as http_request
    from codecs import open  # 打开文件时，可以指定编码
else:
    from urllib.parse import quote
    import urllib.request as http_request

LETTERS = {
    'ā': ('a', '1'), 'á': ('a', '2'), 'ǎ': ('a', '3'), 'à': ('a', '4'),
    'ō': ('o', '1'), 'ó': ('o', '2'), 'ǒ': ('o', '3'), 'ò': ('o', '4'),
    'ē': ('e', '1'), 'é': ('e', '2'), 'ě': ('e', '3'), 'è': ('e', '4'),
    'ī': ('i', '1'), 'í': ('i', '2'), 'ǐ': ('i', '3'), 'ì': ('i', '4'),
    'ū': ('u', '1'), 'ú': ('u', '2'), 'ǔ': ('u', '3'), 'ù': ('u', '4'),
    'ü': ('v', '0'), 'ǖ': ('v', '1'), 'ǘ': ('v', '2'), 'ǚ': ('v', '3'), 'ǜ': ('v', '4'),  # 多一个 ü，轻声
}


def read_file(file_path):
    """读取文件，并返回其内容
    :param file_path: 相对路径(以本文件目录为基准)
    :return: 文件内容
    """
    file_dir = os.path.dirname(file_path)
    # 没有目录，则指本目录
    if not file_dir:
        file_path = os.path.join(current_dir, file_path)
        file_path = os.path.abspath(file_path)
    # 文件找不到
    if not os.path.exists(file_path):
        raise Exception('没有相关文件: %s' % file_path)
    # 读取文件内容
    with open(file_path, 'r') as txt_f:
        context = txt_f.read()
        return context


def write_json(file_path, json_value):
    """写json文件
    :param file_path: 相对路径(以本文件目录为基准)
    :param json_value: 要写入的 json 内容
    """
    file_dir = os.path.dirname(file_path)
    # 没有目录，则指本目录
    if not file_dir:
        file_path = os.path.join(current_dir, file_path)
        file_path = os.path.abspath(file_path)
    # 没有文件的目录，则先创建目录，避免因此报错
    elif not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as dump_file:
        value_json = json.dumps(json_value, ensure_ascii=False)
        value_json = value_json.replace('}, "', '}, \r\n"')  # 各字词换行
        value_json = '{\r\n' + value_json[1: -1] + '\r\n}'  # 首尾换行
        dump_file.write(value_json)


def download_file(url, file_path):
    """文件下载"""
    try:
        # 没有文件的目录，则先创建目录，避免因此报错
        file_dir = os.path.dirname(file_path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        # https 下载，忽略安全警告
        if url.lower().startswith('https'):
            response = http_request.urlopen(url, timeout=TIMEOUT, context=context)
        else:
            response = http_request.urlopen(url, timeout=TIMEOUT)
        with open(file_path, "wb") as f:
            f.write(response.read())
        logging.info('... download_file ... %s, %s', file_path, url)
        return True
    except Exception as e:
        logging.error(u"download_file error: %s  url:%s, file_path:%s", e, url, file_path)
        return False


def get_letter(pronounce):
    """将拼音转成字母加数字的形式
    :param pronounce: 拼音
    :return: 字母加数字形式的拼音(如 zhūn 返回 zhun1)
    """
    # 词
    if ' ' in pronounce:
        return ' '.join([get_letter(p) for p in pronounce.split(' ')])
    # 字
    else:
        for c, v in LETTERS.items():
            if c in pronounce:
                return pronounce.replace(c, v[0]) + v[1]


def sort_character(character, json_characters):
    """json_characters的排序迭代器"""
    keys = json_characters[character].keys()
    pronounces = [k for k in keys if k not in ('right', 'wrong')]
    return pronounces[0]


def load_source_to_json():
    """读取 source 文件，并填充到 json 中"""
    context = read_file('source.txt')
    target_path = 'source.json'

    # 将文件内容，编译成 json
    json_characters = {}
    json_words = {}
    # word_dict = {'character', 'pronounce', 'words', 'mean', 'letter', 'right': 0, 'wrong': 0}
    for line in context.splitlines():
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
            word_dict = {'words': words, 'mean': mean, 'letter': get_letter(pronounce)}
            json_characters.setdefault(character, {'right': 0, 'wrong': 0})[pronounce] = word_dict
        # 词
        else:
            word = results[0]
            pronounce = results[1: len(word) + 1]
            pronounce[0] = pronounce[0].strip('【')
            pronounce[-1] = pronounce[-1].strip('】')
            pronounce = ' '.join(pronounce)
            mean = ' '.join(results[len(word) + 1:])  # 允许含义中有空格
            word_dict = {'pronounce': pronounce, 'mean': mean, 'letter': get_letter(pronounce), 'right': 0, 'wrong': 0}
            json_words[word] = word_dict

    json_values = {}
    # 排序(字 按首个拼音排序)
    for character in sorted(json_characters, key=lambda x: sort_character(x, json_characters)):
        value = json_characters[character]
        json_values[character] = value
    # 排序(词 按字数及首个拼音排序)
    for word in sorted(json_words, key=lambda x: str(len(x)) + json_words[x].get('pronounce')):
        value = json_words[word]
        json_values[word] = value

    # 读取已存数据
    json_context = read_file(target_path)
    old_values = json.loads(json_context) if json_context else {}
    # 加载已存储的数值
    for character, word_dict in old_values.items():
        json_values[character]["right"] = word_dict.get("right") or 0
        json_values[character]["wrong"] = word_dict.get("wrong") or 0

    # 输出 json 文件
    write_json(target_path, json_values)


def show_one():
    """随机返回一个字或者词，但需要按比重来显示"""
    json_context = read_file('source.json')
    json_values = json.loads(json_context)

    # 取出 right + wrong 的最大值
    max_weight = max([word_dict.get("wrong", 0) + word_dict.get("right", 0)
                      for character, word_dict in json_values.items()])
    max_weight = max([max_weight, 2])  # 保证最少为 1，不然没法继续
    # 按 right, wrong 的次数来计算比重。
    # right 次数越多的，比重越低。 wrong 次数越多的，比重越高。right 和 wrong 都为 0 的，要比不为 0 的比重高。
    weight_sum = 0
    for character, word_dict in json_values.items():
        weight = max_weight - word_dict.get("right", 0) + word_dict.get("wrong", 0) * 2
        weight = 1 if weight <= 0 else weight
        word_dict["weight"] = weight
        weight_sum += weight

    # 随机显示一个字或者词，比重越大显示概率越高
    random_number = random.randint(1, weight_sum)
    sum_number = 0
    for character, word_dict in json_values.items():
        weight = word_dict.get("weight", 0)
        sum_number += weight
        if sum_number >= random_number:
            return character, word_dict


@route('/mp3/<pronounce:re:.+>.mp3')
def static_mp3_file(pronounce):
    """加载拼音mp3"""
    audio_path = 'mp3/' + pronounce + '.mp3'
    file_path = os.path.join(current_dir, audio_path)
    file_path = os.path.abspath(file_path)
    # 文件找不到
    if not os.path.exists(file_path):
        url = MP3_DOWNLOAD % quote(pronounce)
        download_file(url, file_path)
    return static_file(audio_path, root=current_dir)


@route('/:file_path#.*#', method=['GET', 'POST'])
def page(file_path):
    """打开页面"""
    if file_path and file_path != '/':
        return ''

    # 有提交，记录是否认识
    submit_btn = bottle_request.params.getunicode('submit_btn')
    submit_character = bottle_request.params.getunicode('character')
    if submit_btn and submit_character:
        target_path = 'source.json'
        json_context = read_file(target_path)
        json_values = json.loads(json_context) if json_context else {}
        if submit_btn == '认识':
            json_values[submit_character]['right'] += 1
        elif submit_btn == '不认识':
            json_values[submit_character]['wrong'] += 1
        if '认识' in submit_btn:
            write_json(target_path, json_values)

    # 显示一个字或者词
    text = read_file('show.html')
    character, word_dict = show_one()  # 随机取一个字或者词
    text = text.replace('{#character#}', character)
    value_json = json.dumps(word_dict, ensure_ascii=False, indent=4)
    text = text.replace('{#values#}', value_json)
    # 显示拼音mp3
    mp3_html = """
    <A href="javascript:document.getElementById('{pronounce}').play();">{pronounce}
    <audio id="{pronounce}">
        <source src="/mp3/{pronounce}.mp3" type="audio/mp3" />
        <embed height="100" width="100" src="/mp3/{pronounce}.mp3" />
    </audio></A>
    """
    pronounce = word_dict.get('pronounce')
    if pronounce:  # 词
        pronounces = pronounce.split(' ')
        letter = word_dict.get('letter')
    else:  # 字
        pronounces = [k for k in word_dict.keys() if k not in ('right', 'wrong', 'weight')]
        letter = ' '.join([word_dict.get(p).get('letter') for p in pronounces])
    pronounces_html = '&nbsp;&nbsp;'.join([mp3_html.format(pronounce=p) for p in pronounces])
    text = text.replace('{#pronounces#}', pronounces_html)
    text = text.replace('{#letter#}', letter)
    return text


if __name__ == '__main__':
    load_source_to_json()
    run(host='localhost', port=18081)
