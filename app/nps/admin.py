from django.contrib import admin
from nps import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("client", "score", "appointment_date", "created_at")
    search_fields = ("client__last_name",)
