from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse


# Create your views here.

def index(request):
    data = {
        'show': '圣诞快乐'
    }
    return render(request, 'book/index.html', context=data)
