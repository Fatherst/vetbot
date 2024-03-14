from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_active",
        "full_name",
        "email",
        "tg_chat_id",
    )

    def username(self, obj):
        return obj.user.username

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def is_active(self, obj):
        return obj.user.is_active

    def email(self, obj):
        return obj.user.email
