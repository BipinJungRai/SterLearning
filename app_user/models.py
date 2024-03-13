""" Models to extend the django user model,
    adding avatars and decorations
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Decoration(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=False, blank=False)

    def __str__(self):
        return self.name

class Avatar(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=False, blank=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    
    avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.SET_NULL, related_name='%(class)s_avatar_used') #User may not have an avatar to begin with, so can be null
    decoration = models.ForeignKey(Decoration, blank=True, null=True, on_delete=models.SET_NULL, related_name='%(class)s_decoration_used') #User may not have a decoration to begin with, so can be null
    email = models.EmailField(null=False, blank=False) #User must have an email to log in, so cannot be null
    inventoryAvatar = models.ManyToManyField(Avatar, blank=True, related_name='%(class)s_avatars_stored') #Inventory starts empty, so can be blank
    inventoryDecoration = models.ManyToManyField(Decoration, blank=True, related_name='%(class)s_decorations_stored') #Inventory starts empty, so can be blank

    def __str__(self):
        return self.username