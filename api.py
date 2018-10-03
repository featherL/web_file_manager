"""
一些api接口
"""

from exts import app
from flask import request, jsonify
from decorators import login_required
from file_operator_tools import get_abs_path, listdir
from user_config import HOME_PATH
from os.path import exists, isfile, join, isdir, basename, dirname
import os
import shutil


CODE_YES = 0    # 操作成功的响应码
CODE_NO = 1     # 操作失败的响应码


def create_api_response(code, errmsg='', data=None):
    """
    返回一个josnify后的对象
    :param code: 响应码
    :param errmsg: 错误信息
    :param data: 要带上的数据
    :return: josnify()后的对象
    """
    json_data = {
        'code': code,
        'errmsg': errmsg,
        'data': data
    }

    return jsonify(json_data)


@app.route('/api/remove/', methods=['POST'])
@login_required
def api_remove():
    """删除文件或目录的api"""

    # path: 文件或目录的路径
    path = request.form.get('path') or HOME_PATH  # 若为空则让后面的if判断失败(不能删除管理的根目录)

    abs_path = get_abs_path(HOME_PATH, path)

    try:
        if abs_path and exists(abs_path) and abs_path != HOME_PATH:
            # 路径在HOME_PAGE内, 且存在, 并且不能删除HOME_PAGE目录
            if isfile(abs_path):
                os.remove(abs_path)  # 删除文件
            else:
                shutil.rmtree(abs_path)

            return create_api_response(CODE_YES)
        else:
            raise Exception('Does the path is home path? Or Is th path not in home path?')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))


@app.route('/api/mkdir/', methods=['POST'])
@login_required
def api_mkdir():
    """新建文件夹api"""

    # dir: 哪个目录下创建目录 name: 新建的目录名字
    dir = request.form.get('dir') or HOME_PATH
    name = request.form.get('name')  # 若名字为空肯定会创建失败, 不用管)

    abs_dir = get_abs_path(HOME_PATH, join(dir, name))
    try:
        if abs_dir:
            os.mkdir(abs_dir)
            return create_api_response(CODE_YES)
        else:
            raise Exception('path is not in home')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))


@app.route('/api/upload/', methods=['POST'])
@login_required
def api_upload():
    """上传文件api"""

    # dir: 存放的目录  files: 文件对象的列表
    dir = request.form.get('dir') or HOME_PATH  # 若为空默认为管理的根目录
    files = request.files.getlist('files')

    # print(f)
    # return create_api_response(CODE_NO)
    success_lst = []
    for f in files:
        abs_path = get_abs_path(HOME_PATH, join(dir, f.filename))
        try:
            if abs_path and not exists(abs_path):
                f.save(abs_path)
                success_lst.append(abs_path)
            else:
                raise Exception()
        except:
            pass

    if success_lst:
        return create_api_response(CODE_YES, data=success_lst)
    else:
        return create_api_response(CODE_NO, errmsg='all operations failed')


@app.route('/api/listdir/', methods=['POST'])
@login_required
def api_listdir():
    """获取目录下内容的api"""

    # dir: 目录名字
    dir = request.form.get('dir')  or HOME_PATH # 传过来的参数为空不影响

    abs_dir = get_abs_path(HOME_PATH, dir)

    try:
        if abs_dir and isdir(abs_dir):
            dirs, files = listdir(abs_dir)
            return create_api_response(CODE_YES, data={'dirs':dirs, 'files': files} )
        else:
            raise Exception('directory not found')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))


@app.route('/api/copy/', methods=['POST'])
@login_required
def api_copy():
    """复制文件/目录api"""

    # src: 源路径 dst: 目标路径
    src = request.form.get('src')
    dst = request.form.get('dst')

    try:
        if src and dst:  # 保证参数不为空
            abs_src = get_abs_path(HOME_PATH, src)  # 源绝对路径(确保在HOME_PATH下)
            abs_dst = get_abs_path(HOME_PATH, dst)  # 目标绝对路径(确保在HOME_PATH下)

            if abs_src and abs_dst:
                if isdir(abs_src):
                    # 目录复制用copytree
                    dir_name = basename(abs_src)  # 获取源目录的目录名
                    abs_dst = join(abs_dst, dir_name)  # 拼接实际目标路径(因为前端传来的dst是已经存在的目录)

                    shutil.copytree(abs_src, abs_dst)
                elif isfile(abs_src):
                    # 文件复制用copy
                    shutil.copy(abs_src, abs_dst)
                else:
                    # 不存在abs_src文件或目录
                    raise Exception('%s not found' % abs_src)

                return create_api_response(CODE_YES)
            else:
                # 路径不在HOME_PATH里
                raise Exception('file or directory is not in home path')
        else:
            raise Exception('src or dst is null')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))


@app.route('/api/move/', methods=['POST'])
@login_required
def api_move():
    """移动文件api"""

    # src: 源路径 dst: 目标路径
    src = request.form.get('src')
    dst = request.form.get('dst')

    try:
        if src and dst:  # 保证参数不为空
            abs_src = get_abs_path(HOME_PATH, src)  # 源绝对路径(确保在HOME_PATH下)
            abs_dst = get_abs_path(HOME_PATH, dst)  # 目标绝对路径(确保在HOME_PATH下)

            if abs_src and abs_dst:
                # 无论目录还是文件直接用move即可
                shutil.move(abs_src, abs_dst)
                return create_api_response(CODE_YES)
            else:
                # 路径不在HOME_PATH里
                raise Exception('file or directory is not in home path')
        else:
            raise Exception('src or dst is null')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))


@app.route('/api/rename/', methods=['POST'])
@login_required
def api_rename():
    """重命名文件或目录api"""

    # path: 文件或目录的路径 name: 目录名字
    path = request.form.get('path')
    name = request.form.get('name')
    # 忽略name中有 ../ 等路径分割符, 正常操作不会出现这种状况, 即使出现也只是文件被移动


    try:
        if path and name:
            abs_src = get_abs_path(HOME_PATH, path)  # 源文件名
            abs_dst = get_abs_path(HOME_PATH, join( dirname(abs_src), name ) )  # 目标文件名

            if abs_src and abs_dst and not exists(abs_dst):
                os.rename(abs_src, abs_dst)
                return create_api_response(CODE_YES)
            else:
                raise Exception('file or directory is not in home path. \nor destination path: %s has already existed.' % abs_dst)
        else:
            raise Exception('path is null')
    except Exception as e:
        return create_api_response(CODE_NO, errmsg=str(e))








