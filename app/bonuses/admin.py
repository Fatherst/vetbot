from django.contrib import admin

from .models import DiscountCard, DiscountCardCategory


@admin.register(DiscountCard)
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "enote_id", "client_id", "category_id", "deleted")


@admin.register(DiscountCardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "name",
    )