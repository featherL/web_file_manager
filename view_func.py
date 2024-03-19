"""
普通的视图函数
"""

from exts import app
from decorators import login_required
from flask import request, render_template,\
    session, g, redirect, url_for, send_file,Response
#from user_config import USERNAME, PASSWORD, HOME_PATH
from user_config import HOME_PATH
from file_operator_tools import listdir, get_abs_path, get_levels, get_m_time
import os

def check_credentials(username, password):
    with open('credentials.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue  # 如果这一行的格式不正确，就跳过这一行
            file_username, file_password = parts
            if username == file_username and password == file_password:
                return True
    return False

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
    print("download varfile:",file)
    print("HOME_PATH",HOME_PATH)
    abs_path = get_abs_path(HOME_PATH, file)
    print("down load abs_path:",abs_path)
    if abs_path and os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)
    else:
        return redirect(url_for('index'))


@app.route('/error.html')
def error():
    return '<h1>error.</h1>'


# @app.route('/view/',methods=['GET'])
# @login_required
# def view():
#     """查看文件内容视图处理函数"""
#     file = request.args.get('file')
#     abs_path = get_abs_path(HOME_PATH, file)
#     print("view abs_path:", abs_path)
#     if abs_path and os.path.isfile(abs_path):
#         with open(abs_path, 'r') as f:
#             content = f.read()
#         return render_template('view.html', file=file, content=content)
#     else:
#         return redirect(url_for('index'))
    

@app.route('/view/', methods=['GET'])
@login_required
def view():
    """查看文件内容视图处理函数"""
    file = request.args.get('file')
    abs_path = get_abs_path(HOME_PATH, file)
    print("view abs_path:", abs_path)
    if abs_path and os.path.isfile(abs_path):
        with open(abs_path, 'r') as f:
            content = f.read()
        if abs_path.endswith('.txt'):
            return content
        elif abs_path.endswith('.html'):
            return content
    return redirect(url_for('index'))
