
#### 首次运行时创建管理员用户
from app import app, db
from models import User


# 创建一个应用上下文
with app.app_context():
    # 创建一个新的管理员用户
    admin_user = User(username='admin', email='admin@admin.com', is_admin=True)
    admin_user.set_password('admin_password')  # 设置管理员密码

    # 将新用户添加到数据库会话
    db.session.add(admin_user)
    db.session.commit()

    print('管理员用户已创建')
