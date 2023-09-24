from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import ModelAdmin
from .models import Company
import os
# Register your models here.

User = get_user_model()

@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = int(os.getenv("COMPANY_PAGE_COUNT"))