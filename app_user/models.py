from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

class Decoration(models.Model):
    name = models.CharField()
    image = models.ImageField()

    def __str__(self):
        return self.name

class User(AbstractUser):

    class AvatarChoices(models.TextChoices):
        TURTLE = "TL", _("Turtle")
        DUCK = "DK", _("Duck")
        CAT = "CT", _("Cat")
    
    avatar = models.CharField(null=True, blank=True, choices=AvatarChoices, max_length=2) #User may not have an avatar to begin with, so can be null/blank
    decoration = models.ForeignKey(null=True, blank=True) #User may not have a decoration to begin with, so can be null/blank
    email = models.EmailField(null=False, blank=False) #User must have an email to log in, so cannot be null/blank
    inventoryAvatar = MultiSelectField(choices=AvatarChoices, max_length=2) #Inventory starts empty, so can be blank
    inventoryDecoration = models.ManyToManyField(Decoration, blank=True) #Inventory starts empty, so can be blank