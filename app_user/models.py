from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

class Decoration(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=False, blank=False)

    def __str__(self):
        return self.name

class User(AbstractUser):

    class AvatarChoices(models.TextChoices):
        TURTLE = "TL", _("Turtle")
        DUCK = "DK", _("Duck")
        CAT = "CT", _("Cat")
    
    avatar = models.CharField(null=True, choices=AvatarChoices, max_length=2) #User may not have an avatar to begin with, so can be null
    decoration = models.ForeignKey(Decoration, null=True, on_delete=models.SET_NULL, related_name='%(class)s_decoration_used') #User may not have a decoration to begin with, so can be null
    email = models.EmailField(null=False, blank=False) #User must have an email to log in, so cannot be null
    inventoryAvatar = MultiSelectField(choices=AvatarChoices, max_length=2, blank=True) #Inventory starts empty, so can be blank
    inventoryDecoration = models.ManyToManyField(Decoration, blank=True, related_name='%(class)s_decorations_stored') #Inventory starts empty, so can be blank

    def __str__(self):
        return self.username