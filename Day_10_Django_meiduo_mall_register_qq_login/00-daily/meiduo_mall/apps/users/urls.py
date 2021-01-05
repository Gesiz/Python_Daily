from django.urls import path
from apps.users.views import UsernameCountView,MobileCountView
urlpatterns = [
    path('usernames/<uc:username>/count/',UsernameCountView.as_view()),
    path('mobiles/<mc:mobile>/count/',MobileCountView.as_view())
]