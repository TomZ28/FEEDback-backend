from django.db import models
from django.db.models import SET_NULL

from restaurants.models import Restaurant

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.ImageField(upload_to="menuitems/") #MEDIA_ROOT/menuitems
    description = models.CharField(max_length=400)
    restaurant = models.ForeignKey(to=Restaurant, related_name='menuitems', null=True, on_delete=SET_NULL)