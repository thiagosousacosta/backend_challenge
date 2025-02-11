from carmaintenance.routes import function_urls, router
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns.extend(function_urls)
