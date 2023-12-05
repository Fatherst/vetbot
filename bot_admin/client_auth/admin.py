from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "client_enote_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone_number",
        "client_telegram_id",
    )
