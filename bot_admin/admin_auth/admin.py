from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_staff",
        "is_active",
        "date_joined",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "admin_telegram_id",
    )