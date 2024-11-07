from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from blogs.models import Blog, BlogLike

class BlogSerializer(ModelSerializer):
    liked_by_user = serializers.SerializerMethodField('is_liked')
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant_owner = serializers.IntegerField(source='restaurant.owner_id', read_only=True)

    def is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return BlogLike.objects.filter(liker=user, blog=obj).exists()
        return False

    class Meta:
        model = Blog
        fields = ['id', 'title', 'details', 'image', 'date_created', 'last_modified', 'restaurant', 'restaurant_id', 'restaurant_owner', 'likes', 'liked_by_user']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'last_modified': {'read_only': True},
            'likes': {'read_only': True},
            'restaurant_id': {'read_only': True},
            'id': {'read_only': True}
        }


class BlogLikeSerializer(ModelSerializer):
    class Meta:
        model = BlogLike
        fields = ['liker', 'blog']
        extra_kwargs = {
            'liker': {'read_only': True},
            'blog': {'read_only': True}
        }
