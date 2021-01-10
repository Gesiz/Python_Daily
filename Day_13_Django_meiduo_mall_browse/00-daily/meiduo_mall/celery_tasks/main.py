from celery import Celery

# 1 创建 celery 实例
# celery 的第一个参数 main 就是一个名字
# 这个名字 一般我们使用 任务的名字



import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")
app = Celery(main='meiduo')

# 2 加载celery的配置信息

# 配置信息中指定了我们的消息队列
# 我们选择redis作为消息队列


app.config_from_object('celery_tasks.config')

# 补充任务包的任务需要celery调用自检检查函数
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
