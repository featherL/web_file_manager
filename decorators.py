"""
这里编写一些装饰器
"""

from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    """如果未登录则重定向到登录页面"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.username:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper
