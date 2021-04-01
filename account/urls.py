from django.contrib.auth import views
from django.contrib.auth.views import logout_then_login
from django.urls import path, reverse_lazy

from account.views import register_view

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', register_view, name='register'),
    path('logout/', logout_then_login, name='logout'),
    path('reset_password/', views.PasswordResetView.as_view(success_url=reverse_lazy('reset_password_done')), name='reset_password'),
    path('reset_password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]