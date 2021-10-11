from .models import Tyre

def refuel_car(car, quantity):

    def liter_to_percentage(quantity, capacity):
        return (quantity*100)/capacity

    quantity_in_percentage = liter_to_percentage(quantity, car.gas_capacity)
    new_current_gas = car.current_gas + quantity_in_percentage

    if new_current_gas >= 100:
        car.current_gas = 100
    else:
        car.current_gas = new_current_gas

    return car

def maintenance_car(car, tyre_id):
    old_tyre = Tyre.objects.get(tyre_id = tyre_id)
    old_tyre.delete()

    new_tyre = Tyre.objects.create(car_id_id=car.car_id)
    new_tyre.save()

    return car   