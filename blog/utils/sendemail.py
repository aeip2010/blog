import os
from django.core.mail import EmailMultiAlternatives
from blog.utils import infor
from django.conf import settings


def send_email(user,email, code,host):
    subject = '来自www.liujiangblog.com的注册确认邮件'
    ip = infor.get_realip()
    text_content = '''感谢注册xxxxx，这里是软件测试者博客和教程站点，专注于Python和Django技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢您的注册</p>
                    <p>用户：{}</p>
                    <p>IP来自于{}</p>
                    <p>你的激活链接：<a href="http://{}/confirm/?code={}" target=blank>点击此处激活</a></p>
                    <p>将于{}天后过期！</p>
                    '''.format(user,ip,host, code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# if __name__ == '__main__':
#     send_email('hu','huadc@huizuche.com','234','www.huizuche.com')