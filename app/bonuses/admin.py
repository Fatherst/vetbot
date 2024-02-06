from django.contrib import admin

from .models import (
    DiscountCard,
    DiscountCardCategory,
    BonusTransaction,
    Program,
    Status,
    BonusAccrual,
)


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


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "registration_bonus_amount",
        "new_client_bonus_amount",
        "is_active",
        "review_bonus_amount",
        "created_at",
    )
    search_fields = ["name"]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "program",
        "cashback_amount",
        "start_amount",
        "end_amount",
    )
    search_fields = ["name"]


@admin.register(BonusAccrual)
class BonusAccrualAdmin(admin.ModelAdmin):
    readonly_fields = ["accrued", "modified_at", "created_at"]
    list_display = (
        "id",
        "client",
        "amount",
        "reason",
        "created_at",
        "modified_at",
        "accrued",
    )
    search_fields = ["client"]
