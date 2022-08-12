# 捉虫大师博客

###### 背景
基于软件测试特性，需要一个测试平台、测试技术博客，规划任务、记录测试点点滴滴

###### 开发计划

##### v2.0版本 2019.06.25：

1.新增 管理员可查看全部文章、登录用户只可查看自己文章<br/>
2.新增 微博、大事件新增ajax实时搜索<br/>
3.新增 博客增加评论功能<br/>
4.新增 导航新增可编辑功能<br/>
5.优化 首页常用数据做缓存<br/>
6.优化 模板化页面<br/>


##### v1.0版本 2019.02.25：

1.登录注册<br/>
2.博客新增、搜索、归类<br/>
3.类微博功能<br/>
4.大事件记录功能<br/>
5.个性化网址收藏<br/>
6.娱乐收藏<br/>


# 博客源码使用

##     开发环境部署
 requirements.txt 安装需要的库，基于python3\mysql5.7

## 准备工作

 数据替换：settings.py中修改数据库、邮件账号、翻页数等(参照注释)

  第一步 ：数据迁移 python manage.py makemigrations

  第二步： 创建真实的数据表 python manage.py migrate

  第三步：创建后台超管账号 python manage.py createsuperuser

## 启动 
开启服务 python manage.py runserver 127.0.0.1:8000<br/>
打开网站 127.0.0.1:8000 <br/>


---

## 简单的使用方法：


1.创建虚拟环境<br/>
2.使用pip安装第三方依赖<br/>
3.修改settings.example.py文件为settings.py<br/>
4.运行migrate命令，创建数据库和数据表<br/>
5.运行python manage.py runserver启动服务器<br/>
