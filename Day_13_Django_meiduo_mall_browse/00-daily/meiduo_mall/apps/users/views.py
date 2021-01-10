from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.views import View
from apps.users.models import User
from django.http import JsonResponse


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


import json


class RegisterView(View):
    """用户注册"""

    def post(self, request):
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        sms_code = json_dict.get('sms_code')

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})

        login(request, user)
        return JsonResponse({'code': 0, 'errmsg': '注册成功!'})


class LoginView(View):
    """用户名登录"""

    def post(self, request):
        # 1.接收参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')

        import re
        if re.match('^1[3-9]\d{9}$', username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'

        # 2.校验(整体 + 单个)
        if not all([username, password]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})

        # 3.验证是否能够登录
        user = authenticate(username=username,
                            password=password)

        # 判断是否为空,如果为空,返回
        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': '用户名或者密码错误'})

        # 4.状态保持
        login(request, user)

        # 5.判断是否记住用户
        if remembered != True:
            # 7.如果没有记住: 关闭立刻失效
            request.session.set_expiry(0)
        else:
            # 6.如果记住:  设置为两周有效
            request.session.set_expiry(None)

        # 8.返回json
        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok'})
        # 注册时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response


class LogoutView(View):
    """退出登录"""

    def delete(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到登录页
        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok'})
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response


from utils.views import LoginRequiredJSONMixin


class UserInfoView(LoginRequiredJSONMixin, View):
    """用户中心"""

    class UserInfoView(LoginRequiredJSONMixin, View):
        """用户中心"""

        def get(self, request):
            """提供个人信息界面"""

            # 获取界面需要的数据,进行拼接
            info_data = {
                'username': request.user.username,
                'mobile': request.user.mobile,
                'email': request.user.email,
                'email_active': request.user.email_active
            }

            # 返回响应
            return JsonResponse({'code': 0,
                                 'errmsg': 'ok',
                                 'info_data': info_data})