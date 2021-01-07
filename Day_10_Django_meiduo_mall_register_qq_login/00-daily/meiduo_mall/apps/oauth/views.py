from QQLoginTool.QQtool import OAuthQQ
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse


# Create your views here.
class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('缺少code')
        pass

class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 提取code请求参数
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('缺少code')
        # QQ登录参数
        # 我们申请的 客户端id
        QQ_CLIENT_ID = '101474184'
        # 我们申请的 客户端秘钥
        QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # 我们申请时添加的: 登录成功后回调的路径
        QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
        # 创建工具对象
        qq = OAuthQQ(client_id=QQ_CLIENT_ID, client_secret=QQ_CLIENT_SECRET, redirect_uri=QQ_REDIRECT_URI)

        access_token = qq.get_access_token(code)

        openid = qq.get_open_id(access_token)

        from apps.oauth.models import OAuthQQUser
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # code 必须是 300 才会显示页面
            return JsonResponse({'code': 300, 'access_token': access_token})
        else:
            # 如果存在 在此进行自动登录 状态保持操作
            from django.contrib.auth import login
            # login 的第二个参数 时User的实例对象
            login(request, qquser.user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username, max_age=14 * 24 * 3600)
        pass