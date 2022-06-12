from django.contrib import admin

from .models import Teacher, Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
