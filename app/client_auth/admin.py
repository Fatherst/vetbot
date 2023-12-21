from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone_number",
        "tg_chat_id",
    )
    search_fields = ["enote_id"]
