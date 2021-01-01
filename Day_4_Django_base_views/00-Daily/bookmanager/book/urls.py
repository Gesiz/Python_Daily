from django.urls import path, register_converter
from book.views import index, book, login, weibo,\
    get_session,get_cookie,get_redirct,get_method,get_header,\
    set_session,set_cookie,res_json,http_res

from book.converters import MobileConverters

register_converter(MobileConverters, 'phone')
urlpatterns = [
    path('index/', index),
    path('<cat_id>/<phone:detail_id>/', book),
    path('login/', login),
    path('weibo/', weibo),
]
