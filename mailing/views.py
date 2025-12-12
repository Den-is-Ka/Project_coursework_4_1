from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Client, Message, Mailing, Attempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View


# Миксины
class OwnerOrManagerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ограничиваем доступ: пользователь видит только своё, менеджеры — всё"""
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name="Managers").exists() or user == self.get_object().owner


class OwnerFilterMixin(LoginRequiredMixin):
    """Фильтруем объекты для обычных пользователей"""
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.groups.filter(name="Managers").exists():
            return qs
        return qs.filter(owner=user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Клиент
class ClientListView(OwnerFilterMixin, ListView):
    model = Client
    template_name = "mailing/list.html"
    context_object_name = "objects"
    extra_context = {"title": "Клиенты"}


class ClientCreateView(OwnerFilterMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:client_list")
    extra_context = {"title": "Добавить клиента"}


class ClientUpdateView(OwnerOrManagerMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:client_list")
    extra_context = {"title": "Редактировать клиента"}


class ClientDeleteView(OwnerOrManagerMixin, DeleteView):
    model = Client
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")
    extra_context = {"title": "Удалить клиента"}


# Рассылка
class MailingListView(OwnerFilterMixin, ListView):
    model = Mailing
    template_name = "mailing/list.html"
    context_object_name = "objects"
    extra_context = {"title": "Рассылки"}


class MailingCreateView(OwnerFilterMixin, CreateView):
    model = Mailing
    fields = ["start_date", "end_date", "status", "message", "clients"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:mailing_list")
    extra_context = {"title": "Создать рассылку"}


class MailingUpdateView(OwnerOrManagerMixin, UpdateView):
    model = Mailing
    fields = ["start_date", "end_date", "status", "message", "clients"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:mailing_list")
    extra_context = {"title": "Редактировать рассылку"}


class MailingDeleteView(OwnerOrManagerMixin, DeleteView):
    model = Mailing
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
    extra_context = {"title": "Удалить рассылку"}


# Попытки
class AttemptListView(OwnerFilterMixin, ListView):
    model = Attempt
    template_name = "mailing/list.html"
    context_object_name = "objects"
    extra_context = {"title": "Попытки рассылки"}


# Сообщение
class MessageListView(OwnerFilterMixin, ListView):
    model = Message
    template_name = "mailing/list.html"
    context_object_name = "objects"
    extra_context = {"title": "Сообщения"}


class MessageCreateView(OwnerFilterMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:message_list")
    extra_context = {"title": "Добавить сообщение"}


class MessageUpdateView(OwnerOrManagerMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailing:message_list")
    extra_context = {"title": "Редактировать сообщение"}


class MessageDeleteView(OwnerOrManagerMixin, DeleteView):
    model = Message
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")
    extra_context = {"title": "Удалить сообщение"}


@method_decorator(cache_page(60 * 5), name="dispatch")  # кэшируем страницу на 5 минут
class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # пробуем взять кэшированные значения
        stats = cache.get("main_stats")
        if not stats:
            total_mailings = Mailing.objects.count()
            active_mailings = Mailing.objects.filter(status="running").count()
            unique_clients = Client.objects.distinct().count()

            stats = {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "unique_clients": unique_clients,
            }
            cache.set("main_stats", stats, 60 * 5)  # кэшируем на 5 минут

        context.update(stats)
        context["title"] = "Главная"
        return context


class MailingReportView(LoginRequiredMixin, DetailView):
    """Отчёт по конкретной рассылке с таблицей всех попыток"""
    model = Mailing
    template_name = "mailing/mailing_report.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object
        attempts = mailing.attempts.all().order_by("-datetime")

        success_count = attempts.filter(status="success").count()
        failed_count = attempts.filter(status="failed").count()
        total = attempts.count()
        success_percent = round((success_count / total) * 100, 2) if total > 0 else 0

        context.update({
            "attempts": attempts,
            "success_count": success_count,
            "failed_count": failed_count,
            "total_attempts": total,
            "success_percent": success_percent,
            "title": f"Отчёт по рассылке #{mailing.id}",
        })
        print(f"📊 Отчёт #{mailing.id}: Успешно={success_count}, Ошибки={failed_count}, Успех={success_percent}%")
        return context


class MailingSendView(LoginRequiredMixin, View):
    """Запуск рассылки вручную через интерфейс"""
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        attempts_created = 0

        for client in mailing.clients.all():
            Attempt.objects.create(
                mailing=mailing,
                status="success",  # можно эмулировать
                server_response="Отправлено вручную из интерфейса"
            )
            attempts_created += 1

        mailing.status = "finished"
        mailing.save()

        messages.success(request, f"Рассылка #{mailing.id} успешно выполнена ({attempts_created} писем).")
        return redirect("mailing:mailing_list")