from rest_framework import serializers

from .models import Parking


class Parking_floorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_floor
        fields = ['p_id', 'pf_floor', 'pf_space', 'pf_data']