from django.conf.urls import url,handler404,handler500
from django.contrib import admin
from blog import views
from django.conf.urls import include
from django.conf import  settings
import os
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin"),
    url(r'^$',views.index,name="home"),
    url(r'^blog/', views.blog,name="blog"),
    url(r'^index/', views.index,name="home"),
    url(r'^login/', views.login,name="loging"),
    url(r'^register/', views.register,name="register"),
    url(r'^logout/', views.logout,name="logout"),
    url(r'^confirm/$', views.user_confirm),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^archives/$',views.archives, name = 'archives'),
    url(r'^search/$',views.blog_search, name = 'search'),
    url(r'^tag=(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^type=(?P<type>\w+)/$', views.search_type, name='search_type'),
    url(r'^name=(?P<name>\w+)/$', views.search_name, name='search_name'),
    url(r'^newpost/$', views.post_new, name='post_new'),
    url(r'^postedit/postid=(?P<postid>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^weibo/$', views.weibo,name="weibo"),
    url(r'^newweibo/$', views.new_weibo,name="new_weibo"),
    url(r'^site/$', views.site,name="site"),
    url(r'^siteedit/site_id=(?P<siteid>\d+)/$', views.site_edit, name='site_edit'),
    url(r'^timeline/$', views.timeline,name="timeline"),
    url(r'^searchtimeline/$',views.timeline_search, name = 'timeline_search'),
    url(r'^searchweibo/$',views.weibo_search, name = 'weibo_search'),
    url(r'^add_comment/$', views.AddCommentView, name='add_comment'),
    url(r'^testversion/$',views.testversion, name = 'testversion'),
    url(r'^testbench/$', views.test_bench, name="test_bench"),
    url(r'^dailylist/$', views.daily_list,name="daily_list"),
    url(r'^about/$', views.about, name="about_me"),
    url(r'^weibosearch/$', views.weibo_search_ajax, name='weibo_search_ajax'),
    url(r'^timesearch/$', views.timeline_search_ajax, name='timeline_search_ajax'),
    url(r'^update/', views.taskupdate, name="taskupdate"),
    url(r'^version/', views.version, name="version"),
]

if settings.DEBUG:
    media_root = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=media_root)

