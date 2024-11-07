from django.db import models
from django.db.models import SET_NULL

from restaurants.models import Restaurant

# Create your models here.

class RestaurantImage(models.Model):
    image = models.ImageField(upload_to="images/")
    restaurant = models.ForeignKey(to=Restaurant, related_name='images', null=True, on_delete=SET_NULL)