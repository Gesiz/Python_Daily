"""
Django settings for bookmanager project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# __file__
# 表示文件
# print(__file__)
# /home/ubuntu/Desktop/44/bookmanager/bookmanager/settings.py
#os.path.abspath(__file__)
# print(os.path.abspath(__file__))
# abspath 获取当前文件的绝对路径
# /home/ubuntu/Desktop/44/bookmanager/bookmanager/settings.py

# os.path.dirname  获取文件的目录 路径
# /home/ubuntu/Desktop/44/bookmanager/bookmanager

# /home/ubuntu/Desktop/44/bookmanager



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=bmo=(3c=am5$orxth^7x3)w-+ci45^+zfb8knf)spw^$r$k_('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#You must set settings.ALLOWED_HOSTS if DEBUG is False.
# 当我们把debug 改为 false 之后,其实就是把我们的项目部署到线上了
# 部署到线上的化 我们需要设置 ALLOWED_HOSTS  允许我们以什么样的形式访问
# 默认是 127.0.0.1
# 如果以 域名的形式 就需要 这么写  ALLOWED_HOSTS = ['www.itcast.cn']
# ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS = []


# Application definition
# 我们需要在这里 安装子应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book',  # 相当于告诉了 工程 我们的工程有一个 book子应用
    # 第二种方法
    # 'book.apps.BookConfig'  # book.apps.BookConfig 的本质其实是加载 BookConfig中的 name属性
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmanager.urls'

# 模板设置相关的
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # dirs 告知 django 我们的模板目录在哪里
        # os.path.join(BASE_DIR, 'db.sqlite3')
        # BASE_DIR 就是 外层 bookmanager
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmanager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# sqlite3 小型 关系型数据库  一般在移动端使用的多

# mysql , sql server ,orical 中型数据库

# DB2 大型数据库     银行
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
#语言
LANGUAGE_CODE = 'zh-Hans'#'en-us'
#时区 -- 东八区
TIME_ZONE =  'Asia/Shanghai' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
