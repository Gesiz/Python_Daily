from django.urls import path, register_converter
from book.views import index, book, login, weibo, \
    get_session, get_cookie, get_redirct, get_method, get_header, \
    set_session, set_cookie, res_json, http_res

from book.converters import MobileConverters

register_converter(MobileConverters, 'phone')
urlpatterns = [
    path('index/', index),
    path('<cat_id>/<phone:detail_id>/', book),
    path('login/', login),
    path('weibo/', weibo),
    path('header/', get_header),
    path('method/', get_method),
    path('httpres/', http_res),
    path('resjson/', res_json),
    path('redirect/', get_redirct),
    path('cookie/', set_cookie),
    path('getcookie/', get_cookie),
    path('a/', set_session),
    path('b/', get_session),
]
