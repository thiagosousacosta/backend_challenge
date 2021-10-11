from rest_framework import serializers

from .models import Car, Tyre


class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        fields = ['tyre_id', 'degradation', 'car_id', 'in_use']


class CarSerializer(serializers.ModelSerializer):
    tyres = TyreSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['car_id', 'gas_capacity', 'current_gas', 'tyres']
