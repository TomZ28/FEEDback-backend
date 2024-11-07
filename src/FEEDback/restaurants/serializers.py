from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Sum

from restaurants.models import Restaurant, RestaurantFollower, RestaurantLike, Comment


class SearchSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField('rating_value')

    def rating_value(self, obj):
        if obj.rating_count == 0:
            return 0
        comments = Comment.objects.filter(restaurant=obj)
        total_ratings = comments.aggregate(Sum('rating'))['rating__sum']
        return total_ratings / obj.rating_count

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'postal_code', 'phone_number', 'follower_count', 'likes', 'rating']
        extra_kwargs = {
            'rating': {'read_only': True},
            'id': {'read_only': True}
        }


class CreateRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'postal_code', 'phone_number', 'description']
        extra_kwargs = {
            'id': {'read_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Restaurant.objects.all(),
                fields=['name', 'address'],
                message="This restaurant already exists at this location"
            )
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if Restaurant.objects.filter(owner=user).exists():
            raise serializers.ValidationError({'error': "You can only own one restaurant"})
        return super().validate(attrs)


class EditRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'postal_code', 'phone_number', 'description']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def update(self, instance, validated_data):
        rest_name = validated_data['name']
        rest_addr = validated_data['address']
        if (instance.name != rest_name or instance.address != rest_addr) and \
            Restaurant.objects.filter(name=rest_name, address=rest_addr).exists():
            raise serializers.ValidationError({'error': "This restaurant already exists at this location"})
        return super().update(instance, validated_data)


class RestaurantDetailSerializer(ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    id = serializers.ReadOnlyField()
    followed_by_user = serializers.SerializerMethodField('is_followed')
    liked_by_user = serializers.SerializerMethodField('is_liked')
    rating = serializers.SerializerMethodField('rating_value')

    def is_followed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return RestaurantFollower.objects.filter(follower=user, restaurant=obj).exists()
        return False

    def is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return RestaurantLike.objects.filter(liker=user, restaurant=obj).exists()
        return False

    def rating_value(self, obj):
        if obj.rating_count == 0:
            return 0
        comments = Comment.objects.filter(restaurant=obj)
        total_ratings = comments.aggregate(Sum('rating'))['rating__sum']
        return total_ratings / obj.rating_count

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'postal_code', 'phone_number',
        'follower_count', 'likes', 'rating_count', 'rating', 'description', 'owner',
        'followed_by_user', 'liked_by_user']
        extra_kwargs = {
            'followed_by_user': {'read_only': True},
            'liked_by_user': {'read_only': True},
            'rating_count': {'read_only': True},
            'rating': {'read_only': True}
        }


class RestaurantFollowerSerializer(ModelSerializer):
    class Meta:
        model = RestaurantFollower
        fields = ['follower', 'restaurant']
        extra_kwargs = {
            'follower': {'read_only': True},
            'restaurant': {'read_only': True}
        }


class RestaurantLikeSerializer(ModelSerializer):
    class Meta:
        model = RestaurantLike
        fields = ['liker', 'restaurant']
        extra_kwargs = {
            'liker': {'read_only': True},
            'restaurant': {'read_only': True}
        }


class CommentSerializer(ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'details', 'rating', 'restaurant', 'date_created']
        extra_kwargs = {
            'date_created': {'read_only': True}
        }
