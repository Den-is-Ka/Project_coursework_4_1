
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attempt


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_attempts = Attempt.objects.count()
        success_attempts = Attempt.objects.filter(status="success").count()
        failed_attempts = Attempt.objects.filter(status="failed").count()

        # избегаем деления на ноль
        success_percent = round((success_attempts / total_attempts) * 100, 2) if total_attempts > 0 else 0

        context.update({
            "title": "Статистика рассылок",
            "total_attempts": total_attempts,
            "success_attempts": success_attempts,
            "failed_attempts": failed_attempts,
            "success_percent": success_percent,
        })

        print(f"📈 Успешные: {success_attempts}, Ошибки: {failed_attempts}, Процент: {success_percent}%")

        return context
