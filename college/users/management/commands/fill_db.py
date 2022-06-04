from datetime import datetime, timedelta, timezone

from django.core.management import BaseCommand

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

        course = Course.objects.create(
            title="Подготовительный",
        )
        course.students.add(petrov, ivanov, sidorov)

        chair = Chair.objects.create(
            title="Математика и физика"
        )
        lesson1 = Lesson.objects.create(
            chair=chair,
            theme="Вводное занятие",
        )
        lesson2 = Lesson.objects.create(
            chair=chair,
            theme="Линейная алгебра",
            homework="Решить уравнения ..."
        )
        auditorium = Auditorium.objects.create(
            address="Зал №1",
        )

        dt = datetime(2021, 9, 1, 8, 0, tzinfo=timezone.utc)
        timetable1, timetable2 = TimeTable.objects.bulk_create([
            TimeTable(
                date=dt.date(),
                start_at=dt.time(),
                course=course,
                lesson=lesson1,
                auditorium=auditorium,
                teacher=malyshkin,
            ),
            TimeTable(
                date=dt.date() + timedelta(days=1),
                start_at=dt.time(),
                course=course,
                lesson=lesson2,
                auditorium=auditorium,
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
