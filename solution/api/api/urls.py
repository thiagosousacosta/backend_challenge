from django import urls
from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework import routers
from carmaintenance.views import CarViewSet

router = routers.DefaultRouter()
router.register('cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
