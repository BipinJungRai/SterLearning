from django.contrib import admin
from .models import ExtendedUser, PointsAwarded
# Register your models here.

admin.site.register(ExtendedUser)
admin.site.register(PointsAwarded)