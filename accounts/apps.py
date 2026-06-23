from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # without this sinals will not run, with this: Django automatically connects signal system

    def ready(self):
        import accounts.signals
