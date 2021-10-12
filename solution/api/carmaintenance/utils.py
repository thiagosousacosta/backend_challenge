from django.db.models import F

from .models import Tyre


def liter_to_percentage(quantity, capacity):
    return (quantity*100)/capacity


def percentage_to_liter(quantity, capacity):
    return (quantity*capacity)/100


def refuel_car(car, quantity):

    quantity_in_percentage = liter_to_percentage(quantity, car.gas_capacity)
    new_current_gas = car.current_gas + quantity_in_percentage

    if new_current_gas >= 100:
        car.current_gas = 100
    else:
        car.current_gas = new_current_gas

    return car


def maintenance_car(car, tyre_id):
    tyres = car.tyres.all()

    old_tyre = tyres.get(tyre_id=tyre_id)
    old_tyre.delete()

    new_tyre = Tyre.objects.create(car_id_id=car.car_id)
    new_tyre.save()

    return car


def make_trip(car, distance):
    tyres = car.tyres.all()
    current_gas_l = percentage_to_liter(car.current_gas, car.gas_capacity)

    for km in range(distance):
        real_km = km + 1

        if real_km != 0:
            if real_km % 3 == 0:
                tyres.update(degradation=F('degradation')+1)

            if real_km % 8 == 0:
                current_gas_l -= 1

            car, current_gas_l = check_car_condition(car, current_gas_l)

    car.current_gas = liter_to_percentage(current_gas_l, car.gas_capacity)

    return car


def check_car_condition(car, current_gas_l):
    tyres = car.tyres.all()
    percent_gas = liter_to_percentage(current_gas_l, car.gas_capacity)

    if percent_gas < 5:
        car = refuel_car(car, car.gas_capacity)
        current_gas_l = car.gas_capacity

    tyres_id = [x.tyre_id for x in tyres if x.degradation > 94]

    for tyre_id in tyres_id:
        car = maintenance_car(car, tyre_id)

    return car, current_gas_l
