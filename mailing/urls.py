from django.urls import path
import mailing.views as views
from . import views_statistics
from .views import (
    IndexView,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    AttemptListView, MailingReportView,
)

app_name = "mailing"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    # Клиенты
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),

    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),

    # Рассылки
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/<int:pk>/report/", MailingReportView.as_view(), name="mailing_report"),

    # Попытки
    path("attempts/", AttemptListView.as_view(), name="attempt_list"),

    # Статистика
    path("statistics/", views_statistics.StatisticsView.as_view(), name="statistics"),

    path("mailings/<int:pk>/send/", views.MailingSendView.as_view(), name="mailing_send"),
]
