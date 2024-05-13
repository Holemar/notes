"""
@desc 批量生成模板文件
@tag datetime file
@version v1.2
@date 2024/5/13
"""

import os
import logging
from datetime import date


def add_last_next():
    """批量给文件加上 上一个例子、下一个例子 """
    today = date.today().strftime('%Y/%m/%d')
    for file in os.listdir('.'):
        file_name, ext = os.path.splitext(file)
        if ext != '.md' or not file_name.isdigit():
            continue
        with open(file, mode='r+', encoding='utf-8') as f:
            file_number = int(file_name)
            try:
                lines = f.readlines()
                # 替换日期
                for index, line in enumerate(lines):
                    if index > 10:
                        break
                    if line.startswith('@date '):
                        lines[index] = f'@date {today}\n'
                c = f'[上一个例子]({file_number-1}.md)    [下一个例子]({file_number+1}.md)'
                # 已经执行过一遍
                if lines[-1] == c:
                    continue
                old = f'<center>[上一个例子]({file_number-1}.md)    [下一个例子]({file_number+1}.md)</center>'
                # 旧版本的错误写法
                if lines[-1] == old:
                    lines[-1] = c
                else:
                    lines.append('\n')
                    lines.append('\n')
                    lines.append(c)

                # 下面两行代码需要说明一下：如果不先清空而只依赖指针移动到0的话，当新内容比之前少，会遗留部分旧内容在后面。
                # 如果只清空不移动指针到0，文件开头会出现一堆乱码字符。
                f.truncate(0)  # 清空文件内容，否则会追加。
                f.seek(0)  # 指针移到0，从开始位置写入内容。
                f.writelines(lines)
                print('文件%s写入成功' % (file,))
            except Exception as ex:
                logging.exception('批量添加 上一个例子、下一个例子 异常')


if __name__ == '__main__':
    add_last_next()

