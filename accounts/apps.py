from django.apps import AppConfig
from django.conf import settings

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .scheduler import MyScheduler, CountinuousScheduler
        scheduler = MyScheduler()
        scheduler.scheduler.start()

        contunuous_scheduler = CountinuousScheduler()
        contunuous_scheduler.scheduler.start()



