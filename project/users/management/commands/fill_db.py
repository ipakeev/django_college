from datetime import datetime, timedelta, timezone

from django.core.management import BaseCommand
from django.db import transaction

from college.models import (
    Chair,
    Lesson,
    Auditorium,
    Course,
    TimeTable,
    Grade,
)
from users.models import Teacher, Student


class Command(BaseCommand):
    help = "gdsg"

    def handle(self, *args, **options):
        with transaction.atomic():
            salmin = Teacher.objects.create(
                email="salmin_em@mail.ru",
                password="password",
                first_name="Евгений",
                last_name="Салмин",
                patronymic="Михайлович",
                degree=Teacher.Degree.doctor,
            )
            malyshkin = Teacher.objects.create(
                email="malyshkin_oa@mail.ru",
                password="password",
                first_name="Олег",
                last_name="Малышкин",
                patronymic="Арсентьевич",
                degree=Teacher.Degree.candidate,
            )

            petrov = Student.objects.create(
                email="petrov@mail.ru",
                password="password",
                first_name="Петр",
                last_name="Петров",
                patronymic="Петрович",
            )
            ivanov = Student.objects.create(
                email="ivanov@mail.ru",
                password="password",
                first_name="Иван",
                last_name="Иванов",
                patronymic="Иванович",
            )
            sidorov = Student.objects.create(
                email="sidorov@mail.ru",
                password="password",
                first_name="Сидор",
                last_name="Сидоров",
                patronymic="Сидорович",
            )

            course_engineering, course_science, course_economic = Course.objects.bulk_create([
                Course(title="Инженерия"),
                Course(title="Наука"),
                Course(title="Экономика"),
            ])
            course_engineering.students.add(petrov, ivanov, sidorov)
            course_science.students.add(petrov, sidorov)
            course_economic.students.add(ivanov)

            chair_math, chair_physics, chair_history = Chair.objects.bulk_create([
                Chair(title="Математика"),
                Chair(title="Физика"),
                Chair(title="История"),
            ])

            lesson1, lesson2, lesson3, lesson4 = Lesson.objects.bulk_create([
                Lesson(chair=chair_math, theme="Вводное занятие"),
                Lesson(chair=chair_math, theme="Линейная алгебра", homework="Решить уравнения"),
                Lesson(chair=chair_physics, theme="Вводное занятие"),
                Lesson(chair=chair_physics, theme="Элементарные частицы"),
            ])

            auditorium1, auditorium2 = Auditorium.objects.bulk_create([
                Auditorium(address="Зал №1"),
                Auditorium(address="Зал №2"),
            ])

            dt = datetime(2021, 9, 1, 8, 0, tzinfo=timezone.utc)
            timetable1, timetable2, timetable3, timetable4 = TimeTable.objects.bulk_create([
                TimeTable(
                    date=dt.date(),
                    start_at=dt.time(),
                    course=course_engineering,
                    lesson=lesson1,
                    auditorium=auditorium1,
                    teacher=malyshkin,
                ),
                TimeTable(
                    date=dt.date() + timedelta(days=1),
                    start_at=dt.time(),
                    course=course_engineering,
                    lesson=lesson2,
                    auditorium=auditorium1,
                    teacher=malyshkin,
                ),
                TimeTable(
                    date=dt.date(),
                    start_at=dt.time(),
                    course=course_science,
                    lesson=lesson3,
                    auditorium=auditorium2,
                    teacher=salmin,
                ),
                TimeTable(
                    date=dt.date() + timedelta(days=1),
                    start_at=dt.time(),
                    course=course_science,
                    lesson=lesson4,
                    auditorium=auditorium2,
                    teacher=salmin,
                ),
            ])

            Grade.objects.bulk_create([
                Grade(
                    student=petrov,
                    timetable=timetable1,
                    value=4,
                ),
                Grade(
                    student=petrov,
                    timetable=timetable2,
                    value=5,
                ),
                Grade(
                    student=ivanov,
                    timetable=timetable1,
                    value=5,
                ),
                Grade(
                    student=sidorov,
                    timetable=timetable1,
                    value=3,
                ),
                Grade(
                    student=sidorov,
                    timetable=timetable2,
                    value=2,
                ),
            ])
