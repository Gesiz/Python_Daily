from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.http import HttpResponse


# Create your views here.

class UsernameContView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return HttpResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class MobileContView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return HttpResponse({'code': 0, 'errmsg': 'ok', 'count': count})
