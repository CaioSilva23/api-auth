from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # my routers

    path("user/api/created/", views.UserRegistrationView.as_view(), name="user-created"),

    # auth JWT
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('api/password/reset/confirm/<str:uid64>/<str:token>/', views.password_account, name='password_reset_confirm'),
    
    path('auth/api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
 

]