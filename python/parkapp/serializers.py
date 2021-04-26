from rest_framework import serializers

from adminapp.serializers import ParkingSerializer
from .models import Parking_floor, Users_car, Users_car_ac


class Parking_floorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_floor
        fields = ['pf_id','u_id', 'p_id', 'pf_floor', 'pf_space', 'pf_data']

class Users_carSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_car
        fields = ['uc_id', 'u_id', 'uc_model', 'uc_number','uc_color','uc_distance','uc_repair','uc_age']

class Users_car_acSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_car_ac
        fields = ['uca_id', 'uc_id', 'u_id', 'uc_number', 'uca_date', 'uca_pulse']