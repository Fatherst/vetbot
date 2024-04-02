from client_auth import filters, models
from django.contrib import admin


class PatientInline(admin.TabularInline):
    model = models.Patient
    extra = 0


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "middle_name",
        "phone_number",
        "tg_chat_id",
    )
    search_fields = (
        "enote_id",
        "last_name",
        "phone_number",
        "email",
        "first_name",
        "middle_name",
    )
    list_filter = ("deleted", filters.WithTelegramIDFilter, filters.WithEnoteIDFilter)
    inlines = (PatientInline,)


@admin.register(models.BlockedClient)
class BlockedClientAdmin(admin.ModelAdmin):
    list_display = ("client", "reason", "created_at")
    autocomplete_fields = ("client",)
    search_fields = ("client__last_name", "client__phone_number", "client__id")


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("client", "name", "kind", "birth_date", "time_of_death")
    search_fields = ("enote_id", "client__last_name", "name")
    list_filter = (
        "deleted",
        "kind",
        filters.DeadPatientFilter,
        filters.AnimalKindFilter,
    )


@admin.register(models.AnimalKind)
class AnimalKindAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "enote_id")


@admin.register(models.Weighing)
class WeighingAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "weight", "date")
    search_fields = ("enote_id", "patient")
    autocomplete_fields = ("patient",)
