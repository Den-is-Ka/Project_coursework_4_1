from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Создаёт группу 'Managers' с нужными правами"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Managers")
        perms = Permission.objects.filter(
            codename__in=[
                "view_all_mailings",
                "view_all_clients",
                "view_all_messages",
            ]
        )
        group.permissions.set(perms)
        group.save()
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Группа 'Managers' создана"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Группа 'Managers' уже существует"))
