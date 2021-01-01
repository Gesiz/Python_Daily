from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from book.models import BookInfo, PeopleInfo
from django.http.response import JsonResponse


# Create your views here.

def index(request):
    return HttpResponse('page')


def book(request, cat_id, detail_id):
    # 关联查询

    # 获取 ID = 2 书籍 中的人物信息
    # 父类会根据外键关系 自动给我们的模型添加属性(字段)
    # book = BookInfo.objects.get(id = cat_id)
    # print(book.peopleinfo_set.all())

    # 获取 ID = 6 人物的 书籍信息
    # people = PeopleInfo.objects.get(id=cat_id)
    # print(people.book,people.book.name,people.book.readcount)

    # 关联过滤查询
    # 查询 人物描述信息中 包含 八 的书籍名
    # print(BookInfo.objects.filter(peopleinfo__description__contains='八'))

    # 查询图书 去要求图书人物为 "郭靖"
    print(BookInfo.objects.get(peopleinfo__name='郭靖'))
    print(BookInfo.objects.get(peopleinfo__name__exact='郭靖'))

    # 查询 图书 阅读量大于 30 的所有人物
    print(PeopleInfo.objects.filter(book__readcount__gt=30))

    # 查询书名为天龙八部的所有人物
    print(PeopleInfo.objects.filter(book__name__exact='天龙八部'))

    # QuerySet 可以被切片

    # 分页
    # 1 首先需要导入
    from django.core.paginator import Paginator
    # 2 查询结果集
    people = PeopleInfo.objects.all().order_by('id')
    # 3 创建分页类
    paginator = Paginator(object_list=people, per_page=2)
    persons = paginator.page(1)
    # 获取分页
    print("获取分页", persons.object_list)
    # 获取分页数量
    print("获取分页数量 ", paginator.num_pages)

    return HttpResponse('book')


def login(request):
    query_string = request.GET
    alist = query_string.getlist('key')

    return HttpResponse(alist)


def weibo(request):
    query_string = request.POST
    alist = query_string.getlist('username')
    b = query_string.get('asdasd', None)
    return HttpResponse(b)


def get_header(request):
    head = request.META
    return HttpResponse(head)


def get_method(request):
    method = request.method
    return HttpResponse(method)


def http_res(request):
    return HttpResponse('123', status=200, content_type='text/html')


def res_json(request):
    idict = {
        'name': 'jack',
        'age': 33
    }
    return JsonResponse(idict, safe=False)


from django.shortcuts import redirect


def get_redirct(request):
    return redirect('https://baidu.com')


def set_cookie(request):
    name = request.GET.get('name')
    response = HttpResponse('set_cookie')
    response.set_cookie(key='name', value=name, max_age=50)
    return response


def get_cookie(request):
    print(request.COOKIES.get('name'))
    return HttpResponse('')


def set_session(request):
    request.session['a'] = "b"
    request.session['c'] = 'd'

    return HttpResponse('')


def get_session(request):
    print(request.session.get('a'))
    return HttpResponse('')
