"""
普通的视图函数
"""

from exts import app
from decorators import login_required
from flask import request, render_template,\
    session, g, redirect, url_for, send_file,Response,flash,jsonify
from user_config import HOME_PATH
from file_operator_tools import listdir, get_abs_path, get_levels, get_m_time,get_rel_path,get_relative_levels
import os
from models import User, db
from data import table_data
import pandas as pd

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route('/', methods=['GET'])
@login_required
def index():
    print("index router=====>")
    home_path = session.get('home_path')  # 获取用户的主目录
    relative_path = request.args.get('path') or '.'
    abs_path = get_abs_path(home_path, relative_path)
    if abs_path and os.path.isdir(abs_path):
        dirs, files = listdir(abs_path)
        levels = get_levels(home_path, abs_path)
        print("router index-> levles:",levels)
        
        rel_levels = get_relative_levels(home_path,levels)
        print("router index-> rel_levels:",rel_levels)

        # 计算相对路径
        rel_path = get_rel_path(home_path, abs_path)
        print("router index-> rel_path:",rel_path)
        session['current_dir'] = os.path.join(home_path, rel_path)
        print("router index-> current_dir:",session.get('current_dir'))
        is_admin = g.user and g.user.is_admin
        context = {
            'rel_path': rel_path,  # 使用相对路径
            'rel_levels': rel_levels,
            'dirs': get_m_time(abs_path, dirs),
            'files': get_m_time(abs_path, files),
            'home_path': home_path,  # 将 HOME_PATH 添加到上下文中
            'relative_path':relative_path,
            'is_admin': is_admin
        }
        return render_template('index4.html', **context)
    else:
        raise Exception('Invalid path or directory does not exist')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    print("login===========>")
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['username'] = username
            session['user_id'] = user.id
            #HOME_PATH 是所有用户的根目录
            #home_path 是用户的根目录
            home_path = os.path.join(HOME_PATH, username)  # 计算用户的主目录
            print("login router home_path====>",home_path)
            session['home_path'] = home_path

            # 如果用户的主目录不存在，创建它
            if not os.path.exists(home_path):
                os.makedirs(home_path)

            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    print("register===========>")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get("email")
        password = request.form.get('password')

        # 检查用户是否已存在
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('login.html', error='Username already exists')

        # 创建新用户
        new_user = User(username=username,email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/logout/')
@login_required
def logout():
    session.clear()  # 清空cookie
    return redirect(url_for('login'))


@app.route('/download/', methods=['GET'])
@login_required
def download():
    file = request.args.get('file')
    home_path = session.get('home_path')  # 获取用户的主目录
    rel_file_path = get_rel_path(home_path, file)  # 计算相对路径
    abs_file_path = os.path.join(home_path, file)  # 获取绝对文件路径
    if os.path.isfile(abs_file_path):
        return send_file(abs_file_path, as_attachment=True)
    else:
        return 'File not found', 404


@app.route('/error.html')
def error():
    return '<h1>error.</h1>'


@app.route('/view/', methods=['GET'])
@login_required
def view():
    """查看文件内容视图处理函数"""
    relative_file_path = request.args.get('file')  # 使用相对路径
    abs_file_path = get_abs_path(session.get('home_path', HOME_PATH), relative_file_path)
    if abs_file_path and os.path.isfile(abs_file_path):
        # 根据文件类型发送不同的响应
        if abs_file_path.endswith('.html'):
            # 直接发送HTML文件
            return send_file(abs_file_path, as_attachment=False)
        elif abs_file_path.endswith('.txt'):
            # 读取并显示文本文件的前10行
            with open(abs_file_path, 'r') as f:
                content = f.readlines()[:10]  # 只取前10行
            # 将文本内容作为HTML渲染
            return render_template('file_view.html', content='\n'.join(content))
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
@login_required
def view_users():
    print("======>g.username",g.username)
    print("======>g.user_id",g.user_id)
    if g.user is None or not g.user.is_admin:
        return redirect(url_for('index'))  # 如果不是管理员或者没有登录就没有查看用户的权限，查看用户页面可以设置管理员用户，重定向到主页

    users = User.query.all()  # 获取所有用户
    return render_template('users.html', users=users)

@app.route('/user/edit/<int:user_id>/')
@login_required
def edit_user(user_id):
    print("edit_user request method:",request.method)
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin  # Toggle between admin and normal user
        db.session.commit()
    return redirect(url_for('view_users'))

@app.route('/user/delete/<int:user_id>/')
@login_required
def delete_user(user_id):
    print("delete_user request method:",request.method)
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('view_users'))


@app.route('/user/new/', methods=['GET', 'POST'])
@login_required
def new_user():
    # if not g.user.is_admin:
    #     return redirect(url_for('index'))  # 如果不是管理员，重定向到主页

    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_admin = request.form.get('is_admin') == 'on'
        
        # 简单验证：确保提供了所有信息，并且两次密码输入一致
        if not username or not password or password != confirm_password:
            flash('Please fill all fields and ensure passwords match.')
            return redirect(url_for('new_user'))

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('new_user'))

        # # 检查用户名和电子邮件是否已存在
        # existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        # if existing_user:
        #     return render_template('new_user.html', error='用户名或电子邮件已存在')

        # 创建新用户
        new_user = User(username=username,email=email,is_admin=is_admin)
        new_user.set_password(password)  # 存储密码散列值而不是明文密码
        db.session.add(new_user)
        db.session.commit()

        flash('New user has been created successfully.')
        return redirect(url_for('view_users'))

    # 如果是GET请求，渲染创建用户的表单
    return render_template('new_user3.html')


@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        # 验证用户名对应的邮箱
        email = user.email
        return render_template('reset_password.html', username=username, email=email)
    else:
        return jsonify({'error': '你的用户名不存在！！！！！！'}), 404


@app.route('/reset_password/<username>', methods=['POST'])
def update_password(username):
    user = User.query.filter_by(username=username).first()
    if user:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == confirm_password:
            user.set_password(password)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # 处理密码不匹配的情况
            return render_template('error.html', message='新密码和确认密码不匹配')
    else:
        return jsonify({'error': '用户名不存在'}), 404
    

@app.route('/table_manager')
@login_required
def table_manager():
    tables = [
        {'id': 1, 'name': 'Users'},
        {'id': 2, 'name': 'Products'},
        {'id': 3, 'name': 'Orders'}
    ]

    # 使用pandas读取文件
    sample_data = []
    try:
        df = pd.read_table('sample.txt')
        sample_data = df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    print(sample_data)
    return render_template('table_manager.html', tables=tables, sample_data=sample_data)


@app.route('/save_table', methods=['POST'])
def save_table():
    try:
        data = request.json['data']
        print("保存数据===》",data)
        df = pd.DataFrame(data)
        print(df)
        df.to_csv('sample.txt', sep='\t', index=False)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/api/tables/<int:table_id>/data', methods=['GET'])
def get_table_data(table_id):
    table_data = table_data.get(table_id)
    if table_data:
        return jsonify(table_data)
    else:
        return jsonify({'error': 'Table not found'}), 404


