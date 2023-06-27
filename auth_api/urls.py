
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls'))
]

schema_view = get_schema_view(
   openapi.Info(
      title="Auth Portfólio API",
      default_version='v1',
      description="Auth Portfólio API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="caio_ceac23@hotmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   # url='https://api-auth.up.railway.app/'
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa: E501
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa: E501
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa: E501
   re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # noqa: E501
   re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # noqa: E501

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
