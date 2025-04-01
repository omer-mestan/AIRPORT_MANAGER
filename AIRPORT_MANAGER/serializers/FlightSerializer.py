from rest_framework import serializers
from AIRPORT_MANAGER.models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'flight_number',
            'departure_time',
            'arrival_time',
            'duration',
            'price',
            'flight_type',
            'status',
            'to_airport',
            'from_airport',
            'airline'
        ]
