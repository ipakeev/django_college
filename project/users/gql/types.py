from graphene_django import DjangoObjectType

from project.users.models import Teacher, Student


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = ("email", "first_name", "last_name", "patronymic", "degree")


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("email", "first_name", "last_name", "patronymic")
