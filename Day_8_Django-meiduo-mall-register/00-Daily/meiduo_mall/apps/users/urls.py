from django.urls import path
from apps.users.views import MobileCountView, UsernameCountView,RegisterView

urlpatterns = [
    path('usernames/<uc:username>/count/', MobileCountView.as_view()),
    path('mobiles/<mc:mobile>/count/', UsernameCountView.as_view()),
    path('register/',RegisterView.as_view())
]
