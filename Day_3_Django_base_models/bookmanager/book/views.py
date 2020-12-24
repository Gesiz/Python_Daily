from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import path
from book.models import BookInfo, PeopleInfo


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
# 数据库的删除 两种方式
# 1 . 通过 get id 获取对象实例 调用 delete 方法
book = BookInfo.object.get(id=2)
book.delete()
# 方法二 直接删除
BookInfo.objects.filter(id=2).delete()

# 查询所有结果 all() count()
BookInfo.objects.all()
BookInfo.objects.all().count()
BookInfo.objects.count()

# 由于 get 方法只能查询唯一值 当查询结果不存在时 会抛出 DoesNotExist 异常
# 可以使用 try: expect: 进行解决
try:
    BookInfo.objects.get(id=2)
except Exception as e:
    print(e)

# 过滤查询
# 1 filter 过滤多个结果 返回列表
# 2 exclude  相当于 not 排除掉符合条件的剩下结果
# 3 get 获取单一的结果

# 在获取的时候可以通过 特殊运算符 来获取 预期期望 数据
BookInfo.objects.filter(id_exact=1)  # exact 精确的 相当于 id=1
# 若 filter 获取数据为空 则会返回空列表

# 获取 图书 id 为 1 的人的数据
PeopleInfo.objects.get(book_id_id=1)  # 当数据超过一个时会 抛出错误
#  get() returned more than one PeopleInfo -- it returned 5!
PeopleInfo.objects.filter(book_id_id=1)

# 查询书名中包含 湖 的图书
BookInfo.objects.filter(name__contains='湖')
# 查询书名中 以 部 结尾的图书
BookInfo.objects.filter(name__endswith='部')
# 查询 署名为空的图书
BookInfo.objects.filter(name__idnull=True)
# 查询编号为 1，3，5的图书
BookInfo.objects.filter(id__in=[1, 3, 5])
