"""
文件操作相关函数
"""

import os
from os.path import join, isdir, abspath, pardir, basename, getmtime
import time


def listdir(dir):
    """遍历dir文件夹，返回目录列表和文件列表"""
    dirs = []
    files = []
    for item in os.listdir(dir):
        full_name = join(dir, item)
        if isdir(full_name):
            dirs.append(item)
        else:
            files.append(item)

    return dirs, files


def get_m_time(start, paths):
    """
    获取文件或目录的创建时间
    :param start:  起始目录
    :param paths:  文件或目录的名字的列表
    :return:  返回包含元组(path, m_time)类型的列表
    """
    lst = []
    for path in paths:
        full_path = join(start, path)
        m_time = getmtime(full_path)
        lst.append((path, time.asctime( time.localtime(m_time) ) ) )

    return lst


def get_levels(start, path):
    """
    获取path每一层的路径, 以start为起始目录 (应确保path在start下)
    :param start: 根目录绝对路径
    :param path: 路径绝对路径
    :return: 包含每层目录的绝对路径的列表
    """

    levels = []
    full_path = path
    base_name = basename(full_path)
    levels.append((full_path, base_name))
    while full_path != start:
        full_path = abspath(join(full_path, pardir))  # 移动到父目录
        base_name = basename(full_path)
        levels.append((full_path, base_name))

    return levels[ : : -1]  # 返回反转后的列表

def get_relative_levels(user_path, abs_levels):
    """
    根据绝对路径层级信息，计算相对路径层级信息。
    
    :param user_path: 用户根目录的绝对路径。
    :param abs_levels: 包含绝对路径层级信息的列表，每个元素为一个元组，形如(绝对路径, 显示名称)。
    :return: 包含相对路径层级信息的列表，每个元素为一个元组，形如(相对路径, 显示名称)。
    """
    rel_levels = []
    for abs_path, display_name in abs_levels:
        if abs_path == user_path:
            # 特殊处理根目录的情况
            rel_levels.append(('/', display_name))
        else:
            # 计算相对于根目录的相对路径
            rel_path = os.path.relpath(abs_path, user_path)
            rel_levels.append((rel_path, display_name))
    
    return rel_levels


# def get_abs_path(start, path):
#     """
#     获取path的绝对路径,
#     :param start: 根目录
#     :param path: 相对路径
#     :return: 如果path不在start下返回None， 反之返回其绝对路径
#     """
#     print("传入的start:start:",start)
#     print("传入的path::",path)
#     if start and path:
#         # start 和 path 都不能为空
#         start =  abspath(start)
#         print("start====>",start)
#         abs_path = abspath(path)
#         print("abs_path====>",abs_path)
#         print(abs_path.startswith(start))
#         if abs_path.startswith(start):
#             return abs_path
#     return None

def get_abs_path(start, path):
    """
    获取path的绝对路径,
    :param start: 根目录
    :param path: 相对路径
    :return: 如果path是start的有效子路径，返回其绝对路径；否则返回None
    """
    print("传入的start:", start)
    print("传入的path:", path)
    if start and path:
        start = os.path.abspath(start)
        if path:  # 确保path不为空
            abs_path = os.path.abspath(os.path.join(start, path))
        else:
            # 如果path为空，直接使用start作为绝对路径
            abs_path = start
        print("abs_path====>", abs_path)
        print(abs_path.startswith(start))
        if abs_path.startswith(start):
            return abs_path
    return None



def get_rel_path(start, path):
    """
    获取相对于起始目录的路径
    :param start: 起始目录的绝对路径
    :param path: 绝对路径
    :return: 相对于起始目录的路径
    """
    start = os.path.abspath(start)
    path = os.path.abspath(path)
    return os.path.relpath(path, start)