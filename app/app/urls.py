"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import (
      SpectacularAPIView,
      SpectacularRedocView,
      SpectacularSwaggerView
    )

from user import views as user_views


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # User
    path('api/user/register/', user_views.UserRegistrationAPI.as_view(), name='register'),
    path('api/user/login/', user_views.UserLoginAPI.as_view(), name='login'),
    path('api/user/profile/', user_views.UserProfileAPI.as_view(), name='profile'),
    path('api/user/change-password/', user_views.UserChangePasswordView.as_view(), name='change-password'),
    path('api/user/reset-password/', user_views.PasswordResetEmailView.as_view(), name='reset-password'),

    # DRF SPECTACULAR
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
