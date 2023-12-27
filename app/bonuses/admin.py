from django.contrib import admin

from .models import DiscountCard, DiscountCardCategory, BonusTransaction


@admin.register(DiscountCard)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "card_number",
        "client_id",
        "category_id",
        "deleted",
    )
    search_fields = ["enote_id", "client__id"]


@admin.register(DiscountCardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "name",
    )
    search_fields = ["enote_id"]


@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "enote_id", "sum", "discount_card", "datetime")
    search_fields = ["enote_id"]
