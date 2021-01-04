from django.urls import path
from apps.users.views import UsernameContView, MobileContView

urlpatterns = [
    path('usernames/<uc:username>/count', UsernameContView.as_view()),
    path('mobiles/<mc:mobile>/count', MobileContView.as_view()),
]
