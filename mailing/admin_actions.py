from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Client, Mailing, Message


@admin.action(description="Создать или обновить группу Managers с нужными правами")
def create_managers_group(modeladmin, request, queryset):
    group, created = Group.objects.get_or_create(name="Managers")

    # Разрешаем только просмотр
    content_types = ContentType.objects.get_for_models(Client, Mailing, Message)
    view_perms = Permission.objects.filter(
        content_type__in=content_types.values(),
        codename__startswith="view_"
    )

    group.permissions.set(view_perms)
    group.save()

    if created:
        msg = "Группа Managers создана."
    else:
        msg = "Группа Managers обновлена."

    modeladmin.message_user(request, msg)
