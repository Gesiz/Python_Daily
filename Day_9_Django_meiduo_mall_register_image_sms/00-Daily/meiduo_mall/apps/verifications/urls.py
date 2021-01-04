from django.urls import path
from apps.verifications.views import ImageCodeView,SMSCodeView

urlpatterns = [
    path('image_codes/<uuid:uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile>/',SMSCodeView.as_view()),
]
