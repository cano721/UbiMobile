from rest_framework import serializers

from .models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['p_id', 'u_id', 'p_name', 'p_addr', 'p_cap']