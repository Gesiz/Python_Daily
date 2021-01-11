from django.urls import path, include
from . import views

urlpatterns = [
    path('image_codes/<UUID:uuid>/', views.ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', views.SMSCodeView.as_view()),

]
