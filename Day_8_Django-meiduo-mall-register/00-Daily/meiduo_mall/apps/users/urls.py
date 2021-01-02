from django.urls import path
from apps.users.views import MobileCountView, UsernameCountView

urlpatterns = [
    path('usernames/<uc:username>/count/', MobileCountView.as_view()),
    path('mobiles/<mc:mobile>/count/', UsernameCountView.as_view()),
]
