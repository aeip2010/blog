import datetime
# 导入logging库
import logging
import os,time
import re
import  json
from django.http import JsonResponse

from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from django.views.decorators.cache import cache_page

from blog import forms
from blog.utils import infor, sendemail, helper
from . import models
from django.core.cache import cache #缓存读取
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers #序列化


# 获取一个logger对象
logger = logging.getLogger(__name__)

#当前时间
ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
c_dir = os.getcwd()

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#********************************************************全局设置************************************************************************************

#全局变量
weibo_status = False

# 首页
def index(request):
    return redirect("/blog/")


#********************************************************登录注册系统************************************************************************************
"""
login 登录
register  注册
logout 登出
user_confirm 用户邮件确认
"""

#登录
def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # print(infor.hash_code(password))
            #账号密码记录
            with open('logs/user.txt', 'a+') as f:
                f.write(username + "    " + password + "    %s"%ctime + '\n')
            try:
                user = models.User.objects.get(name=username)
                # print(infor.hash_code(password))
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', locals())
                if user.password == infor.hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    # 获取相应对象
                    response = HttpResponseRedirect(request.session['login_from'])
                    # 设置cookie
                    response.set_cookie("username", user.name, 604800)  # 过期时间单位是s (这里设置为7天)
                    return response
                    # return HttpResponseRedirect(request.session['login_from'])
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"

        return render(request, 'login/login.html', locals())

    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

#注册
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                    # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.email = email
                new_user.sex = sex


                #调用外部包
                ip = infor.get_realip()
                new_user.from_ip = ip
                new_user.password = infor.hash_code(password1)
                new_user.save()

                code = infor.make_confirm_string(new_user)
                host = request.get_host()

                sendemail.send_email(username, email, code,host)
                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面。

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

#登出
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#用户邮件确认
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.create_time
    c_time = c_time.replace(tzinfo=None)  #时间转换 去掉时区
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True #更改user表确认字段
        confirm.user.save()
        confirm.has_confirmed = True  #更改确认状态
        confirm.save() #保存状态
        #confirm.delete()  #确认code相关数据删除
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())



#********************************************************装饰器大全************************************************************************************
"""
check_login 校验用户是否登录状态
"""
#登录判断装饰器 未登录跳转登录
#装饰器，登录判断
def check_login(func):
    def inner(request,*args,**kwargs): #带有通用参数
        #登录判断
        if not request.session.get('is_login', None):
            data = {}
            data['goto_url'] = '/'
            return redirect('/login/',data)
        else:
            return func(request,*args,**kwargs)

    return inner


#********************************************************统计数据************************************************************************************
"""
搜索统计 search_tongji
数据统计 version
"""
@csrf_exempt
def version(request):
    a={}
    # print("2345")
    json_receive = json.loads(request.body)
    # print(2345,json_receive)
    blogtongji = str(json_receive)
    f = open(settings.LOG_DIR,"a+")
    f.write(ctime + "  "  + blogtongji + "\n")
    mes = "2345777"
    a['status'] = 'success'
    a['message'] = mes
    return JsonResponse(a)


def search_tongji(profile_no,search_range,search_type,content,current_url):
    """
    搜索词 当前页面 搜索类别 用户 时间 浏览器信息 ip 搜索次数
    search_range blog/weibo/timeline
    search_type search/submit/view
    servicecode
    """
    new_search = models.Search_submit_record()
    new_search.ip = infor.get_ip()
    new_search.profile_no = profile_no
    new_search.search_time = get_time()
    new_search.search_range = search_range
    new_search.search_type = search_type
    new_search.content = content
    new_search.current_url = current_url
    # print("okok")
    new_search.save()

#********************************************************博客系统************************************************************************************
"""
tag_count 标签与条目统计
type_count  分类与条目统计
blog    博客主页
detail 博客详情页
archives 博客汇总
search_tag 标签搜索
search_type 分类搜索
search_name 作者文章搜索
blog_search 博客标题关键字搜索
aboutme 关于我介绍页面
post_new 新增博客
post_edit 博客编辑
AddCommentView 博客评论
"""

#tag的总数
def tag_count(posts):
    tags = models.Tag.objects.all()
    tags_dic = {}
    for tag in tags:
        s = tag.name
        tags_dic[s] = posts.filter(tage=s).count()

    return tags_dic


#分类的总数
def type_count(posts):
    blog_type = models.Category.objects.all()
    type_dic = {}
    for type1 in blog_type:
        s = type1.name
        type_dic[s] = posts.filter(category_id=type1.id).count()
    return type_dic

