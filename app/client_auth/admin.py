from django.contrib import admin
from .models import Client
from django.utils.html import format_html


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    empty_value_display = "Поле не задано"
    list_display = (
        "enote_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone_number",
        "tg_chat_id",
    )
