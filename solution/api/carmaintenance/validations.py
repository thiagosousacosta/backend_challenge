from .constants import MAX_TYRE_DEGRADATION
from .exceptions import EnoughUsableTyresException, NotUsableCarException

def validate_car(car):
    car.current_gas
    tyres = car.tyres.all()
    tyre_quantity = len([x for x in tyres])

    if car.current_gas > 0 and tyre_quantity == car.max_tyres:
        return True
    else:
        raise NotUsableCarException


def validate_tyre_creation(car):
    valid_tyres = [x.degradation for x in car.tyres.all(
    ) if x.degradation < MAX_TYRE_DEGRADATION]
    if len(valid_tyres) < 4:
        return True
    else:
        raise EnoughUsableTyresException
