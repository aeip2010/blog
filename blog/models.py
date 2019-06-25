from django.db import models
from django.utils import timezone
from DjangoUeditor.models import UEditorField


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    has_confirmed = models.BooleanField(default=False)
    from_ip = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "用户"
        verbose_name_plural = "用户"

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.CASCADE,)
    has_confirmed = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)


    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "确认码"
        verbose_name_plural = "确认码"


#博客系统 分类 标签 博客内容 评论 点击数
class Category(models.Model):
    """
    博客分类
    """
    name = models.CharField(verbose_name='博客类别', max_length=20)
    number = models.IntegerField(verbose_name='分类数目', default=1)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField(verbose_name='博客标签', max_length=20)

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=100,unique=True)
    # content = models.TextField(verbose_name='正文', default='')
    content = UEditorField(u'内容', width=800, height=300, toolbars="full", imagePath="uploads/blog/images/",
                           filePath="uploads/blog/files/", blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    # click_nums = models.IntegerField(verbose_name='点击量', default=0)
    category = models.ForeignKey(Category, verbose_name='博客类别',on_delete=models.CASCADE)
    # category = models.CharField(verbose_name='博客类别', max_length=20)
    # tag = models.ManyToManyField(Tag, verbose_name='博客标签')
    tage = models.CharField(max_length=50, blank=True)  # 博客标签
    tags = models.ManyToManyField(Tag, blank=True)  # 多对多字段，绑定下面的Tag模型
    author = models.CharField(max_length=256)
    is_activate = models.BooleanField(default=True)

    # 阅读数（>0的数）
    views = models.PositiveIntegerField(default=0)

    # 增加阅读数的方法
    def increase_views(self):
        self.views += 1
        # update_fields 只更新数据库中的views
        self.save(update_fields=['views'])

    class Meta:
        ordering = ["-create_time"]  # 按照事件倒序排列
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    博客评论
    """
    name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name='内容', max_length=300)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(Blog, verbose_name='博客',on_delete=models.CASCADE)
    # ip = models.CharField(max_length=256)
    is_activate = models.BooleanField(default=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:15]

class Counts(models.Model):
    """
    统计博客、分类和标签的数目
    """
    blog_nums = models.IntegerField(verbose_name='博客数目', default=0)
    category_nums = models.IntegerField(verbose_name='分类数目', default=0)
    tag_nums = models.IntegerField(verbose_name='标签数目', default=0)
    visit_nums = models.IntegerField(verbose_name='网站访问量', default=0)


    class Meta:
        verbose_name = '数目统计'
        verbose_name_plural = verbose_name



class Search_submit_record(models.Model):
    '''
    统计
    # '''
    # range = (
    #     ('blog', "博客"),
    #     ('weibo', "微博"),
    #     ('timeline', "时间线"),
    # )
    #
    # type = (
    #     ('search', "搜索"),
    #     ('submit', "提交"),
    # )
    profile_no = models.CharField(max_length=256)
    ip = models.CharField(max_length=256)
    search_time = models.DateTimeField(auto_now_add=True)
    search_range = models.CharField(max_length=32, default="")
    search_type = models.CharField(max_length=32, default="")
    content = models.CharField(max_length=256)
    current_url = models.CharField(max_length=256)
    is_activate = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "统计"   #定义后台名称
        verbose_name_plural = "统计"


class Note(models.Model):
    '''
    微博碎语
    '''
    content = models.CharField(max_length=256)
    createuser = models.CharField(max_length=256)
    comment = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    ip =  models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "微博"   #定义后台名称
        verbose_name_plural = "微博"


class Site(models.Model):
    """
    站点导航页面
    """
    sitetype =  models.CharField(max_length=256)
    sitename = models.CharField(max_length=256)
    sitelink = models.CharField(max_length=256)
    sitenote = models.CharField(max_length=256)
    createuser = models.CharField(max_length=256)
    createtime = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)


    class Meta:
        ordering = ["-createtime"]  # 按照事件倒序排列
        verbose_name = "站点导航"  # 定义后台名称
        verbose_name_plural = "站点导航"

#导航栏 分类
class SiteCategory(models.Model):
    """
    分类
    """
    name = models.CharField(verbose_name='站点类别', max_length=20)
    number = models.IntegerField(verbose_name='分类数目', default=1)

    class Meta:
        verbose_name = '站点类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TimeLine(models.Model):
    '''
    时间线
    '''
    year = models.CharField(max_length=256)
    month = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    createuser = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    has_activate = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now_add=True)
    landmark = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    linetime = models.DateTimeField()
    keyword = models.CharField(max_length=256)
    type =  models.CharField(max_length=256)


    class Meta:
        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "大事件"   #定义后台名称
        verbose_name_plural = "大事件"

    def __str__(self):
        return self.content


#城市 地标
class City(models.Model):

    type = (
        ('city', "城市"),
        ('tag', "地标"),
    )
    name = models.CharField(max_length=128, unique=True)
    content = models.CharField(max_length=32, choices=type, default="城市")
    has_confirmed = models.BooleanField(default=False)
    plantime =  models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_time"] #按照事件倒序排列
        verbose_name = "城市地标"
        verbose_name_plural = "城市地标"


class TestBench(models.Model):
    tasktype = (
        ('miss', "漏测大全"),
        ('bug', "线上反馈"),
        ('research', "成果展示"),
    )
    content = models.TextField(max_length=999,default="--")
    task = models.CharField(max_length=32,choices=tasktype, default="bug")
    createuser = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    has_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-c_time"]  # 按照事件倒序排列
        verbose_name = "测试工作台"  # 定义后台名称
        verbose_name_plural = "测试工作台"

    def __str__(self):
        return self.content


class DailyReport(models.Model):
    task_1 = models.CharField(max_length=256)
    task_2 = models.CharField(max_length=256)
    task_3 = models.CharField(max_length=256)
    task_4 = models.CharField(max_length=256)
    createuser = models.CharField(max_length=256)
    comment = models.CharField(max_length=256)
    has_confirmed = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)

    class Meta:
        verbose_name = "日报"
        verbose_name_plural = "日报"

    def __str__(self):
        return self.c_time
