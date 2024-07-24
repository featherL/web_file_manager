# web_file_manager
由**flask**与**bootstarp**开发而成的简单的web在线文件管理工具

# 适用平台
+ linux
+ window (**可能由于模板文件中某些路径分隔符写死为 / 而出现一些问题**)

## 用法
+ 在配置文件`config.py`配置flask的配置信息
+ 在配置文件`user_config.py`中配置**用户名**、**密码**、**文件根目录**
+ 运行`python web_file_manager.py`
+ 打开网页`http://127.0.0.1:5000` (**这flask的默认配置**)

## 概览
+ 登录页面
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/login.png)
+ 主页
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/index.png)
+ 新建文件
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/new_dir.png)
+ 上传文件
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/upload.png)
+ 点击文件右端的复制按钮(**鼠标停留在按钮上有提示**)
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/copy.png)
+ 画图工具
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/img_tools.png)
+ stackplot
  ![image](https://github.com/featherL/web_file_manager/raw/master/screenshots/stackplot.png)
+ ......
