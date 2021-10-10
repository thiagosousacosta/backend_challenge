from django.shortcuts import render

from rest_framework import viewsets
from .serializers import CarSerializer, TyreSerializer
from .models import Car, Tyre


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class TyreViewSet(viewsets.ModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer