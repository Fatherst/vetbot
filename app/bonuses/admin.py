from django.contrib import admin

from bonuses import models


class StatusInline(admin.TabularInline):
    model = models.Status
    extra = 0


@admin.register(models.DiscountCard)
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "category")
    search_fields = ("enote_id", "client__last_name", "client__enote_id")
    autocomplete_fields = ("client", "category")
    list_filter = ("deleted",)


@admin.register(models.DiscountCardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "enote_id", "name")
    search_fields = ("enote_id", "name")


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "registration_bonus_amount",
        "new_client_bonus_amount",
        "review_bonus_amount",
        "is_active",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("is_active",)
    inlines = (StatusInline,)


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "program", "cashback_amount", "start_amount", "end_amount")
    search_fields = ("name",)
    autocomplete_fields = ("program",)


@admin.register(models.BonusAccrual)
class BonusAccrualAdmin(admin.ModelAdmin):
    readonly_fields = ("accrued", "modified_at", "created_at")
    list_display = (
        "client",
        "amount",
        "reason",
        "accrued",
        "created_at",
        "modified_at",
    )
    search_fields = ("client__enote_id", "client__last_name")
    list_filter = ("accrued", "reason")


@admin.register(models.Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")
    list_display = ("client", "promocode", "issued", "created_at", "modified_at")
    search_fields = ("client__enote_id", "client__last_name", "promocode")
    list_filter = ("issued",)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.issued:
            return super().get_readonly_fields(request, obj=obj) + ["issued"]
        return super().get_readonly_fields(request, obj=obj)
