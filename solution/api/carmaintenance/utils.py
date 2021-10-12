from django.db.models import F

from .constants import (KM_GAS_LITRE, KM_TYRE_DEGRADATION,
                        MAX_TYRE_DEGRADATION, MIN_GAS_ALLOWED)
from .exceptions import EnoughGasException, NotSwappabledTyresException
from .models import Tyre
from .validations import validate_car


def liter_to_percentage(quantity, capacity):
    return (quantity*100)/capacity


def percentage_to_liter(quantity, capacity):
    return (quantity*capacity)/100


def refuel_car(car, quantity):
    if car.current_gas < MIN_GAS_ALLOWED:
        quantity_in_percentage = liter_to_percentage(
            quantity, car.gas_capacity)
        new_current_gas = car.current_gas + quantity_in_percentage
        if new_current_gas >= 100:
            car.current_gas = 100
        else:
            car.current_gas = new_current_gas
    else:
        raise EnoughGasException

    return car


def maintenance_car(car, tyre_id):
    tyres = car.tyres.all()
    old_tyre = tyres.get(tyre_id=tyre_id)

    if old_tyre.degradation > MAX_TYRE_DEGRADATION:
        old_tyre.delete()

        new_tyre = Tyre.objects.create(car_id_id=car.car_id)
        new_tyre.save()

    else:
        raise NotSwappabledTyresException

    return car


def make_trip(car, distance):
    tyres = car.tyres.all()
    current_gas_l = percentage_to_liter(car.current_gas, car.gas_capacity)

    if validate_car(car):
        for km in range(distance):
            real_km = km + 1

            if real_km != 0:
                if real_km % KM_TYRE_DEGRADATION == 0:
                    tyres.update(degradation=F('degradation')+1)

                if real_km % KM_GAS_LITRE == 0:
                    current_gas_l -= 1

                car, current_gas_l = check_car_condition(car, current_gas_l)

        car.current_gas = liter_to_percentage(current_gas_l, car.gas_capacity)

    return car


def check_car_condition(car, current_gas_l):
    tyres = car.tyres.all()

    car = refuel_car(car, car.gas_capacity)
    current_gas_l = car.gas_capacity

    tyres_id = [x.tyre_id for x in tyres if x.degradation >
                MAX_TYRE_DEGRADATION]

    for tyre_id in tyres_id:
        car = maintenance_car(car, tyre_id)

    return car, current_gas_l
