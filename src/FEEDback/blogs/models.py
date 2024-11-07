from django.db import models
from django.db.models import SET_NULL
from django.core.validators import MinValueValidator

from users.models import FEEDbackUser
from restaurants.models import Restaurant

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=2000)
    image = models.ImageField(upload_to="blogimages/", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(to=Restaurant, related_name='blogs', null=True, on_delete=SET_NULL)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])


class BlogLike(models.Model):
    liker = models.ForeignKey(to=FEEDbackUser, related_name='blogLikers', on_delete=SET_NULL, null=True)
    blog = models.ForeignKey(to=Blog, related_name='blogsLiked', null=True, on_delete=SET_NULL)