from django.contrib import admin
from client_auth import models


class WithTelegramIDFilter(admin.SimpleListFilter):
    title = "Зарегистрирован в боте"
    parameter_name = "register_in_bot"

    def lookups(self, request, model_admin):
        return [
            ("register_in_bot", "Да"),
            ("not_register_in_bot", "Нет"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "register_in_bot":
            return queryset.exclude(tg_chat_id=None)
        if self.value() == "not_register_in_bot":
            return queryset.filter(tg_chat_id=None)


class WithEnoteIDFilter(admin.SimpleListFilter):
    title = "Зарегистрирован в enote"
    parameter_name = "register_in_enote"

    def lookups(self, request, model_admin):
        return [
            ("register_in_enote", "Да"),
            ("not_register_in_enote", "Нет"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "register_in_enote":
            return queryset.exclude(enote_id=None)
        if self.value() == "not_register_in_enote":
            return queryset.filter(enote_id=None)


class DeadPatientFilter(admin.SimpleListFilter):
    title = "Умер"
    parameter_name = "dead"

    def lookups(self, request, model_admin):
        return [
            ("dead", "Да"),
            ("not_dead", "Нет"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "dead":
            return queryset.exclude(time_of_death=None)
        if self.value() == "not_dead":
            return queryset.filter(time_of_death=None)


class AnimalKindFilter(admin.SimpleListFilter):
    title = "Вид"
    parameter_name = "animal_kind"

    def lookups(self, request, model_admin):
        kinds = models.AnimalKind.objects.all()
        return [(kind.id, kind.name) for kind in kinds]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(kind=self.value())
