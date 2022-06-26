from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

from utils.mixins import MarkAsDeletedMixin, MarkAsDeletedObjectManager


class UserManager(MarkAsDeletedObjectManager, BaseUserManager):
    use_in_migrations = True

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
            extra_fields["is_social_auth"] = True

        if extra_fields.get("is_superuser") is True:
            raise ValueError("User must have is_superuser=False.")

        return self._create_user(email, password, **extra_fields)

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


class User(MarkAsDeletedMixin, AbstractUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Все пользователи"

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
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный",
    )
    is_social_auth = models.BooleanField(
        default=False,
        verbose_name="Через социальную сеть",
    )

    def get_username(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name

    def __str__(self) -> str:
        return self.get_full_name()


class Teacher(User):
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    class Degree(models.TextChoices):
        bachelor = ("bachelor", "Бакалавр")
        master = ("master", "Магистр")
        candidate = ("candidate", "Доцент")
        doctor = ("doctor", "Профессор")

    degree = models.CharField(
        max_length=16,
        choices=Degree.choices,
        verbose_name="Категория",
    )

    def __str__(self) -> str:
        return f"{self.get_degree_display()} {self.get_full_name()}"


class Student(User):
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
