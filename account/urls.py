
from django.urls import path
from . import views

urlpatterns = [
    # api/user
    path('register/', views.UserRegistrationAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('profile/', views.UserProfileAPI.as_view(), name='profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),  # noqa: E501

    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),  # noqa: E501
    path('reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='reset-password'),  # noqa: E501

]
