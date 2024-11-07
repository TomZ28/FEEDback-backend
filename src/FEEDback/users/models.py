from django.db import models
from django.db.models import SET_NULL
from django.contrib.auth.models import AbstractUser

# Create your models here.

class FEEDbackUser(AbstractUser): #user class
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)


class Notification(models.Model):
    recipient = models.ForeignKey(to=FEEDbackUser, related_name='notification', on_delete=SET_NULL, null=True)
    message = models.CharField(max_length=100)
    when = models.DateTimeField(auto_now_add=True)