from django.contrib import admin

from .models import (
    DiscountCard,
    DiscountCardCategory,
    BonusTransaction,
    Program,
    Status,
    BonusAccrual,
    Recommendation,
)


@admin.register(DiscountCard)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "card_number",
        "client",
        "category",
        "deleted",
    )
    autocomplete_fields = ["client"]
    search_fields = ["enote_id", "client__id"]
    list_display_links = ["enote_id"]


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
    autocomplete_fields = ["discount_card"]


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
    autocomplete_fields = ["program"]
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
    autocomplete_fields = ["client"]
    list_display_links = ["client"]
    search_fields = ["client__last_name"]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "modified_at"]
    list_display = ("id", "promocode", "issued", "client", "created_at", "modified_at")
    search_fields = ["client", "promocode"]
    list_display_links = ["promocode"]
    autocomplete_fields = ["client"]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.issued:
            return super().get_readonly_fields(request, obj=obj) + ["issued"]
        return super().get_readonly_fields(request, obj=obj)
