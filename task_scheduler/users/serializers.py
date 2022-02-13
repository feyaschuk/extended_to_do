from djoser.serializers import UserSerializer
# from rest_framework import serializers

from .models import User


class CustomUserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'id', 'password', 'email', 'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'id',
            'email', 'first_name',
            'last_name'
        )
