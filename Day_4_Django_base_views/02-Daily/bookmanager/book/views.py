from django.shortcuts import render
from django.http import HttpResponse, request
from book.models import BookInfo, PeopleInfo


# Create your views here.


def index(request):
    # return HttpResponse('this is page')
    data = {
        'key': '元旦快乐',
    }
    # 查询编号为 1 的图书
    BookInfo.objects.get(id__exact=2)
    print(f"查询编号为1的图书是   {BookInfo.objects.filter(id=1)}")

    print(f"查询书名中包含湖的图书 {BookInfo.objects.filter(name__contains='湖')}")

    print(f"查询书名以部结尾的图书 {BookInfo.objects.filter(name__endswith='部')}")

    print(f"查询书名为空的图书    {BookInfo.objects.filter(name__isnull=True)}")

    print(f"查询编号1or3or5的图书{BookInfo.objects.filter(id__in=[1, 3, 5])}")

    print(f"查询编号大于3的图书   {BookInfo.objects.filter(id__gt=3)}")

    print(f"查询1980之后发表的图书 {BookInfo.objects.filter(pub_date__year=1986)}")

    print(f"查询1990年1月1日后发表的图书 {BookInfo.objects.filter(pub_date__gt='1990-1-1')}")

    print(f"查询编号不等于3的图书     {BookInfo.objects.exclude(id=3)}")

    from django.db.models import Q, F
    print(f"查询阅读量大于等于评论量的书 {BookInfo.objects.filter(readcount__gte=F('commentcount'))}")

    print(f"查询编号大于2并且阅读量大于20的图书 {BookInfo.objects.filter(id__gt=2).filter(readcount__gt=20)}")
    print(f"查询编号大于2并且阅读量大于20的图书 {BookInfo.objects.filter(id__gt=2, readcount__gt=20)}")
    print(f"查询编号大于2并且阅读量大于20的图书 {BookInfo.objects.filter(Q(id__gt=2) & Q(readcount__gt=20))}")
    print(f"查询编号大于2或阅读量大于20的图书 {BookInfo.objects.filter(Q(id__gt=2) | Q(readcount__gt=20))}")
    print(f"查询编号不等于3的图书     {BookInfo.objects.filter(~Q(id=3))}")

    print(f"使用order by readcount 进行排序 {BookInfo.objects.order_by('readcount')}")

    print(f"使用order by id 进行排序 {BookInfo.objects.order_by('id')}")

    print(f'查询书籍 id=1 得所有人物信息 {BookInfo.objects.get(id=1).peopleinfo_set.all()}')

    print(f'查询人物 id=1 得书籍信息 {PeopleInfo.objects.get(id=1).book.name}')
    print(f'查询人物 id=1 得书籍信息 {PeopleInfo.objects.get(id=1).book_id}')

    print(f'查询图书 要求图书人物为 郭靖 {BookInfo.objects.filter(peopleinfo__name="郭靖")}')

    print(f'查询图书 要求图书的任务描述包含八 {BookInfo.objects.filter(peopleinfo__description__contains="八")}')
    books = BookInfo.objects.filter(peopleinfo__description__contains="八")
    print([book.id for book in books])

    return render(request, 'book/index.html', data)
