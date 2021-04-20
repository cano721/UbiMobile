from rest_framework import serializers

from .models import Parking


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['u_id', 'u_nick', 'u_pwd', 'u_name','u_age']