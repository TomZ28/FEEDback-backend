from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from images.models import RestaurantImage

class RestaurantImageSerializer(ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model=RestaurantImage
        fields=['id', 'image']
        extra_kwargs = {
            'id': {'read_only': True}
        }
