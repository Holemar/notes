#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取 PDF 的内容

需要安装 PyPDF2 库：
pip install PyPDF2==3.0.1
"""
import PyPDF2


def read_pdf(pdf_path):
    """
    读取 PDF 的内容
    :param pdf_path: PDF 文件路径
    :return: PDF 内容
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_document = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_document.pages)  # 获取PDF文件的总页数
        contents = [pdf_document.pages[i].extract_text() for i in range(num_pages)]
        return ''.join(contents)


if __name__ == '__main__':
    print(read_pdf('/Users/holemar/Downloads/handbook.pdf'))


