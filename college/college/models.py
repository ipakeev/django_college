from django.db import models


class Chair(models.Model):
    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедры"

    title = models.CharField(
        max_length=64,
        verbose_name="Название",
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    chair = models.ForeignKey(
        "Chair",
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Кафедра",
    )
    theme = models.CharField(
        max_length=64,
        verbose_name="Тема занятия",
    )
    homework = models.TextField(
        blank=True,
        null=True,
        verbose_name="Домашнее задание",
    )

    def __str__(self):
        return f"{self.chair}: {self.theme}"


class Auditorium(models.Model):
    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"

    address = models.CharField(
        max_length=64,
        verbose_name="Адрес",
    )

    def __str__(self):
        return self.address


class TimeTable(models.Model):
    class Meta:
        verbose_name = "Расписание занятий"
        verbose_name_plural = "Расписания занятий"

    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.PROTECT,
        related_name="timetables",
        verbose_name="Занятие",
    )
    auditorium = models.ForeignKey(
        "Auditorium",
        on_delete=models.PROTECT,
        related_name="timetables",
        verbose_name="Аудитория",
    )
    teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.PROTECT,
        related_name="timetables",
        verbose_name="Преподаватель",
    )
    date = models.DateField(verbose_name="Дата расписания")
    start_at = models.TimeField(verbose_name="Время начала занятия")
    duration = models.PositiveSmallIntegerField(
        default=90,
        verbose_name="Продолжительность (мин.)",
    )

    def __str__(self):
        return f"{self.date.isoformat()} {self.start_at.strftime('%H:%M')}"


class Grade(models.Model):
    class Meta:
        verbose_name = "Оценка за урок"
        verbose_name_plural = "Оценки за уроки"

    student = models.ForeignKey(
        "users.Student",
        on_delete=models.SET_NULL,
        related_name="grades",
        null=True,
        verbose_name="Студент",
    )
    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.SET_NULL,
        related_name="grades",
        null=True,
        verbose_name="Занятие",
    )
    value = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
    )

    def __str__(self):
        return f"{self.student} | {self.lesson} | {self.value}"
