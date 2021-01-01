from django.shortcuts import render
from django.http import HttpResponse, request


# Create your views here.


def index(request):
    # return HttpResponse('this is page')
    data = {
        'key': '元旦快乐',
    }
    return render(request, 'book/index.html', data)
