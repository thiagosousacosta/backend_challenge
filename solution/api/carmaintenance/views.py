from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import *
from .models import Car, Tyre
from .serializers import CarSerializer, TyreSerializer
from .utils import maintenance_car, make_trip, refuel_car
from .validations import validate_tyre_creation


class CarViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = CarSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        try:
            data = request.data
            car = Car.objects.filter(car_id=data['car_id'])
            car_serializer = CarSerializer(car, many=True)
            return Response(car_serializer.data)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            data = request.data
            car = Car.objects.get(car_id=data['car_id'])

            if validate_tyre_creation(car):
                tyre = Tyre.objects.create(car_id_id=car.car_id)
                tyre.save()
                tyre_serializer = TyreSerializer(tyre)
                car.save()
                return Response(tyre_serializer.data)

        except EnoughUsableTyresException as e:
            return Response({'error': f'{e.message}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('PUT',))
def refuel(request):
    try:
        data = request.data

        car = Car.objects.get(car_id=data['car_id'])
        car = refuel_car(car, data['gas_quantity'])
        car.save()

        car_serializer = CarSerializer(car)

        return Response({'current_gas': car_serializer.data['current_gas']})

    except EnoughGasException as e:
        return Response({'error': f'{e.message}'})
    except KeyError as e:
        return Response({'error': f'Missing argument: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(('PUT',))
def maintenance(request):
    try:
        data = request.data
        car = Car.objects.get(car_id=data['car_id'])

        replace_data = data['replace_part']

        if 'tyre_id' in data['replace_part']:
            replace_part_id = replace_data.get('tyre_id')

            car = maintenance_car(car, replace_part_id)
            car.save()

            car_serializer = CarSerializer(car)

            return Response(car_serializer.data)
        else:
            return Response({"error": "Part not listed"}, status=status.HTTP_400_BAD_REQUEST)

    except NotSwappabledTyresException as e:
        return Response({'error': f'{e.message}'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response({'error': f'Missing argument: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def trip(request):
    try:
        data = request.data
        car = Car.objects.get(car_id=data['car_id'])
        distance = data['distance']

        car = make_trip(car, distance)
        car.save()

        car_serializer = CarSerializer(car)
        return Response(car_serializer.data)

    except NotUsableCarException as e:
        return Response({'error': f'{e.message}'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response({'error': f'Missing argument: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
