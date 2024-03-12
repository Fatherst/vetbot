from django.contrib import admin
from .models import Specialization, Doctor, Appointment, Invoice


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "first_name",
        "middle_name",
        "last_name",
        "get_specializations",
        "photo",
        "detail_info",
        "fired_date",
        "deleted",
    )
    search_fields = ["first_name"]

    def get_specializations(self, obj):
        return "\n".join([s.name for s in obj.specializations.all()])


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "status",
        "patient",
        "doctor",
        "date_time",
        "deleted",
    )
    search_fields = ["enote_id"]


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enote_id",
        "name",
    )
    search_fields = ["enote_id"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "enote_id", "client", "date", "sum")
    list_display_links = ["enote_id"]
    search_fields = ["enote_id"]
