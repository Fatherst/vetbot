from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    verbose_name = "Записи и врачи"
    default_auto_field = "django.db.models.BigAutoField"
    name = "appointment"
