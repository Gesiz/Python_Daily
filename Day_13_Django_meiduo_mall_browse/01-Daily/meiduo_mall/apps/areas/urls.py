from django.urls import path
from . import views

urlpatterns = [

    path('areas/', views.AreasView.as_view()),
    path('areas/<pk>/', views.AreasView.as_view()),
]
