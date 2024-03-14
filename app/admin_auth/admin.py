from django.contrib import admin
from admin_auth.models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("user", "tg_chat_id")
    autocomplete_fields = ("user",)
