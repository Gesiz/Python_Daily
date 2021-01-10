from django.shortcuts import render

# Create your views here.
from django.views import View
from django.contrib.auth import login, authenticate, logout
from apps.users.models import User
from django.http import JsonResponse
import json, re

from utils.views import LoginRequiredJSONMixin


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
        :param mobile:
        :param request: 请求对象
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    """用户注册"""

    def post(self, request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """

        # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        sms_code = json_dict.get('sms_code')

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

        # 2.校验(整体 + 单个)
        if not all([username, password]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})
        # 判断多用户登录
        import re
        if re.match(r'^1[3-9]\d{9}$', username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'

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


class UserInfoView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
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


class EmailView(View):
    """添加邮箱"""

    def put(self, request):
        """实现添加邮箱逻辑"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 校验参数
        if not email:
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数email有误'})
        # 赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:

            return JsonResponse({'code': 0, 'errmsg': '添加邮箱失败'})

        # 异步发送验证邮件
        from celery_tasks.email.tasks import send_verify_email
        from apps.users.utils import generate_verify_email_url
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)
        # 响应添加邮箱结果
        return JsonResponse({'code': 0, 'errmsg': '添加邮箱成功'})

class VerifyEmailView(View):
    def put(self, request):
        # - 1.接收 token
        token = request.GET.get('token')

        if not token:
            return JsonResponse({'code': 400, 'errmsg': 'token缺少'})

        # - 2.解密
        from apps.users.utils import check_verify_email_token
        data_dict = check_verify_email_token(token)

        # - 4.去数据库对比 user_id,email
        try:
            user = User.objects.get(pk=data_dict.get('user_id'), email=data_dict.get('email'))
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '参数有误!'})

        # - 5.修改激活状态
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            return JsonResponse({'code': 0, 'errmsg': '激活失败!'})