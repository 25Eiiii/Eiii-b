from rest_framework import serializers
import re
from accounts.models import Profile
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'user', 'title', 'place', 'memo', 'date', 'time']
        read_only_fields = ['user']