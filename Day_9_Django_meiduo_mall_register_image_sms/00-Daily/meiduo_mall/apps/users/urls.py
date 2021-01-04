from django.urls import path
from apps.users.views import UsernameCountView, MobileCountView,RegisterView

urlpatterns = [
    path('usernames/<uc:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mc:mobile>/count/', MobileCountView.as_view()),
    path('register/',RegisterView.as_view()),
]
