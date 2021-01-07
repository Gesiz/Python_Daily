from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from apps.users.models import User


# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8080/success_verify_email.html'


def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = Serializer('ABC', expires_in=3600)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data).decode()
    verify_url = EMAIL_VERIFY_URL + '?token=' + token
    return verify_url





def check_verify_email_token(token):
    """
    验证token并提取user
    :param token: 用户信息签名后的结果
    :return: user, None
    """
    serializer = Serializer('ABC', expires_in=3600)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user
