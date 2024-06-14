from rest_framework import serializers
from .models import UserStatus

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['user', 'is_online']