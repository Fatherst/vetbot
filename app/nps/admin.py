from django.contrib import admin
from nps import models


class ScoreFilter(admin.SimpleListFilter):
    title = "Оценки"
    parameter_name = "score"

    def lookups(self, request, model_admin):
        return (
            ("positive", "Положительные"),
            ("negative", "Отрицательные"),
        )

    def queryset(self, request, queryset):
        if self.value() == "positive":
            return queryset.filter(score__gt=8)
        if self.value() == "negative":
            return queryset.filter(score__lte=8)


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("client", "score", "appointment_date", "created_at")
    search_fields = ("client__last_name",)
    list_filter = (
        ScoreFilter,
        "appointment_date",
    )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ["status", "resource"]
    list_display = (
        "client",
        "status",
        "resource",
        "screenshot",
        "created_at",
        "modified_at",
        "rejection_reason",
    )
    search_fields = ("client__last_name",)
