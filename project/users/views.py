from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from project.college.models import Grade
from .models import Teacher, Student


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class StudentListView(ListView):
    model = Student


class StudentDetailView(View):
    model = Student

    def get(self, request, pk: int):
        context = {
            "student": Student.objects.filter(id=pk).prefetch_related("courses").first(),
            "grades": Grade.objects.filter(student_id=pk).select_related(
                "timetable",
                "timetable__course",
                "timetable__lesson",
                "timetable__lesson__chair",
            ),
        }
        return render(request, "users/student_detail.html", context=context)
