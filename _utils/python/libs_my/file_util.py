#!python
# -*- coding:utf-8 -*-
"""
Created on 2014/9/25
Updated on 2019/1/18
@author: Holemar

本模块专门处理文件用
"""
import os
import logging
import datetime

try:
    # py3
    from queue import Queue
    from urllib.request import urlretrieve
    from urllib.request import URLError as HTTPError
    long = int
except:
    # py2
    from Queue import Queue
    from urllib import urlretrieve
    from urllib2 import HTTPError

__all__ = ('get_first_lines', 'get_last_lines', 'remove', 'clear', 'download_file', 'file_quantity',
           'get_file_quantity', 'file_update_dt', 'get_file_size')


def get_first_lines(file_path, num=1, include_blank=False):
    """
    获取文件的开头几行
    :param {string} file_path: 要读取的文件路径
    :param {int} num: 要读取的行数(默认读取最后一行)
    :param {bool} include_blank: 获取的内容是否包含空行
    :return {string | list<string>}: 开头几行内容的字符串列表(如果是只读取最后一行,则返回那一行字符串)
    """
    assert isinstance(num, (int, long)) and num >= 1

    n_lines = []
    with open(file_path) as fp:
        # n_lines = fp.readlines(num) # 为了便于去掉空行，改成逐行读取
        for line in fp:
            if len(n_lines) >= num: break
            if line:
                # 判断空行
                if not include_blank:
                    line = line.strip()
                    if not line:
                        continue
                    n_lines.append(line)
                else:
                    n_lines.append(line.rstrip())  # 去掉最后边的换行符
    # 返回内容
    if num == 1 and len(n_lines) == 1:
        return n_lines[0]
    return n_lines


def get_last_lines(file_path, num=1, include_blank=False):
    """
    获取文件的最后几行
    :param {string} file_path: 要读取的文件路径
    :param {int} num: 要读取的行数(默认读取最后一行)
    :param {bool} include_blank: 获取的内容是否包含空行
    :return {string | list<string>}: 最后几行内容的字符串列表(如果是只读取最后一行,则返回那一行字符串)
    """
    blk_size_max = 4096
    n_lines = []
    with open(file_path) as fp:
        fp.seek(0, os.SEEK_END)
        cur_pos = fp.tell()
        while cur_pos > 0 and len(n_lines) < num:
            blk_size = min(blk_size_max, cur_pos)
            fp.seek(cur_pos - blk_size, os.SEEK_SET)
            blk_data = fp.read(blk_size)
            assert len(blk_data) == blk_size
            lines = blk_data.split('\n')

            # adjust cur_pos
            if len(lines) <= 2:
                if len(lines[1]) > 0:
                    n_lines[0:0] = lines[1:]
                    cur_pos -= (blk_size - len(lines[0]))
                else:
                    n_lines[0:0] = lines[0:]
                    cur_pos -= blk_size
            elif len(lines) > 1 and len(lines[0]) > 0:
                n_lines[0:0] = lines[1:]
                cur_pos -= (blk_size - len(lines[0]))
            else:
                n_lines[0:0] = lines
                cur_pos -= blk_size
            fp.seek(cur_pos, os.SEEK_SET)
        fp.close()
    # 去掉空行
    if not include_blank:
        n_lines[:] = [r.strip() for r in n_lines if r.strip()]
    else:
        n_lines[:] = [r.rstrip() for r in n_lines]  # 去掉最后边的换行符
    # 最后一行如果是空值，则删掉
    if len(n_lines) > 0 and len(n_lines[-1]) == 0:
        del n_lines[-1]
    # 返回内容
    res = n_lines[-num:]
    if num == 1 and len(res) == 1:
        res = res[0]
    return res


def remove(file_path):
    """
    删除文件
    :param {string} file_path: 要删除的文件路径
    """
    file_path = os.path.abspath(file_path)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)  # 不知道什么原因，这句会报错
            return True
        except:
            pass
        try:
            os.popen('del /q /f "%s"' % file_path)
            return True
        except:
            pass
        try:
            os.popen('rm -f "%s"' % file_path)
            return True
        except:
            pass


