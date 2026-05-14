from django.apps import AppConfig


class NewappConfig(AppConfig):
    #is a 64-bit integer 
    default_auto_field = 'django.db.models.BigAutoField' #prevents for the software to crash
    name = 'newApp'
    def ready(self):
        import newApp.signals
