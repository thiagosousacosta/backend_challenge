from rest_framework import routers

from carmaintenance.views import CarViewSet, TyreViewSet

router = routers.DefaultRouter()
router.register('cars', CarViewSet, basename='cars')
router.register('tyres', TyreViewSet, basename='tyres')
