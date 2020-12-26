from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


# Create your views here.

def index(request):
    return HttpResponse('page')


def book(request):
    return HttpResponse('book')


def login(request):
    return HttpResponse('login')


def weibo(request):
    return HttpResponse('weibo')