#评论的总数
def comment_count(blogid):
    Comment_type = models.Comment.objects.all()
    comment_count = Comment_type.filter(blog_id=blogid).count()
    return comment_count


@check_login
#分页的博客系统
def blog(request):
    #判断登录者身份
    if request.session['user_id'] == 24:
        posts = models.Blog.objects.filter(is_activate=1).order_by("-update_time")
    else:
        posts = models.Blog.objects.filter(is_activate=True,author=request.session['user_name'])
        blog_type = models.Category.objects.all().order_by("id")
        blog_view = models.Blog.objects.filter(is_activate=True)

    if posts:
        data = {}
        paginator,post_list = helper.blog_home(request,posts)
        data["posts"] = posts
        data['pages'] = paginator
        data['blogs'] = post_list
        data["tags"] = models.Tag.objects.all()

        data_list = get_count_cache()
        # print(data_list,'这是list')
        # type_dic = type_count(posts)
        type_dic = data_list[0]
        # tags_dic = tag_count(posts)
        tags_dic = data_list[1]
        comment_dic = data_list[3]
        data["comment_list"] = comment_dic
        data['info_dict'] = type_dic
        data["tags"] = tags_dic
        blog_view = models.Blog.objects.filter(is_activate=True)
        data['blog_view'] = blog_view.order_by("-views")[0:20]
        data["tongji_blog"] = data_list[2]["tongji_blog"]
        data["tongji_weibo"] = data_list[2]["tongji_weibo"]
        data["tongji_tag"] = data_list[2]["tongji_tag"]
        data["tongji_timeline"] = data_list[2]["tongji_timeline"]
        data["tongji_user"] = data_list[2]["tongji_user"]
        data["tongji_site"] = data_list[2]["tongji_site"]
        data["tongji_comment"] = data_list[2]["tongji_comment"]

        return render(request, 'blog/home.html', data)
    else:
        message = '博客无内容，2秒后自动跳转到博客创建页页！'
        return render(request, 'blog/blog_confirm.html', locals())

@check_login
# @cache_page(60*5)
#博客详情页
def detail(request, id):
    data = {}
    try:
        prev_id = int(id) - 1
        next_id = int(id) + 1
        post = models.Blog.objects.get(id=str(id),is_activate=1,author=request.session['user_name'])

        try:
            next_post = models.Blog.objects.get(id=str(next_id),is_activate=1,author=request.session['user_name']) # 下一篇文章对象
        except:
            next_post = {}

        try:
            prev_post = models.Blog.objects.get(id=str(prev_id), is_activate=1,author=request.session['user_name'])  # 上一篇文章对象
        except:
            prev_post = {}

        search_tongji(request.session['user_name'], "blog", "view", post.title, request.get_full_path())

        all_comment = models.Comment.objects.filter(blog_id=id)
        # print(all_comment)
        data_list = get_count_cache()
        comment_dic = data_list[3]
        data["comment_list"] = comment_dic
        data['post']=post
        data['next_post']=next_post
        data['prev_post']=prev_post
        data["all_comment"] = all_comment


        #访问一次阅读一次


    except models.Blog.DoesNotExist:
        return render(request,'blog/404.html')

    post.increase_views()
    return render(request, 'blog/blog_detail.html', data)

@check_login
@cache_page(60*5,key_prefix="tag")
#标签搜索
def search_tag(request,tag) :
    data = {}
    try:
        # 判断登录者身份
        if request.session['user_id'] == 1:
            post_list = models.Blog.objects.filter(tage__contains=tag, is_activate=1)  # contains
        else:
            post_list = models.Blog.objects.filter(tage__contains=tag,is_activate=True, author=request.session['user_name'])
    except models.Blog.DoesNotExist:
        return render(request, 'blog/404.html')

    search_tongji(request.session['user_name'], "blog", "search", tag, request.get_full_path())
    data["post_list"] = post_list
    data["tag"] = tag
    return render(request, 'blog/tag_search.html', data)

