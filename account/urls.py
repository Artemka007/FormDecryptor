from django.contrib.auth import views
from django.urls import path

from account.views import RegisterView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]