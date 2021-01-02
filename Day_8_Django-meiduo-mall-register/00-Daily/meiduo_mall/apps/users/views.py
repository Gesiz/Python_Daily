from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.users.models import User


# Create your views here.

class UsernameCountView(View):
    """此处用来判断用户名是否注册"""

    def get(self, request, username):
        """
        :param request:  请求对象
        :param username:  请求参数
        :return:
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse(request, {'code': 0, 'errmsg': 'ok', 'count': count})
