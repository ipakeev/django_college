from django.contrib import admin

from .models import Teacher, Student, OAuth2User


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "patronymic", "email")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "patronymic", "email")


@admin.register(OAuth2User)
class OAuth2UserAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "patronymic", "email")
