from django.contrib import admin
from .models import EngineerRegisterationToken
from django.contrib.admin import ModelAdmin


@admin.register(EngineerRegisterationToken)
class EngineerRegisterationTokenAdmin(ModelAdmin):
    pass