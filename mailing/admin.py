from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment", "owner")
    search_fields = ("full_name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner")
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_date", "end_date", "owner")
    list_filter = ("status",)
    date_hierarchy = "start_date"


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("datetime", "status", "mailing")
    list_filter = ("status", "mailing")


# Создание группы Managers
def create_managers_group():
    group, created = Group.objects.get_or_create(name="Managers")
    if created:
        print("✅ Группа 'Managers' создана.")
    perms = Permission.objects.filter(
        codename__in=[
            "view_all_mailings",
            "view_all_clients",
            "view_message",
            "view_attempt"
        ]
    )
    group.permissions.set(perms)
    group.save()
    print("✅ Права добавлены группе Managers.")


admin.site.add_action(create_managers_group)
