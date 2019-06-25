# Register your models here.
from django.contrib import admin
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加包


@admin.register(models.Blog)
#后台博客内容展示、过滤个性化
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title','tage')
    list_display = ('title', 'category','author','update_time')
    list_filter = ('category','author')
    # 分页，每页显示条数
    list_per_page = 10

# admin.site.register(models.Blog, BlogAdmin)

@admin.register(models.Tag)
#后台博客内容展示、过滤个性化
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'id')

    # 分页，每页显示条数
    list_per_page = 30

@admin.register(models.Category)
#后台博客内容展示、过滤个性化
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'number')

    # 分页，每页显示条数
    list_per_page = 30


@admin.register(models.SiteCategory)
#后台博客内容展示、过滤个性化
class SiteCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'number')

    # 分页，每页显示条数
    list_per_page = 10

@admin.register(models.User)
#用户后台内容展示个性化
class UserAdmin(admin.ModelAdmin):
    search_fields = ('name','email')
    list_display = ('name', 'email','from_ip','update_time')


@admin.register(models.TimeLine)
#大事件后台内容展示个性化
class TimeLineAdmin(admin.ModelAdmin):
    list_display = ('content', 'keyword','city','linetime')
    search_fields = ('keyword', 'content','city')
    list_filter = ('year', )
    # 分页，每页显示条数
    list_per_page = 10
    # 分页，显示全部（真实数据<该值时，才会有显示全部）
    list_max_show_all = 200
    # 分页插件
    paginator = Paginator


@admin.register(models.City)
#配置展示个性化
class CityAdmin(admin.ModelAdmin):
    search_fields = ('type','content')
    list_display = ( 'content','name','update_time','is_activate')
    list_filter = ('content', )



@admin.register(models.TestBench)
#配置测试工作台
class TestBenchAdmin(admin.ModelAdmin):
    search_fields = ('task',)
    list_display = ( 'task','c_time','has_confirmed')



admin.site.register(models.ConfirmString)  #后台增加管理窗口