@check_login
@cache_page(60*5)
#分类搜索
def search_type(request,type) :
    data = {}
    categoryid = models.Category.objects.only('id','name')
    # print(categoryid)
    for x in categoryid:
        if x.name == type:
            categoryid1 = x.id
    try:
        # 判断登录者身份
        posts = models.Blog.objects.filter(is_activate=1)  # contains
        if request.session['user_id'] == 1:
            posts_type = models.Blog.objects.filter(category_id=categoryid1,is_activate=True)
        else:
            posts_type = models.Blog.objects.filter(category_id=categoryid1,is_activate=True, author=request.session['user_name'])
    except models.Blog.DoesNotExist:
        return render(request, 'blog/404.html')
    search_tongji(request.session['user_name'], "blog", "search", type, request.get_full_path())

    data_list = get_count_cache()

    # type_dic = type_count(posts)
    data['info_dict'] = data_list[0]

    paginator, post_list = helper.blog_home(request, posts_type)
    blog_view = models.Blog.objects.filter(is_activate=True)
    data['blog_view'] = blog_view.order_by("-views")[0:20]
    data["blogs"] = post_list
    data["posttype"] = posts_type
    data['pages'] = paginator
    data["tongji_blog"] = data_list[2]["tongji_blog"]
    data["tongji_weibo"] = data_list[2]["tongji_weibo"]
    data["tongji_tag"] = data_list[2]["tongji_tag"]
    data["tongji_timeline"] = data_list[2]["tongji_timeline"]
    data["tongji_user"] = data_list[2]["tongji_user"]
    data["tongji_site"] = data_list[2]["tongji_site"]

    data["type"] = type
    # tags_dic = tag_count(posts)
    data["tags"] = data_list[1]


    # print(post_list)
    return render(request, 'blog/type_search.html', data)

@check_login
@cache_page(60*5)
#用户名搜索
def search_name(request, name) :
    data = {}
    try:
        post_list =models.Blog.objects.filter(author =name,is_activate=1) #contains
    except models.Blog.DoesNotExist :
        return render(request, 'blog/404.html')

    data["name"] = name
    data["post_list"] = post_list
    search_tongji(request.session['user_name'], "blog", "search", name, request.get_full_path())
    return render(request, 'blog/name_search.html',data)

@check_login
# @cache_page(60*5)
#用户名搜索
def archives(request) :
    data = {}
    try:
        post_list =models.Blog.objects.filter(is_activate=True)
    except models.Blog.DoesNotExist :
        return render(request, 'blog/404.html')

    years = []
    for x in range(2018, 2020):
        years.append(str(x))

    years.reverse()
    data['years'] = years

    months = []
    for x in range(1, 13):
        months.append(str(x))
    months.reverse()
    data['months'] = months

    data_list = get_count_cache()
    comment_dic = data_list[3]

    data["post_list"] = post_list
    data["comment_list"] = comment_dic
    return render(request, 'blog/blog_archives.html',data)

@check_login
@cache_page(60)
#博客内容搜索
def blog_search(request):
    data = {}
    if 'keyword' in request.GET:
        s = request.GET['keyword']
        if len(s)>=1 :
            # print(len(s),s)
            print("ok-2")
            # 判断登录者身份
            if request.session['user_id'] == 1:
                post_list = models.Blog.objects.filter(title__icontains=s, is_activate=1)
            else:
                post_list = models.Blog.objects.filter(title__icontains=s, is_activate=True,
                                                       author=request.session['user_name'])

            search_tongji(request.session['user_name'], "blog", "search", s, request.get_full_path())
            if len(post_list) == 0:
                data["error"] = True
                data["post_list"] = post_list
                data["keyword"] = s
                return render(request, 'blog/blog_search.html', data)
            else:
                data["error"] = False
                data["post_list"] = post_list
                data["keyword"] = s
                return render(request, 'blog/blog_search.html', data)



        else:
            post_list = models.Blog.objects.filter(title__icontains=s, is_activate=True,
                                                   author=request.session['user_name'])
            data["error"] = True
            data["post_list"] = post_list
            data["keyword"] = s
            return render(request, 'blog/blog_search.html', data)

    return redirect('/')

# @cache_page(60*60)
#关于我
def about(request) :
    return render(request, 'blog/about.html')


def ajax_demo(request) :
    return render(request, 'ajax/ajax.html')


# tag创建
def tag_create(tag):
    # 切割标签
    if "," in tag:
        # print(tag)
        tag_list = tag.split(",")
        # print(tag_list)
    else:
        tag_list = [tag, "2019"]

    # 搜索标签id 新的插入
    all_tags = models.Tag.objects.only("name")
    tags_list = []
    for z in all_tags:
        tags_list.append(z.name)

    for y in tag_list:
        if y in tags_list:
            # print(type(y),y)
            pass
        else:
            models.Tag.objects.create(name=y)  # 保存新标签
            models.Blog.tags

