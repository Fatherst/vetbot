from django.apps import AppConfig


class AdminDialogConfig(AppConfig):
    verbose_name = 'Авторизация администраторов'
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_auth"
