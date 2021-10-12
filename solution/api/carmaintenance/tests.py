from django.test import TestCase

from .constants import MAX_TYRE_DEGRADATION
from .models import Car, Tyre
from .utils import make_trip, refuel_car


class CarTripTestCase(TestCase):
    def setUp(self):

        car = Car.objects.create()

        for x in range(car.max_tyres):
            tyre = Tyre.objects.create(car_id_id=car.car_id)
            tyre.save()

        car.save()

        self.car = car

    def test_10000km_trip(self):
        """Run a trip of 10.000 KM, without breaking any part or swapping cars or gets out of gas"""
        distance = 10000
        quantity_to_refuel = 50

        car = self.car
        car = refuel_car(car, quantity_to_refuel)
        car = make_trip(car, distance)

        self.assertTrue(car.current_gas > 0)
        self.assertTrue(self.car == car)

        total_usable_tyres = len([x for x in car.tyres.all(
        ) if x.degradation < MAX_TYRE_DEGRADATION])

        self.assertTrue(total_usable_tyres == 4)

# without breaking any part
# or swapping cars
# or gets out of gas
