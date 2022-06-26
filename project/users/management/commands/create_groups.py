from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db import transaction

from project.users.models import Teacher, Student, User
from project.application.permissions import (
    GROUP_TEACHER,
    GROUP_STUDENT,
    GROUP_OAUTH2,
    GROUPS_PERMISSIONS,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        with transaction.atomic():
            for group_name, permissions in GROUPS_PERMISSIONS.items():
                group, _ = Group.objects.get_or_create(name=group_name)
                group.permissions.clear()
                group.user_set.clear()
                group_permissions = Permission.objects.filter(codename__in=permissions)
                group.permissions.add(*group_permissions)

            group = Group.objects.get(name=GROUP_TEACHER)
            group.user_set.add(*Teacher.objects.all())

            group = Group.objects.get(name=GROUP_STUDENT)
            group.user_set.add(*Student.objects.all())

            group = Group.objects.get(name=GROUP_OAUTH2)
            group.user_set.add(*User.objects.filter(is_social_auth=True).all())
