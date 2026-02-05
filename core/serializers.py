from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fleet, Device

# Sérializer for Fleets
class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner'] 

# Serializer for Users
class UserSerializer(serializers.ModelSerializer):
    fleets = FleetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'fleets']

# Serializer for Devices
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'serial_number', 'fleet', 'os_version']
        