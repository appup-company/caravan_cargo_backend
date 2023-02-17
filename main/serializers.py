from django.db.models import fields
from rest_framework import serializers
from .models import *




class UserDetaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'groups', 'user_permissions', 'first_name', 'last_name', 'player_id', 'registered')


class PackageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'