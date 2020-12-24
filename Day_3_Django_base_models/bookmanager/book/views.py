from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import path
from book.models import BookInfo


# Create your views here.

def index(request):
    return HttpResponse("this is edge")


# 数据库的增删改查 通过SHELL
# python manage.py shell
# 数据库的增加 两种方法
# 1 . 手动调用 save 方法
book = BookInfo()
book.name = 'django'
book.readcount = 10
book.commentcount = 100
book.pub_date = '2002-2-2'
book.save()
# 2 . 通过中间对象创建
BookInfo.objects.create(
    name='python',
    readcount=10,
    commentcount=100,
    pub_date='2002-2-2'
)

# 数据库的修改 两种方式
# 1. 通过 get 获取 book 对象
book = BookInfo.objects.get(id=1)
book.name = '射雕英雄前传'
book.save()

# 2. 通过 get 或 filter 方法中的 update 更新数据
BookInfo.objects.filter(id=1).update(
    name='射雕英雄后传'
)
