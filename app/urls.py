
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
      SpectacularAPIView,
      SpectacularRedocView,
      SpectacularSwaggerView
    )


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/user/', include('account.urls')),
   path('api-auth/', include('rest_framework.urls')),

   # DRF SPECTACULAR
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
