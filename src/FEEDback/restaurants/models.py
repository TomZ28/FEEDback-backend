from django.db import models
from django.db.models import SET_NULL
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import FEEDbackUser

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    follower_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rating_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(max_length=400)
    owner = models.ForeignKey(to=FEEDbackUser, related_name='restaurant', on_delete=SET_NULL, null=True)


class RestaurantFollower(models.Model):
    follower = models.ForeignKey(to=FEEDbackUser, related_name='restaurantFollowers', on_delete=SET_NULL, null=True)
    restaurant = models.ForeignKey(to=Restaurant, related_name='restaurantsFollowed', null=True, on_delete=SET_NULL)


class RestaurantLike(models.Model):
    liker = models.ForeignKey(to=FEEDbackUser, related_name='restaurantLikers', on_delete=SET_NULL, null=True)
    restaurant = models.ForeignKey(to=Restaurant, related_name='restaurantsLiked', null=True, on_delete=SET_NULL)


class Comment(models.Model):
    author = models.ForeignKey(to=FEEDbackUser, related_name='commenter', on_delete=SET_NULL, null=True)
    details = models.CharField(max_length=400)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    restaurant = models.ForeignKey(to=Restaurant, related_name='comments', null=True, on_delete=SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
