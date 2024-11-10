from django.contrib import admin

from .models import *


@admin.register(CustomUser)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone", "role")
