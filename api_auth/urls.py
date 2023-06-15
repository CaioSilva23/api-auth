from django.urls import path
from django.urls import include
from . import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.schemas import get_schema_view


urlpatterns = [
 # ...

    # SCHEMA DRF
    path('api_schema/', get_schema_view(
        title='Auth API Portfólio',
        version='V1',
        description='Guide for the REST API'
    ), name='api_schema'),
 
    #SCHEMA DRF
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),

    # my routers
    path("auth/user/api/created/", views.UserRegistrationView.as_view(), name="user-created"),

    # auth JWT
    path('auth/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/api/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/api/password/reset/confirm/<str:uid64>/<str:token>/', views.password_account, name='password_reset_confirm'),

    path('auth/api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]