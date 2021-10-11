from carmaintenance.routes import router
from carmaintenance.views import refuel, maintenance
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('refuel/', refuel, name='refuel'),
    path('maintenance/', maintenance, name='maintenance'),
]
