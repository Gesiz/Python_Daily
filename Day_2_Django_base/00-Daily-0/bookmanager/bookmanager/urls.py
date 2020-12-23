
"""bookmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from book.views import index

# hhtp://127.0.0.1:8000/index/
# 当我们在浏览器中输入一个路由之后 会发送请求
# 发送了请求之后 django会根据路由进行路由 匹配
# 路由匹配的规则是

# 1 http://ip:port/uri/?key=value&key=value ip地址和端口以及查询字符串不进行路由匹配
# 2 路由中path 会顺次urlpatterns 中的每一个元素进行匹配
#       如果uri 和 path 中的第一个参数 不满足 则继续向下匹配
#       如果uri 和 path 中的第一个参数 满足 则进入该视图函数
#       如果uri 和 path 中的第一个参数 都匹配过了 依然没有满足的 则返回404


urlpatterns = [
    path('admin/', admin.site.urls),
    # path
    # path 的第一个参数是路由
    # path 的第二个参数 是视图函数名
    path('book/', include('book.urls')),

]
