from rest_framework import serializers

from .models import Car, Tyre


class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        fields = ['tyre_id', 'degradation', 'car_id']


class CarSerializer(serializers.ModelSerializer):
    tyres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Car
        fields = ['car_id', 'gas_capacity', 'current_gas', 'tyres']
