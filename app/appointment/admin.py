from django.contrib import admin

from appointment import models


@admin.register(models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "show_in_bot")
    list_filter = ("show_in_bot",)
    search_fields = ("name",)


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "show_in_bot")
    list_filter = ("show_in_bot",)
    search_fields = ("name",)


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "get_specializations",
        "get_positions",
        "photo",
        "fired_date",
        "show_in_bot",
        "deleted",
    )
    list_filter = ("deleted", "show_in_bot")
    search_fields = ("last_name", "enote_id")
    filter_horizontal = ("specializations", "positions")

    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specializations.all()])

    get_specializations.short_description = "Специализации"

    def get_positions(self, obj):
        return ", ".join([s.name for s in obj.positions.all()])

    get_positions.short_description = "Должности"


@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "patient",
        "doctor",
        "status",
        "approved",
        "date_time",
        "deleted",
    )
    autocomplete_fields = ("client", "patient", "doctor")
    search_fields = ("enote_id", "client__last_name", "doctor__last_name")
    list_filter = ("approved", "deleted")


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "enote_id", "client", "date", "sum")
    list_display_links = ["enote_id"]
    search_fields = ["enote_id"]
