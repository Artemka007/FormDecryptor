from django.contrib.auth import views
from django.urls import path, reverse_lazy

from account.views import RegisterView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset_password/', views.PasswordResetView.as_view(success_url=reverse_lazy('reset_password_done')), name='reset_password'),
    path('reset_password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]