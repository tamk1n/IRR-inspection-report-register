from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import MyUser

# Register your models here.

User = get_user_model()

@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_filter = ('position', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {"fields": ("username", )}),
        (_("Personal info"),
            {"fields": ("first_name", "last_name", "email", "position", )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
