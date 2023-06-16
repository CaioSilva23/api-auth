from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # auth JWT
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa: E501
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # noqa: E501
    # my routers
    path("auth/api/v1/user/created/", views.UserRegistrationAPI.as_view(), name="user-created"),  # noqa: E501
    path("auth/api/v1/user/list", views.UserListAPI.as_view(), name="user-list"),  # noqa: E501
    path('auth/api/v1/password/change/', views.ChangePasswordView.as_view(), name='change-password'),  # noqa: E501
    path('auth/api/v1/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),  # noqa: E501
    path("auth/api/v1/user/detail/<int:pk>/", views.UserDetailAPI.as_view(), name="user-detail"),  # noqa: E501

    # func
    path('auth/api/v1/password/reset/confirm/<str:uid64>/<str:token>/', views.password_account, name='password_reset_confirm'),  # noqa: E501

]