@check_login
#新增博客
def post_new(request):
    if request.method == "POST":
        form = forms.BlogForm(request.POST)
        message = '请检查填写的内容!'
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            tag = form.cleaned_data['tage']

            tag_create(tag)
            category = request.POST.get('category')
            categoryid = models.Category.objects.only('id','name')

            for x in categoryid:
                if x.name == category:
                    categoryid1 = x.id

            if models.Blog.objects.filter(title__exact= title)  :
                message = "标题不可重复！"
                blog_form = forms.BlogForm() #(initial={'title':title})
                return render(request, 'blog/post_new.html',locals())

            new_blog = models.Blog()
            new_blog.title = title
            new_blog.content = content
            new_blog.tage = tag
            new_blog.category_id = categoryid1
            try:
                new_blog.author = request.session['user_name']  # 当前用户名
            except:
                new_blog.author = 'test'
            new_blog.save()
            search_tongji(request.session['user_name'], "blog", "submit", "新增博客", request.get_full_path())

            blog_id = models.Blog.objects.filter(title__exact= title)[0].id
            # models.Blog.tags.create({"blog_id":blog_id,"tag_id":})
            post = models.Blog.objects.filter(title__exact= title)
            return redirect('detail', post[0].id)

    else:
        blog_form = forms.BlogForm()
        data = {}
        data['blog_form'] = blog_form
        data['posts'] = models.Category.objects.all()
        data["tags"] = models.Tag.objects.all()
        return render(request, 'blog/post_new.html', data)


#编辑博客
def post_edit(request,postid):
    if request.method == "GET":
        data = {}
        post = models.Blog.objects.filter(id=postid)[0]
        blog_form = forms.BlogForm(initial={'title':post.title,'tage':post.tage,'content':post.content})
        data['posts'] = models.Category.objects.all()
        data['blog_form'] = blog_form
        data["post_id"] = postid
        data["post_title"] = post.title
        data["post_type"] = models.Category.objects.filter(id=post.category_id)[0].name
        # print(data["post_type"])
        return render(request, 'blog/post_edit.html',data)

    if request.method == "POST":
        form = forms.BlogForm(request.POST)
        message = '请检查填写的内容!'
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            tag = form.cleaned_data['tage']

            tag_create(tag)
            category = request.POST.get('category')
            categoryid = models.Category.objects.only('id', 'name')
            for x in categoryid:
                if x.name == category:
                    categoryid1 = x.id

            new_blog = models.Blog.objects.get(id=postid)
            new_blog.title = title
            new_blog.content = content
            new_blog.tage = tag
            new_blog.category_id = categoryid1

            try:
                new_blog.author = request.session['user_name']  # 当前用户名
            except:
                new_blog.author = 'test'
            search_tongji(request.session['user_name'], "blog", "submit", "编辑博客", request.get_full_path())
            new_blog.save()

            blog_id = models.Blog.objects.filter(title__exact=title)[0].id
            post = models.Blog.objects.filter(title__exact=title)
            return redirect('detail', post[0].id)

def AddCommentView(request):
    #判断登录者身份
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST)
        a={}
        if comment_form.is_valid():
            id = comment_form.cleaned_data['blog']
            # print(id,type(id),id.id)
            name = comment_form.cleaned_data['name']
            con = request.POST.get('content')
            content = con.replace("\r\n", "<br/>")
            new_comment = models.Comment()
            new_comment.name = name
            new_comment.content = content
            new_comment.blog_id = id.id
            new_comment.save()

            # comment_form.save()
            a['status'] = 'success'
            a["comments"] = serializers.serialize("json", models.Comment.objects.filter(blog_id=id))
            a["comments_count"] = models.Comment.objects.filter(blog_id=id).count()
            return JsonResponse(a)
            # return HttpResponse('%s'%a, content_type='application/json')
        else:
            mes="检查用户名、内容是否符合要求:不得为空、字数不得超出限制"
            a['status'] = 'false'
            a['message'] = mes
            return JsonResponse(a)

