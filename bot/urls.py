from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.chat_page, name="index"),
    path('api/chat/', views.chat_endpoint, name='chat_endpoint'),
]
