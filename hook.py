"""
一些钩子
"""

from flask import session, g
from exts import app
from user_config import HOME_PATH, HOME_NAME


@app.before_request
def set_session():
    g.username = session.get('username')
    g.user_id = session.get('user_id')
    # g.username = 'feather'   # debug


@app.context_processor
def set_username():
    context = {
        'home_path': HOME_PATH,  # 文件管理的根目录路径
        'home_name':HOME_NAME  # 文件管理的根目录名字
    }

    if g.username:
        context['username'] = g.username

    return context
