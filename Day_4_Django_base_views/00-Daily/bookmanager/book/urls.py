from django.urls import path
from book.views import index, book, login, weibo

urlpatterns = [
    path('index/', index),
    path('<cat_id>/<detail_id>', book),
    path('login/', login),
    path('weibo/', weibo),
]