#********************************************************微博系统************************************************************************************
"""
weibo 微博首页
new_weibo 新建微博
weibo_search 微博内容搜索
"""
@check_login
def weibo(request):
    if request.session['user_id'] == 1:
        weibo_list = models.Note.objects.filter(is_activate=1)
    else:
        weibo_list = models.Note.objects.filter(is_activate=1,createuser=request.session['user_name'])
    data = {}
    if weibo_list:
        pages,posts = helper.blog_weibo(request,weibo_list)
        data['posts'] = posts
        data['pages'] = pages
        data['all_post'] = weibo_list
        # print(posts)
        date = now().date() + timedelta(days=0)  # 今天
        tian = date.day
        yue = date.month

        day_count = weibo_list.filter()
        now_time = "%s-%s-%s"%(date.year,date.month,date.day)
        n = 0
        for x in day_count:
            if x.create_time.day==tian and x.create_time.month==yue:
                # print(x,type(x))
                n+=1

        data['weibo_count'] = n
        data['now_time'] = now_time
        return render(request, 'blog/weibo_list.html', data)

    else:
        message = '你还没有叨叨，来一波吧'
        data['posts'] = weibo_list
        data['message'] = message
        return render(request,'blog/weibo_list.html',data)

@check_login
def new_weibo(request):
    data = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        message = ""
        if len(request.POST.get('content')) > 5:  # 获取数据
            con = request.POST.get('content')
            content = con.replace("\r\n","<br/>")
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
            try:
                url = re.findall(pattern, content)[0]
                content = content.replace(str(url), "<a href='%s' target='_blank'>%s</a>" % (url,url))
            except:
                pass
            new_weibo= models.Note()
            try:
                new_weibo.createuser = request.session['user_name']  # 当前用户名
            except:
                new_weibo.createuser = 'test'

            new_weibo.content = content
            new_weibo.ip = infor.get_address(infor.get_realip())

            #
            # print(new_weibo.content)
            search_tongji(request.session['user_name'], "weibo", "submit", "新增碎语", request.get_full_path())
            new_weibo.save()
            weibo_status = True
            # src = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
            # post.post_weibo(src, 120, con)
            return redirect('/weibo/')
        else:
            message = '字数不足5个无法提交，请重试'
            # data['posts'] = weibo_list
            data['message'] = message
            return  render(request,'blog/weibo_list.html',data)

    else:
        return redirect('/weibo/')


@cache_page(60*5)
#微博内容搜索
def weibo_search(request):
    data = {}
    if request.session.get('is_login', None):
        if 'keyword' in request.GET:
            s = request.GET['keyword']
            if not s:
                post_list = models.Note.objects.filter(is_activate=1).order_by("-create_time")
                post_list = post_list.filter(content__contains=s)
                data["posts"] = post_list
                data["error"] = True
                data["keyword"] = s
                return render(request, 'blog/weibo_search.html', data)
            else:
                # 判断登录者身份
                if request.session['user_id'] == 1:
                    post_list = models.Note.objects.filter(is_activate=1 ).order_by("-create_time")
                    post_list = post_list.filter(content__contains=s)
                else:
                    post_list = models.Note.objects.filter(is_activate=True, createuser=request.session['user_name']).order_by("-create_time")
                    post_list = post_list.filter(content__contains=s)

                if len(post_list) == 0 :
                    data["posts"] = post_list
                    data["error"] = True
                    data["keyword"] = s
                    return render(request, 'blog/weibo_search.html', data)

                else :
                    data["posts"] = post_list
                    data["error"] = False
                    data["keyword"] = s
                    return render(request, 'blog/weibo_search.html', data)

        return redirect('/')
    else:
        return redirect("/login/")


def weibo_search_ajax(request):
    q = request.GET.get('q')
    a = {}
    if q:
        post_list = models.Note.objects.filter(is_activate=1).order_by("-create_time")
        recontents = post_list.filter(content__contains=q)
        # search_tongji(request.session['user_name'], "weibo", "search", q, request.get_full_path())
        if recontents:
            a["weibos"] =serializers.serialize("json",recontents)
            a["weibos_count"] = recontents.count()
            a['message'] = "false"
            return JsonResponse(a)
        else:
            a['message'] = "true"
            return JsonResponse(a)
    else:
        post_list = models.Note.objects.filter(is_activate=1).order_by("-create_time")
        a["weibos"] = serializers.serialize("json", post_list)
        a["weibos_count"] = post_list.count()
        a['message'] = "false"
        return JsonResponse(a)



#********************************************************导航系统************************************************************************************

