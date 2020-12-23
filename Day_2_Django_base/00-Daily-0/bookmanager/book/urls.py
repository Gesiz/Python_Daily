from django.urls import path
from book.views import index

# 子应用中定义子应用的路由

urlpatterns = [
    path('index/', index),
]
