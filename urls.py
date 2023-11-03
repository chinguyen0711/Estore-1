"""
URL configuration for EStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from app_store.views import ProductViewSet

router = routers.DefaultRouter()
router.register('san-pham', ProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_store.urls')),
    path('', include('app_customer.urls')),
    path('', include('app_cart.urls')),
    path('', include('app_admin.urls')),
    path('', include('app_report.urls')),
    path('', include('app_analysis.urls')),
    path('', include('app_visualization.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
