from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from menuitems.models import MenuItem

class MenuItemSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant_owner = serializers.IntegerField(source='restaurant.owner_id', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'image', 'description', 'restaurant', 'restaurant_owner']
        extra_kwargs = {
            'id': {'read_only': True}
        }
