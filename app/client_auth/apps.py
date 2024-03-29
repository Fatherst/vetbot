from django.apps import AppConfig


class ClientBotConfig(AppConfig):
    verbose_name = "Клиенты"
    default_auto_field = "django.db.models.BigAutoField"
    name = "client_auth"

    def ready(self):
        import client_auth.signals
