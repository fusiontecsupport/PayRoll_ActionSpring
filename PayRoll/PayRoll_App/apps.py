from django.apps import AppConfig


class PayrollAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PayRoll_App'

    def ready(self):
        import PayRoll_App.signals