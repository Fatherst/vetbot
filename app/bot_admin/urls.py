from bot.views import webhook
from bot_admin.api import api
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("webhook", webhook, name="webhook"),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
