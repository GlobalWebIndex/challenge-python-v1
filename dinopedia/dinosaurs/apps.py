from django.apps import AppConfig


class DinosaursConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dinosaurs"

    def ready(self) -> None:
        import dinosaurs.signals
