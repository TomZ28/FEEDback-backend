import email
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from restaurants.models import Restaurant

from users.models import FEEDbackUser, Notification


class SignupSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = FEEDbackUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': "The two password fields didn't match"})
        attrs.pop('confirm_password')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class EditProfileSerializer(ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = FEEDbackUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar', 'new_password', 'confirm_new_password', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'min_length': 8}
        }

    def validate(self, attrs):
        if 'new_password' in attrs and attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'new_password': "The two password fields didn't match"})
        if 'confirm_new_password' in attrs:
            attrs.pop('confirm_new_password')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['password']):
            raise serializers.ValidationError({'password': "The entered password is incorrect"})
        if 'new_password' in validated_data:
            validated_data['password'] = make_password(validated_data['new_password'])
            validated_data.pop('new_password')
        else:
            validated_data.pop('password')
        return super().update(instance, validated_data)


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'when']
        extra_kwargs = {
            'message': {'read_only': True},
            'when': {'read_only': True},
            'id': {'read_only': True}
        }

class FEEDbackTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['id'] = self.user.id
        data['username'] = self.user.username
        if self.user.first_name:
            data['first_name'] = self.user.first_name
        if self.user.last_name:
            data['last_name'] = self.user.last_name
        if self.user.email:
            data['email'] = self.user.email
        if self.user.phone_number:
            data['phone'] = self.user.phone_number
        if self.user.avatar:
            data['avatar'] = self.user.avatar

        restaurant = Restaurant.objects.filter(owner=self.user)
        if restaurant.exists():
            data['restaurant_id'] = restaurant.first().id

        return data
