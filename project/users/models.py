from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

from project.application import permissions
from project.application.permissions import GROUP_OAUTH2, GROUP_TEACHER, GROUP_STUDENT
from utils.mixins import MarkAsDeletedMixin, MarkAsDeletedObjectManager


class UserManager(MarkAsDeletedObjectManager, BaseUserManager):
    use_in_migrations = True

    def _add_to_group(self, user: "User") -> None:
        group = Group.objects.get(name=user.group_name)
        group.user_set.add(user)

    def _create_user(self, email: str, password: str, **extra_fields: Any):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if password is None:
            password = ""
            extra_fields["group_name"] = GroupName.oauth2.value

        if extra_fields.get("is_superuser") is True:
            raise ValueError("User must have is_superuser=False.")

        user = self._create_user(email, password, **extra_fields)
        self._add_to_group(user)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "Admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class GroupName(models.TextChoices):
    teacher = (GROUP_TEACHER, "Учитель")
    student = (GROUP_STUDENT, "Студент")
    oauth2 = (GROUP_OAUTH2, "Через соц.сеть")


class Degree(models.TextChoices):
    bachelor = ("bachelor", "Бакалавр")
    master = ("master", "Магистр")
    candidate = ("candidate", "Доцент")
    doctor = ("doctor", "Профессор")


class User(MarkAsDeletedMixin, AbstractUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Все пользователи"
        permissions = (
            permissions.EditLessonsPermission.perm,
            permissions.ViewStudentDetailsPermission.perm,
            permissions.SendEmailPermission.perm,
            permissions.ViewTimetablePermission.perm,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None

    objects = UserManager()

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    first_name = models.CharField(
        max_length=32,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=32,
        verbose_name="Фамилия",
    )
    patronymic = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name="Отчество",
    )
    degree = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=Degree.choices,
        verbose_name="Категория",
    )
    group_name = models.CharField(
        max_length=16,
        choices=GroupName.choices,
        verbose_name="Название группы пользователей",
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный",
    )

    def get_username(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name

    def has_perm(self, perm: str, obj=None):
        return super().has_perm(f"{self._meta.app_label}.{perm}")

    def __str__(self) -> str:
        return self.get_full_name()


class UserGroupModelManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(group_name=self.model.GROUP)


class Teacher(User):
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        proxy = True

    GROUP = GROUP_TEACHER
    objects = UserGroupModelManager()

    def __str__(self) -> str:
        return f"{self.get_degree_display()} {self.get_full_name()}"


class Student(User):
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        proxy = True

    GROUP = GROUP_STUDENT
    objects = UserGroupModelManager()


class OAuth2User(User):
    class Meta:
        verbose_name = "OAuth2"
        verbose_name_plural = "OAuth2"
        proxy = True

    GROUP = GROUP_OAUTH2
    objects = UserGroupModelManager()
