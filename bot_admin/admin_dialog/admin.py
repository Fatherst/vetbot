from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "admin_telegram_id",
    )