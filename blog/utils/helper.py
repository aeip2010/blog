from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加包
from django.conf import settings
from blog import models
import requests
import json


#分页的博客系统
def blog_home(request,objectlist):
    paginator = Paginator(objectlist,settings.BLOG_HOME_NUMBER) #每页显示两个
    page = request.GET.get('page')

    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)

    # print(paginator.count)
    return paginator,post_list

#分页的碎语
def blog_weibo(request,objectlist):
    paginator = Paginator(objectlist,settings.BLOG_WEIBO_NUMBER) #每页显示两个
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.paginator(paginator.num_pages)

    return paginator,post_list
