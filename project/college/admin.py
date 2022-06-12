from django.contrib import admin

from .models import (
    Chair,
    Lesson,
    Auditorium,
    Course,
    TimeTable,
    Grade,
)


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Auditorium)
class AuditoriumAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass
