"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# jobportal/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

# JWT token views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Health check root view
def home(request):
    return JsonResponse({"message": "Job Portal API Running..."})

# Swagger schema config
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.generators import OpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="Job Portal API",
        default_version='v1',
        description="API docs",

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[JWTAuthentication],
)


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # JWT token auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App routes (from apps/)
    path('api/users/', include('apps.users.urls')),
    path('api/seekers/', include('apps.seekers.urls')),
    path('api/employers/', include('apps.employers.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/common/', include('apps.common.urls')),



    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Media file serving (e.g., resumes, company logos)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

