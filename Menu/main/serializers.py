from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Special, Customer

class SpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Special
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

