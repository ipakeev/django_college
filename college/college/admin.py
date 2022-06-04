from django.contrib import admin

from college.models import (
    Chair,
    Lesson,
    Auditorium,
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


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass
