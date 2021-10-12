from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Car, Tyre
from .serializers import CarSerializer, TyreSerializer
from .utils import maintenance_car, make_trip, refuel_car


class CarViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = CarSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        data = request.data
        car = Car.objects.filter(car_id=data['car_id'])
        car_serializer = CarSerializer(car, many=True)
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
        car = Car.objects.get(car_id=data['car_id'])
        tyre = Tyre.objects.create(car_id_id=car.car_id)
        tyre_serializer = TyreSerializer(tyre)
        return Response(tyre_serializer.data)


@api_view(('PUT',))
def refuel(request):
    data = request.data
    car = Car.objects.get(car_id=data['car_id'])

    car = refuel_car(car, data['gas_quantity'])
    car.save()

    car_serializer = CarSerializer(car)

    return Response({'current_gas': car_serializer.data['current_gas']})


@api_view(('PUT',))
def maintenance(request):
    data = request.data
    car = Car.objects.get(car_id=data['car_id'])

    replace_data = data['replace_part']
    replace_part_id = replace_data.get('tyre_id')

    car = maintenance_car(car, replace_part_id)
    car.save()

    car_serializer = CarSerializer(car)

    return Response(car_serializer.data)


@api_view(('GET',))
def trip(request):
    data = request.data
    car = Car.objects.get(car_id=data['car_id'])
    distance = data['distance']

    car = make_trip(car, distance)
    car.save()

    car_serializer = CarSerializer(car)
    return Response(car_serializer.data)
