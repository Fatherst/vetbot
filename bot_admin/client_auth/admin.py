from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "clientEnoteId",
        "firstName",
        "middleName",
        "lastName",
        "email",
        "phoneNumber",
        "clientTelegramId",
    )
