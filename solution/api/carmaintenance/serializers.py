from rest_framework import serializers
from .models import Car, Tyre


class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        fields = ['tyre_id', 'degradation']


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['car_id', 'gas_capacity', 'current_gas', 'max_tyres', 'tyre_id']
