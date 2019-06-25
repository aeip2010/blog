from django import forms
# from captcha.fields import CaptchaField
from .models import Blog,Comment
from DjangoUeditor.forms import UEditorField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'请输入用户密码'}))
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'请输入用户邮箱'}))
    # captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    # captcha = CaptchaField(label='验证码')


class SiteForm(forms.Form):
    sitename = forms.CharField(label="网站名称", max_length=128, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    sitelink = forms.CharField(label="网站链接", max_length=128, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    sitenote = forms.CharField(label="备注", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class BlogForm(forms.Form):
    title =  forms.CharField( max_length=128, required=True,widget=forms.TextInput(attrs={'class': 'form-control col-md-6','placeholder':'请输入文章标题','name':'title'}))
    tage = forms.CharField(max_length=128, required=True,widget=forms.TextInput(attrs={'class': 'form-control col-md-6','placeholder':'请输入标签，多标签逗号分隔','name':'tage'}))

    content = UEditorField('',width=1000, height=500, toolbars="full",  imagePath="uploads/blog/images/",filePath="uploads/blog/files/",
                           upload_settings={"imageMaxSize":12040000},settings={})

class DailyForm(forms.Form):
    task_1 = forms.CharField(label="任务1",required=True,widget=forms.Textarea(attrs={"class":"form-control",'rows':'3','placeholder':'[xxxx]:\n1.xxx\n2.xxxx\n3.xxx'}))
    task_2 = forms.CharField(label="任务2",required=True,widget=forms.Textarea(attrs={"class":"form-control",'rows':'3','placeholder':'[xxxx]:\n1.xxx\n2.xxxx\n3.xxx'}))
    task_3 = forms.CharField(label="任务3",required=True,widget=forms.Textarea(attrs={"class":"form-control",'rows':'3','placeholder':'[xxxx]:\n1.xxx\n2.xxxx\n3.xxx'}))
    task_4 = forms.CharField(label="任务4",required=False,widget=forms.Textarea(attrs={"class":"form-control",'rows':'3','placeholder':'[xxxx]:\n1.xxx\n2.xxxx\n3.xxx'}))



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content', 'blog']