from django.urls import path
from . import views

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
