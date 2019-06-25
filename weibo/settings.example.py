import os
import pymysql         # 一定要添加这两行！通过pip install pymysql！
pymysql.install_as_MySQLdb()
import datetime

# time
ctime = datetime.datetime.now().strftime('%Y-%m-%d')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_%=9s_1dt)^y2i1ph(+j900()zp^l1f=4_t#hj=)2!^r#@bs7-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    # 'captcha',
    'DjangoUeditor',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware', # 注意位置，在前
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', # 注意位置，在后
]

ROOT_URLCONF = 'weibo.urls'


#缓存系统
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'weibo_cache',
#         'TIMEOUT': 600, # 默认的缓存有效时间,以秒计. 默认值是 300 秒(五分钟).
#         'OPTIONS': {
#             'MAX_ENTRIES': 1000 # 缓存的最大条目数(超出该数旧的缓存会被清除,默认值是 300).
#         },
#     }
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': '127.0.0.1:6379',
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     },
# }



#美化后台
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ]
        },
    },
]

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

WSGI_APPLICATION = 'weibo.wsgi.application'


#mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testblog',
        'HOST': '127.0.0.1',
        'USER': 'xxxx',
        'PASSWORD': 'xxxxx',
        'PORT': '3306',
    }
}

#发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxxxx'
EMAIL_HOST_PASSWORD = 'xxxx'
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators


#celery setting
# import djcelery
# djcelery.setup_loader()
# BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'  # 127.0.0.1即为rabbitmq-server所在服务器ip地址
# BROKER_POOL_LIMIT = 0
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
# CELERY_TIMEZONE='Asia/Shanghai'


# 注册有效期天数
CONFIRM_DAYS = 7

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#缓存有效期
# SESSION_COOKIE_AGE=60*60 #30分钟。
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False  #会话cookie可以在用户浏览器中保持有效期。True：关闭浏览器，则Cookie失效。
# SESSION_COOKIE_NAME = bamboo_blog #cookie中保存session的名称

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#
LOGIN_URL = '/login/'

STATIC_URL = '/static/'
LOG_DIR = os.path.join(BASE_DIR, 'logs/tongji.log')

#定义媒体路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'media'),
    os.path.join(BASE_DIR,'static')

]
#自定义全局变量
#blog翻页配置
BLOG_HOME_NUMBER = 10
BLOG_WEIBO_NUMBER = 20


#日志配置 打印到控制台
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
#编辑器设置
# UEDITOR_SETTINGS={
#                 "toolbars":{           #定义多个工具栏显示的按钮，允行定义多个
#                     "name1":[[ 'source', '|','bold', 'italic', 'underline']],
#                     "name2":[]
#                 },
#                 "images_upload":{
#                     "allow_type":"jpg",    #定义允许的上传的图片类型
#                     "max_size":"2222kb"        #定义允许上传的图片大小，0代表不限制
#                 },
#                 "files_upload":{
#                      "allow_type":"zip,rar",   #定义允许的上传的文件类型
#                      "max_size":"2222kb"       #定义允许上传的文件大小，0代表不限制
#                  },
#                 "image_manager":{
#                      "location":""         #图片管理器的位置,如果没有指定，默认跟图片路径上传一样
#                 },
#             }
#日志保存
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/%s.log'%ctime),   #定义位置
            'formatter': 'standard',    #定义格式
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],   #定义应用的容器
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}