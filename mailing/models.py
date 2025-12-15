from django.db import models
from django.conf import settings


class Client(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='clients'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = [
            ("view_all_clients", "Может просматривать всех клиентов"),
        ]


class Message(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='messages'
    )
    subject = models.CharField(max_length=250, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ("view_all_messages", "Может просматривать все сообщения"),
        ]


class Mailing(models.Model):
    STATUS_CHOISES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='mailings'
    )
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='created', verbose_name='Статус')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, related_name="mailings", verbose_name='Клиенты')

    def __str__(self):
        return f'Рассылка #{self.id} - {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("view_all_mailings", "Может просматривать все рассылки"),
        ]


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Ошибка'),
    ]

    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ сервера', blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='attempts')

    def __str__(self):
        return f'Попытка {self.id} - {self.status}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

class Meta:
    verbose_name = 'Сообщение'
    verbose_name_plural = 'Сообщения'
    permissions = [
        ("view_all_messages", "Может просматривать все сообщения"),
    ]
