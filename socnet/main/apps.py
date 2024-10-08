from django.core.cache import cache
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    # Подключаем сигналы
    def ready(self):
        import main.signals

        # чистим весь кеш при рестарте сервера
        cache.clear()



