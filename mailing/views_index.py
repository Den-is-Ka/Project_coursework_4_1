from django.core.cache import cache
from django.views.generic import TemplateView
from .models import Mailing, Client


class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, есть ли данные в кэше
        stats = cache.get("main_stats")

        if not stats:
            # Если нет — считаем и сохраняем
            total_mailings = Mailing.objects.count()
            active_mailings = Mailing.objects.filter(status="running").count()
            unique_clients = Client.objects.count()

            stats = {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "unique_clients": unique_clients,
            }
            cache.set("main_stats", stats, 60 * 5)  # кэшируем на 5 минут
            print("📦 Кэш пересчитан и записан:", stats)
        else:
            print("♻️ Используем кэшированные данные:", stats)

        # Добавляем данные в контекст
        context.update(stats)
        context["title"] = "Главная страница"

        # Печать текущего состояния кэша в консоль
        print("🧠 Кэш статистики:", cache.get("main_stats"))

        return context
