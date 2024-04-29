from django.contrib import admin
from .models import ExtendedUser, PointsAwarded, Friend
# Register your models here.

admin.site.register(ExtendedUser)
admin.site.register(PointsAwarded)
admin.site.register(Friend)