import random

from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from django.views import View
from django.http import JsonResponse, HttpResponse


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpeg
        """
        # 生成图片验证码
        text, image = captcha.generate_captcha()

        # 保存图片验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 响应图片验证码
        return HttpResponse(image, content_type='image/jpeg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收通过GET方式传过来得数据
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('image_code_id')

        if not all([image_code_client, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        redis_conn = get_redis_connection('code')

        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})

        image_code_server = redis_conn.get('img_%s' % uuid)

        if image_code_server is None:
            # 图形验证码过期或者不存在
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'})

        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            pass
        image_code_server = image_code_server.decode()  # bytes转字符串

        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return JsonResponse({'code': 400, 'errmsg': '输入图形验证码有误'})

        sms_code = random.randint(100000, 999999)

        redis_conn.setex('sms_%s' % mobile, 300, sms_code)

        # 创建Redis管道
        pl = redis_conn.pipeline()
        # 将Redis请求添加到队列
        pl.setex('sms_%s' % mobile, 300, sms_code)
        pl.setex('send_flag_%s' % mobile, 60, 1)
        # 执行请求
        pl.execute()
        from celery_tasks.sms.tasks import celery_send_sms_code
        celery_send_sms_code.delay(mobile, sms_code)

        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})
