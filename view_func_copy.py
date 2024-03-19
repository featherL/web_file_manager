"""
普通的视图函数
"""

from exts import app
from decorators import login_required
from flask import request, render_template,\
    session, g, redirect, url_for, send_file
#from user_config import USERNAME, PASSWORD, HOME_PATH
from user_config import HOME_PATH
from file_operator_tools import listdir, get_abs_path, get_levels, get_m_time
import os


def check_credentials(username, password):
    print("密码文件")
    with open('credentials.txt', 'r') as f:
        for line in f:
            file_username, file_password = line.strip().split(':')
            if username == file_username and password == file_password:
                return True
    return False


# @app.route('/', methods=['GET'])
# @login_required
# def index():
#     """首页处理试图函数"""
#     path = request.args.get('path') or HOME_PATH # 若是path为None则f_get_abs_path也为None那么就会一直重定向
#     try:
#         abs_path =  get_abs_path(HOME_PATH, path)  # 获取绝对路径
#         if abs_path and os.path.isdir(abs_path):
#             dirs, files = listdir(abs_path)
#             levels = get_levels(HOME_PATH, abs_path)
#             context = {
#                 'path':abs_path,
#                 'levels': levels,
#                 'dirs':get_m_time(abs_path, dirs),
#                 'files':get_m_time(abs_path, files)
#             }
#             return render_template('index.html', **context)
#         else:
#             raise Exception()  # 让外面捕捉异常来跳转页面
#     except Exception as e:
#         return redirect(url_for('error'))

@app.route('/', methods=['GET'])
@login_required
def index():
    """首页处理试图函数"""
    home_path = session.get('home_path')  # 获取用户的主目录
    path = request.args.get('path') or home_path
    try:
        abs_path =  get_abs_path(home_path, path)
        if abs_path and os.path.isdir(abs_path):
            dirs, files = listdir(abs_path)
            levels = get_levels(home_path, abs_path)
            context = {
                'path':abs_path,
                'levels': levels,
                'dirs':get_m_time(abs_path, dirs),
                'files':get_m_time(abs_path, files)
            }
            return render_template('index.html', **context)
        else:
            raise Exception()
    except Exception as e:
        return redirect(url_for('error'))



# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     """登录处理视图函数"""
#     if g.username:
#         # 已经登录过了, 重定向到首页
#         return redirect(url_for('index'))
#     if request.method == 'GET':
#         # GET方法
#         return render_template('login.html')
#     else:
#         # POST方法
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == USERNAME and password == PASSWORD:
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             return render_template('login.html', error='login error')
        
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if check_credentials(username, password):
#             session['username'] = username
#             return redirect(url_for('download'))
#         else:
#             return render_template('login.html', error='Invalid username or password')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if check_credentials(username, password):
            session['username'] = username
            home_path = os.path.join(HOME_PATH, username)  # 计算用户的主目录
            session['home_path'] = home_path

            # 如果用户的主目录不存在，创建它
            if not os.path.exists(home_path):
                os.makedirs(home_path)

            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')



@app.route('/logout/')
@login_required
def logout():
    session.clear()  # 清空cookie
    return redirect(url_for('login'))


@app.route('/download/', methods=['GET'])
@login_required
def download():
    """下载文件视图处理函数"""
    file = request.args.get('file')
    abs_path = get_abs_path(HOME_PATH, file)
    if abs_path and os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)
    else:
        return redirect(url_for('index'))


@app.route('/error.html')
def error():
    return '<h1>error.</h1>'

