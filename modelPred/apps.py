from django.apps import AppConfig


class ModelpredConfig(AppConfig):
    name = 'modelPred'

    def ready(self):
       return True
       
