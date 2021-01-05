from django.shortcuts import render
from libs.captcha.captcha import captcha
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection
import random, json


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpeg
        """
        text, image = captcha.generate_captcha()

        redis_cli = get_redis_connection('code')

        redis_cli.setex(f'img_{uuid}', 300, text)

        return HttpResponse(image, content_type='image/jpeg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 校验参数
        if not all([image_code_client, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        redis_cli = get_redis_connection('code')

        send_flag = redis_cli.get(f'send_flag_{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})
        image_code_server = redis_cli.get(f'img_{uuid}')
        if image_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        try:
            redis_cli.delete(f'img_{uuid}')
        except Exception as e:
            pass
        if image_code_server.decode().lower() != image_code_client.lower():
            return JsonResponse({'code': 400, 'errmsg': '验证码错误'})
        from celery_tasks.sms.tasks import send_sms_code
        sms_code = random.randint(100000, 999999)
        send_sms_code(mobile, sms_code)
        p1 = redis_cli.pipeline()
        p1.setex(f'sms_{mobile}', 300, sms_code)
        p1.setex(f'send_flag_{mobile}', 60, 1)
        p1.execute()

        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})
