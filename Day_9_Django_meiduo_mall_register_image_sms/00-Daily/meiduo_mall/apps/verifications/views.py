from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from django.http import HttpResponse, JsonResponse
import random, json
from ronglian_sms_sdk import SmsSDK


# Create your views here.
class ImageCodeView(View):
    def get(self, request, uuid):
        # 生成验证码
        text, image = captcha.generate_captcha()
        # 保存图片 验证码

        redis_cli = get_redis_connection('code')
        redis_cli.setex(f'image_{uuid}', 300, text)
        return HttpResponse(image, content_type='image/jpeg')


class SMSCodeView(View):
    def get(self, request, mobile):
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([image_code_client, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        redis_cli = get_redis_connection('code')

        send_flag = redis_cli.get(f'send_flag_{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '操作过于频繁'})

        image_code_server = redis_cli.get(f'image_{uuid}')
        if image_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'})
        try:
            redis_cli.delete(f'image_{uuid}')
        except Exception as e:
            pass

        image_code_server = image_code_server.decode()

        if image_code_server.lower() != image_code_client.lower():
            return JsonResponse({'code': 400, 'errmsg': '输入图片验证码有误'})

        sms_code = random.randint(100000, 999999)

        p1 = redis_cli.pipeline()
        p1.setex(f'sms_{mobile}', 300, sms_code)
        p1.setex(f'send_flag_{mobile}', 60, 1)
        p1.execute()

        accId = '8aaf0708762cb1cf0176c60392973587'
        accToken = 'a099e3b6a8a14e09bae6d133051decb9'
        appId = '8aaf0708762cb1cf0176c603936b358e'
        sdk = SmsSDK(accId, accToken, appId)

        tid = '1'
        mobile = f'{mobile}'
        datas = (sms_code, 2)
        resp = sdk.sendMessage(tid, mobile, datas)
        data = json.loads(resp)

        if data.get('statusCode') == '000000':
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            return JsonResponse({'code': 400, 'errmsg': '稍后再试'})
