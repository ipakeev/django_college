import graphene
from graphene_django import DjangoObjectType

from project.college.models import (
    Chair,
    Lesson,
    Auditorium,
    Course,
    TimeTable,
    Grade,
)
from project.users.gql.types import StudentType, TeacherType
from project.users.models import Teacher


class ChairType(DjangoObjectType):
    class Meta:
        model = Chair
        exclude = ("is_deleted",)


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson
        exclude = ("chair", "is_deleted",)


class AuditoriumType(DjangoObjectType):
    class Meta:
        model = Auditorium
        exclude = ("is_deleted",)


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        exclude = ("is_deleted",)

    students = graphene.List(StudentType)
    teachers = graphene.List(TeacherType)

    def resolve_students(self: Course, info):
        return self.students.all()

    def resolve_teachers(self: Course, info):
        return Teacher.objects.filter(timetable__course=self).distinct()


class TimeTableType(DjangoObjectType):
    class Meta:
        model = TimeTable
        exclude = ("is_deleted",)


class GradeType(DjangoObjectType):
    class Meta:
        model = Grade
        exclude = ("is_deleted",)
