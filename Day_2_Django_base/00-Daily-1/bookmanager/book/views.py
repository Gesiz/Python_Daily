from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
# Create your views here.

def index(request):
    data = {
        'value' : '新年快乐呀'
    }
    return render(request,'book/index.html',context=data)
