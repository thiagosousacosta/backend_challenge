from rest_framework import viewsets
from rest_framework.response import Response

from .models import Car, Tyre
from .serializers import CarSerializer, TyreSerializer, CarTyresSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = CarSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        data = request.data
        car = Car.objects.filter(car_id = data['car_id'])
        car_serializer = CarTyresSerializer(car, many=True)
        return Response(car_serializer.data)

    def create(self, request, *args, **kwargs):
        car = Car.objects.create()
        car.save()
        car_serializer = CarSerializer(car)
        return Response(car_serializer.data)


class TyreViewSet(viewsets.ModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        car = Car.objects.get(car_id = data['car_id'])
        tyre = Tyre.objects.create(car_id_id = car.car_id)
        tyre_serializer = TyreSerializer(tyre)
        return Response(tyre_serializer.data)