"""
site 站点主页与创建页
site_edit 站点编辑
site_delete 站点删除
"""
#站点导航
def site(request):
    if request.session.get('is_login', None):
        if  request.method == "POST":
            sitecreate_form = forms.SiteForm(request.POST)
            message = '请检查填写的内容!'
            if sitecreate_form.is_valid():
                sitetype = request.POST.get('sitetype')
                sitename = request.POST.get('sitename')
                sitelink = request.POST.get('sitelink')
                sitenote = request.POST.get('sitenote')

                new_site = models.Site()
                try:
                    new_site.createuser = request.session['user_name']  # 当前用户名
                except:
                    new_site.createuser = ''
                new_site.sitetype = sitetype
                new_site.sitename = sitename
                new_site.sitelink = sitelink
                new_site.sitenote = sitenote
                new_site.is_activate = True #默认赋值True

                new_site.save()

                # sitelist = models.Site.objects.all()
                # return render(request, 'wiki/Site.html', {'sitelist': sitelist})
                return redirect('/site/')

        #登录下get
        # print("234")
        sitecreate_form = forms.SiteForm()

        # 判断登录者身份
        if request.session['user_id'] == 1:
            sites = models.Site.objects.filter(is_activate=True)
        else:
            sites = models.Site.objects.filter(is_activate=True, createuser=request.session['user_name'])

        data = {}
        data['sitecreate_form'] = sitecreate_form
        data["sitetypes"] = models.SiteCategory.objects.all()
        data["sites"] = sites

        # return render(request, 'wiki/Site.html', {'sitelist': sitelist})
        return render(request, 'blog/Site.html',data)

    return redirect('/login/')


def music(request):
    return render(request,"blog/music.html")



def site_edit(request,siteid):

    if request.method == "GET":
        data = {}
        post = models.Site.objects.filter(id=siteid)[0]
        sitecreate_form = forms.SiteForm(initial={'sitename': post.sitename, 'sitelink': post.sitelink, 'sitenote': post.sitenote})
        data['sitecreate_form'] = sitecreate_form
        data["sitetypes"] = models.SiteCategory.objects.all()
        data["post_id"] = siteid
        data["post_type"] = post.sitetype
        data["post_title"] = post.sitename
        return render(request, 'blog/site_edit.html', data)

    if request.method == "POST":
        sitecreate_form = forms.SiteForm(request.POST)
        message = '请检查填写的内容!'
        if sitecreate_form.is_valid():
            sitetype = request.POST.get('sitetype')
            sitename = request.POST.get('sitename')
            sitelink = request.POST.get('sitelink')
            sitenote = request.POST.get('sitenote')

            new_site = models.Site.objects.get(id=siteid)
            try:
                new_site.createuser = request.session['user_name']  # 当前用户名
            except:
                new_site.createuser = ''

            new_site.sitetype = sitetype
            new_site.sitename = sitename
            new_site.sitelink = sitelink
            new_site.sitenote = sitenote
            new_site.is_activate = True  # 默认赋值True
            new_site.save()
            return redirect('/site/')


def site_delete(request,siteid):
    models.Site.objects.filter(id=siteid).delete()
    return redirect('/site/')

#********************************************************时间线系统************************************************************************************
"""
timeline 大事件首页及创建页
timeline_search 地铁、内容关键字搜索
"""

@check_login
def timeline(request):
    data = {}
    message = '请检查填写的内容!'
    new_timeline = models.TimeLine.objects.filter(is_activate=True).order_by("-linetime")
    years = []
    for x in range(1986,2020):
        years.append(str(x))
    years.reverse()
    data['years'] =years
    citys = models.City.objects.filter(has_confirmed=True, is_activate=1, content='city')
    landmarks = models.City.objects.filter(has_confirmed=True, is_activate=1, content='tag')
    data['citys'] = citys
    data['landmarks'] = landmarks
    data["all_timeline"] = new_timeline

    if request.method == "POST":
        content = request.POST.get('content')
        content = content.replace("\r\n", "<br/>")
        city = request.POST.get('city')
        timer = request.POST.get('timer')
        # print(timer,type(timer))
        try:
            year = timer.split("-")[0]
            month = timer.split("-")[1]
        except:
            pass
        landmark = request.POST.get('landmark')
        time_type = request.POST.get('time_type')
        keyword = request.POST.get('keyword')

        if not content:
            message = "事件内容不能为空!"
            data['message'] =message
            return render(request, "blog/timeline.html", data)
        if not timer:
            message = '时间选择不能为空!'
            data['message'] = message
            return render(request, "blog/timeline.html", data)
        if not keyword:
            message = '关键字不能为空!'
            data['message'] = message
            return render(request, "blog/timeline.html", data)

        new_timeline = models.TimeLine()
        new_timeline.content = content
        new_timeline.year = year
        new_timeline.city = city
        new_timeline.linetime = timer
        new_timeline.landmark = landmark
        new_timeline.type = time_type
        new_timeline.keyword = keyword
        new_timeline.createuser = request.session['user_name']  # 当前用户名
        new_timeline.year = year
        new_timeline.month = month
        search_tongji(request.session['user_name'], "timeline", "submit", "新增大事件", request.get_full_path())
        new_timeline.save_base()

        return redirect("/timeline/")
    else:
        return render(request, "blog/timeline.html",data)




