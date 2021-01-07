from django.shortcuts import render
from apps.users.models import User
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django_redis import get_redis_connection
import json, re


# Create your views here.

class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class RegisterView(View):

    def post(self, request):
        json_bytes = request.body
        json_str = json_bytes.decode()
        json_dict = json.loads(json_str)
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

        redis_cli = get_redis_connection('code')
        sms_code_server = redis_cli.get(f'sms_{mobile}')

        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
            # 对比用户输入的和服务端存储的短信验证码是否一致
        if sms_code != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        # 判断是否勾选用户协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                mobile=mobile,
            )
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})

        login(request, user)
        return JsonResponse({'code': 0, 'errmsg': '注册成功!'})


class LoginView(View):

    def post(self, request):
        idict = json.loads(request.body.decode())
        username = idict.get('username')
        password = idict.get('password')
        remembered = idict.get('remembered')

        if not all([username, password]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})

        if re.match('^1[3-9]\d{9}$', username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'

        user = authenticate(username=username,
                            password=password)

        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': '用户名或者密码错误'})

        login(request, user)
        if not remembered:
            # 7.如果没有记住: 关闭立刻失效
            request.session.set_expiry(0)
        else:
            # 6.如果记住:  设置为两周有效
            request.session.set_expiry(None)

            # 8.返回json
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=15 * 24 * 3600)
        return response


class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = JsonResponse({'code': 400, 'errmsg': 'ok'})
        response.delete_cookie('username')
        return response


from utils.views import LoginRequiredJSONMixin


class UserInfoView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        user = request.user
        user_info = {
            'username': user.username,
            'mobile': user.mobile,
            'email': user.email,
            'email_activate': False,  # 明天才讲 email_active 先给一个固定值
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': user_info})
