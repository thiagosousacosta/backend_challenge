from django.urls import path
from rest_framework import routers

from carmaintenance.views import (CarViewSet, TyreViewSet, maintenance, refuel,
                                  trip)

router = routers.DefaultRouter()
router.register('cars', CarViewSet, basename='cars')
router.register('tyres', TyreViewSet, basename='tyres')

function_urls = [
    path('refuel/', refuel, name='refuel'),
    path('maintenance/', maintenance, name='maintenance'),
    path('trip/', trip, name='trip'),
]
