from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.http.response import JsonResponse
from django.contrib.auth import login
import json, re


class UsernameCountView(View):
    # usernames/<username>/count
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class RegisterView(View):

    def post(self, request):
        body = request.body
        body_str = body.decode()
        data = json.loads(body_str)

        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        allow = data.get('allow')

        if all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        if not re.match('[a-zA-Z0-9]{5,29}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足条件'})

        if not re.match('[a-zA-Z0-9]{8,20}', password):
            return JsonResponse({'code': 400, 'errmsg': '密码不满足条件'})

        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不一致'})

        if not re.match(r'1[3-9]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': '电话号码格式不正确'})

        if not allow:
            return JsonResponse({'code': 400, 'errmsg': '用户协议格式不正确'})

        try:
            user = User.objects.create_user(username, password, mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})

        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '注册成功'})
