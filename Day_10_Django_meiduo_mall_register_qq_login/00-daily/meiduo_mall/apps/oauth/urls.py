from django.urls import path
from apps.oauth.views import QQ
urlpatterns = [
    # path('')
    path('oauth_callback/', QQAuthUserView.as_view()),
]