import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.users.models import User
import re
from django.contrib.auth import login


# Create your views here.

class UsernameCountView(View):
    """此处用来判断用户名是否注册"""

    def get(self, request, username):
        """
        :param request:  请求对象
        :param username:  请求参数
        :return: JSON类型参数数据
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class MobileCountView(View):
    """此处用来判断手机号是否注册"""

    def get(self, request, mobile):
        """
        :param request:  请求对象
        :param mobile:  请求参数
        :return: JSON类型参数数据
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class RegisterView(View):
    def post(self, request):
        """
        :param request:  请求对象
        :return:  注册结果
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        json_dict = json.loads(json_str)

        # 提取参数

        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        sms_code = json_dict.get('sms_code')

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数!'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})

        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '注册成功'})
