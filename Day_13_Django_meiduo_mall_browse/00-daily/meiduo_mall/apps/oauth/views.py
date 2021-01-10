from QQLoginTool.QQtool import OAuthQQ
from django.contrib.auth import login,logout
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest,JsonResponse
# Create your views here.
# QQ登录参数
# 我们申请的 客户端id
QQ_CLIENT_ID = '101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 我们申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
import json
import re
from apps.users.models import User
from django.db import DatabaseError
from django_redis import get_redis_connection
from .utils import check_access_token

class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('缺少code')
        oauth = OAuthQQ(client_id=QQ_CLIENT_ID, client_secret=QQ_CLIENT_SECRET,
                        redirect_uri=QQ_REDIRECT_URI)
        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            JsonResponse({'code': 400, 'errmsg': 'oauth2.0认证失败, 即获取qq信息失败'})
        from apps.oauth.models import OAuthQQUser
        try:
            # 查看是否有 openid 对应的用户
            oauth_qq = OAuthQQUser.objects.get(openid=openid)

        except OAuthQQUser.DoesNotExist:
            # 如果 openid 没绑定美多商城用户,进入这里:
            # 使用加密类加密 openid
            from apps.oauth.utils import generate_access_token
            access_token = generate_access_token({'openid': openid})
            # 注意: 这里一定不能返回 0 的状态码. 否则不能进行绑定页面
            return JsonResponse({'code': 300, 'errmsg': 'ok', 'access_token': access_token})
            pass
        else:
            # 如果 openid 已绑定美多商城用户
            # 根据 user 外键, 获取对应的 QQ 用户(user)
            user = oauth_qq.user

            # 实现状态保持
            login(request, user)

            # 创建重定向到主页的对象
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})

            # 将用户信息写入到 cookie 中，有效期14天
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

            # 返回响应
            return response

    def post(self,request):
        # 1.接收参数
        data_dict = json.loads(request.body.decode())
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        sms_code_client = data_dict.get('sms_code')
        access_token = data_dict.get('access_token')



        # 3.判断短信验证码是否一致
        # 创建 redis 链接对象:
        redis_conn = get_redis_connection('code')

        # 从 redis 中获取 sms_code 值:
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 判断获取出来的有没有:
        if sms_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400,
                                      'errmsg': '验证码失效'})
        # 如果有, 则进行判断:
        if sms_code_client != sms_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400,
                                      'errmsg': '输入的验证码有误'})

            # 调用我们自定义的函数, 检验传入的 access_token 是否正确:
        # 错误提示放在 sms_code_errmsg 位置
        openid = check_access_token(access_token)
        if not openid:
            return JsonResponse({'code': 400,
                                      'errmsg': '缺少openid'})
        # 4.保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                          'errmsg': '输入的密码不正确'})
        # 5.将用户绑定 openid
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except DatabaseError:
            return JsonResponse({'code': 400,
                                      'errmsg': '往数据库添加数据出错'})
        # 6.实现状态保持
        login(request, user)

        # 7.创建响应对象:
        response = JsonResponse({'code': 0,
                                      'errmsg': 'ok'})

        # 8.登录时用户名写入到 cookie，有效期14天
        response.set_cookie('username',
                            user.username,
                            max_age=3600 * 24 * 14)

        # 9.响应
        return response