def clear(file_path):
    """
    清空文件
    :param {string} file_path: 要清空的文件路径
    """
    file_path = os.path.abspath(file_path)
    if os.path.isfile(file_path):
        try:
            open(file_path, mode="w").close()
        except:
            os.popen('echo""> "%s"' % file_path)


def download_file(url, file_path):
    """
    下载网络文件
    :param {string} url: 要下载的文件网址
    :param {string} file_path: 要下载到本地的文件名(包含目录+文件名的路径)
    """
    try:
        remove(file_path)  # 先删除旧文件
        file_dir = os.path.dirname(file_path)
        # 没有文件的目录，则先创建目录，避免因此报错
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        # 文件下载
        urlretrieve(url, file_path)
    except HTTPError as e:
        status_code = e.code
        res = e.read()
        logging.error("文件下载失败, 返回码:%s, 返回内容:%s", status_code, res, exc_info=True)


def file_quantity(path):
    """统计文件数量
    :param path:目录路径
    :return: 此目录下的总文件数量(不包括目录数，系统自动生成的隐藏文件可能会不统计)
    """
    file_num = 0
    for file_or_folder in os.listdir(path):
        sub_path = os.path.join(path, file_or_folder)
        if os.path.isfile(sub_path):
            file_num += 1
        elif os.path.isdir(sub_path):
            file_num += file_quantity(sub_path)
    return file_num


def get_file_quantity(folder):
    """BFS获取文件夹下文件的总数量
    前面写的是递归的方式处理，感觉对资源的占用不友好，而且python的最大递归深度不超过1000。
    所以优化了一下，这里用广度优先遍历的方式实现。实测发现，性能差异不大。
    :param folder:目录路径
    :return: 此目录下的总文件数量(不包括目录数，系统自动生成的隐藏文件可能会不统计)
    """
    # 判断初始文件夹
    assert os.path.isdir(folder), '请输入有效的文件夹参数'
    file_num = 0  # 初始化文件数量
    folder_queue = Queue()
    folder_queue.put_nowait(folder)  # 初始化队列的值
    # 处理队列里的文件夹
    while not folder_queue.empty():
        folder = folder_queue.get_nowait()
        for file_or_folder in os.listdir(folder):
            sub_path = os.path.join(folder, file_or_folder)
            if os.path.isfile(sub_path):
                file_num += 1
            elif os.path.isdir(sub_path):
                folder_queue.put_nowait(sub_path)
    return file_num


def file_update_dt(file_path):
    """获取文件的最后更新时间
    :param file_path:文件路径
    :return: 文件的最后更新时间（datetime.datetime类型）
    """
    create_time = os.path.getctime(file_path)  # 文件的创建时间
    modify_time = os.path.getmtime(file_path)  # 文件的修改时间
    file_time = max(create_time, modify_time)  # 选一个最新的时间为文件更新时间
    return datetime.datetime.fromtimestamp(file_time)


def get_file_size(file_path):
    """获取文件大小，单位：字节"""
    # 特别大的文件过滤
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def show_file_size(file_path=None, file_size=None):
    """显示文件大小，单位分别为 B、K、M、G
    :param file_path:文件路径
    :param file_size:文件大小(单位为字节，整数类型)。没有传入此值则根据路径获取文件的大小
    :return: 文件大小的容易人看的模式。
    """
    if file_size is None and file_path:
        file_size = os.path.getsize(file_path)
    if not file_size:
        return '0B'
    if file_size < 1024:
        return "%sB" % file_size
    if 1024 <= file_size < 1024 * 1024:
        return "%.2fK" % (file_size / 1024.0)
    elif 1024 * 1024 <= file_size < 1024 * 1024 * 1024:
        return "%.2fM" % (file_size / (1024 * 1024.0))
    else:
        return "%.2fG" % (file_size / (1024 * 1024 * 1024.0))

