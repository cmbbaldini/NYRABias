from rest_framework import serializers
from .models import Race

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['date', 'track', 'raceNumber', 'surface', 'distance', 
                  'condition', 'fieldSize', 'maidens', 'firstCall', 'secondCall']