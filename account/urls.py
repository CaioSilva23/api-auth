
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('profile/', views.UserProfileAPI.as_view(), name='profile'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', views.PasswordResetEmailView.as_view(), name='reset-password'),
]
