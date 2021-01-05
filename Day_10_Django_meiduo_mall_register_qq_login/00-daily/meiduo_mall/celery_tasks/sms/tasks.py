from celery_tasks.main import app
from ronglian_sms_sdk import SmsSDK


@app.task
def send_sms_code(mobile, sms_code):
    accId = '8aaf0708762cb1cf0176c60392973587'
    accToken = 'a099e3b6a8a14e09bae6d133051decb9'
    appId = '8aaf0708762cb1cf0176c603936b358e'
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'  # 因为是测试用户 所以我们发送短信的模板只能是1
    mobile = f'{mobile}'
    datas = (sms_code, 10)  # 涉及到模板的变量
    # 您的验证码为 1 请于 2 分钟内输入
    resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)
    # return JsonResponse({'code': 0, 'errmsg': '验证码发送成功'})