@cache_page(60*5)
#时间线内容搜索
def timeline_search(request):
    data = {}
    if request.session.get('is_login', None):
        if 'keyword' in request.GET:
            s = request.GET['keyword']
            if not s:
                post_list = models.TimeLine.objects.filter(is_activate=1).order_by("-linetime")
                post_list = post_list.filter(Q(keyword__contains=s) | Q(content__contains=s) | Q(city__contains=s) |Q(year_contains=s))
                data["post_list"] = post_list
                data["error"] = True
                data['keyword'] = s
                return render(request, 'blog/timeline_search.html', data)
            else:
                # 判断登录者身份
                if request.session['user_id'] == 1:
                    post_list = models.TimeLine.objects.filter(is_activate=1 ).order_by("-linetime")
                    post_list = post_list.filter(Q(keyword__contains=s)|Q(content__contains=s)|Q(city__contains=s))
                else:
                    post_list = models.TimeLine.objects.filter(is_activate=True, createuser=request.session['user_name']).order_by("-linetime")
                    post_list = post_list.filter(Q(keyword__contains=s) | Q(content__contains=s) | Q(city__contains=s))
                if len(post_list) == 0 :
                    data["post_list"] = post_list
                    data["error"] = True
                    data['keyword'] = s
                    return render(request, 'blog/timeline_search.html', data)
                else :
                    data["post_list"] = post_list
                    data["error"] = False
                    data['keyword'] = s
                    return render(request, 'blog/timeline_search.html', data)
        return redirect('/')
    else:
        return redirect("/login/")


def timeline_search_ajax(request):
    q = request.GET.get('q')
    a = {}
    if q:
        post_list = models.TimeLine.objects.filter(is_activate=1 ).order_by("-linetime")
        recontents = post_list.filter(Q(keyword__contains=q)|Q(content__contains=q)|Q(city__contains=q))
        if recontents:
            a["weibos"] =serializers.serialize("json",recontents)
            a["weibos_count"] = recontents.count()
            a['message'] = "false"
            return JsonResponse(a)
        else:
            a['message'] = "true"
            return JsonResponse(a)
    else:
        post_list = models.TimeLine.objects.filter(is_activate=1).order_by("-linetime")
        a["weibos"] = serializers.serialize("json", post_list)
        a["weibos_count"] = post_list.count()
        a['message'] = "false"
        return JsonResponse(a)

#********************************************************测试平台系统************************************************************************************
"""
test_bench 测试工作台主页及创建
daily_list 测试日报
learn   培训计划
"""
def testversion(request):
    return render(request,"test/test_version.html")

def test_bench(request):
    data = {}
    if request.method == "POST":
        if len(request.POST.get('content')) > 5 and  len(request.POST.get('timer')) > 5: # 获取数据
            content = request.POST.get('content')
            content = content.replace("\r\n", "<br/>")
            task = request.POST.get('tasktype')
            timer = request.POST.get('timer')
            new_testbench = models.TestBench()
            try:
                new_testbench.createuser = request.session['user_name']  # 当前用户名
            except:
                new_testbench.createuser = 'test'

            new_testbench.task = task
            new_testbench.content = content
            new_testbench.plantime = timer
            new_testbench.save()

            return HttpResponseRedirect('/testbench/')

        message = "请检查输入项[内容][时间]是否正确！"
        testbench_list = models.TestBench.objects.filter(is_activate=True)
        data['rows1'] = testbench_list
        data['message'] = message
        return render(request, 'test/test_bench.html', data)

    # 非post
    message = "请在下表框中填入你的问题！"
    testbench_list = models.TestBench.objects.filter(is_activate=True)
    data['rows1'] = testbench_list
    data['message'] = message
    # print(testbench_list)

    return render(request, 'test/test_bench.html', data)

