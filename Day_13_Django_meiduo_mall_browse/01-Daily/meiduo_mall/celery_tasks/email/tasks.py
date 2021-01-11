from django.core.mail import send_mail
from celery_tasks.main import app


@app.task
def celery_send_email(email, html_message):
    subject = '麋鹿'
    message = '我是赵子旭 我可太帅了啊 我怎么能这么帅啊 ！！！！！！！！！！！！！！！！！！！！！！！！！！！'
    from_email = '美多商城<qi_rui_hua@163.com>'
    recipient_list = [email]
    send_mail(subject,
              message,
              from_email,
              html_message=html_message,
              recipient_list=recipient_list)
