from django.contrib import admin
from django.urls import include, path
from django.urls import re_path as url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as drf_yasg
from rest_framework import permissions

schema_view = drf_yasg(
    openapi.Info(
        title="Auth API Portfólio",
        default_version='v1',
        description="Auth API Portfólio",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="caio_ceac23@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_auth.urls')),

]

# swagger
urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa E501
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa E501
]
