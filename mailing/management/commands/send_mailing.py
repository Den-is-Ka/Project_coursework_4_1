from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailing.models import Mailing, Attempt
from django.utils import timezone


class Command(BaseCommand):
    help = "Отправляет активные рассылки пользователям"

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status="running", end_date__gte=timezone.now())

        for mailing in mailings:
            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=None,
                        recipient_list=[client.email],
                    )
                    Attempt.objects.create(mailing=mailing, status="success", server_response="OK")
                    self.stdout.write(self.style.SUCCESS(f"Успешно отправлено {client.email}"))
                except Exception as e:
                    Attempt.objects.create(mailing=mailing, status="failed", server_response=str(e))
                    self.stdout.write(self.style.ERROR(f"Ошибка при отправке {client.email}: {e}"))
