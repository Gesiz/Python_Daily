from celery_tasks.main import celery_app
from ronglian_sms_sdk import SmsSDK


@celery_app.task
def send_sms_code(mobile, sms_code):
    """
    发送短信异步任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    """
    try:
        accId = '8aaf0708762cb1cf0176c60392973587'
        accToken = 'a099e3b6a8a14e09bae6d133051decb9'
        appId = '8aaf0708762cb1cf0176c603936b358e'
        sdk = SmsSDK(accId, accToken, appId)

        tid = '1'
        mobile = f'{mobile}'
        datas = (sms_code, 2)
        sdk.sendMessage(tid, mobile, datas)
    except Exception as e:
        pass
