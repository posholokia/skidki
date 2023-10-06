from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'first_name',
            'last_name',
            'age',
            'gender',
            'city',
            'description_user',
        ]


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