#日报列表
@check_login
def daily_list(request):
    #判断登录者身份
    if request.method == "POST":
        dailycreate_form = forms.DailyForm(request.POST)
        if dailycreate_form.is_valid():
            if len(request.POST.get('task_1')) >=5 :
                new_dailyreport = models.DailyReport()
                task1 = request.POST.get('task_1')
                task1 = task1.replace("\r\n", "<br/>")
                task2 = request.POST.get('task_2')
                task2 = task2.replace("\r\n", "<br/>")
                task3 = request.POST.get('task_3')
                task3 = task3.replace("\r\n", "<br/>")
                task4 = request.POST.get('task_4')
                task4 = task4.replace("\r\n", "<br/>")
                # task5 = request.POST.get('task_5')
                # task5 = task5.replace("\r\n", "<br/>")
                # task6 = request.POST.get('task_6')
                # task6 = task6.replace("\r\n", "<br/>")

                new_dailyreport.task_1 = task1
                new_dailyreport.task_2 = task2
                new_dailyreport.task_3 = task3
                new_dailyreport.task_4 = task4
                # new_dailyreport.task_5 = task5
                # new_dailyreport.task_6 = task6
                try:
                    new_dailyreport.createuser =  request.session['user_name'] #当前用户名
                except:
                    new_dailyreport.createuser = 'test'

                new_dailyreport.comment = ''
                new_dailyreport.has_confirmed = False
                new_dailyreport.save()
                message = '日报填写完成，2秒后自动太转到日报结果页！'
                return render(request, 'test/daily_confirm.html', locals())
    else:
        if request.session['user_id'] == 1:
            dailylist = models.DailyReport.objects.filter(is_activate=True)
        else:
            dailylist = models.DailyReport.objects.filter(createuser=request.session['user_name'])
        data = {}
        message = '请检查填写信息'
        dailycreate_form = forms.DailyForm()
        data['rows'] = dailylist
        data['rows_done'] = dailylist.filter(has_confirmed=True)
        data['rows_on'] = dailylist.filter(has_confirmed=False)
        try:
            data['done_rate'] = '{:.0f}%'.format((dailylist.filter(has_confirmed=True).count()/dailylist.count())*100)
        except:
            data['done_rate'] = 0
        data["dailycreate_form"] = dailycreate_form
        return render(request, 'test/daily_list.html', data)


@csrf_exempt
def taskupdate(request):
    if request.method == 'POST':
        pk = request.POST.get('q')
        try:
            a = models.DailyReport.objects.get(id=pk)
            a.has_confirmed = 1
            a.save()
        except:
            pass

    return redirect("/dailylist/")

#********************************************************Redis缓存************************************************************************************
"""
**********获取不常更新数据**********
type_count 分类与数目条数
tag_count   标签与数目条数
tongji 站点统计条数

"""

#存入redis缓存
def get_count_cache():
    key = 'blog_count1'
    if cache.has_key(key):
        data = cache.get(key)
        # print('数据存在',get_time())
    else:
        # 不存在，则获取数据，并写入缓存
        # print('数据不存在',get_time())
        data = get_blog_count()

        # 写入缓存
        cache.set(key, data, 600000)
        # cache.set(key, data, 5)
    return data


def get_blog_count():
    posts = models.Blog.objects.filter(is_activate=True)
    #获取分类count
    blog_type = models.Category.objects.all()
    type_dic = {}
    for type1 in blog_type:
        s = type1.name
        type_dic[s] = posts.filter(category_id=type1.id).count()
    type_count = type_dic


    #获取标签count
    tags = models.Tag.objects.all()
    tags_dic = {}
    for tag in tags:
        s = tag.name
        tags_dic[s] = posts.filter(tage=s).count()
    tag_count = tags_dic

    #获取评论comment
    comments = models.Comment.objects.all()
    comment_dic = {}
    for tag in comments:
        s = tag.blog_id
        comment_dic[s] = comments.filter(blog_id=s).count()
    comment_count = comment_dic


    #站点数据 总数合计
    tongji = {}
    tongji_blog = models.Blog.objects.filter(is_activate=1).count()
    tongji['tongji_blog'] = tongji_blog
    tongji_tag = models.Tag.objects.all().count()
    tongji['tongji_tag'] = tongji_tag
    tongji_weibo = models.Note.objects.filter(is_activate=1).count()
    tongji['tongji_weibo'] = tongji_weibo
    tongji_site = models.Site.objects.filter(is_activate=1).count()
    tongji['tongji_site'] = tongji_site
    tongji_user = models.User.objects.all().count()
    tongji['tongji_user'] = tongji_user
    tongji_timeline = models.TimeLine.objects.filter(is_activate=1).count()
    tongji['tongji_timeline'] = tongji_timeline
    tongji_comment = models.Comment.objects.filter(is_activate=1).count()
    tongji['tongji_comment'] = tongji_comment


    data = [type_count,tag_count,tongji,comment_count]
    # print("这是在读取数据")

    return data