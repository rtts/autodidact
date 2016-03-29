from django.apps import AppConfig

class UvtUserConfig(AppConfig):
    name = 'uvt_user'

    def ready(self):
        from . import signals
