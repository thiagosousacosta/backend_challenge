from django.db import models


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    gas_capacity = models.IntegerField(default=50)
    current_gas = models.IntegerField(default=100)
    max_tyres = models.IntegerField(default=4, editable=False)
    
 
    def __str__(self):
        return f'{self.car_id}'

class Tyre(models.Model):
    tyre_id = models.AutoField(primary_key=True)
    degradation = models.IntegerField(default=0)
    car_id = models.ManyToManyField(Car)

    def __str__(self):
        return f'{self.tyre_id}'