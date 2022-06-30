from django.db import models


class MarkAsDeletedObjectManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self) -> models.QuerySet:
        return super().get_queryset()


class MarkAsDeletedMixin:
    objects = MarkAsDeletedObjectManager()

    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")

    def delete(self, *args, **kwargs) -> None:
        self.is_deleted = True
        self.save()
