from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # auth JWT
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # my routers
    path("auth/user/api/created/", views.UserRegistrationView.as_view(), name="user-created"),
    path('auth/user/api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('auth/user/api/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/user/api/password/reset/confirm/<str:uid64>/<str:token>/', views.password_account, name='password_reset_confirm'),

]

